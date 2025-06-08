import jwt
import time


def generate_superset_embed_token(chart_uuid, representante_id, campana_id, tipo_donacion):
    now = int(time.time())
    payload = {
        "resource": {"chart": chart_uuid},
        "params": {
            "representante_id": representante_id,
            "campana_id": campana_id,
            "tipo_donacion": tipo_donacion,
        },
        "exp": now + 3600,
        "iat": now,
        "aud": "superset_embedded",
        "iss": "bloodpoint-core-qa",
        "sub": "guest",
    }

    secret = "django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp"
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token





# def generate_superset_embed_token(chart_uuid):
#     now = int(time.time())
#     payload = {
#         "resource": {"chart": chart_uuid},
#         "params": {},
#         "exp": now + 3600,  # token válido 1 hora
#         "iat": now,
#         "aud": "superset_embedded",
#         "iss": "bloodpoint-core-qa",
#         "sub": "guest",  # puede ser cualquier usuario con permisos
#     }

#     secret = "django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp"  # tu secreto JWT
#     token = jwt.encode(payload, secret, algorithm="HS256")
#     return token
