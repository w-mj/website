from django.urls import path

from schedule import views

urlpatterns = [
    path('neu/', views.neu),
    path('neu/<slug:uid>', views.neu_ics)
]