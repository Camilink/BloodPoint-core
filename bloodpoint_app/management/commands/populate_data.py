from django.core.management.base import BaseCommand
import random
from datetime import datetime, timedelta
from faker import Faker
from bloodpoint_app.models import CustomUser, adminbp, donante, representante_org, centro_donacion, donacion, campana, solicitud_campana_repo

class Command(BaseCommand):
    help = 'Puebla la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        fake = Faker('es_CL')

        # Limpieza
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
        representantes_data = [
            ('camilaajojeda@gmail.com', 'bloodpoint123', 'Camila', 'Jopia', '17388920-5', 'Voluntaria Cruz Roja', True, 'credencial1.pdf'),
            ('paulina678@gmail.com', 'bloodpoint123', 'Paulina', 'Ríos', '18845236-1', 'Representante DMKS', False, 'credencial2.pdf'),
            ('cristian333@gmail.com', 'bloodpoint123', 'Cristian', 'Morales', '16578431-9', 'Director Técnico Lab', True, 'credencial3.pdf'),
            ('ana.solis@gmail.com', 'bloodpoint123', 'Ana', 'Solís', '16899877-3', 'Tecnólogo', True, 'credencial4.pdf'),
            ('mario.acuna@gmail.com', 'bloodpoint123', 'Mario', 'Acuña', '17234655-2', 'Coordinador campaña Cruz Roja', False, 'credencial5.pdf'),
        ]

        representantes = []
        for email, pwd, first_name, last_name, rut, rol, verificado, credencial in representantes_data:
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
            representantes.append(rep)

        # Donantes
        donantes = []
        nombres = ['Juan', 'Andrea', 'Roberto', 'Camila', 'Lucía', 'Felipe', 'María', 'Carlos']
        apellidos = ['Araya', 'Castro', 'Mena', 'Herrera', 'Reyes', 'Gómez', 'Vera', 'López']
        comunas = ['Providencia', 'Ñuñoa', 'Las Condes', 'Macul']
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        ocupaciones = ['estudiante', 'trabajador', 'jubilado', 'otro']
        tipo_sangres = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']

        for _ in range(100):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            email = fake.unique.email()
            rut = fake.unique.bothify(text='########-#')
            user = CustomUser.objects.create_user(email=email, password='bloodpoint123', rut=rut, tipo_usuario='donante')
            d = donante.objects.create(
                user=user,
                rut=rut,
                nombre_completo=f"{nombre} {apellido}",
                sexo=random.choice(['M', 'F']),
                ocupacion=random.choice(ocupaciones),
                direccion=fake.address().replace('\n', ', '),
                comuna=random.choice(comunas),
                fono=fake.phone_number(),
                fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=65),
                nacionalidad='Chilena',
                tipo_sangre=random.choice(tipo_sangres),
                dispo_dia_donacion=random.choice(dias),
                nuevo_donante=random.choice([True, False]),
                noti_emergencia=random.choice([True, False])
            )
            donantes.append(d)

        # Centros de donación
        centros = []
        for _ in range(5):
            c = centro_donacion.objects.create(
                nombre_centro=fake.company(),
                direccion_centro=fake.address().replace('\n', ', '),
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
        for _ in range(15):
            fecha_campana = fake.date_between(start_date='-1y', end_date='today')
            fecha_termino = fecha_campana + timedelta(days=7)

            latitud = round(fake.pyfloat(min_value=-37.0, max_value=-33.0), 6)
            longitud = round(fake.pyfloat(min_value=-73.0, max_value=-70.0), 6)

            c = campana.objects.create(
                nombre_campana=fake.company(),
                fecha_campana=fecha_campana,
                id_centro=random.choice(centros),
                apertura=datetime.strptime('09:00', '%H:%M').time(),
                cierre=datetime.strptime('16:00', '%H:%M').time(),
                meta=str(random.randint(50, 200)),
                latitud=latitud,
                longitud=longitud,
                id_representante=random.choice(representantes),
                fecha_termino=fecha_termino,
                validada=random.choice([True, False]),
                estado=random.choice(['pendiente', 'desarrollandose', 'cancelado', 'completo'])
            )
            campanas.append(c)

        # Solicitudes
        solicitudes = []
        for _ in range(5):
            fecha_solicitud = fake.date_between(start_date='-1y', end_date='today')
            fecha_termino = fecha_solicitud + timedelta(days=14)
            s = solicitud_campana_repo.objects.create(
                tipo_sangre_sol=random.choice(tipo_sangres),
                fecha_solicitud=fecha_solicitud,
                cantidad_personas=random.randint(10, 100),
                descripcion_solicitud=fake.text(max_nb_chars=200),
                comuna_solicitud=random.choice(comunas),
                ciudad_solicitud=fake.city(),
                region_solicitud=random.choice(['RM', 'Valparaíso', 'Biobío']),
                id_donante=random.choice(donantes),
                centro_donacion=random.choice(centros),
                fecha_termino=fecha_termino,
                desactivado_por=random.choice(representantes)
            )
            solicitudes.append(s)

        # Donaciones
        for _ in range(100):
            fecha_donacion = fake.date_between(start_date='-1y', end_date='today')
            donacion.objects.create(
                id_donante=random.choice(donantes),
                fecha_donacion=fecha_donacion,
                cantidad_donacion=random.randint(450, 500),
                centro_id=random.choice(centros),
                tipo_donacion=random.choice(['campana', 'solicitud']),
                validada=random.choice([True, False]),
                es_intencion=random.choice([True, False]),
                campana_relacionada=random.choice(campanas),
                solicitud_relacionada=random.choice(solicitudes)
            )

        print("¡Datos insertados correctamente!")
