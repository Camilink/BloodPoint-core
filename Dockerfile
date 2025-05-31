FROM python:3.11.12-slim 

FROM apache/superset:latest

USER root

# Instalación de librerías adicionales si necesitas
RUN pip install flask-cors psycopg2-binary

# Copia tu archivo de configuración si tienes uno personalizado
COPY superset_config.py /app/pythonpath/

# Opcional: copia tu requirements si tienes dependencias adicionales
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8088

CMD ["superset", "run", "-h", "0.0.0.0", "-p", "8088"]