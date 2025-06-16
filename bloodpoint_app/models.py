import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from bloodpoint_app.models import donante, representante_org, centro_donacion, campana, donacion, adminbp

User = get_user_model()

OCUPACIONES = ['estudiante', 'trabajador', 'jubilado', 'otro']
TIPO_SANGRE = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']

# Coordenadas aproximadas para Región Metropolitana (Santiago)
LAT_MIN, LAT_MAX = -33.75, -33.35
LON_MIN, LON_MAX = -70.95, -70.45

def random_lat_lon():
    lat = round(random.uniform(LAT_MIN, LAT_MAX), 6)
    lon = round(random.uniform(LON_MIN, LON_MAX), 6)
    return lat, lon

class Command(BaseCommand):
    help = 'Populate database with test users, donantes, representantes, campañas, centros y donaciones'

    def handle(self, *args, **options):
        self.stdout.write("Borrando datos antiguos...")
        donacion.objects.all().delete()
        campana.objects.all().delete()
        centro_donacion.objects.all().delete()
        representante_org.objects.all().delete()
        donante.objects.all().delete()
        adminbp.objects.all().delete()
        User.objects.exclude(email='admin@example.com').delete()

        self.stdout.write("Creando admin...")
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='12345678'
        )
        adminbp.objects.create(
            user=admin_user,
            nombre='Administrador Principal',
            email=admin_user.email,
            contrasena='12345678'
        )

        self.stdout.write("Creando representante especial y su campaña...")
        # Crear usuario representante especial
        rep_user = User.objects.create_user(
            email='camilaajojeda@gmail.com',
            password='12345678',
            tipo_usuario='representante',
            is_staff=True,
        )
        representante = representante_org.objects.create(
            user=rep_user,
            rut_representante='12345678-9',
            rol='Líder',
            nombre='Camila',
            apellido='Ajo',
            verificado=True
        )

        # Crear centro de donación ligado al representante
        centro = centro_donacion.objects.create(
            nombre_centro='Centro Donación Santiago',
            direccion_centro='Av. Libertador 123',
            comuna='Santiago',
            telefono='123456789',
            fecha_creacion=datetime.now().date(),
            id_representante=representante,
            horario_apertura=datetime.strptime('08:00', '%H:%M').time(),
            horario_cierre=datetime.strptime('18:00', '%H:%M').time()
        )

        lat, lon = random_lat_lon()

        # Crear campaña ligada al centro y representante especial
        camp = campana.objects.create(
            nombre_campana='Campaña Camila Especial',
            fecha_campana=datetime.now().date(),
            id_centro=centro,
            apertura=datetime.strptime('08:00', '%H:%M').time(),
            cierre=datetime.strptime('18:00', '%H:%M').time(),
            meta='100',
            latitud=int(lat * 1e6),  # Según modelo, es IntegerField, por eso escalamos
            longitud=int(lon * 1e6),
            id_representante=representante,
            fecha_termino=(datetime.now() + timedelta(days=30)).date(),
            validada=True,
            estado='desarrollandose'
        )

        self.stdout.write("Creando 20 donantes...")

        donantes_list = []
        for i in range(20):
            user = User.objects.create_user(
                email=f'donante{i}@example.com',
                password='12345678',
                tipo_usuario='donante',
                rut=f'1111111{i}-1',
            )
            d = donante.objects.create(
                user=user,
                rut=user.rut,
                nombre_completo=f'Donante {i}',
                sexo=random.choice(['M', 'F']),
                ocupacion=random.choice(OCUPACIONES),
                direccion=f'Calle {i} #123',
                comuna='Santiago',
                fono=f'91234567{i}',
                fecha_nacimiento=(datetime.now() - timedelta(days=365*random.randint(18,65))).date(),
                nacionalidad='Chilena',
                tipo_sangre=random.choice(TIPO_SANGRE),
                dispo_dia_donacion='Fines de semana',
                nuevo_donante=random.choice([True, False]),
                noti_emergencia=True,
            )
            donantes_list.append(d)

        self.stdout.write("Creando 4 representantes adicionales...")

        for i in range(4):
            user = User.objects.create_user(
                email=f'representante{i}@example.com',
                password='12345678',
                tipo_usuario='representante',
                is_staff=True,
            )
            representante_org.objects.create(
                user=user,
                rut_representante=f'2222222{i}-2',
                rol='Coordinador',
                nombre=f'RepNombre{i}',
                apellido=f'RepApellido{i}',
                verificado=bool(random.getrandbits(1)),
            )

        self.stdout.write("Creando campañas y donaciones para los donantes...")

        # Crear más centros y campañas
        for j in range(3):  # 3 centros extra
            rep_random = representante_org.objects.order_by('?').first()
            centro_extra = centro_donacion.objects.create(
                nombre_centro=f'Centro Donacion Extra {j}',
                direccion_centro=f'Avenida Extra {j} 456',
                comuna='Santiago',
                telefono=f'98765432{j}',
                fecha_creacion=datetime.now().date(),
                id_representante=rep_random,
                horario_apertura=datetime.strptime('08:00', '%H:%M').time(),
                horario_cierre=datetime.strptime('17:00', '%H:%M').time()
            )
            lat, lon = random_lat_lon()
            camp_extra = campana.objects.create(
                nombre_campana=f'Campaña Extra {j}',
                fecha_campana=datetime.now().date(),
                id_centro=centro_extra,
                apertura=datetime.strptime('09:00', '%H:%M').time(),
                cierre=datetime.strptime('16:00', '%H:%M').time(),
                meta=str(random.randint(50, 150)),
                latitud=int(lat * 1e6),
                longitud=int(lon * 1e6),
                id_representante=rep_random,
                fecha_termino=(datetime.now() + timedelta(days=20)).date(),
                validada=True,
                estado='desarrollandose'
            )

            # Crear donaciones para estas campañas (entre 10 y 20 por campaña)
            donantes_para_esta_campana = random.sample(donantes_list, k=15)
            for donante_obj in donantes_para_esta_campana:
                donacion.objects.create(
                    id_donante=donante_obj,
                    fecha_donacion=datetime.now().date() - timedelta(days=random.randint(0,30)),
                    cantidad_donacion=random.choice([1, 2]),
                    centro_id=centro_extra,
                    tipo_donacion='campana',
                    validada=True,
                    es_intencion=False,
                    campana_relacionada=camp_extra
                )

        # Crear 30 donaciones para la campaña especial de Camila con los mismos donantes
        for i in range(30):
            don_obj = random.choice(donantes_list)
            donacion.objects.create(
                id_donante=don_obj,
                fecha_donacion=datetime.now().date() - timedelta(days=random.randint(0,30)),
                cantidad_donacion=random.choice([1, 2]),
                centro_id=centro,
                tipo_donacion='campana',
                validada=True,
                es_intencion=False,
                campana_relacionada=camp
            )

        self.stdout.write(self.style.SUCCESS("Datos creados exitosamente."))
