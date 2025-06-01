import jwt
import time

def generate_superset_embed_token(dashboard_uuid):
    now = int(time.time())
    payload = {
        "resources": [  # ← aquí el cambio
            {"type": "dashboard", "id": dashboard_uuid}
        ],
        "params": {},
        "exp": now + 3600,
        "iat": now,
        "aud": "superset_embedded",
        "iss": "bloodpoint-core-qa",
        "sub": "admin_user",  # o cualquier string de usuario ficticio
    }

    secret = "django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp"
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token
