import json

from woocommerce import API

def get_data_category(per_page: int = 10, endpoint: str = None, params: dict = None, after = None, before = None):
    # Configuración de la API de WooCommerce
    wcapi = API(
        url="http://127.0.0.1",
        consumer_key="ck_0a0e9da8255301519bf6b0f664025509804fb1f8",
        consumer_secret="cs_59994bef4d81f92aeac617c32cdabae475534ed6",
        version="wc/v3"
    )
    # Realiza la solicitud a la API de WooCommerce
    response = wcapi.get(endpoint, params=params)
    # Inicializa un diccionario vacío como valor predeterminado
    data = {
        'total_pages': 0,  # Valor predeterminado
        'response': {},  # Valor predeterminado
    }

    # Verifica si la respuesta contiene datos y si es una lista vacía
    if response:
        # Verifica si la respuesta es una lista vacía
        if isinstance(response.json(), list):
            # Actualiza el diccionario data con una respuesta vacía en lugar de una lista
            data['response'] = {}
        else:
            # Obtiene la información de paginación
            headers = response.headers
            if headers.get('X-WP-TotalPages'):
                total_pages = int(headers.get('X-WP-TotalPages'))
            else:
                total_pages = 10

            # Actualiza el diccionario data con los datos de la respuesta
            data['total_pages'] = total_pages
            data['response'] = response.json()

    # Retorna los datos y el total de páginas
    return data

def get_data(per_page: int = 10, endpoint: str = None, params: dict = None, after = None, before = None):
    # Configuración de la API de WooCommerce
    wcapi = API(
        url="http://127.0.0.1",
        consumer_key="ck_0a0e9da8255301519bf6b0f664025509804fb1f8",
        consumer_secret="cs_59994bef4d81f92aeac617c32cdabae475534ed6",
        version="wc/v3"
    )
    # Realiza la solicitud a la API de WooCommerce
    response = wcapi.get(endpoint, params=params)
    # Obtiene la información de paginación
    headers = response.headers

    if headers.get('X-WP-TotalPages'):
        total_pages = int(headers.get('X-WP-TotalPages'))
    else:
        total_pages = 10

    data = {
        'total_pages': total_pages,
        'response': response.json(),
    }
    # Retorna los datos y el total de páginas
    return data