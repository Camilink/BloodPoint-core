from rest_framework import serializers
from .models import donante
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class donanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = donante
        fields = 'id_donante', 'rut', 'nombre_completo', 'email', 'contrasena', 'direccion', 'comuna', 'fono', 'fecha_nacimiento', 'nacionalidad', 'tipo_sangre', 'dispo_dia_donacion', 'nuevo_donante', 'noti_emergencia'

        extra_kwargs = {
            'constrasena': {'write_only': True},
        }

class userDonanteSerializer(serializers.ModelSerializer):
    contrasena = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = donante
        fields =  'email', 'contrasena'
    
    def create(self, validated_data):

        validated_data['contrasena'] = make_password(validated_data.pop(['contrasena']))
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id_donante
        return representation