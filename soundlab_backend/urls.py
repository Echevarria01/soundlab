from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
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




