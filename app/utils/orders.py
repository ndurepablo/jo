from app.utils.api_client import get_data

def get_orders(date_type, page = 10,after = None, before = None):
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
        lacteos = key['category_counter']['lacteos'] if 'lacteos' in key['category_counter'] else 0
        freezer = key['category_counter']['congelado'] if 'congelado' in key['category_counter'] else 0
        huerta = key['category_counter']['huerta'] if 'huerta' in key['category_counter'] else 0
        billing = key['billing']
        order_data = {
            'id': key['id'],
            'delivery_date': key['delivery_date'],
            'delivery_time': key['delivery_time'],
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