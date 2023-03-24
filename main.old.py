import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from math import ceil

from flask import Flask, flash, redirect, url_for, render_template, request
from flask_mysqldb import MySQL

from woocommerce import API

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from app.utils.orders import orders


app = Flask(__name__)

# Configuración de la API de WooCommerce
wcapi = API(
    url="https://dev.jardinorganico.com.ar",
    consumer_key="ck_5c5521a7554f61e1775a5821b9d0f46af4c71864",
    consumer_secret="cs_ac0a59dbbfa06b42bf6ea7f311fb42a47495e5a3",
    version="wc/v3"
)

async def get_orders(per_page, page, after=None, before=None):
    params = {"per_page": per_page, "page": page, "expand": "line_items.product"}
    if after:
        params["after"] = f'{after}T00:00:01'
    if before:
        params["before"] = f'{before}T23:59:59'
        
    async with aiohttp.ClientSession() as session:
        async with session.get('https://dev.jardinorganico.com.ar/wp-json/wc/v3/orders', params=params, auth=aiohttp.BasicAuth('ck_5c5521a7554f61e1775a5821b9d0f46af4c71864', 'cs_ac0a59dbbfa06b42bf6ea7f311fb42a47495e5a3')) as response:
            headers = response.headers
            total_pages = int(headers.get('X-WP-TotalPages'))
            orders = await response.json()
            return orders, total_pages
        
@app.route('/', methods=['GET'])
async def actualizar_ordenes():
    page = int(request.args.get("page", 1))
    per_page = 10
    # Obtener valores de los campos de fecha desde y hasta
    desde = request.args.get('after')
    hasta = request.args.get('before')
    

    # Convertir fechas a objetos datetime si están definidas
    if desde:
        desde = datetime.strptime(desde, '%Y-%m-%d').date()
    if hasta:
        hasta = datetime.strptime(hasta, '%Y-%m-%d').date()

    # Esperar a que se completen las consultas
    orders, total_pages = await get_orders(per_page=per_page, page=page, after=desde, before=hasta)
    

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
        orders_data = []
        for order in orders:
            lacteo_count = 0
            congelado_count = 0
            huerta_count = 0
            user_id = order["customer_id"]
            plano_numero = None
            found_delivery_date = False
            found_delivery_time = False
            for meta_data in order['meta_data']:
                if meta_data['key'] == '_delivery_date':
                    dia_entrega = meta_data['value']
                    found_delivery_date = True
                if meta_data['key'] == '_delivery_time':
                    hora_entrega = meta_data['value']
                    found_delivery_time = True
            if not found_delivery_date:
                dia_entrega = "sin dia entrega"
            if not found_delivery_time:
                hora_entrega = "sin hora entrega"

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
                    
            order_data = {
                'dia_entrega': dia_entrega,
                'hora_entrega': hora_entrega,
                'orden': order['id'],
                'lacteos': lacteo_count,
                'congelado': congelado_count,
                'huerta': huerta_count,
                'plano_numero': plano_numero,
                'plano_letra': plano_letra,
                'longitud': longitud,
                'latitud': latitud,
                'nombre': order['billing']['first_name'] + ' ' + order['billing']['last_name'],
                'telefono': order['billing']['phone'],
                'direccion': order['billing']['address_1'] + ' ' + order['billing']['address_2'],
                'monto': order['total'],
                'info_adicional': order['customer_note'],
                'metodo_de_pago': order['payment_method_title'],
            }
            orders_data.append(order_data)
    return render_template('index.html', orders = orders_data, page = page, per_page = per_page, total_pages = total_pages)


def get_category_id(category_name):
    categories = wcapi.get("products/categories").json()
    category_id = None
    for category in categories:
        if category['name'] == category_name:
            category_id = category['id']
            break
    return category_id

def get_products_by_category(category_id):
    products = wcapi.get("products", params={"category": category_id}).json()
    for product in products:
        product['quantity'] = 0
    orders = wcapi.get("orders").json()
    for order in orders:
        if 'line_items' in order:
            for item in order['line_items']:
                if 'product_id' in item and 'quantity' in item:
                    for product in products:
                        if product['id'] == item['product_id']:
                            product['quantity'] += item['quantity']
    return products

@app.route('/productos_lacteos')
def productos_lacteos():
    category_id = get_category_id("Lácteos")
    products = get_products_by_category(category_id)
    return render_template('productos.html', products=products)

@app.route('/category')
async def category():
    page = int(request.args.get("page", 1))
    per_page = 10
    # Obtener valores de los campos de fecha desde y hasta
    desde = request.args.get('after')
    hasta = request.args.get('before')
    

    # Convertir fechas a objetos datetime si están definidas
    if desde:
        desde = datetime.strptime(desde, '%Y-%m-%d').date()
    if hasta:
        hasta = datetime.strptime(hasta, '%Y-%m-%d').date()
        
    orders, total_pages = await get_orders(per_page=per_page, page=page, after=desde, before=hasta)
    
    return orders

