import os
from dotenv import load_dotenv


# Cargar variables de entorno desde el archivo .env
load_dotenv()

BASE_URL = os.getenv('BASE_URL')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
VERSION_API = os.getenv('VERSION_API')

app.config['DEBUG'] = os.getenv('DEBUG')