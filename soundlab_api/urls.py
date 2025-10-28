# soundlab_api/urls.py

from django.urls import path
from .views import (
    ProtectedView,
    UserProfileView,
    RegisterView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    HardLoginView,
    AdminOnlyView,
    ClientOnlyView,
    TechnicianOnlyView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 🔹 Autenticación JWT estándar
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔹 Login hardcodeado (sin base de datos)
    path('hard-login/', HardLoginView.as_view(), name='hard_login'),

    # 🔹 Registro y perfil de usuario
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),

    # 🔹 Productos (solo admin puede crear, editar o borrar)
    path('products/', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product_detail'),

    # 🔹 Rutas protegidas por rol hardcodeado
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('client-only/', ClientOnlyView.as_view(), name='client_only'),
    path('technician-only/', TechnicianOnlyView.as_view(), name='technician_only'),

    # 🔹 Endpoint protegido de prueba
    path('protected/', ProtectedView.as_view(), name='protected'),
]


