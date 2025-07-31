from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


from google.cloud.sql.connector import Connector
import pg8000
import sqlalchemy

# Crea el conector
connector = Connector()

def getconn():
    conn = connector.connect(
        "PROJECT_ID:REGION:INSTANCE_NAME",  # ← reemplázalo
        "pg8000",
        user="postgres",
        password=os.environ["DB_PASSWORD"],  # ← viene desde tus credentials
        db="DATABASE_NAME"                   # ← reemplázalo
    )
    return conn

# Crea el engine de SQLAlchemy
engine = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=getconn,
    pool_pre_ping=True
)



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_ENGINE'] = engine
    #app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        from app import routes  # Importa aquí para registrar las rutas

    return app

