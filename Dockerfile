FROM python:3.11.12-slim 

RUN apt-get update && apt-get install -y \
    libpq-dev gcc g++ python3-dev musl-dev build-essential postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

ENV PORT=8000
EXPOSE 8000

CMD ["gunicorn", "bloodpoint_project.wsgi", "--bind", "0.0.0.0:8000"]
