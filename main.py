import json
import asyncio
import aiohttp
from datetime import datetime, timedelta


from flask import Flask, flash, redirect, url_for, render_template, request
from flask_mysqldb import MySQL

from woocommerce import API

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc



app = Flask(__name__)

# Configuración de la API de WooCommerce
wcapi = API(
    url="https://dev.jardinorganico.com.ar",
    consumer_key="ck_5c5521a7554f61e1775a5821b9d0f46af4c71864",
    consumer_secret="cs_ac0a59dbbfa06b42bf6ea7f311fb42a47495e5a3",
    version="wc/v3"
)

async def get_orders():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://dev.jardinorganico.com.ar/wp-json/wc/v3/orders', params={"per_page": 10, "page": 1, "expand": "line_items.product"}, auth=aiohttp.BasicAuth('ck_5c5521a7554f61e1775a5821b9d0f46af4c71864', 'cs_ac0a59dbbfa06b42bf6ea7f311fb42a47495e5a3')) as response:
            return await response.json()
        
@app.route('/', methods=['GET'])
async def actualizar_ordenes():
    # Esperar a que se completen las consultas
    orders = await get_orders()

    # Crear una lista de todos los ID de productos únicos
    product_ids = []
    for order in orders:
        for item in order["line_items"]:
            product_id = item["product_id"]
            if product_id not in product_ids:
                product_ids.append(product_id)
    
    # Concatenar los IDs de productos separados por coma
    include = ','.join(str(i) for i in product_ids)

    # Contar la cantidad de productos de cada categoría de cada orden y el número de plano de cada usuario
    async with aiohttp.ClientSession() as session:
        async with session.get('https://dev.jardinorganico.com.ar/wp-json/wc/v3/products', params={"include": include}, auth=aiohttp.BasicAuth('ck_5c5521a7554f61e1775a5821b9d0f46af4c71864', 'cs_ac0a59dbbfa06b42bf6ea7f311fb42a47495e5a3')) as response:
            products = await response.json()
        answers = []
        for order in orders:
            lacteo_count = 0
            congelado_count = 0
            huerta_count = 0
            user_id = order["customer_id"]
            plano_numero = None
            
            for item in order["line_items"]:
                product_id = item["product_id"]
                for product in products:
                    if product["id"] == product_id:
                        for category in product["categories"]:
                            if category["name"] == "Lácteos":
                                lacteo_count += item["quantity"]
                            elif category["name"] == "Congelado":
                                congelado_count += item["quantity"]
                            elif category["name"] == "Huerta":
                                huerta_count += item["quantity"]
            
            async with aiohttp.ClientSession() as session2:
                async with session2.get(f'https://dev.jardinorganico.com.ar/wp-json/wc/v3/customers/{user_id}', auth=aiohttp.BasicAuth('ck_5c5521a7554f61e1775a5821b9d0f46af4c71864', 'cs_ac0a59dbbfa06b42bf6ea7f311fb42a47495e5a3')) as response:
                    user = await response.json()
                    for meta in user["meta_data"]:
                        if meta["key"] == "plano_numero":
                            plano_numero = meta["value"]
                        elif meta["key"] == "plano_letra":
                            plano_letra = meta["value"]
                        elif meta["key"] == "longitud":
                            longitud = meta["value"]
                        elif meta["key"] == "latitud":
                            latitud = meta["value"]
                    
            answer = f"La orden {order['id']} tiene {lacteo_count} productos lácteos, {congelado_count} productos congelados y {huerta_count} productos de huerta. El usuario {user_id} tiene el número de plano {plano_numero}, la letra de plano {plano_letra}, longitud {longitud} y latitud {latitud}."
            answers.append(answer)
    return answers

    # # Crear un diccionario que asocie cada ID de producto con su categoría correspondiente
    # product_categories = {}
    # for product in products:
    #     product_categories[product["id"]] = product["categories"][0]["name"]

    # # Actualizar cada objeto de `line_item` en la matriz de `line_items` de cada orden de compra
    # for order in orders:
    #     for item in order["line_items"]:
    #         product_id = item["product_id"]
    #         if product_id in product_categories:
    #             product_category = product_categories[product_id]
    #             if product_category:
    #                 item["product_category"] = product_category


    #     # Actualizar la orden de compra con la información de categoría de producto agregada
    #     order_id = order["id"]
    #     response = wcapi.put(f"orders/{order_id}", {"line_items": order["line_items"]})

    # # Devolver los detalles de todas las órdenes de compra con la información de categoría de producto agregada
    # orders = wcapi.get("orders").json()
    
    # order_data = []
    # for order in orders:
    #     for item in order["line_items"]:
    #         product_id = item["product_id"]
    #         if product_id in product_categories:
    #             product_category = product_categories[product_id]
    #             if product_category:
    #                 item["product_category"] = product_category
    #         order_data.append(order)
    # return products
