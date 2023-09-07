from datetime import datetime

from flask import Flask, flash, redirect, url_for, render_template, request

from app.utils.api_client import get_data
from app.utils.orders import get_orders
from app.utils.tickets import get_tickets
from app.utils.details import get_details
from app.utils.category import get_category


app = Flask(__name__)


@app.route('/orders/', methods=['GET', 'POST'])
def orders_completed():

    page = int(request.args.get("page", 1))
    after = request.args.get('after')
    before = request.args.get('before')
    submit_button = request.args.get('submit_button')

    dateType = request.args.get('dateType')

    orders = None
    total_pages = None
    delivery_date = None

    if submit_button == 'ENVIAR':
        if dateType == 'period':
            if after:
                after = datetime.strptime(after, '%Y-%m-%d').date()
            if before:
                before = datetime.strptime(before, '%Y-%m-%d').date()
            orders, total_pages = get_orders(date_type='period', after=after, before=before, page=page)
        elif dateType == 'delivery':
            if after:
                parts = after.split('-')
                delivery_date = f'{parts[2]}/{parts[1]}/{parts[0]}'

            orders, total_pages = get_orders(date_type='delivery', after=delivery_date, page=page)

    return render_template('orders.html', orders = orders, total_pages = total_pages, page = page)


@app.route('/tickets/', methods=['GET', 'POST'])
def tickets_delivery():

    after = request.args.get('after')
    before = request.args.get('before')
    submit_button = request.args.get('submit_button')

    dateType = request.args.get('dateType')

    orders = None
    total_pages = None
    delivery_date = None

    if submit_button == 'ENVIAR':
        if dateType == 'period':
            if after:
                after = datetime.strptime(after, '%Y-%m-%d').date()
            if before:
                before = datetime.strptime(before, '%Y-%m-%d').date()
            orders, total_pages = get_tickets(date_type='period', after=after, before=before)
        elif dateType == 'delivery':
            if after:
                parts = after.split('-')
                delivery_date = f'{parts[2]}/{parts[1]}/{parts[0]}'

            orders, total_pages = get_tickets(date_type='delivery', after=delivery_date)


    return render_template('tickets.html', orders=orders, total_pages=total_pages)

@app.route('/details/')
def orders_details():

    after = request.args.get('after')
    before = request.args.get('before')
    submit_button = request.args.get('submit_button')

    dateType = request.args.get('dateType')

    orders = None
    total_pages = None
    delivery_date = None

    if submit_button == 'ENVIAR':
        if dateType == 'period':
            if after:
                after = datetime.strptime(after, '%Y-%m-%d').date()
            if before:
                before = datetime.strptime(before, '%Y-%m-%d').date()
            orders, total_pages = get_details(date_type='period', after=after, before=before)
        elif dateType == 'delivery':
            if after:
                parts = after.split('-')
                delivery_date = f'{parts[2]}/{parts[1]}/{parts[0]}'

            orders, total_pages = get_details(date_type='delivery', after=delivery_date) 

    return render_template('details.html', orders=orders)

@app.route('/category/')
def category():
    after = request.args.get('after')
    before = request.args.get('before')
    submit_button = request.args.get('submit_button')

    dateType = request.args.get('dateType')

    orders = None
    total_pages = None
    delivery_date = None

    if submit_button == 'ENVIAR':
        if dateType == 'period':
            if after:
                after = datetime.strptime(after, '%Y-%m-%d').date()
            if before:
                before = datetime.strptime(before, '%Y-%m-%d').date()
            orders, total_pages = get_category(date_type='period', after=after, before=before)
        elif dateType == 'delivery':
            if after:
                parts = after.split('-')
                delivery_date = f'{parts[2]}/{parts[1]}/{parts[0]}'

            orders, total_pages = get_category(date_type='delivery', after=delivery_date)
        # Procesa los datos para la tabla
        table_data = []

        if orders:
            headers = set()  # Usaremos un conjunto para recopilar todos los nombres de usuario únicos
            for order in orders:
                product_name = order['name']
                total_quantity = order['total_quantity']
                user_data = order['users']

                # Agrega los nombres de usuario a los encabezados
                headers.update(user_data.keys())

                # Creamos una fila para la tabla con los valores que necesitas
                row = {
                    'product_name': product_name,
                    'total_quantity': total_quantity,
                    **user_data  # Desempaqueta todos los usuarios y sus cantidades
                }
                table_data.append(row)

            # Convierte los encabezados a una lista para ordenarlos
            headers = sorted(list(headers))


    return render_template('category.html', table_data=table_data, headers=headers)

