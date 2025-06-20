"""
Django settings for bloodpoint_project project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
import secrets
from pathlib import Path
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['bloodpoint-core-qa.herokuapp.com','bloodpoint-core-qa-35c4ecec4a30.herokuapp.com',
    'localhost','127.0.0.1', 'bloodpoint-core.onrender.com','.onrender.com','localhost:8000']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bloodpoint_app.apps.BloodpointConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_extensions',
    'cloudinary',
    'cloudinary_storage',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
]


ROOT_URLCONF = 'bloodpoint_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bloodpoint_project.wsgi.application'

#image upload

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
AUTH_USER_MODEL = 'bloodpoint_app.CustomUser'

# Configuración prioritaria para Docker
import os
import dj_database_url

# Configuración """""""""ABSOLUTAMENTE""""""""" segura para Docker
DATABASES = {
    "default": dj_database_url.config(default=os.environ.get("DATABASE_URL"))
}

# Configuración de Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('GMAIL_EMAIL')
EMAIL_HOST_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Superset Integration Settings
SUPERSET_JWT_SECRET = "django-insecure-08&ko%+7k8l=v1-@1y@1g-(7ht_uc816k#_&nt@uncpc^ki$jp"
SUPERSET_JWT_AUDIENCE = "superset_embedded"
SUPERSET_JWT_ISSUER = "bloodpoint-core-qa"
SUPERSET_JWT_ALGO = "HS256"
SUPERSET_JWT_EXP_SECONDS = 3600



# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-cl'  # Español de Chile

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static/",
]
# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

import corsheaders.defaults

CORS_ALLOW_HEADERS = list(corsheaders.defaults.default_headers) + [
    'authorization',
    'x-guesttoken',
    'content-type',
]


AUTHENTICATION_BACKENDS = [
    'bloodpoint_app.backends.EmailAuthBackend',  # Primero: navegador (email)
    'bloodpoint_app.backends.RutAuthBackend',     # Segundo: móvil (RUT)
    'django.contrib.auth.backends.ModelBackend',
    
]


CSRF_TRUSTED_ORIGINS = [
    'https://bloodpoint-core-qa-35c4ecec4a30.herokuapp.com',
    'http://localhost:8000'
]

SESSION_COOKIE_SECURE = True   # Send session cookie only over HTTPS
CSRF_COOKIE_SECURE = True      # Send CSRF cookie only over HTTPS


import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()


#LOGIN Y AUTENTICACION:

LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'  # o '/login/' según tu configuración
LOGIN_REDIRECT_URL = "/redirect/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

import cloudinary

cloudinary.config(
    cloudinary_url=os.getenv("CLOUDINARY_URL")
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Firebase Configuration
# FIREBASE_SERVICE_ACCOUNT_KEY = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
# For cloud deployments, you might want to use the service account key file path
FIREBASE_SERVICE_ACCOUNT_KEY = os.path.join(BASE_DIR, 'firebase-service-account-key.json')

# Optional: Use Celery for asynchronous notifications
USE_CELERY = os.getenv('USE_CELERY', 'False').lower() == 'true'

