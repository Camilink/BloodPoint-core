# superset_utils.py
import jwt
import time

# Esta función genera el token JWT compatible con Superset
def generate_superset_embed_token(dashboard_id):
    now = int(time.time())
    payload = {
        "resource": {"dashboard": dashboard_id},
        "params": {},  # puedes usar filtros aquí si quieres
        "exp": now + 3600,
        "iat": now,
        "aud": "superset_embedded",
        "iss": "bloodpoint-core-qa",
        "sub": "admin_user",  # puede ser el nombre de usuario, opcional
    }

    # Usa el mismo secreto que está en tu superset_config.py
    secret = "django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp"

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token
