# Use Heroku's Python base image (optimized for dynos)
FROM python:3.11.12-slim 

# Install system dependencies including build tools
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    python3-dev \
    musl-dev \
    build-essential \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip first
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

ENV PORT=8000
EXPOSE $PORT

CMD gunicorn bloodpoint_project.wsgi --bind 0.0.0.0:$PORT