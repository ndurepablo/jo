from datetime import datetime
from app.utils.api_client import get_data_category, get_data


def format_date(date: str):
    date = datetime.strptime(date, "%Y-%m-%d")
    return date.strftime("%d-%m-%Y")

def get_category(date_type, category: str, page = 10,after = None, before = None):
    params = {}
    if after:
        params["shipping_date"] = format_date(after)
    params['category'] = category

    orders = get_data_category(endpoint="product-category", params=params)
    total_pages = orders['total_pages']
    orders_response = orders['response'].values()
    return orders_response, total_pages

def get_details(date_type, page = 10,after = None, before = None):
    # buscar en base al tipo de filtro: periodo, o fecha de entrega
    params = {}
    if after:
        params["delivery_date"] = format_date(after)
    orders = get_data(endpoint="orders", params=params)

    total_pages = orders['total_pages']

    orders_response = orders['response']
    orders_data = []
    for key in orders_response:
        products_data = []
        billing = key['billing']
        order_data = {
            'id': key['id'],
            'custom_shipping_date': key['custom_shipping_date'],
            'name': billing['first_name'] + billing['last_name'],
            'adress': billing['address_1'] + billing['address_2'],
            'city': billing['city'],
            'cp': billing['postcode'],
            'phone': billing['phone'],
            'total': key['total'],
            'notes': key['customer_note'],
            'payment_method': key['payment_method_title'],
            'shipping_total': key['shipping_total']
        }
        total_products = 0
        for product in key['line_items']:
            total_quantity = 0
            total_quantity += product['quantity']
            product_data = {
                'name': product['name'],
                'quantity': product['quantity'],
                'total_product': product['total']
            }
            products_data.append(product_data)
            order_data['products'] = products_data
            total_products += total_quantity
        orders_data.append(order_data)
        order_data['total_products'] = total_products
    return orders_data, total_pages

def get_orders(date_type, page = 10,after = None, before = None):
    params = {}
    if after:
        params["delivery_date"] = format_date(after)
    orders = get_data(endpoint="orders", params=params)
    total_pages = orders['total_pages']

    orders_response = orders['response']
    print(orders_response)
    orders_data = []

    for key in orders_response:
        lacteos = key['category_counter']['lacteos'] if 'lacteos' in key['category_counter'] else 0
        freezer = key['category_counter']['congelado'] if 'congelado' in key['category_counter'] else 0
        huerta = key['category_counter']['huerta'] if 'huerta' in key['category_counter'] else 0
        billing = key['billing']
        order_data = {
            'id': key['id'],
            'delivery_date': key['custom_shipping_date'],
            'lacteos_counter': lacteos,
            'freezer_counter': freezer,
            'huerta': huerta,
            'plano_numero': key['customer']['plano_numero'],
            'plano_letra': key['customer']['plano_letra'],
            'latitud': key['customer']['latitud'],
            'longitud': key['customer']['longitud'],
            'name': billing['first_name'] + billing['last_name'],
            'adress': billing['address_1'] + billing['address_2'],
            'city': billing['city'],
            'cp': billing['postcode'],
            'phone': billing['phone'],
            'total': key['total'],
            'notes': key['customer_note'],
            'payment_method': key['payment_method_title']
        }
        orders_data.append(order_data)
    return orders_data, total_pages

def get_tickets(date_type, page = 10,after = None, before = None):
    params = {}
    if after:
        params["delivery_date"] = format_date(after)

    orders = get_data(endpoint="orders", params=params)

    total_pages = orders['total_pages']

    orders_response = orders['response']
    orders_data = []
    for key in orders_response:
        billing = key['billing']
        order_data = {
            'id': key['id'],
            'name': billing['first_name'] + billing['last_name'],
            'delivery_date': key['delivery_date'],
        }
        orders_data.append(order_data)
    return orders_data, total_pages
