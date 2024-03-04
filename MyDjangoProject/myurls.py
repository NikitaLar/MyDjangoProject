from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [

    path('getusers/', views.getusers, name="getusers"),
    path('getusersid/', views.getusersid, name="GetUseById"),
    path('Addusers/', views.postusers, name="postusers"),
    path('Editusers/', views.Editusers, name="Editusers"),
    path('Delete_User/', views.Delete_User, name="Delete_User"),
]