from django.urls import path
from . import views
from django.shortcuts import redirect

def root_view(request):
    return redirect('login')  # or 'home' if you prefer

urlpatterns = [
    path('', root_view),
    path('home/', views.home, name='home'),
    path('login/', views.login_representante_view, name='login'),
    path('signup/representante/', views.signup_representante, name='signup_representante'),
]