from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('trip_add', views.trip_add),
    path('add_trip', views.add_trip),
    path('join/<id>', views.join),
    path ('delete/<id>', views.delete),
    path('cancel/<id>', views.cancel)
  
]