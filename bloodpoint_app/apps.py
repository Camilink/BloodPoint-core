from django.apps import AppConfig


class BloodpointConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloodpoint_app'
    
    def ready(self):
        import bloodpoint_app.signals
