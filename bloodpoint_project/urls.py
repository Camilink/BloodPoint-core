from django.contrib import admin
from django.urls import path, include, re_path
from bloodpoint_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Admin at standard /admin/ path
    path('admin/', admin.site.urls),
    
    path('donantes_listado/', views.donantes_listado, name='donantes-listado'),
    path('donantes/<int:id>/', views.donante_detail, name='donante-detail'),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),




    # Frontend routes (optional)
    path('', include('bloodpoint_app.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)