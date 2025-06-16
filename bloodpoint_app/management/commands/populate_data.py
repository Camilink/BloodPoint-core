from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, date
from bloodpoint_app.models import CustomUser, adminbp, donante, representante_org, centro_donacion, donacion, campana, solicitud_campana_repo

class Command(BaseCommand):
    help = 'Llena la base de datos con datos de prueba específicos (basados en la query)'

    def handle(self, *args, **options):
        # Limpieza opcional: eliminar registros previos si quieres (descomenta si quieres)
        adminbp.objects.all().delete()
        representante_org.objects.all().delete()
        donante.objects.all().delete()
        CustomUser.objects.filter(tipo_usuario__in=['admin', 'representante', 'donante']).delete()
        campana.objects.all().delete()
        solicitud_campana_repo.objects.all().delete()
        centro_donacion.objects.all().delete()
        donacion.objects.all().delete()

        # --- ADMINISTRADORES ---
        admins = [
            ('admin@gmail.com', 'bloodpoint123', 'admin', 'Juan', 'Pérez'),
            ('admin2@gmail.com', 'bloodpoint123', 'admin', 'Carla', 'Soto'),
            ('admin3@gmail.com', 'bloodpoint123', 'admin', 'María', 'Olivares'),
        ]

        for email, pwd, tipo, first_name, last_name in admins:
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'tipo_usuario': tipo,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_staff': True,
                    'is_superuser': True,
                    'is_superadmin': True,
                    'is_active': True,
                    'date_joined': datetime.now(),
                }
            )
            if created:
                user.set_password(pwd)
                user.save()

            if not adminbp.objects.filter(user=user).exists():
                adminbp.objects.create(
                    user=user,
                    nombre=f'{first_name} {last_name}',
                    email=email,
                    contrasena=pwd,
                    created_at=datetime.now()
                )

        # --- REPRESENTANTES ---
        representantes = [
            ('camilaajojeda@gmail.com', 'bloodpoint123', 'representante', 'Camila', 'Jopia', '17388920-5', 'Voluntaria Cruz Roja', True, 'credencial1.pdf'),
            ('paulina678@gmail.com', 'bloodpoint123', 'representante', 'Paulina', 'Ríos', '18845236-1', 'Representante institucional', False, 'credencial2.pdf'),
            ('cristian333@gmail.com', 'bloodpoint123', 'representante', 'Cristian', 'Morales', '16578431-9', 'Encargado logístico', True, 'credencial3.pdf'),
            ('lorena222@gmail.com', 'bloodpoint123', 'representante', 'Lorena', 'Silva', '15793211-3', 'Representante institucional', True, 'credencial4.pdf'),
            ('matias999@gmail.com', 'bloodpoint123', 'representante', 'Matías', 'Figueroa', '17845622-5', 'Encargado logístico', False, 'credencial5.pdf'),
        ]

        for email, pwd, tipo, first_name, last_name, rut_representante, rol, verificado, credencial in representantes:
            user, created = CustomUser.objects.get_or_create(
                email=email,
                defaults={
                    'tipo_usuario': tipo,
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True,
                    'is_superadmin': False,
                    'is_staff': False,
                    'is_superuser': False,
                    'date_joined': datetime.now(),
                }
            )
            if created:
                user.set_password(pwd)
                user.save()

            if not representante_org.objects.filter(user=user).exists():
                representante_org.objects.create(
                    user=user,
                    rut_representante=rut_representante,
                    rol=rol,
                    nombre=first_name,
                    apellido=last_name,
                    credencial=credencial,
                    verificado=verificado,
                    created_at=datetime.now()
                )

        # --- DONANTES ---
        nombres = ['Juan', 'Andrea', 'Roberto', 'Camila', 'Lucía', 'Felipe', 'María', 'Carlos', 'Sofía', 'Javier', 'Valentina', 'Pedro', 'Daniela', 'Tomás', 'Fernanda', 'Ignacio', 'Antonia', 'Diego', 'Martina', 'Benjamín', 'Josefa', 'Sebastián', 'Florencia', 'Vicente', 'Javiera', 'Agustín', 'Constanza', 'Matías', 'Trinidad', 'Andrés', 'Francisca', 'Leonardo', 'Catalina', 'Cristóbal', 'Paula']
        apellidos = ['Araya', 'Castro', 'Mena', 'Herrera', 'Reyes', 'Gómez', 'Vera', 'López', 'Soto', 'Martínez', 'Ramírez', 'Rojas', 'Morales', 'Navarro', 'Gutiérrez', 'Salazar', 'Fuentes', 'Pizarro', 'Campos', 'Escobar', 'Alvarez', 'Peña', 'Carrasco', 'Silva', 'Muñoz', 'Torres', 'Orellana', 'Vargas', 'Ortega', 'Núñez', 'Zúñiga', 'Henríquez', 'Barrera', 'Sepúlveda', 'Palma']
        tipo_sangres = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
        comunas = ['Providencia', 'Ñuñoa', 'Las Condes', 'Macul', 'San Miguel', 'La Florida', 'Puente Alto', 'Maipú', 'Recoleta', 'Santiago Centro']
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']

        for i in range(35):
            rut_gen = f'1{i+1}234567-{(i % 9) + 1}'
            correo = f"{nombres[i].lower()}{i+1}@gmail.com"

            user, created = CustomUser.objects.get_or_create(
                email=correo,
                defaults={
                    'tipo_usuario': 'donante',
                    'rut': rut_gen,
                    'first_name': nombres[i],
                    'last_name': apellidos[i],
                    'is_active': True,
                    'is_superadmin': False,
                    'is_staff': False,
                    'is_superuser': False,
                    'date_joined': datetime.now(),
                }
            )
            if created:
                user.set_password('bloodpoint123')
                user.save()

            if not donante.objects.filter(user=user).exists():
                donante.objects.create(
                    user=user,
                    rut=rut_gen,
                    nombre_completo=f"{nombres[i]} {apellidos[i]}",
                    sexo='F' if (i % 2 == 0) else 'M',
                    ocupacion='Profesional Salud',
                    direccion=f'Calle Ficticia {i+1}',
                    comuna=comunas[(i % len(comunas))],
                    fono=f'+5691234{str(i+1).zfill(4)}',
                    fecha_nacimiento=date(1990, 1, 1) + timedelta(days=100*(i+1)),
                    nacionalidad='Chilena',
                    tipo_sangre=tipo_sangres[(i % len(tipo_sangres))],
                    dispo_dia_donacion=dias[(i % len(dias))],
                    nuevo_donante=(i % 2 == 0),
                    noti_emergencia=True,
                    created_at=datetime.now()
                )

        self.stdout.write(self.style.SUCCESS('¡Datos insertados en la base de datos con éxito!'))
