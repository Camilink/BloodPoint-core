FROM apache/superset:latest

USER root

# Actualiza y instala dependencias necesarias para psycopg2 y compilación
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala librerías adicionales que necesitas
RUN pip install flask-cors psycopg2-binary

# Copia tu archivo de configuración personalizado a la ruta deseada
COPY config/superset_config.py /opt/render/project/src/config/superset_config.py

# Define PYTHONPATH para que superset encuentre el archivo de configuración
ENV PYTHONPATH="/opt/render/project/src/config"

# Si tienes dependencias adicionales en requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt

# Expone el puerto por defecto de superset
EXPOSE 8088

# Comando para correr superset
CMD ["superset", "run", "-h", "0.0.0.0", "-p", "8088"]
