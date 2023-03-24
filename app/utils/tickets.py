from app.utils.api_client import get_data

def get_tickets(date_type, page = 10,after = None, before = None):
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
        billing = key['billing']
        order_data = {
            'id': key['id'],
            'name': billing['first_name'] + billing['last_name'],
            'delivery_date': key['delivery_date'],
        }
        orders_data.append(order_data)
    return orders_data, total_pages
    