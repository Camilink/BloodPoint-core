from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, rut=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        tipo_usuario = extra_fields.get('tipo_usuario')
        if tipo_usuario == 'donante' and not rut:
            raise ValueError('El rut es obligatorio para los donantes')
        email = self.normalize_email(email)
        user = self.model(email=email, rut=rut, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_superadmin', True)
        extra_fields.setdefault('tipo_usuario', 'admin')
        return self.create_user(email=email, password=password, **extra_fields)
class CustomUser(AbstractUser):
    username = None  # Eliminamos el campo username predeterminado
    email = models.EmailField(unique=False, blank=True, null=True)  # Puedes mantener email como opcional o requerido, sin unique=True
    rut = models.CharField(unique=True, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20, choices=[  # Agrega esto
        ('donante', 'Donante'),
        ('representante', 'Representante'),
        ('admin', 'Administrador'),
    ])
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    #configuracion de login
    USERNAME_FIELD = 'rut'  # Define rut como el identificador único
    REQUIRED_FIELDS = ['email']  # Email sigue siendo requerido

    objects = CustomUserManager()  # Usa el manager personalizado
    def __str__(self):
        return f'{self.rut} - {self.tipo_usuario}'

TIPO_SANGRE_CHOICES = [
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
]
class donante(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # Vinculación correcta
    id_donante = models.AutoField(primary_key=True)
    rut = models.CharField(unique=True, max_length=12)
    nombre_completo = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1)
    direccion = models.CharField(max_length=255)
    comuna = models.CharField(max_length=100)
    fono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=50)
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES)
    dispo_dia_donacion = models.CharField(max_length=50)
    nuevo_donante = models.BooleanField(default=False)
    noti_emergencia = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo

class representante_org(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # Añadido este campo
    id_representante = models.AutoField(primary_key=True)
    rut_representante = models.CharField(max_length=12, unique=True)
    rol = models.CharField(max_length=100)  # Añadido max_length
    nombre = models.CharField(max_length=100)  # Añadido max_length
    apellido = models.CharField(max_length=100)
    credencial = models.ImageField(upload_to='credenciales', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verificado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre

class centro_donacion(models.Model):
    id_centro = models.AutoField(primary_key=True)
    nombre_centro = models.CharField()
    direccion_centro = models.CharField()
    comuna = models.CharField()
    telefono = models.CharField()
    fecha_creacion = models.DateField()
    id_representante = models.ForeignKey(representante_org, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    horario_apertura = models.TimeField()
    horario_cierre = models.TimeField()
    
TIPO_DONACION_CHOICES = [
    ('punto', 'Punto de Donación'),
    ('campana', 'Campaña'),
    ('solicitud', 'Solicitud de Campaña'),
]
class donacion(models.Model):
    id_donacion = models.AutoField(primary_key=True)
    id_donante = models.ForeignKey(donante, on_delete=models.CASCADE)
    fecha_donacion = models.DateField()
    cantidad_donacion = models.IntegerField()
    centro_id = models.ForeignKey(centro_donacion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tipo_donacion = models.CharField(max_length=20, choices=TIPO_DONACION_CHOICES)
       # Asociación con campaña o solicitud
    campana_relacionada = models.ForeignKey('campana', null=True, blank=True, on_delete=models.SET_NULL)
    solicitud_relacionada = models.ForeignKey('solicitud_campana_repo', null=True, blank=True, on_delete=models.SET_NULL)

class campana(models.Model):
    id_campana = models.AutoField(primary_key=True)
    fecha_campana = models.DateField()
    id_centro = models.ForeignKey(centro_donacion, on_delete=models.CASCADE)
    apertura = models.TimeField()
    cierre = models.TimeField()
    meta = models.CharField()
    latitud = models.CharField()
    longitud = models.CharField()
    id_representante = models.ForeignKey(representante_org, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateField()  # Fecha límite
    id_solicitud = models.ForeignKey('solicitud_campana_repo', null=True, blank=True, on_delete=models.SET_NULL)
    validada = models.BooleanField(default=True)  # Por ahora, se marca como validada al crear
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('desarrollandose', 'Desarrollándose'),
        ('cancelado', 'Cancelado'),
        ('completo', 'Completo')
    ], default='pendiente')
class adminbp(models.Model):
    id_admin = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    contrasena = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(max_length=50)

class solicitud_campana_repo(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    tipo_sangre_sol= models.CharField()
    fecha_solicitud = models.DateField()
    cantidad_personas = models.IntegerField()
    descripcion_solicitud = models.CharField()
    comuna_solicitud = models.CharField()
    ciudad_solicitud = models.CharField()
    region_solicitud = models.CharField()
    id_donante = models.ForeignKey(donante, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    centro_donacion = models.ForeignKey(centro_donacion, on_delete=models.CASCADE, null=True)
    fecha_termino = models.DateField()
    desactivado_por = models.ForeignKey(representante_org, on_delete=models.SET_NULL, null=True, blank=True)
    campana_asociada = models.OneToOneField('campana', on_delete=models.SET_NULL, null=True, blank=True)

class logro(models.Model):
    id_logro = models.AutoField(primary_key=True)
    descripcion_logro = models.CharField()
    id_donante = models.ForeignKey(donante, on_delete=models.CASCADE)
    fecha_logro = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)