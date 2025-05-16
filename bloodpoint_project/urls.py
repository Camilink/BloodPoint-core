from django.contrib import admin
from django.urls import path, include, re_path
from bloodpoint_app import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static 
from django.conf import settings


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
    #super set
    path('api/superset-token/<str:chart_id>/', views.generate_guest_token, name='chart-token'),

    # Frontend routes (optional)
    path('', include('bloodpoint_app.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)