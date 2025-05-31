FROM python:3.11.12-slim 

FROM apache/superset:latest

USER root
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalación de librerías adicionales si necesitas
RUN pip install flask-cors psycopg2-binary

# Crea el directorio para el config personalizado
RUN mkdir -p /app/pythonpath/
# Copia tu archivo de configuración si tienes uno personalizado
ENV PYTHONPATH="/app/pythonpath"
COPY config/superset_config.py /app/pythonpath/


# Opcional: copia tu requirements si tienes dependencias adicionales
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8088

CMD ["superset", "run", "-h", "0.0.0.0", "-p", "8088"]