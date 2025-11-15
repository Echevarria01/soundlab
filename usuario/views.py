from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .serializers import UsuarioSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


Usuario = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        # --- Validaciones básicas ---
        if not username or not email or not password:
            return Response({"error": "Todos los campos son obligatorios."}, status=400)

        # Validar formato del correo
        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "El correo electrónico no es válido."}, status=400)

        # Verificar si el usuario o email ya existen
        if Usuario.objects.filter(username=username).exists():
            return Response({"error": "El nombre de usuario ya está en uso."}, status=400)

        if Usuario.objects.filter(email=email).exists():
            return Response({"error": "Ya existe un usuario con este correo electrónico."}, status=400)

        # Validar contraseña segura
        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": list(e)}, status=400)

        # Crear usuario cliente (no admin)
        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=False
        )

        return Response({"message": "Usuario registrado correctamente."}, status=201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Debe ingresar usuario y contraseña."}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Inicio de sesión exitoso."})
        else:
            return Response({"error": "Credenciales inválidas."}, status=401)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Sesión cerrada correctamente."})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer