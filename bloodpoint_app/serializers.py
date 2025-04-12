from rest_framework import serializers
from .models import donante

class donanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = donante
        fields = 'id_donante', 'rut', 'nombre_completo', 'email', 'contrasena', 'direccion', 'comuna', 'fono', 'fecha_nacimiento', 'nacionalidad', 'tipo_sangre', 'dispo_dia_donacion', 'nuevo_donante', 'noti_emergencia'