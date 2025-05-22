# bloodpoint_app/backends.py

from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class EmailOrRutBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        if username is None:
            username = kwargs.get('email') or kwargs.get('rut')
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(rut=username)
            except CustomUser.DoesNotExist:
                return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
