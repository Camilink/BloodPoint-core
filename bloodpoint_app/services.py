from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Q
from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging
import logging
from .models import (
    donante, AchievementDefinition, UserAchievement, UserStats, 
    donacion, centro_donacion, campana
)

logger = logging.getLogger(__name__)


class AchievementService:
    
    @staticmethod
    def initialize_achievements():
        """Initialize all achievement definitions in the database"""
        achievements = [
            # Basic Achievements
            {
                'key': 'basic_welcome',
                'name': 'Bienvenido al Ciclo',
                'description': 'Te registraste en la aplicación.',
                'category': 'basic',
                'symbol': 'fa-user-plus',
                'required_value': 1
            },
            {
                'key': 'basic_intencion_vital',
                'name': 'Intención Vital',
                'description': 'Programaste tu primera intención de donación.',
                'category': 'basic',
                'symbol': 'fa-heart-pulse',
                'required_value': 1
            },
            {
                'key': 'basic_explorador_solidario',
                'name': 'Explorador Solidario',
                'description': 'Donaste en dos centros distintos.',
                'category': 'basic',
                'symbol': 'fa-compass',
                'required_value': 2
            },
            {
                'key': 'basic_mi_historia',
                'name': 'Mi Historia de Vida',
                'description': 'Consultaste tu historial de donaciones 5 veces.',
                'category': 'basic',
                'symbol': 'fa-history',
                'required_value': 5
            },
            
            # Level Achievements
            {
                'key': 'level_1_plaqueta',
                'name': 'Nivel 1: Plaqueta',
                'description': 'El inicio, pequeño pero esencial.',
                'category': 'level',
                'symbol': 'fa-medal',
                'required_value': 0
            },
            {
                'key': 'level_2_globulo_rojo',
                'name': 'Nivel 2: Glóbulo Rojo',
                'description': 'Energía, aporte vital.',
                'category': 'level',
                'symbol': 'fa-droplet',
                'required_value': 3
            },
            {
                'key': 'level_3_globulo_blanco',
                'name': 'Nivel 3: Glóbulo Blanco',
                'description': 'Protección, apoyo a otros.',
                'category': 'level',
                'symbol': 'fa-shield-virus',
                'required_value': 4
            },
            {
                'key': 'level_4_linfocito_t',
                'name': 'Nivel 4: Linfocito T',
                'description': 'Constancia e impacto sostenido.',
                'category': 'level',
                'symbol': 'fa-brain',
                'required_value': 7
            },
            {
                'key': 'level_5_medula_osea',
                'name': 'Nivel 5: Médula Ósea',
                'description': 'Fuente de vida.',
                'category': 'level',
                'symbol': 'fa-dna',
                'required_value': 10
            },
            {
                'key': 'level_6_corazon',
                'name': 'Nivel 6: Corazón',
                'description': 'Donante ejemplar, motor de la comunidad.',
                'category': 'level',
                'symbol': 'fa-heart',
                'required_value': 15
            },
            
            # Social Achievements
            {
                'key': 'social_embajador_flujo_lvl1',
                'name': 'Embajador del Flujo (Nivel 1)',
                'description': 'Compartiste la app en redes sociales 1 vez.',
                'category': 'social',
                'symbol': 'fa-share-nodes',
                'required_value': 1
            },
            {
                'key': 'social_embajador_flujo_lvl2',
                'name': 'Embajador del Flujo (Nivel 2)',
                'description': 'Compartiste la app 3 veces.',
                'category': 'social',
                'symbol': 'fa-share-nodes',
                'required_value': 3
            },
            {
                'key': 'social_embajador_flujo_lvl3',
                'name': 'Embajador del Flujo (Nivel 3)',
                'description': 'Compartiste la app 10 veces.',
                'category': 'social',
                'symbol': 'fa-share-nodes',
                'required_value': 10
            },
            {
                'key': 'social_vocero_vital',
                'name': 'Vocero Vital',
                'description': 'Compartiste la app 10 veces o generaste alto tráfico.',
                'category': 'social',
                'symbol': 'fa-bullhorn',
                'required_value': 10
            },
            
            # Rare Achievements
            {
                'key': 'rare_tipo_unico',
                'name': 'Tipo Único',
                'description': 'Tienes un grupo sanguíneo poco común (AB-).',
                'category': 'rare',
                'symbol': 'fa-gem',
                'required_value': 1
            },
            {
                'key': 'rare_heroe_emergencia',
                'name': 'Héroe de Emergencia',
                'description': 'Donaste en una campaña urgente.',
                'category': 'rare',
                'symbol': 'fa-shield',
                'required_value': 1
            },
            {
                'key': 'rare_donante_universal',
                'name': 'Donante Universal',
                'description': 'Logro exclusivo para donantes con grupo 0-.',
                'category': 'rare',
                'symbol': 'fa-earth-americas',
                'required_value': 1
            },
            {
                'key': 'rare_heroe_silencioso',
                'name': 'Héroe Silencioso',
                'description': 'Donaste sin compartir y sin reclamar recompensa.',
                'category': 'rare',
                'symbol': 'fa-user-secret',
                'required_value': 1
            }
        ]
        
        for achievement_data in achievements:
            AchievementDefinition.objects.update_or_create(
                key=achievement_data['key'],
                defaults=achievement_data
            )
    
    @staticmethod
    def get_or_create_user_stats(donante_obj):
        """Get or create user stats for a donor"""
        stats, created = UserStats.objects.get_or_create(donante=donante_obj)
        return stats
    
    @staticmethod
    def update_user_stats(donante_obj):
        """Update user statistics"""
        stats = AchievementService.get_or_create_user_stats(donante_obj)
        
        # Count total donations
        stats.total_donations = donacion.objects.filter(
            id_donante=donante_obj, validada=True
        ).count()
        
        # Count emergency donations
        stats.emergency_donations = donacion.objects.filter(
            id_donante=donante_obj, 
            validada=True,
            campana_relacionada__es_emergencia=True
        ).count()
        
        # Count different centers
        stats.different_centers = donacion.objects.filter(
            id_donante=donante_obj, validada=True
        ).values('centro_id').distinct().count()
        
        # Calculate years active
        registration_date = donante_obj.created_at
        years_diff = (timezone.now() - registration_date).days / 365.25
        stats.years_active = int(years_diff)
        
        stats.save()
        return stats
    
    @staticmethod
    def check_and_award_achievements(donante_obj):
        """Check and award all applicable achievements for a donor"""
        stats = AchievementService.update_user_stats(donante_obj)
        new_achievements = []
        
        # Check basic achievements
        new_achievements.extend(AchievementService._check_basic_achievements(donante_obj, stats))
        
        # Check level achievements
        new_achievements.extend(AchievementService._check_level_achievements(donante_obj, stats))
        
        # Check social achievements
        new_achievements.extend(AchievementService._check_social_achievements(donante_obj, stats))
        
        # Check rare achievements
        new_achievements.extend(AchievementService._check_rare_achievements(donante_obj, stats))
        
        return new_achievements
    
    @staticmethod
    def _check_basic_achievements(donante_obj, stats):
        """Check basic achievements"""
        new_achievements = []
        
        # Basic Welcome - awarded on registration
        if not UserAchievement.objects.filter(donante=donante_obj, achievement_id='basic_welcome').exists():
            achievement = AchievementDefinition.objects.get(key='basic_welcome')
            UserAchievement.objects.create(donante=donante_obj, achievement=achievement)
            new_achievements.append(achievement)
        
        # Basic Intention - awarded when first donation intention is created
        if donacion.objects.filter(id_donante=donante_obj, es_intencion=True).exists():
            if not UserAchievement.objects.filter(donante=donante_obj, achievement_id='basic_intencion_vital').exists():
                achievement = AchievementDefinition.objects.get(key='basic_intencion_vital')
                UserAchievement.objects.create(donante=donante_obj, achievement=achievement)
                new_achievements.append(achievement)
        
        # Basic Explorer - donated in 2 different centers
        if stats.different_centers >= 2:
            if not UserAchievement.objects.filter(donante=donante_obj, achievement_id='basic_explorador_solidario').exists():
                achievement = AchievementDefinition.objects.get(key='basic_explorador_solidario')
                UserAchievement.objects.create(donante=donante_obj, achievement=achievement)
                new_achievements.append(achievement)
        
        # Basic History - viewed history 5 times
        if stats.history_views >= 5:
            if not UserAchievement.objects.filter(donante=donante_obj, achievement_id='basic_mi_historia').exists():
                achievement = AchievementDefinition.objects.get(key='basic_mi_historia')
                UserAchievement.objects.create(donante=donante_obj, achievement=achievement)
                new_achievements.append(achievement)
        
        return new_achievements
    
    @staticmethod
    def _check_level_achievements(donante_obj, stats):
        """Check level-based achievements"""
        new_achievements = []
        level_achievements = [
            ('level_1_plaqueta', 0),
            ('level_2_globulo_rojo', 3),
            ('level_3_globulo_blanco', 4),
            ('level_4_linfocito_t', 7),
            ('level_5_medula_osea', 10),
            ('level_6_corazon', 15)
        ]
        
        for key, required_donations in level_achievements:
            if stats.total_donations >= required_donations:
                # Special conditions for some levels
                if key == 'level_3_globulo_blanco' and stats.emergency_donations < 1:
                    continue
                if key == 'level_4_linfocito_t' and stats.emergency_donations < 1:
                    continue
                if key == 'level_5_medula_osea' and stats.emergency_donations < 5:
                    continue
                if key == 'level_6_corazon' and stats.years_active < 2:
                    continue
                
                if not UserAchievement.objects.filter(donante=donante_obj, achievement_id=key).exists():
                    achievement = AchievementDefinition.objects.get(key=key)
                    UserAchievement.objects.create(donante=donante_obj, achievement=achievement)
                    new_achievements.append(achievement)
        
        return new_achievements
    
    @staticmethod
    def _check_social_achievements(donante_obj, stats):
        """Check social achievements"""
        new_achievements = []
        social_achievements = [
            ('social_embajador_flujo_lvl1', 1),
            ('social_embajador_flujo_lvl2', 3),
            ('social_embajador_flujo_lvl3', 10),
            ('social_vocero_vital', 10)
        ]
        
        for key, required_shares in social_achievements:
            if stats.app_shares >= required_shares:
                if not UserAchievement.objects.filter(donante=donante_obj, achievement_id=key).exists():
                    achievement = AchievementDefinition.objects.get(key=key)
                    UserAchievement.objects.create(donante=donante_obj, achievement=achievement)
                    new_achievements.append(achievement)
        
        return new_achievements
    
    @staticmethod
    def _check_rare_achievements(donante_obj, stats):
        """Check rare achievements"""
        new_achievements = []
        
        # Rare blood type (AB-)
        if donante_obj.tipo_sangre == 'AB-':
            if not UserAchievement.objects.filter(donante=donante_obj, achievement_id='rare_tipo_unico').exists():
                achievement = AchievementDefinition.objects.get(key='rare_tipo_unico')
                UserAchievement.objects.create(donante=donante_obj, achievement=achievement)
                new_achievements.append(achievement)
        
        # Universal donor (O-)
        if donante_obj.tipo_sangre == 'O-' and stats.total_donations >= 1:
            if not UserAchievement.objects.filter(donante=donante_obj, achievement_id='rare_donante_universal').exists():
                achievement = AchievementDefinition.objects.get(key='rare_donante_universal')
                UserAchievement.objects.create(donante=donante_obj, achievement=achievement)
                new_achievements.append(achievement)
        
        # Emergency hero
        if stats.emergency_donations >= 1:
            if not UserAchievement.objects.filter(donante=donante_obj, achievement_id='rare_heroe_emergencia').exists():
                achievement = AchievementDefinition.objects.get(key='rare_heroe_emergencia')
                UserAchievement.objects.create(donante=donante_obj, achievement=achievement)
                new_achievements.append(achievement)
        
        return new_achievements
    
    @staticmethod
    def record_app_share(donante_obj):
        """Record that the user shared the app"""
        stats = AchievementService.get_or_create_user_stats(donante_obj)
        stats.app_shares += 1
        stats.save()
        return AchievementService.check_and_award_achievements(donante_obj)
    
    @staticmethod
    def record_history_view(donante_obj):
        """Record that the user viewed their donation history"""
        stats = AchievementService.get_or_create_user_stats(donante_obj)
        stats.history_views += 1
        stats.save()
        return AchievementService.check_and_award_achievements(donante_obj)
    
    @staticmethod
    def get_user_achievements(donante_obj):
        """Get all achievements for a user"""
        return UserAchievement.objects.filter(donante=donante_obj).select_related('achievement')
    
    @staticmethod
    def get_unnotified_achievements(donante_obj):
        """Get achievements that haven't been notified yet"""
        return UserAchievement.objects.filter(
            donante=donante_obj, 
            notified=False
        ).select_related('achievement')
    
    @staticmethod
    def mark_achievements_as_notified(achievement_ids):
        """Mark achievements as notified"""
        UserAchievement.objects.filter(id__in=achievement_ids).update(notified=True)


