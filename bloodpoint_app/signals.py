from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging
from .models import UserAchievement
from .services import FCMNotificationService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=UserAchievement)
def send_achievement_notification(sender, instance, created, **kwargs):
    """
    Send Firebase notification when a UserAchievement is created
    """
    if created and not instance.notified:
        try:
            # Send notification asynchronously if possible, otherwise synchronously
            if hasattr(settings, 'USE_CELERY') and settings.USE_CELERY:
                # If Celery is configured, send notification asynchronously
                send_achievement_notification_task.delay(instance.id)
            else:
                # Send notification synchronously
                response = FCMNotificationService.send_achievement_notification(instance)
                if response:
                    logger.info(f"Achievement notification sent for user {instance.user.id}, achievement {instance.achievement.key}")
                else:
                    logger.info(f"Achievement notification skipped (Firebase not configured) for user {instance.user.id}, achievement {instance.achievement.key}")
                
        except Exception as e:
            logger.error(f"Failed to send achievement notification for user {instance.user.id}: {e}")


# Celery task for asynchronous notification sending (optional)
try:
    from celery import shared_task
    
    @shared_task
    def send_achievement_notification_task(user_achievement_id):
        """
        Celery task to send achievement notification asynchronously
        """
        try:
            user_achievement = UserAchievement.objects.get(id=user_achievement_id)
            FCMNotificationService.send_achievement_notification(user_achievement)
            logger.info(f"Async achievement notification sent for user {user_achievement.user.id}, achievement {user_achievement.achievement.key}")
        except UserAchievement.DoesNotExist:
            logger.error(f"UserAchievement with id {user_achievement_id} not found")
        except Exception as e:
            logger.error(f"Failed to send async achievement notification: {e}")
            
except ImportError:
    # Celery not available, which is fine
    pass
