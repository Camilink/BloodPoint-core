from django.urls import path
from . import views

urlpatterns = [
#    path('', views.home_view, name='home'),
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('signup/representante/', views.signup_representante, name='signup_representante'),
    path ('login/', views.login_representante_view, name='login')]