from django.contrib import admin
from .models import donante, representante_org, centro_donacion, donacion, campana, adminbp, solicitud_campana_repo, logro
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ['email'] 
    list_display = ['email']  # Ajustar si es necesario


admin.site.register(donante)
admin.site.register(representante_org)
admin.site.register(centro_donacion)
admin.site.register(donacion)
admin.site.register(campana)
admin.site.register(adminbp)
admin.site.register(solicitud_campana_repo)
admin.site.register(logro)
