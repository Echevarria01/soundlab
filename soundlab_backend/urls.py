from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def api_root(request):
    return JsonResponse({
        "api": "SoundLab Backend",
        "status": "online",
        "endpoints": {
            "auth": "/token/",
            "auth_refresh": "/token/refresh/",
            "user": "/user/",
            "store": "/store/",
            "orders": "/api/orders/"  # Este es el endpoint correcto
        }
    })

urlpatterns = [
    path("", api_root),  # Página principal de la API

    path("admin/", admin.site.urls),  # Admin

    # JWT Token
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Usuario
    path("user/", include("usuario.urls")),  # Ruta de usuario

    # Productos + Home
    path("store/", include("soundlab_store.urls")),  # Ruta de productos

    # Orders - ruta API de orders
    path("api/", include("orders.urls")),
    # Asegúrate de que esté con el prefijo /api/
]

