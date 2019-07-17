from django.urls import path

from dialog_label import views

urlpatterns = [
    path('', views.index),
    path('clear', views.clear),
    path('labeldialog', views.label),
    path('getdialog', views.get_dialog),
    path('console/', views.console),
    path('uploadfile', views.upload),
    path('download', views.download),
]

