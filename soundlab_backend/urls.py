from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def api_root(request):
    return JsonResponse({
        "api": "SoundLab Backend",
        "status": "online",
        "endpoints": {
            "auth": "/api/token/",
            "auth_refresh": "/api/token/refresh/",
            "user": "/api/user/",
            "store": "/api/",
            "orders": "/api/orders/"
        }
    })

urlpatterns = [
    # Ruta raíz
    path("", api_root),

    # Django admin
    path("admin/", admin.site.urls),

    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Usuario
    path("api/user/", include("usuario.urls")),

    # Productos y categorías
    path("api/", include("soundlab_store.urls")),

    # Orders
    path("api/orders/", include("orders.urls")),
]
