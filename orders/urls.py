from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')  # Registra 'orders'

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas de 'orders'
]




