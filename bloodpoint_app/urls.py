from django.urls import path
from . import views

urlpatterns = [
#    path('', views.home_view, name='home'),
    path('home/', views.HomePage, name='home'),
    path('login/', views.LoginPage, name='login'),
    path('', views.SignupPage, name='signup'),
]