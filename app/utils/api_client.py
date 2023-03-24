import json

from woocommerce import API

def get_data(per_page: int = 10, endpoint: str = None, params: dict = None, after = None, before = None):
    # Configuración de la API de WooCommerce
    wcapi = API(
        url="https://dev.jardinorganico.com.ar",
        consumer_key="ck_5c5521a7554f61e1775a5821b9d0f46af4c71864",
        consumer_secret="cs_ac0a59dbbfa06b42bf6ea7f311fb42a47495e5a3",
        version="wc/v3"
    )

    # Realiza la solicitud a la API de WooCommerce
    response = wcapi.get(endpoint, params=params)

    # Obtiene la información de paginación
    headers = response.headers
    total_pages = int(headers.get('X-WP-TotalPages'))

    data = {
        'total_pages': total_pages,
        'response': response.json(),
    }
    # Retorna los datos y el total de páginas
    return data
