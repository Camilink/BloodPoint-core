from django.contrib import admin
from django.urls import path, include, re_path
from bloodpoint_app import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static 
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin at standard /admin/ path
    path('admin/', admin.site.urls),
    
    path('donantes_listado/', views.donantes_listado, name='donantes-listado'),
    path('donantes/<int:id>/', views.donante_detail, name='donante-detail'),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('representantes/', views.list_representantes, name='listar-representantes'), # Para listar representantes de org
    path('representantes/<int:id>/', views.representante_detail, name='representante-detail'),
    path('representantes/register/', views.register_representante, name='register-representante'),  # Para registrar
    path('centros/', views.centros_listado, name='centros-listado'),  # Para listar centros
    path('centros/<int:id>/', views.centro_detail, name='centro-detail'),  # Para obtener un centro (y hacer get,put,delete, etc)
    path('donaciones/registrar/', views.registrar_donacion, name='registrar-donacion'),
    path('donaciones/historial/', views.historial_donaciones, name='historial-donaciones'),
    path('solicitudes/crear/', views.crear_solicitud_campana, name='crear-solicitud'),
    path('solicitudes/', views.listar_solicitudes_campana, name='listar-solicitudes'),
    path('campanas/<int:campana_id>/progreso/', views.progreso_campana, name='progreso-campana'),
    path('donaciones/<int:donacion_id>/validar/', views.validar_donacion),
    path('donaciones/qr/', views.escanear_qr_donacion, name='qr-donacion'),
    path('campanas/crear/', views.crear_campana, name='crear_campana'),
    path('campanas/activas/', views.campanas_activas, name='campanas_activas'),
    path('api/campanas_activas_representante/', views.campanas_activas_representante, name='campanas_activas_representante'),
    path('ask/', views.ask_bot, name='preguntar-llm'),
    
    # Achievement endpoints
    path('achievements/', views.user_achievements, name='user-achievements'),
    path('achievements/stats/', views.user_stats, name='user-stats'),
    path('achievements/share/', views.record_app_share, name='record-app-share'),
    path('achievements/history-view/', views.record_history_view, name='record-history-view'),
    path('achievements/unnotified/', views.unnotified_achievements, name='unnotified-achievements'),
    path('achievements/mark-notified/', views.mark_achievements_notified, name='mark-achievements-notified'),

    #super set
    path('api/superset-token/<str:chart_id>/', views.generate_guest_token, name='chart-token'),

    # Frontend routes (optional)
    path('', include('bloodpoint_app.urls')),

    #MAIL
    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            html_email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='/password-reset/done/'
        ), 
        name='password_reset'),

    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ), 
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/password-reset-complete/'
        ), 
        name='password_reset_confirm'),

    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ), 
        name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
