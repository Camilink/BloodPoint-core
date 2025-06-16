from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, date
import random
from bloodpoint_app.models import CustomUser, adminbp, donante, representante_org, centro_donacion, donacion, campana, solicitud_campana_repo

class Command(BaseCommand):
    help = 'Llena la base de datos con datos de prueba específicos'

    def handle(self, *args, **options):
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
        representantes = [
            ('camilaajojeda@gmail.com', 'bloodpoint123', 'Camila', 'Jopia', '17388920-5', 'Voluntaria Cruz Roja', True, 'credencial1.pdf'),
            ('paulina678@gmail.com', 'bloodpoint123', 'Paulina', 'Ríos', '18845236-1', 'Representante institucional', False, 'credencial2.pdf'),
            ('cristian333@gmail.com', 'bloodpoint123', 'Cristian', 'Morales', '16578431-9', 'Encargado logístico', True, 'credencial3.pdf'),
        ]

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
        tipo_sangres = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        comunas = ['Providencia', 'Ñuñoa', 'Las Condes', 'Macul', 'San Miguel', 'La Florida', 'Maipú', 'Recoleta']
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']
        ocupaciones = ['estudiante', 'trabajador', 'jubilado', 'otro']
        donantes = []

        for i in range(35):
            email = f"{nombres[i].lower()}{i+1}@gmail.com"
            user = CustomUser.objects.create_user(
                email=email,
                password='bloodpoint123',
                tipo_usuario='donante',
                rut=f'1{i+1}234567-{(i % 9) + 1}',
                first_name=nombres[i],
                last_name=apellidos[i]
            )
            d = donante.objects.create(
                user=user,
                rut=user.rut,
                nombre_completo=f"{user.first_name} {user.last_name}",
                sexo='F' if i % 2 == 0 else 'M',
                ocupacion=random.choice(ocupaciones),
                direccion=f'Calle Ficticia {i+1}',
                comuna=random.choice(comunas),
                fono=f'+5691234{str(i+1).zfill(4)}',
                fecha_nacimiento=date(1990, 1, 1) + timedelta(days=100 * (i + 1)),
                nacionalidad='Chilena',
                tipo_sangre=random.choice(tipo_sangres),
                dispo_dia_donacion=random.choice(dias),
                nuevo_donante=(i % 2 == 0),
                noti_emergencia=True,
                created_at=datetime.now()
            )
            donantes.append(d)

        # Centro de Donación
        centro = centro_donacion.objects.create(
            nombre='Centro Donación Santiago',
            direccion='Av. Principal 123',
            comuna='Santiago',
            region='Región Metropolitana',
            telefono='+56212345678',
            email='centro@sangre.cl',
            latitud=-33.4489,
            longitud=-70.6693,
            created_at=datetime.now()
        )

        # Campañas
        coordenadas_rm = [
            (-33.4569, -70.6483), (-33.4378, -70.6505), (-33.4143, -70.6044),
            (-33.5001, -70.6155), (-33.4711, -70.7233), (-33.4530, -70.6781)
        ]
        campañas = []

        for i in range(5):
            lat, lon = coordenadas_rm[i % len(coordenadas_rm)]
            email = list(rep_users.keys())[i % len(rep_users)]
            rep = rep_users[email]
            camp = campana.objects.create(
                nombre=f'Campaña N°{i+1}',
                descripcion='Campaña de recolección de sangre',
                tipo='campaña',
                fecha_inicio=datetime.now() - timedelta(days=random.randint(1, 30)),
                fecha_fin=datetime.now() + timedelta(days=random.randint(5, 20)),
                centro_donacion=centro,
                representante=rep,
                latitud=lat,
                longitud=lon,
                created_at=datetime.now()
            )
            campañas.append(camp)


        for i, d in enumerate(donantes):
            for j in range(1 if i > 30 else 0, 2 if i > 30 else 1):  # para balancear
                if i < 30:
                    camp = campañas[0]  # campaña de Camila
                else:
                    camp = random.choice(campañas[1:])
                donacion.objects.create(
                    donante=d,
                    campana=camp,
                    fecha_donacion=datetime.now() - timedelta(days=random.randint(0, 15)),
                    validada=bool(random.getrandbits(1)),
                    created_at=datetime.now()
                )

        self.stdout.write(self.style.SUCCESS('¡Datos insertados exitosamente!'))
