import os

class Config:
    SECRET_KEY = 'tu_clave_super_secreta'
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///default.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False