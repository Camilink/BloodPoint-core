# BloodPoint 🩸

**Sistema de Promoción y Gestión de Donaciones de Sangre**

> Desarrollado con Django, PostgreSQL, Apache Superset y Chatbot IA

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/)  [![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)](https://www.postgresql.org/)  [![Apache Superset](https://img.shields.io/badge/Apache%20Superset-4.1.2-orange.svg)](https://superset.apache.org/)  [![Django REST Framework](https://img.shields.io/badge/DRF-3.16.0-red.svg)](https://www.django-rest-framework.org/)

[![Cloudinary](https://img.shields.io/badge/Cloudinary-Storage-blue.svg)](https://cloudinary.com/)  [![OpenRouter](https://img.shields.io/badge/OpenRouter-AI%20API-purple.svg)](https://openrouter.ai/)  [![Render](https://img.shields.io/badge/Render-Deployment-green.svg)](https://render.com/)  [![Heroku](https://img.shields.io/badge/Heroku-Staging-purple.svg)](https://heroku.com/)

[![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey.svg)](https://flask.palletsprojects.com/)  [![JWT](https://img.shields.io/badge/JWT-Authentication-orange.svg)](https://jwt.io/)  [![CORS](https://img.shields.io/badge/CORS-Enabled-green.svg)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)  [![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)](https://www.docker.com/)

## Tabla de Contenidos

-  [Descripción](#descripción)

-  [Componentes Principales](#componentes-principales)

-  [Backend Django](#backend-django)

-  [Sistema de Analytics (Apache Superset)](#sistema-de-analytics-apache-superset)

-  [Chatbot FAQ (IA)](#chatbot-faq-ia)

-  [Tecnologías Utilizadas](#tecnologías-utilizadas)

-  [Estructura del Proyecto](#estructura-del-proyecto)

-  [Variables de Entorno](#variables-de-entorno)

-  [Instalación Local](#instalación-local)

-  [Docker](#docker)

-  [Despliegue en Render](#despliegue-en-render)

-  [Dashboard Superset](#dashboard-superset)

-  [Endpoints](#endpoints)

-  [Estructura de ramas](#estructura-de-ramas)

-  [Testeo](#testeo)

-  [Seguridad](#seguridad)

-  [Desarrollo y Contribución](#desarrollo-y-contribución)

  

------------

  

## Descripción

BloodPoint es una plataforma web integral para la gestión de donaciones de sangre en Chile. Permite administrar campañas, donantes, centros y representantes; visualizar estadísticas interactivas con dashboards, y resolver dudas frecuentes mediante un chatbot con IA. Esta solución digital está orientada a organizaciones de salud, bancos de sangre y usuarios registrados.

  

## Componentes Principales

### Backend Django

- Gestión de usuarios por tipo (Donante, Representante, Administrador)

- Campañas de donación y registros de donaciones

- API REST para integración móvil

  

### Sistema de Analytics (Apache Superset)

- Dashboards embebidos con JWT para visualización segura

- Paneles por centro, región y volumen de donación

  

### Chatbot FAQ (IA)

- Motor de preguntas frecuentes usando OpenRouter (DeepSeek Chat v3)

- Base de conocimiento: BPCB.json (1.400+ preguntas y respuestas)

- Autenticación y validación semántica de entradas

## Tecnologías Utilizadas

| Componente     | Tecnología                         |
|----------------|------------------------------------|
| Backend Web    | Django 5.2 + Django REST Framework |
| Base de Datos  | PostgreSQL 16                      |
| Almacenamiento | Cloudinary                         |
| Dashboards     | Apache Superset 4.1.2 + Flask JWT  |
| Chatbot        | OpenRouter API (DeepSeek v3)       |
| Despliegue     | Render.com, Heroku, Docker         |

## Estructura del Proyecto

```bash

bloodpoint/

├──  bloodpoint_app/  # App principal

│  ├──  models.py  # Modelos (Donante, Campaña, etc.)

│  ├──  views.py  # Vistas API y lógica chatbot

│  ├──  urls.py  # Rutas del sistema

│  ├──  serializers.py  # Serializadores DRF

│  └──  templates/  # Paneles de administración

├──  superset_config.py  # Configuración de dashboards

├──  BPCB.json  # Base de datos del chatbot

├──  manage.py

└──  requirements.txt

```

## Variables de Entorno

>Las siguientes variables son necesarias:

    SECRET_KEY=clave_django
    
    DATABASE_URL=postgres://...
    
    CLOUDINARY_URL=cloudinary://...
    
    SUPERSET_JWT_SECRET=clave_secreta_dashboard
    
    FLASK_APP=superset

  

## Instalación Local

1. Clonar e instalar dependencias

```bash

git  clone  https://github.com/usuario/BloodPoint-Web.git

cd  BloodPoint-Web

pip  install  -r  requirements.txt

```

2. Migraciones y archivos estáticos

```bash

python  manage.py  migrate

python  manage.py  collectstatic

```

3. Ejecutar servidor

```bash

python  manage.py  runserver

```

  

## Docker

>Build y despliegue

```bash

docker  build  -t  bloodpoint  .

docker  run  -d  -p  8000:8000  bloodpoint

```

  

## Despliegue en Render

1. Subir código a GitHub

2. Crear nuevo servicio en Render.com

3. Usar render.yaml para configuración automática

  

## Dashboard Superset

>La plataforma integra Apache Superset con autenticación embebida:

```bash

Visualización  de  donaciones  por  región,  centro  y  tipo  sanguíneo

Paneles  accesibles  desde  el  menú  web  del  administrador

Configurado  en  "superset_config.py"

```

## Endpoints

| Método | Endpoint                  | Descripción                          |
|--------|---------------------------|--------------------------------------|
| GET    | /campanas/activas/        | Listado de campañas activas          |
| POST   | /donaciones/registrar/    | Registrar donación por representante |
| GET    | /donante/historial/       | Ver historial de donaciones          |
| POST   | /ask/                     | Enviar pregunta al chatbot           |
| GET    | /admin/dashboard/embed/   | Obtener dashboard embebido JWT       |

## Estructura de ramas

| Rama                         | Propósito                                                                 |
|------------------------------|---------------------------------------------------------------------------|
| `main`                       | Contiene el código principal de la aplicación web desarrollada en Django |
| `analytics/superset`         | Implementación de Apache Superset para dashboards, desplegado en Render  |
| `ai/chatbot`                 | Integración del chatbot con OpenRouter y su base de conocimiento en JSON |
| `deployment/infrastructure` | Scripts y configuraciones para despliegue en Docker, Render y Heroku     |


## Testeo

```bash

python  manage.py  test

```

## Seguridad

1. Autenticación JWT para dashboards

2. Protección de rutas por permisos

3. Validación RUT chileno

4. CORS configurado para integración con app móvil


## Desarrollo y Contribución

1. Crea tu fork del proyecto

2. Trabaja en una nueva rama

3. Ejecuta tests y validaciones

4. Abre un Pull Request con tus cambios
