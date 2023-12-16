import json
import os

from woocommerce import API

from dotenv import load_dotenv

load_dotenv()

def get_wcapi():
    # Configuración de la API de WooCommerce
    return API(
        url=os.getenv("BASE_URL"),
        consumer_key=os.getenv("CONSUMER_KEY"),
        consumer_secret=os.getenv("CONSUMER_SECRET"),
        version=os.getenv("VERSION_API")
    )


def get_data_category(per_page: int = 10, endpoint: str = None, params: dict = None, after = None, before = None):
    wcapi = get_wcapi()
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
    wcapi = get_wcapi()
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