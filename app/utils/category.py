from datetime import datetime
from app.utils.api_client import get_data

def get_category(date_type, page = 10,after = None, before = None):
    # buscar en base al tipo de filtro: periodo, o fecha de entrega
    formato_deseado = "%Y-%m-%d"
    params = {}
    if date_type == 'period':
        if after:
            params["after"] = f'{after}T00:01:00'
        if before:
            params["before"] = f'{before}T23:59:59'
    elif date_type == 'delivery':
        if after:
            # Convierte el formato de la fecha
            after_formated = after.replace("/", "-")

            # Convierte la cadena con el nuevo formato a un objeto datetime
            fecha_objeto = datetime.strptime(after_formated, "%d-%m-%Y")
            params["delivery_date"] = after_formated

    orders = get_data(endpoint="product-category", params=params)
    total_pages = orders['total_pages']

    orders_response = orders['response'].values()
    print(orders_response)
    return orders_response, total_pages