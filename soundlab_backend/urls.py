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
            "store": "/",
            "orders": "/orders/"
        }
    })

urlpatterns = [
    path("", api_root),

    path("admin/", admin.site.urls),

    # JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Usuario
    path("user/", include("usuario.urls")),

    # Productos + Home
    path("", include("soundlab_store.urls")),

    # Orders
    path("orders/", include("orders.urls")),
]
