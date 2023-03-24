from app.utils.api_client import get_data

def get_details(date_type, page = 10,after = None, before = None):
    # buscar en base al tipo de filtro: periodo, o fecha de entrega
    params = {}
    if date_type == 'period':
        if after:
            params["after"] = f'{after}T00:01:00'
        if before:
            params["before"] = f'{before}T23:59:59'
    elif date_type == 'delivery':
        if after:
            params["delivery_date"] = after
    
    orders = get_data(endpoint="orders", params=params)
    
    total_pages = orders['total_pages']
    
    orders_response = orders['response']
    orders_data = []
    for key in orders_response:
        products_data = []
        billing = key['billing']
        order_data = {
            'id': key['id'],
            'delivery_date': key['delivery_date'],
            'delivery_time': key['delivery_time'],
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
            order_data['total_products'] = total_quantity
        orders_data.append(order_data)
    print(orders_data)
    return orders_data, total_pages