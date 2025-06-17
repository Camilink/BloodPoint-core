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
            ('camilaajojeda@gmail.com', 'bloodpoint123', 'Camila', 'Jopia', '17388920-5', 'Voluntaria Cruz Roja', True ),
            ('paulina678@gmail.com', 'bloodpoint123', 'Paulina', 'Ríos', '18845236-1', 'Representante DMKS', False),
            ('cristian333@gmail.com', 'bloodpoint123', 'Cristian', 'Morales', '16578431-9', 'Director Técnico Lab', True),
            ('ana.solis@gmail.com', 'bloodpoint123', 'Ana', 'Solís', '16899877-3', 'Tecnólogo', True),
            ('mario.acuna@gmail.com', 'bloodpoint123', 'Mario', 'Acuña', '17234655-2', 'Coordinador campaña Cruz Roja', False),
            ('valeria.perez@gmail.com', 'bloodpoint123', 'Valeria', 'Pérez', '18233456-4', 'Gestora Territorial', True),
            ('fernando.lagos@gmail.com', 'bloodpoint123', 'Fernando', 'Lagos', '16789423-7', 'Encargado de Voluntariado', False),
            ('marta.espinoza@gmail.com', 'bloodpoint123', 'Marta', 'Espinoza', '19564328-2', 'Líder Social', True),
            ('raul.navarro@gmail.com', 'bloodpoint123', 'Raúl', 'Navarro', '15439287-5', 'Técnico en Salud', False),
            ('ines.moraga@gmail.com', 'bloodpoint123', 'Inés', 'Moraga', '18876123-1', 'Organizadora Comunitaria', True),
            ('gonzalo.munoz@gmail.com', 'bloodpoint123', 'Gonzalo', 'Muñoz', '16234577-0', 'Analista de Proyectos', True),
            ('roberta.acevedo@gmail.com', 'bloodpoint123', 'Roberta', 'Acevedo', '17654398-6', 'Asistente Social', False),
            ('luis.sandoval@gmail.com', 'bloodpoint123', 'Luis', 'Sandoval', '18543289-4', 'Enlace Institucional', True),
            ('claudia.vargas@gmail.com', 'bloodpoint123', 'Claudia', 'Vargas', '19098456-2', 'Asesora de Gestión', False),
            ('ricardo.toledo@gmail.com', 'bloodpoint123', 'Ricardo', 'Toledo', '17432765-3', 'Enfermero Coordinador', True),
        ]

        representantes = []
        for email, pwd, first_name, last_name, rut, rol, verificado in representantes_data:
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
                verificado=verificado,
                created_at=datetime.now()
            )
            representantes.append(rep)

        # Donantes
        ruts_reales = [
            '5.861.814-4', '14.219.039-7', '5.573.364-3', '25.153.799-2', '16.531.446-8',
            '33.901.432-9', '8.701.844-K', '9.049.722-7', '36.568.945-8', '30.343.131-4',
            '10.175.772-2', '33.431.057-4', '25.909.279-5', '7.905.112-8', '30.205.452-5',
            '9.133.044-K', '21.055.238-3', '4.104.285-0', '26.898.080-6', '3.804.208-4',
            '24.110.564-4', '32.344.718-7', '21.357.564-3', '35.592.465-3', '19.357.064-K',
            '10.032.716-3', '29.275.070-6', '14.095.304-0', '29.785.203-5', '14.019.658-4',
            '21.332.869-7', '5.861.249-9', '20.946.250-8', '7.389.229-5', '31.230.207-1',
            '29.274.319-K', '1.626.671-K', '2.567.973-3', '25.413.141-5', '32.794.787-7',
            '2.505.269-2', '28.195.057-6', '33.802.521-1', '13.470.402-0', '4.651.921-3',
            '28.560.577-6', '29.921.223-8', '35.057.005-5', '19.905.757-K', '32.155.773-2',
            '2.650.104-0', '36.261.424-4', '3.191.055-2', '1.534.333-8', '17.241.251-3',
            '19.918.967-0', '21.144.260-3', '33.277.662-2', '31.823.714-K', '15.846.593-0',
            '16.126.554-3', '34.587.520-4', '38.842.105-3', '7.996.703-3', '17.941.307-8',
            '34.068.383-8', '6.421.938-3', '30.368.083-7', '31.633.096-7', '17.774.509-K',
            '5.607.008-7', '39.300.586-6', '34.713.333-7', '39.103.278-5', '24.736.993-7',
            '11.657.052-1', '6.312.501-6', '18.097.611-6', '7.337.067-1', '30.539.528-5',
            '12.362.522-6', '29.606.835-7', '35.048.207-5', '20.672.855-8', '10.992.372-9',
            '20.862.554-3', '35.353.762-8', '39.513.100-1', '13.204.170-9', '38.049.010-2',
            '8.403.624-2', '33.908.802-0', '1.598.966-1', '9.919.261-5', '5.685.946-2',
            '10.777.572-2', '4.489.787-3', '12.344.428-0', '14.450.695-2', '22.843.004-8'
        ]
        donantes = []
        nombres = ['Juan', 'Andrea', 'Roberto', 'Camila', 'Lucía', 'Felipe', 'María', 'Carlos']
        apellidos = ['Araya', 'Castro', 'Mena', 'Herrera', 'Reyes', 'Gómez', 'Vera', 'López']
        comunas = ['Providencia', 'Ñuñoa', 'Las Condes', 'Macul']
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        ocupaciones = ['estudiante', 'trabajador', 'jubilado', 'otro']
        tipo_sangres = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']

        for i in range(100):
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            email = fake.unique.email()
            user = CustomUser.objects.create_user(email=email, password='bloodpoint123', rut=rut, tipo_usuario='donante')
            d = donante.objects.create(
                user=user,
                rut = ruts_reales[i],
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
