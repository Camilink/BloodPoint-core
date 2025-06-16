import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from bloodpoint_app.models import (
    donante, representante_org, centro_donacion, campana, donacion, adminbp,
    solicitud_campana_repo
)

CustomUser = get_user_model()

TIPO_SANGRE = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
COMUNAS = ['Providencia', 'Ñuñoa', 'Las Condes', 'Macul', 'San Miguel', 'La Florida', 'Maipú', 'Recoleta']
OCUPACIONES = ['estudiante', 'trabajador', 'jubilado', 'otro']
DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

LAT_MIN, LAT_MAX = -33.75, -33.35
LON_MIN, LON_MAX = -70.95, -70.45

def random_lat_lon():
    return round(random.uniform(LAT_MIN, LAT_MAX), 6), round(random.uniform(LON_MIN, LON_MAX), 6)

class Command(BaseCommand):
    help = 'Pobla la base con usuarios, representantes, donantes, campañas, centros y donaciones con datos reales'

    def handle(self, *args, **options):
        self.stdout.write("Limpiando datos antiguos...")
        adminbp.objects.all().delete()
        representante_org.objects.all().delete()
        donante.objects.all().delete()
        CustomUser.objects.filter(tipo_usuario__in=['admin', 'representante', 'donante']).delete()
        campana.objects.all().delete()
        solicitud_campana_repo.objects.all().delete()
        centro_donacion.objects.all().delete()
        donacion.objects.all().delete()

        # Admins
        admins = [
            ('admin@gmail.com', 'bloodpoint123', 'admin', 'Juan', 'Pérez'),
            ('admin2@gmail.com', 'bloodpoint123', 'admin', 'Carla', 'Soto'),
            ('admin3@gmail.com', 'bloodpoint123', 'admin', 'María', 'Olivares'),
        ]

        self.stdout.write("Creando admins...")
        for email, pwd, tipo, first_name, last_name in admins:
            user = CustomUser.objects.create_user(email=email, password=pwd)
            user.tipo_usuario = tipo
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = True
            user.is_superuser = True
            user.is_superadmin = True
            user.save()
            adminbp.objects.create(
                user=user,
                nombre=f'{first_name} {last_name}',
                email=email,
                contrasena=pwd,
                created_at=datetime.now()
            )

        # Representantes
        representantes = [
            ('camilaajojeda@gmail.com', 'bloodpoint123', 'Camila', 'Jopia', '17388920-5', 'Voluntaria Cruz Roja', True, 'credencial1.pdf'),
            ('paulina678@gmail.com', 'bloodpoint123', 'Paulina', 'Ríos', '18845236-1', 'Representante institucional', False, 'credencial2.pdf'),
            ('cristian333@gmail.com', 'bloodpoint123', 'Cristian', 'Morales', '16578431-9', 'Encargado logístico', True, 'credencial3.pdf'),
        ]

        self.stdout.write("Creando representantes...")
        rep_users = {}
        for email, pwd, first_name, last_name, rut, rol, verificado, credencial in representantes:
            user = CustomUser.objects.create_user(email=email, password=pwd)
            user.tipo_usuario = 'representante'
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            rep = representante_org.objects.create(
                user=user,
                rut_representante=rut,
                rol=rol,
                nombre=first_name,
                apellido=last_name,
                credencial=credencial,
                verificado=verificado,
                created_at=datetime.now()
            )
            rep_users[email] = rep

        # Donantes
        nombres = ['Juan', 'Andrea', 'Roberto', 'Camila', 'Lucía', 'Felipe', 'María', 'Carlos', 'Sofía', 'Javier',
                   'Valentina', 'Pedro', 'Daniela', 'Tomás', 'Fernanda', 'Ignacio', 'Antonia', 'Diego', 'Martina',
                   'Benjamín', 'Josefa', 'Sebastián', 'Florencia', 'Vicente', 'Javiera', 'Agustín', 'Constanza',
                   'Matías', 'Trinidad', 'Andrés', 'Francisca', 'Leonardo', 'Catalina', 'Cristóbal', 'Paula']
        apellidos = ['Araya', 'Castro', 'Mena', 'Herrera', 'Reyes', 'Gómez', 'Vera', 'López', 'Soto', 'Martínez',
                     'Ramírez', 'Rojas', 'Morales', 'Navarro', 'Gutiérrez', 'Salazar', 'Fuentes', 'Pizarro', 'Campos',
                     'Escobar', 'Alvarez', 'Peña', 'Carrasco', 'Silva', 'Muñoz', 'Torres', 'Orellana', 'Vargas',
                     'Ortega', 'Núñez', 'Zúñiga', 'Henríquez', 'Barrera', 'Sepúlveda', 'Palma']

        self.stdout.write("Creando donantes...")
        donantes_list = []
        for i in range(20):
            email = f'donante{i}@example.com'
            pwd = 'bloodpoint123'
            user = CustomUser.objects.create_user(email=email, password=pwd)
            user.tipo_usuario = 'donante'
            user.first_name = random.choice(nombres)
            user.last_name = random.choice(apellidos)
            user.save()

            d = donante.objects.create(
                user=user,
                rut=f'{random.randint(10000000, 20000000)}-{random.randint(1,9)}',
                nombre_completo=f'{user.first_name} {user.last_name}',
                sexo=random.choice(['M', 'F']),
                ocupacion=random.choice(OCUPACIONES),
                direccion=f'Calle {random.randint(1,300)} #123',
                comuna=random.choice(COMUNAS),
                fono=f'9{random.randint(10000000, 99999999)}',
                fecha_nacimiento=(datetime.now() - timedelta(days=365 * random.randint(18, 65))).date(),
                nacionalidad='Chilena',
                tipo_sangre=random.choice(TIPO_SANGRE),
                dispo_dia_donacion=', '.join(random.sample(DIAS, k=2)),
                nuevo_donante=random.choice([True, False]),
                noti_emergencia=True,
            )
            donantes_list.append(d)

        # Crear campaña especial para Camila sin crear su centro en ciclo general
        rep_camila = rep_users.get('camilaajojeda@gmail.com')
        if rep_camila:
            lat, lon = random_lat_lon()
            centro_camila = centro_donacion.objects.create(
                nombre_centro='Centro Donación Camila',
                direccion_centro='Avenida Siempre Viva 123',
                comuna=random.choice(COMUNAS),
                telefono=f'2{random.randint(20000000, 29999999)}',
                fecha_creacion=datetime.now().date(),
                id_representante=rep_camila,
                horario_apertura=datetime.strptime('08:00', '%H:%M').time(),
                horario_cierre=datetime.strptime('18:00', '%H:%M').time()
            )
            camp_camila = campana.objects.create(
                nombre_campana='Campaña Camila Especial',
                fecha_campana=datetime.now().date(),
                id_centro=centro_camila,
                apertura=datetime.strptime('09:00', '%H:%M').time(),
                cierre=datetime.strptime('17:00', '%H:%M').time(),
                meta='100',
                latitud=int(lat * 1e6),
                longitud=int(lon * 1e6),
                id_representante=rep_camila,
                fecha_termino=(datetime.now() + timedelta(days=30)).date(),
                validada=True,
                estado='desarrollandose'
            )
            donantes_para_camila = random.choices(donantes_list, k=30)
            for d_obj in donantes_para_camila:
                donacion.objects.create(
                    id_donante=d_obj,
                    fecha_donacion=datetime.now().date() - timedelta(days=random.randint(0, 30)),
                    cantidad_donacion=random.choice([1, 2]),
                    centro_id=centro_camila,
                    tipo_donacion='campana',
                    validada=True,
                    es_intencion=False,
                    campana_relacionada=camp_camila
                )

        self.stdout.write("Creando centros de donación y campañas para otros representantes...")

        # Crear centros y campañas para otros representantes (excepto Camila)
        for email, rep in rep_users.items():
            if email == 'camilaajojeda@gmail.com':
                continue  # ya creada su campaña y centro arriba

            lat, lon = random_lat_lon()
            centro = centro_donacion.objects.create(
                nombre_centro=f'Centro Donación {rep.nombre}',
                direccion_centro=f'Avenida {rep.apellido} {random.randint(100, 999)}',
                comuna=random.choice(COMUNAS),
                telefono=f'2{random.randint(20000000, 29999999)}',
                fecha_creacion=datetime.now().date(),
                id_representante=rep,
                horario_apertura=datetime.strptime('08:00', '%H:%M').time(),
                horario_cierre=datetime.strptime('18:00', '%H:%M').time()
            )

            camp = campana.objects.create(
                nombre_campana=f'Campaña {rep.nombre}',
                fecha_campana=datetime.now().date(),
                id_centro=centro,
                apertura=datetime.strptime('09:00', '%H:%M').time(),
                cierre=datetime.strptime('17:00', '%H:%M').time(),
                meta=str(random.randint(50, 150)),
                latitud=int(lat * 1e6),
                longitud=int(lon * 1e6),
                id_representante=rep,
                fecha_termino=(datetime.now() + timedelta(days=random.randint(15, 40))).date(),
                validada=True,
                estado='desarrollandose'
            )

            # Crear donaciones para esta campaña con algunos donantes random
            donantes_para_camp = random.sample(donantes_list, k=10)
            for d_obj in donantes_para_camp:
                donacion.objects.create(
                    id_donante=d_obj,
                    fecha_donacion=datetime.now().date() - timedelta(days=random.randint(0, 30)),
                    cantidad_donacion=random.choice([1, 2]),
                    centro_id=centro,
                    tipo_donacion='campana',
                    validada=True,
                    es_intencion=False,
                    campana_relacionada=camp
                )

        self.stdout.write(self.style.SUCCESS('Datos poblados correctamente.'))
