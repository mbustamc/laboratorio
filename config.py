# config.py
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables de entorno desde un archivo .env

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_super_secreta')
    # La URI de la base de datos se configurará dinámicamente en __init__.py
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    