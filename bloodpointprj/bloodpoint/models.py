from django.db import models

# Create your models here.
class donante(models.Model):
    id_donante = models.AutoField(primary_key=True)
    rut = models.CharField(unique=True)    
    nombre_completo = models.CharField()
    email = models.EmailField()
    contrasena = models.CharField()    
    direccion = models.CharField()
    comuna = models.CharField()
    fono = models.CharField()
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField()
    tipo_sangre = models.CharField()
    dispo_dia_donacion= models.DateField()
    nuevo_donante = models.BooleanField()
    noti_emergencia = models.BooleanField()

class representante_org(models.Model):
    id_representante = models.AutoField(primary_key=True)
    rol = models.CharField()
    nombre = models.CharField()
    email = models.EmailField()
    contrasena = models.CharField()

class centro_donacion(models.Model):
    id_centro = models.AutoField(primary_key=True)
    nombre_centro = models.CharField()
    direccion_centro = models.CharField()
    comuna = models.CharField()
    telefono = models.CharField()
    fecha_creacion = models.DateField()
    id_representante = models.ForeignKey(representante_org, on_delete=models.CASCADE)

class donacion(models.Model):
    id_donacion = models.AutoField(primary_key=True)
    id_donante = models.ForeignKey(donante, on_delete=models.CASCADE)
    fecha_donacion = models.DateField()
    cantidad_donacion = models.IntegerField()
    centro_id = models.ForeignKey(centro_donacion, on_delete=models.CASCADE)

class campana(models.Model):
    id_campana = models.AutoField(primary_key=True)
    fecha_campana = models.DateField()
    id_centro = models.ForeignKey(centro_donacion, on_delete=models.CASCADE)
    apertura = models.TimeField()
    cierre = models.TimeField()
    meta = models.CharField()

class adminbp(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nombre = models.CharField()
    email = models.EmailField()
    contrasena = models.CharField()

class solicitud_campana_repo(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    tipo_sangre_sol= models.CharField()
    fecha_solicitud = models.DateField()
    cantidad_personas = models.IntegerField()
    descripcion_solicitud = models.CharField()
    direccion_solicitud = models.CharField()
    comuna_solicitud = models.CharField()
    id_donante = models.ForeignKey(donante, on_delete=models.CASCADE)

class logro(models.Model):
    id_logro = models.AutoField(primary_key=True)
    descripcion_logro = models.CharField()
    id_donante = models.ForeignKey(donante, on_delete=models.CASCADE)
    fecha_logro = models.DateField()