from django.urls import path
from . import views

urlpatterns = [
#    path('', views.home_view, name='home'),
    path('home/', views.home, name='home'),
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]