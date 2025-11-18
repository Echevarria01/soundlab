from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import logout, get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .serializers import UsuarioSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

Usuario = get_user_model()

# -----------------------------
# Registro de usuario
# -----------------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if not username or not email or not password:
            return Response({"error": "Todos los campos son obligatorios."}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "El correo electrónico no es válido."}, status=400)

        if Usuario.objects.filter(username=username).exists():
            return Response({"error": "El nombre de usuario ya está en uso."}, status=400)

        if Usuario.objects.filter(email=email).exists():
            return Response({"error": "Ya existe un usuario con este correo electrónico."}, status=400)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": list(e)}, status=400)

        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=False
        )

        return Response({"message": "Usuario registrado correctamente."}, status=201)


# -----------------------------
# Login con JWT
# -----------------------------
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer








# -----------------------------
# Logout
# -----------------------------
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Sesión cerrada correctamente."})


# -----------------------------
# Perfil de usuario autenticado
# -----------------------------
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


# -----------------------------
# Vista JWT estándar extendida
# -----------------------------
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# -----------------------------
# Solo admin puede ver todos los usuarios
# -----------------------------
class ListUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = Usuario.objects.all()
        serializer = UsuarioSerializer(users, many=True)
        return Response(serializer.data)

