from django.urls import path
from . import views
from django.shortcuts import redirect
from .views import descargar_top3_campanas

def root_view(request):
    return redirect('login')  # or 'home' if you prefer

urlpatterns = [
    path('', root_view),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/representante/', views.signup_representante, name='signup_representante'),
    
    path('administrador/crear/', views.crear_admin, name='crear_admin'),
    path('administrador/', views.admin_index, name='admin_index'),
    path('administrador/detalles/<int:id>/', views.detalles_admin, name='detalles_admin'),
    path('administrador/editar/<int:id>/', views.editar_admin, name='editar_admin'),
    path('administrador/eliminar/<int:id>/', views.eliminar_admin, name='eliminar_admin'),
    path("dashboard/admin/", views.admin_home, name="admin_home"),

    path('representante/', views.representante_index, name='representante_index'),
    path('representante/detalles/<int:id>/', views.detalles_representante, name='detalles_representante'),
    path('representante/editar/<int:id>/', views.editar_representante, name='editar_representante'),
    path('representante/eliminar/<int:id>/', views.eliminar_representante, name='eliminar_representante'),
    path('representante/verificar/<int:id>/', views.verificar_representante, name='verificar_representante'),

    path('representante/lista_verificar/', views.lista_verificar, name='lista_verificar'),
    path('representante/lista_verificar/<int:id>/', views.detalles_verificar, name='detalles_verificar'),

    path('campana/<int:campana_id>/descargar_csv/', views.exportar_resumen_una_campana_csv, name='descargar_csv_campana'),
    path('campana/<int:campana_id>/descargar_excel/', views.descargar_excel_campana, name='descargar_excel_campana'),
    path('exportar-top3-campanas/', descargar_top3_campanas, name='exportar_top3_campanas'),

    path('campanas/', views.campana_index, name='campana_index'),
    path('campanas/detalles/<int:id>/', views.detalles_campana, name='detalles_campana'),
    path('campanas/<int:campana_id>/', views.validar_campana, name='validar_campana'),
    path('logout/', views.logout_view, name='logout')
]
