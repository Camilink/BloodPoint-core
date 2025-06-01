import os

# ===========================
# 🔐 Seguridad
# ===========================
SECRET_KEY = "Okiqzq/LVgWIDvxZ5nCU4bzNxA4Hyi37VD0dIQUeeB8qjaTv39XfJw1v"

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
# Usa un solo secreto para firmar y verificar tokens
JWT_SECRET = "django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp"
JWT_ISSUER = "bloodpoint-core-qa"
JWT_AUDIENCE = "superset_embedded"

# ===========================
# 🧩 Embedded Charts & Dashboards
# ===========================
GUEST_TOKEN_JWT_SECRET = JWT_SECRET  # Usa el mismo secreto
GUEST_TOKEN_JWT_ALGO = "HS256"
GUEST_TOKEN_JWT_EXP_SECONDS = 3600
GUEST_TOKEN_JWT_AUDIENCE = JWT_AUDIENCE
GUEST_TOKEN_HEADER_NAME = "X-GuestToken"
GUEST_ROLE_NAME = "Embedded"
PUBLIC_ROLE_LIKE = "Embedded"  # Hereda permisos este rol

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
                "https://bloodpoint-core-qa-35c4ecec4a30.herokuapp.com",
            ]
        },
        r"/superset/explore/*": {"origins": ["*"]},
    },
}
