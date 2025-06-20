# ---- Dockerfile (sin netcat) ----
FROM python:3.11-slim

# Librerías de sistema necesarias para psycopg2 y compilación
RUN apt-get update && apt-get install -y \
        gcc g++ build-essential \
        libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Gunicorn para producción/desarrollo
CMD ["gunicorn", "bloodpoint_project.wsgi:application", "-b", "0.0.0.0:8000:8000"] 