class FCMNotificationService:
    """Service for sending Firebase Cloud Messaging notifications"""
    
    _firebase_initialized = False
    
    @classmethod
    def initialize_firebase(cls):
        """Initialize Firebase Admin SDK if not already initialized"""
        if not cls._firebase_initialized and not firebase_admin._apps:
            try:
                # Check if Firebase service account key is configured
                firebase_key = getattr(settings, 'FIREBASE_SERVICE_ACCOUNT_KEY', None)
                
                if firebase_key and firebase_key != 'None' and firebase_key.strip():
                    # Try to parse as JSON dict first, then as file path
                    try:
                        import json
                        # If it's a JSON string, parse it
                        if firebase_key.startswith('{'):
                            cred_dict = json.loads(firebase_key)
                            cred = credentials.Certificate(cred_dict)
                        else:
                            # Treat as file path
                            cred = credentials.Certificate(firebase_key)
                        firebase_admin.initialize_app(cred)
                        cls._firebase_initialized = True
                        logger.info("Firebase Admin SDK initialized successfully with service account")
                    except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
                        logger.error(f"Invalid Firebase service account configuration: {e}")
                        raise ValueError(f"Firebase service account key is invalid: {e}")
                else:
                    # No service account key configured
                    logger.warning("FIREBASE_SERVICE_ACCOUNT_KEY not configured. Firebase notifications disabled.")
                    raise ValueError("Firebase service account key not configured")
                    
            except Exception as e:
                logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
                raise
    
    @classmethod
    def send_achievement_notification(cls, user_achievement):
        """Send notification for a new achievement"""
        try:
            cls.initialize_firebase()
            
            # Import here to avoid circular imports
            from .models import DeviceToken
            
            # Get user device tokens
            device_tokens = DeviceToken.objects.filter(
                user=user_achievement.user,
                is_active=True
            ).values_list('token', flat=True)
            
            if not device_tokens:
                logger.warning(f"No device tokens found for user {user_achievement.user.id}")
                return
            
            # Create notification message
            achievement = user_achievement.achievement
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title='¡Nuevo Logro Desbloqueado!',
                    body=f'Has conseguido: {achievement.name}',
                    image=None  # You can add an achievement image URL here if available
                ),
                data={
                    'type': 'achievement',
                    'achievement_id': str(achievement.id),
                    'achievement_key': achievement.key,
                    'achievement_name': achievement.name,
                    'achievement_description': achievement.description,
                    'achievement_category': achievement.category,
                    'achievement_symbol': achievement.symbol,
                    'user_achievement_id': str(user_achievement.id)
                },
                tokens=list(device_tokens)
            )
            
            # Send the message
            response = messaging.send_multicast(message)
            
            # Log results
            logger.info(f"Achievement notification sent to {len(device_tokens)} devices. "
                       f"Success: {response.success_count}, Failures: {response.failure_count}")
            
            # Handle failed tokens (remove invalid ones)
            if response.failure_count > 0:
                cls._handle_failed_tokens(device_tokens, response.responses, user_achievement.user)
            
            return response
            
        except ValueError as e:
            # Firebase not configured - log but don't raise error
            logger.warning(f"Firebase not configured, skipping achievement notification: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to send achievement notification: {e}")
            return None
    
    @classmethod
    def _handle_failed_tokens(cls, tokens, responses, user):
        """Remove invalid device tokens"""
        from .models import DeviceToken
        
        invalid_tokens = []
        for i, response in enumerate(responses):
            if not response.success:
                error = response.exception
                # Check if token is invalid or unregistered
                if (hasattr(error, 'code') and 
                    error.code in ['invalid-registration-token', 'registration-token-not-registered']):
                    invalid_tokens.append(tokens[i])
        
        if invalid_tokens:
            DeviceToken.objects.filter(
                user=user,
                token__in=invalid_tokens
            ).update(is_active=False)
            logger.info(f"Deactivated {len(invalid_tokens)} invalid device tokens for user {user.id}")
    
    @classmethod
    def send_custom_notification(cls, user, title, body, data=None):
        """Send a custom notification to a user"""
        try:
            cls.initialize_firebase()
            
            # Import here to avoid circular imports
            from .models import DeviceToken
            
            device_tokens = DeviceToken.objects.filter(
                user=user,
                is_active=True
            ).values_list('token', flat=True)
            
            if not device_tokens:
                logger.warning(f"No device tokens found for user {user.id}")
                return None
            
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                tokens=list(device_tokens)
            )
            
            response = messaging.send_multicast(message)
            logger.info(f"Custom notification sent to {len(device_tokens)} devices. "
                       f"Success: {response.success_count}, Failures: {response.failure_count}")
            
            if response.failure_count > 0:
                cls._handle_failed_tokens(device_tokens, response.responses, user)
            
            return response
            
        except ValueError as e:
            # Firebase not configured - log but don't raise error
            logger.warning(f"Firebase not configured, skipping custom notification: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to send custom notification: {e}")
            return None
