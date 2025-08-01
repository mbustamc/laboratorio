FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

# Ejecuta init_db.py antes de levantar la app
CMD echo "Ejecutando migración..." && python init_db.py

# Expone el puerto que usará la aplicación
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:create_app()"]
