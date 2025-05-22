from django.urls import path
from . import views
from django.shortcuts import redirect

def root_view(request):
    return redirect('login')  # or 'home' if you prefer

urlpatterns = [
    path('', root_view),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/representante/', views.signup_representante, name='signup_representante'),
    
    path('adminbp/crear/', views.crear_admin, name='crear_admin'),
    path('adminbp/', views.listar_admins, name='listar_admins'),
    path('adminbp/editar/<int:id>/', views.editar_admin, name='editar_admin'),
    path('adminbp/eliminar/<int:id>/', views.eliminar_admin, name='eliminar_admin'),
    
    path('representantes/', views.listar_representantes, name='listar_representantes'),
    path('representantes/editar/<int:id>/', views.editar_representante, name='editar_representante'),
    path('representantes/eliminar/<int:id>/', views.eliminar_representante, name='eliminar_representante'),

]