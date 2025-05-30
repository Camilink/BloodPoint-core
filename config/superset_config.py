import os

# Superset specific config
ROW_LIMIT = 5000


SECRET_KEY = 'Okiqzq/LVgWIDvxZ5nCU4bzNxA4Hyi37VD0dIQUeeB8qjaTv39XfJw1v'
SQLALCHEMY_DATABASE_URI = 'postgres://u5mh9fi08iuct0:pb0d6bd9f0e847a780e5403a376a825847485c97a50a2dd1459a86dc144440ced@ca932070ke6bv1.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d50aqolcf988ab'
SUPERSET_WEBSERVER_PORT = int(os.environ.get("PORT", 8088))
FEATURE_FLAGS = {"EMBEDDED_SUPERSET": True, "EMBEDDABLE_CHARTS": True,
    "DASHBOARD_RBAC": True}

# Superset JWT Config (Render)
JWT_SECRET = "Okiqzq/LVgWIDvxZ5nCU4bzNxA4Hyi37VD0dIQUeeB8qjaTv39XfJw1v"  # Must match Django's SUPERSET_JWT_SECRET
JWT_ISSUER = "bloodpoint-core-qa"  # Must match Django's SUPERSET_JWT_ISSUER
JWT_AUDIENCE = "https://bloodpoint-core.onrender.com"  # Must match Django's SUPERSET_JWT_AUDIENCE

TALISMAN_ENABLED = False
WTF_CSRF_ENABLED = False

        

# Dashboard embedding

PUBLIC_ROLE_LIKE = "Embedded"      # = SUPERSET_PUBLIC_ROLE_LIKE
GUEST_ROLE_NAME = "Embedded"       # = SUPERSET_GUEST_ROLE_NAME
GUEST_TOKEN_JWT_ALGO = "HS256" 
GUEST_TOKEN_HEADER_NAME = "X-GuestToken" 
GUEST_TOKEN_JWT_EXP_SECONDS = 300 # 5 minutes
PUBLIC_ROLE_LIKE = "Gamma"  # Permite acceso público con permisos controlados
GUEST_TOKEN_JWT_SECRET = "django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp"  # Debe coincidir con tu Django
GUEST_TOKEN_JWT_ALGO = "HS256"
GUEST_TOKEN_JWT_EXP_SECONDS = 3600  # 1 hora

# Permisos para recursos embebidos
GUEST_ROLE_NAME = "Embedded"
GUEST_TOKEN_JWT_AUDIENCE = "superset_embedded"


# CORS Config (Más seguro)
ENABLE_CORS = True 
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["Content-Type", "Authorization", "X-GuestToken"],
    "expose_headers": ["Content-Disposition"],
    "resources": {
        r"/api/*": {"origins": ["http://localhost:3000", "https://bloodpoint-core-qa-35c4ecec4a30.herokuapp.com"]},
        r"/superset/explore/*": {"origins": ["*"]}  # Solo necesario para embedding público
    }
}

# Embedded Config (REVISAR ESTO CRÍTICAMENTE)
PUBLIC_ROLE_LIKE = "Gamma"  # Usa Gamma como base
GUEST_ROLE_NAME = "Embedded"
GUEST_TOKEN_JWT_SECRET = "django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp"  # ¡Cambiar en producción!
GUEST_TOKEN_JWT_ALGO = "HS256"
GUEST_TOKEN_JWT_EXP_SECONDS = 3600  # 1 hora
GUEST_TOKEN_JWT_AUDIENCE = "superset_embedded"
GUEST_TOKEN_HEADER_NAME = "X-GuestToken"