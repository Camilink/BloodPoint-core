from rest_framework import serializers
from .models import donante, representante_org, centro_donacion,donacion,solicitud_campana_repo, adminbp, CustomUser, campana
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import CustomUser


class AdminBPSerializer(serializers.ModelSerializer):
    class Meta:
        model = adminbp
        fields = '__all__'
class CentroDonacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = centro_donacion
        fields = '__all__'
        
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

    def update(self, instance, validated_data):
        # Extraer los datos del usuario (CustomUser)
        user_data = validated_data.pop('user', {})

        # Actualizar datos del usuario
        user = instance.user
        if 'email' in user_data:
            user.email = user_data['email']
        if 'rut' in user_data:
            user.rut = user_data['rut']
        user.save()

        # Actualizar campos del modelo Donante
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class DonacionSerializer(serializers.ModelSerializer):
    centro = serializers.CharField(source='centro_id.nombre_centro', read_only=True)
    class Meta:
        model = donacion
        fields = [
            'id_donacion',
            'id_donante',
            'fecha_donacion',
            'cantidad_donacion',
            'centro_id',
            'centro',
            'created_at',
            'campana_relacionada',
            'solicitud_relacionada',
            'tipo_donacion',
            'validada',
            'es_intencion',
        ]

class SolicitudCampanaSerializer(serializers.ModelSerializer):

     class Meta:
        model = solicitud_campana_repo
        fields = '__all__'
        
class CampanaSerializer(serializers.ModelSerializer):
    centro = serializers.CharField(source='id_centro.nombre_centro', read_only=True)
    class Meta:
        model = campana
        fields = [
            'id_campana',
            'fecha_campana',
            'fecha_termino',
            'apertura',
            'cierre',
            'meta',
            'latitud',
            'longitud',
            'id_centro',
            'centro',
            'id_solicitud',
            'validada',
            'estado',
            'id_representante'
        ]
