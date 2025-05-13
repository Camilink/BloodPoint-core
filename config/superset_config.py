# Superset specific config
ROW_LIMIT = 5000


SECRET_KEY = 'Okiqzq/LVgWIDvxZ5nCU4bzNxA4Hyi37VD0dIQUeeB8qjaTv39XfJw1v'
SQLALCHEMY_DATABASE_URI = 'postgres://u5mh9fi08iuct0:pb0d6bd9f0e847a780e5403a376a825847485c97a50a2dd1459a86dc144440ced@ca932070ke6bv1.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d50aqolcf988ab'
SUPERSET_WEBSERVER_PORT = 8088
FEATURE_FLAGS = {"EMBEDDED_SUPERSET": True, "EMBEDDABLE_CHARTS": True}



TALISMAN_ENABLED = False
WTF_CSRF_ENABLED = False


# CORS Enabling 
ENABLE_CORS = True 
CORS_OPTIONS = { 
    "supports_credentials": True, 
    "allow_headers": "*", 
    "expose_headers": "*", 
    "resources": "*", 
    "origins": ["http://localhost:3000","https://bloodpoint-core-qa-35c4ecec4a30.herokuapp.com/"]  
    }
        

# Dashboard embedding 
GUEST_ROLE_NAME = "Gamma" 
GUEST_TOKEN_JWT_SECRET = "PASTE_GENERATED_SECRET_HERE" 
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