from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  # o la vista que quieras probar
]

