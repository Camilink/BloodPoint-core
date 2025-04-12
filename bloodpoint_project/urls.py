from django.contrib import admin
from django.urls import path, include
from bloodpoint_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # Admin at standard /admin/ path
    path('admin/', admin.site.urls),
    
    # API endpoints under /api/ prefix
    path('donantes/', views.donantes_listado),
    path('donantes/<int:id>/', views.donante_detail, name='donante-detail'),
    
    
    # Frontend routes (optional)
    path('', include('bloodpoint_app.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)