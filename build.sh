#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "🚀 Iniciando build de Superset..."

# --- Instalar dependencias ---
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Asegúrate de instalar Superset y PostgreSQL driver (si no están ya)
pip install apache-superset psycopg2-binary

# --- Configuración de Django (si aplica) ---
echo "⚙️ Ejecutando collectstatic y migrate de Django..."
python manage.py collectstatic --no-input
python manage.py migrate

# --- Configuración de Superset ---
echo "🔧 Migrando base de datos de Superset..."
superset db upgrade

# Crear usuario admin solo si no existe
echo "👤 Intentando crear usuario admin..."
export FLASK_APP=superset
superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com \
    --password admin123 || echo "⚠️ Usuario admin ya existe o no pudo crearse"

# Inicializar Superset
echo "🔄 Inicializando Superset..."
superset init

echo "✅ Build finalizado correctamente."
