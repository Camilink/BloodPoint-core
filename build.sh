#!/usr/bin/env bash
# Exit on error
set -o errexit
echo "Render assigned PORT is: $PORT"


# Instalar Apache Superset y driver de PostgreSQL (si no están en requirements.txt)
pip install apache-superset psycopg2-binary


# --- Configuración de Superset ---
# 1. Migrar la base de datos de Superset
superset db upgrade

# 2. Crear usuario admin (opcional, o hazlo manual después del despliegue)
# ¡Cambia las credenciales!
export FLASK_APP=superset
superset fab create-admin \
    --username admin \
    --firstname Admin \
    --lastname User \
    --email admin@example.com \
    --password admin123  # ¡Usa una contraseña segura!

# 3. Inicializar Superset (roles y permisos básicos)
superset init