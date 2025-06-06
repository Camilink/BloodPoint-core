from django.urls import path
from . import views
from django.shortcuts import redirect

def root_view(request):
    return redirect('login')  # or 'home' if you prefer

urlpatterns = [
    path('', root_view),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path("redirect/", views.redirect_after_login, name="redirect_after_login"),
    path('signup/representante/', views.signup_representante, name='signup_representante'),
    
    path('administrador/crear/', views.crear_admin, name='crear_admin'),
    path('administrador/', views.admin_index, name='admin_index'),
    path('administrador/detalles/<int:id>/', views.detalles_admin, name='detalles_admin'),
    path('administrador/editar/<int:id>/', views.editar_admin, name='editar_admin'),
    path('administrador/eliminar/<int:id>/', views.eliminar_admin, name='eliminar_admin'),
    path("dashboard/admin/", views.admin_home, name="admin_home"),
    
    path('representantes/', views.representante_index, name='representante_index'),
    path('representantes/editar/<int:id>/', views.editar_representante, name='editar_representante'),
    path('representantes/eliminar/<int:id>/', views.eliminar_representante, name='eliminar_representante'),
    path('logout/', views.logout_view, name='logout')
]