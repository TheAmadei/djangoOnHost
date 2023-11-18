from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='users'),
    path('userRecords/<int:user_id>', views.listOfUserRecords, name='listOfUserRecords'),
]
