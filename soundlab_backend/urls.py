from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    # AUTH JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # USUARIOS (registro, login, perfil)
    path("api/user/", include("usuario.urls")),

    # STORE
    path("", include("soundlab_store.urls")),

    # ORDERS
    path("api/orders/", include("orders.urls")),
]


