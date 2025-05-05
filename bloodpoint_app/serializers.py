from rest_framework import serializers
from .models import donante, representante_org
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import CustomUser

class RepresentanteOrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = representante_org
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['rut', 'email', 'first_name', 'last_name', 'date_joined', 'is_active']  # Incluye los campos que deseas mostrar o actualizar


class donanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = donante
        fields = '__all__'
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

class DonantePerfilSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    rut = serializers.CharField(source='user.rut')

    class Meta:
        model = donante
        fields = [
            'rut',
            'email',
            'nombre_completo',
            'sexo',
            'direccion',
            'comuna',
            'fono',
            'fecha_nacimiento',
            'nacionalidad',
            'tipo_sangre',
            'noti_emergencia',
        ]
