from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, OrderListCreateView, home

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', home, name='home'),
    path('orders/', OrderListCreateView.as_view(), name='order-create'),
    path('', include(router.urls)),
]



