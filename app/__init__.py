import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy
from .config import Config

# Inicializa el conector de Cloud SQL
connector = Connector()

# Función para obtener la conexión a la base de datos
def getconn() -> pg8000.dbapi.Connection:
    conn = connector.connect(
        os.environ["INSTANCE_CONNECTION_NAME"],  # Formato: "project:region:instance"
        "pg8000",
        user=os.environ["DB_USER"],          # ej: "postgres"
        password=os.environ["DB_PASS"],
        db=os.environ["DB_NAME"]
    )
    return conn

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Crea el "engine" de SQLAlchemy para conectarse a Cloud SQL
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )

    # Configura la aplicación para usar el engine de Cloud SQL
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+pg8000://"
    app.config["SQLALCHEMY_ENGINE"] = engine
    
    db.init_app(app)

    with app.app_context():
        # Importa los modelos aquí para que se registren con SQLAlchemy
        # from . import models
        db.create_all()
        from app import routes

    return app