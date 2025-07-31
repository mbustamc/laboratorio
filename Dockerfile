FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

# Ejecuta init_db.py antes de levantar la app
CMD echo "Ejecutando migración..." && python init_db.py

CMD ["flask", "run", "--host=0.0.0.0"]
