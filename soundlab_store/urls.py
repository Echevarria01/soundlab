# soundlab_store/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, OrdenViewSet, PagoViewSet, ProductoViewSet, InstrumentoViewSet, AdministradorViewSet, CarritoViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'ordenes', OrdenViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'instrumentos', InstrumentoViewSet)
router.register(r'administradores', AdministradorViewSet)
router.register(r'carritos', CarritoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

