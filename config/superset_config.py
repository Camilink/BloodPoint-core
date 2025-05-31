import os

# ===========================
# 🔐 Seguridad
# ===========================
SECRET_KEY = 'Okiqzq/LVgWIDvxZ5nCU4bzNxA4Hyi37VD0dIQUeeB8qjaTv39XfJw1v'

# ===========================
# ⚙️ Configuración general
# ===========================
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_PORT = int(os.environ.get("PORT", 8088))

# ===========================
# 📦 Base de datos
# ===========================


SQLALCHEMY_DATABASE_URI = "postgresql://u5mh9fi08iuct0:pb0d6bd9f0e847a780e5403a376a825847485c97a50a2dd1459a86dc144440ced@ca932070ke6bv1.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d50aqolcf988ab"


# ===========================
# 🔄 CSRF / HTTPS
# ===========================
TALISMAN_ENABLED = False
WTF_CSRF_ENABLED = False

# ===========================
# 🧩 Feature Flags
# ===========================
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "EMBEDDABLE_CHARTS": True,
    "DASHBOARD_RBAC": True,
}

# ===========================
# 🔐 JWT (para integración con Django)
# ===========================
JWT_SECRET = "Okiqzq/LVgWIDvxZ5nCU4bzNxA4Hyi37VD0dIQUeeB8qjaTv39XfJw1v"  # Debe coincidir con Django
JWT_ISSUER = "bloodpoint-core-qa"
JWT_AUDIENCE = "https://bloodpoint-core.onrender.com"

# ===========================
# 🌐 CORS
# ===========================
ENABLE_CORS = True
CORS_OPTIONS = {
    "supports_credentials": True,
    "allow_headers": ["Content-Type", "Authorization", "X-GuestToken"],
    "expose_headers": ["Content-Disposition"],
    "resources": {
        r"/api/*": {
            "origins": [
                "http://localhost:3000",
                "https://bloodpoint-core-qa-35c4ecec4a30.herokuapp.com"
            ]
        },
        r"/superset/explore/*": {"origins": ["*"]},
    },
}

# ===========================
# 🧩 Embedded Charts & Dashboards
# ===========================
PUBLIC_ROLE_LIKE = "Gamma"
GUEST_ROLE_NAME = "Embedded"
GUEST_TOKEN_JWT_SECRET = "django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp"  # Cambiar en producción
GUEST_TOKEN_JWT_ALGO = "HS256"
GUEST_TOKEN_JWT_EXP_SECONDS = 3600  # 1 hora
GUEST_TOKEN_JWT_AUDIENCE = "superset_embedded"
GUEST_TOKEN_HEADER_NAME = "X-GuestToken"

print(f"✅ Using custom SECRET_KEY: {SECRET_KEY[:10]}... (truncated)")
