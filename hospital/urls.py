from django.urls import path

from hospital import views, func

urlpatterns = [
    path('index', views.index),
    path('picture', func.picture),
    path('ill', func.uploadill),
    path('checkcode', func.checkcode),
]