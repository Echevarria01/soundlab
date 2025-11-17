from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserProfileView, MyTokenObtainPairView, ListUsersView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('list/', ListUsersView.as_view(), name='list_users'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]




