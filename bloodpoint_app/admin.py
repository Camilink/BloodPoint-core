from django.contrib import admin
from .models import donante, representante_org, centro_donacion, donacion, campana, adminbp, solicitud_campana_repo, logro
# Register your models here.

admin.site.register(donante)
admin.site.register(representante_org)
admin.site.register(centro_donacion)
admin.site.register(donacion)
admin.site.register(campana)
admin.site.register(adminbp)
admin.site.register(solicitud_campana_repo)
admin.site.register(logro)
