from django.contrib.auth.backends import BaseBackend, ModelBackend
from bloodpoint_app.models import CustomUser


class RutAuthBackend(BaseBackend):
    def authenticate(self, request, rut=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(rut=rut)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
# bloodpoint_app/backends.py

class EmailOrRutBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        if username is None:
            username = kwargs.get('email') or kwargs.get('rut')

        user = CustomUser.objects.filter(email=username).first()
        
        if not user:
            user = CustomUser.objects.filter(rut=username).first()
        
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

