from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from soundlab_api.views import UserProfileView, RegisterView, HardLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Usuarios
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/profile/', UserProfileView.as_view(), name='profile'),

    # Hard login
    path('api/hard-login/', HardLoginView.as_view(), name='hard_login'),

    # Incluye todas las URLs de la app
    path('api/', include('soundlab_api.urls')),  # 🔹 Esto requiere import include
]




