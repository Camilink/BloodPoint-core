from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, donante, representante_org, centro_donacion, donacion, 
    campana, adminbp, solicitud_campana_repo, logro, AchievementDefinition, 
    UserAchievement, UserStats
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ['email'] 
    list_display = ['email']  # Ajustar si es necesario


@admin.register(AchievementDefinition)
class AchievementDefinitionAdmin(admin.ModelAdmin):
    list_display = ['key', 'name', 'category', 'symbol', 'required_value']
    list_filter = ['category']
    search_fields = ['name', 'key']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['donante', 'achievement', 'achieved_at', 'notified']
    list_filter = ['achievement__category', 'notified', 'achieved_at']
    search_fields = ['donante__nombre_completo', 'achievement__name']

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['donante', 'total_donations', 'emergency_donations', 'different_centers', 'app_shares']
    search_fields = ['donante__nombre_completo']

admin.site.register(donante)
admin.site.register(representante_org)
admin.site.register(centro_donacion)
admin.site.register(donacion)
admin.site.register(campana)
admin.site.register(adminbp)
admin.site.register(solicitud_campana_repo)
admin.site.register(logro)
