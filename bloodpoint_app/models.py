from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from cloudinary.models import CloudinaryField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, rut=None, **extra_fields):
        # Validación de email obligatorio para todos
        if not email:
            raise ValueError('El email es obligatorio para todos los usuarios')
        
        # Validación de RUT obligatorio solo para donantes
        tipo_usuario = extra_fields.get('tipo_usuario')
        if tipo_usuario == 'donante' and not rut:
            raise ValueError('El RUT es obligatorio para donantes')
        
        # Limpieza y creación del usuario
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            rut=rut if tipo_usuario == 'donante' else None,  # RUT solo para donantes
            **extra_fields
        )
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
    # Eliminamos username y usamos email como identificador principal
    username = None
    email = models.EmailField('correo electrónico', unique=True)  # Obligatorio y único
    rut = models.CharField('RUT', max_length=12, unique=True, null=True, blank=True)  # Solo para donantes
    
    # Tipo de usuario
    TIPO_USUARIO_CHOICES = [
        ('donante', 'Donante'),
        ('representante', 'Representante'),
        ('admin', 'Administrador'),
    ]
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='donante'
    )
    
    # Campos de permisos
    is_superadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Configuración de login
    USERNAME_FIELD = 'email'  # Todos inician sesión con email por defecto
    REQUIRED_FIELDS = []  # Campos adicionales para createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email} ({self.tipo_usuario})'

    def get_username(self):
        """Sobrescribe para permitir login con RUT solo para donantes"""
        return self.rut if self.tipo_usuario == 'donante' else self.email

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
    ocupacion = models.CharField(max_length=100)
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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True) 
    id_representante = models.AutoField(primary_key=True)
    rut_representante = models.CharField(max_length=12, unique=True)
    rol = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    credencial = CloudinaryField('image', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    verificado = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre

    def email(self):
        return self.user.email

    def full_name(self):
        return self.nombre + ' ' + self.apellido

    def verificado_text(self):
        return 'Representante verificado' if self.verificado else 'Representante sin verificar'

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
    ('campana', 'Campaña'),
    ('solicitud', 'Solicitud de Campaña'),
]
class donacion(models.Model):
    id_donacion = models.AutoField(primary_key=True)
    id_donante = models.ForeignKey(donante, on_delete=models.CASCADE)
    fecha_donacion = models.DateField()
    cantidad_donacion = models.IntegerField()
    centro_id = models.ForeignKey(centro_donacion, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tipo_donacion = models.CharField(max_length=20, choices=TIPO_DONACION_CHOICES)
    validada = models.BooleanField(default=False)
    es_intencion = models.BooleanField(default=False)
        # Asociación con campaña o solicitud
    campana_relacionada = models.ForeignKey('campana', null=True, blank=True, on_delete=models.SET_NULL)
    solicitud_relacionada = models.ForeignKey('solicitud_campana_repo', null=True, blank=True, on_delete=models.SET_NULL)

class campana(models.Model):
    id_campana = models.AutoField(primary_key=True)
    nombre_campana = models.CharField(max_length=100)
    fecha_campana = models.DateField()
    id_centro = models.ForeignKey(centro_donacion, on_delete=models.CASCADE, blank=True, null=True)
    apertura = models.TimeField()
    cierre = models.TimeField()
    meta = models.CharField()
    latitud = models.IntegerField()
    longitud = models.IntegerField()
    id_representante = models.ForeignKey(representante_org, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    fecha_termino = models.DateField()
    id_solicitud = models.ForeignKey('solicitud_campana_repo', null=True, blank=True, on_delete=models.SET_NULL)
    validada = models.BooleanField(default=True)  # Por ahora, se marca como validada al crear
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('desarrollandose', 'Desarrollándose'),
        ('cancelado', 'Cancelado'),
        ('completo', 'Completo')
    ], default='pendiente')
    es_emergencia = models.BooleanField(default=False)
class adminbp(models.Model):
    id_admin = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    contrasena = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

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

class AchievementDefinition(models.Model):
    key = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('basic', 'Básico'),
        ('level', 'Nivel'),
        ('social', 'Social'),
        ('rare', 'Raro/Especial')
    ])
    symbol = models.CharField(max_length=10, blank=True, null=True)
    required_value = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.key})"

class UserAchievement(models.Model):
    donante = models.ForeignKey(donante, on_delete=models.CASCADE)
    achievement = models.ForeignKey(AchievementDefinition, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('donante', 'achievement')

    def __str__(self):
        return f"{self.donante.nombre_completo} - {self.achievement.name}"

class UserStats(models.Model):
    donante = models.OneToOneField(donante, on_delete=models.CASCADE)
    total_donations = models.IntegerField(default=0)
    emergency_donations = models.IntegerField(default=0)
    different_centers = models.IntegerField(default=0)
    app_shares = models.IntegerField(default=0)
    history_views = models.IntegerField(default=0)
    registration_date = models.DateTimeField(auto_now_add=True)
    years_active = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Stats for {self.donante.nombre_completo}"

# Keep the old model for backwards compatibility
class logro(models.Model):
    id_logro = models.AutoField(primary_key=True)
    descripcion_logro = models.CharField()
    id_donante = models.ForeignKey(donante, on_delete=models.CASCADE)
    fecha_logro = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class preguntas_usuario(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    pregunta=models.CharField(max_length=255)
    respondida=models.BooleanField(default=False)
    fecha_pregunta = models.DateTimeField(auto_now_add=True)

class respuestas_representante(models.Model):
    id = models.AutoField(primary_key=True)
    respuesta=models.CharField(max_length=255)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)
    id_pregunta = models.ForeignKey(preguntas_usuario, on_delete=models.CASCADE)
    id_representante = models.ForeignKey(representante_org, on_delete=models.CASCADE)
