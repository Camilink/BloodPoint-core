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

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(email=email)
            if user.tipo_usuario != 'donante' and user.check_password(password):  # Excluye donantes
                return user
        except CustomUser.DoesNotExist:
            return None