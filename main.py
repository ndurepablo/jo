from datetime import datetime

from flask import Flask, flash, redirect, url_for, render_template, request

from app.utils.service import get_category, get_details, get_orders, get_tickets


app = Flask(__name__)
# Configuración para deshabilitar el modo de depuración
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

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
        if after:
            orders, total_pages = get_orders(date_type='delivery', after=after)

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
        if after:
            orders, total_pages = get_details(date_type='delivery', after=after)

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
        if after:
            orders, total_pages = get_details(date_type='delivery', after=after)

    return render_template('details.html', orders=orders)

@app.route('/category/')
def category():
    category = request.args.get('category')
    after = request.args.get('after')
    before = request.args.get('before')
    submit_button = request.args.get('submit_button')

    dateType = request.args.get('dateType')

    orders = None
    total_pages = None
    delivery_date = None

    if submit_button == 'ENVIAR':
        if after:
            orders, total_pages = get_category(date_type='period', after=after, before=before, category=category)
    # Procesa los datos para la tabla
    table_data = []
    headers = set() # Usaremos un conjunto para recopilar todos los nombres de usuario únicos
    if orders:
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

