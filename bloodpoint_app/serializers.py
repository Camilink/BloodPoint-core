from rest_framework import serializers
from .models import (
    donante, representante_org, centro_donacion, donacion, solicitud_campana_repo, 
    adminbp, CustomUser, campana, AchievementDefinition, UserAchievement, UserStats
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


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
            'ocupacion',
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
    centro = serializers.SerializerMethodField()
    centro_nombre = serializers.SerializerMethodField() 
    centro_direccion = serializers.SerializerMethodField()
    tipo_sangre = serializers.SerializerMethodField()
    nombre_contexto = serializers.SerializerMethodField()
    
    def get_centro(self, obj):
        return obj.centro_id.nombre_centro if obj.centro_id else None
        
    def get_centro_nombre(self, obj):
        # 🔥 ESTA ES LA PARTE IMPORTANTE
        if obj.campana_relacionada:
            return f"Campaña: {obj.campana_relacionada.nombre_campana}"
        elif obj.solicitud_relacionada:
            centro = obj.solicitud_relacionada.centro_donacion
            return f"Solicitud: {centro.nombre_centro if centro else 'Centro no especificado'}"
        elif obj.centro_id:
            return obj.centro_id.nombre_centro
        return "Centro no especificado"
    
    def get_centro_direccion(self, obj):
        if obj.campana_relacionada and obj.campana_relacionada.id_centro:
            return obj.campana_relacionada.id_centro.direccion_centro
        elif obj.solicitud_relacionada and obj.solicitud_relacionada.centro_donacion:
            return obj.solicitud_relacionada.centro_donacion.direccion_centro
        elif obj.centro_id:
            return obj.centro_id.direccion_centro
        return "Dirección no disponible"
    
    def get_tipo_sangre(self, obj):
        # Obtener tipo de sangre del donante
        return obj.id_donante.tipo_sangre if obj.id_donante else None
    
    def get_nombre_contexto(self, obj):
        # Para el frontend, contexto completo
        if obj.campana_relacionada:
            return obj.campana_relacionada.nombre_campana
        elif obj.solicitud_relacionada:
            centro = obj.solicitud_relacionada.centro_donacion
            centro_nombre = centro.nombre_centro if centro else "Centro"
            fecha = obj.solicitud_relacionada.fecha_solicitud.strftime('%d/%m/%Y')
            return f"{centro_nombre} - Solicitud {fecha}"
        elif obj.centro_id:
            return obj.centro_id.nombre_centro
        return "Donación registrada"
        
    class Meta:
        model = donacion
        fields = [
            'id_donacion',
            'fecha_donacion',
            'cantidad_donacion',  
            'centro_id',
            'centro',
            'centro_nombre',      # 🔥 NUEVO
            'centro_direccion',   # 🔥 NUEVO  
            'tipo_sangre',        # 🔥 NUEVO
            'nombre_contexto',    # 🔥 NUEVO
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
    centro = serializers.SerializerMethodField()
    
    def get_centro(self, obj):
        return obj.id_centro.nombre_centro if obj.id_centro else None
        
    class Meta:
        model = campana
        fields = [
            'id_campana',
            'nombre_campana',
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
            'id_representante',
            'es_emergencia'
        ]

class AchievementDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementDefinition
        fields = ['key', 'name', 'description', 'category', 'symbol', 'required_value']

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementDefinitionSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ['id', 'achievement', 'achieved_at', 'notified']

class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = [
            'total_donations', 'emergency_donations', 'different_centers', 
            'app_shares', 'history_views', 'years_active'
        ]
