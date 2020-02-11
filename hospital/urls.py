from django.urls import path

from hospital import views

urlpatterns = [
    path('index', views.index),
]