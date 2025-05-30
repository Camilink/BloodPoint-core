import os
import django
import random
from datetime import datetime, timedelta
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bloodpoint_project.settings')  # Ajusta tu proyecto
django.setup()

from bloodpoint_app.models import CustomUser, donante, representante_org, centro_donacion, donacion, campana, solicitud_campana_repo

fake = Faker('es_CL')

TIPO_SANGRE_CHOICES = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
TIPO_DONACION_CHOICES = ['punto', 'campana', 'solicitud']
ESTADO_CAMPANA_CHOICES = ['pendiente', 'desarrollandose', 'cancelado', 'completo']

# Donantes
donantes = []
for _ in range(5):
    email = fake.unique.email()
    password = 'password123'
    rut = fake.unique.rut() if hasattr(fake, 'rut') else fake.unique.bothify(text='########-#')
    user = CustomUser.objects.create_user(email=email, password=password, rut=rut, tipo_usuario='donante')
    d = donante.objects.create(
        user=user,
        rut=rut,
        nombre_completo=fake.name(),
        sexo=random.choice(['M', 'F']),
        direccion=fake.address(),
        comuna=fake.city(),
        fono=fake.phone_number(),
        fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=65),
        nacionalidad='Chilena',
        tipo_sangre=random.choice(TIPO_SANGRE_CHOICES),
        dispo_dia_donacion=random.choice(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']),
        nuevo_donante=random.choice([True, False]),
        noti_emergencia=random.choice([True, False])
    )
    donantes.append(d)

# Representantes
representantes = []
for _ in range(5):
    email = fake.unique.email()
    password = 'password123'
    user = CustomUser.objects.create_user(email=email, password=password, tipo_usuario='representante')
    r = representante_org.objects.create(
        user=user,
        rut_representante=fake.unique.bothify(text='########-#'),
        rol=fake.job(),
        nombre=fake.first_name(),
        apellido=fake.last_name(),
        verificado=random.choice([True, False])
    )
    representantes.append(r)

# Centros de donación
centros = []
for _ in range(5):
    c = centro_donacion.objects.create(
        nombre_centro=fake.company(),
        direccion_centro=fake.address(),
        comuna=fake.city(),
        telefono=fake.phone_number(),
        fecha_creacion=fake.date_between(start_date='-2y', end_date='today'),
        id_representante=random.choice(representantes),
        horario_apertura=datetime.strptime('08:00', '%H:%M').time(),
        horario_cierre=datetime.strptime('17:00', '%H:%M').time()
    )
    centros.append(c)

# Campañas
campanas = []
for _ in range(5):
    fecha_campana = fake.date_between(start_date='-1y', end_date='today')
    fecha_termino = fecha_campana + timedelta(days=7)
    c = campana.objects.create(
        fecha_campana=fecha_campana,
        id_centro=random.choice(centros),
        apertura=datetime.strptime('09:00', '%H:%M').time(),
        cierre=datetime.strptime('16:00', '%H:%M').time(),
        meta=str(random.randint(50, 200)),
        latitud=str(fake.latitude()),
        longitud=str(fake.longitude()),
        id_representante=random.choice(representantes),
        fecha_termino=fecha_termino,
        validada=random.choice([True, False]),
        estado=random.choice(ESTADO_CAMPANA_CHOICES)
    )
    campanas.append(c)

# Solicitudes
solicitudes = []
for _ in range(5):
    fecha_solicitud = fake.date_between(start_date='-1y', end_date='today')
    fecha_termino = fecha_solicitud + timedelta(days=14)
    s = solicitud_campana_repo.objects.create(
        tipo_sangre_sol=random.choice(TIPO_SANGRE_CHOICES),
        fecha_solicitud=fecha_solicitud,
        cantidad_personas=random.randint(10, 100),
        descripcion_solicitud=fake.text(max_nb_chars=200),
        comuna_solicitud=fake.city(),
        ciudad_solicitud=fake.city(),
        region_solicitud='Región Metropolitana',
        id_donante=random.choice(donantes),
        centro_donacion=random.choice(centros),
        fecha_termino=fecha_termino,
        desactivado_por=random.choice(representantes)
    )
    solicitudes.append(s)

# Donaciones
for _ in range(5):
    fecha_donacion = fake.date_between(start_date='-1y', end_date='today')
    donacion.objects.create(
        id_donante=random.choice(donantes),
        fecha_donacion=fecha_donacion,
        cantidad_donacion=random.randint(450, 500),
        centro_id=random.choice(centros),
        tipo_donacion=random.choice(TIPO_DONACION_CHOICES),
        validada=random.choice([True, False]),
        es_intencion=random.choice([True, False]),
        campana_relacionada=random.choice(campanas),
        solicitud_relacionada=random.choice(solicitudes)
    )

print("¡Datos insertados en la base de datos de Heroku con éxito!")
