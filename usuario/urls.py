from django.urls import path
from .views import RegistroView, login_view

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', login_view, name='login'),
]
