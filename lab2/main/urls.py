from django.urls import path
from . import views
from .views import register

app_name = 'main'

urlpatterns = [
    path('', views.index, name='home'),
    path('profile', views.profile, name='profile'),
    path('register', register.as_view(), name='register'),
]
