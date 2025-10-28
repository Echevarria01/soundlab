from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from soundlab_store.models import Product
from soundlab_store.serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import permissions

# ---------------------------------------------------------
# 🔹 HARDCODED USERS
# ---------------------------------------------------------
HARDCODED_USERS = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "cliente", "password": "cliente123", "role": "cliente"},
    {"username": "tecnico", "password": "tecnico123", "role": "tecnico"},
]

User = get_user_model()

# ---------------------------------------------------------
# 🔹 LOGIN CON SIMPLEJWT
# ---------------------------------------------------------
class HardLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # Buscar usuario hardcodeado
        user_data = next(
            (u for u in HARDCODED_USERS if u["username"] == username and u["password"] == password),
            None
        )
        if not user_data:
            return Response({"error": "Credenciales inválidas"}, status=401)

        # Crear un token JWT válido (usando un usuario real o dummy)
        dummy_user = User.objects.first() or User(username="dummy")
        refresh = RefreshToken.for_user(dummy_user)

        # Agregar datos personalizados al payload
        refresh["username"] = username
        refresh["role"] = user_data["role"]

        return Response({
            "message": "Login exitoso",
            "username": username,
            "role": user_data["role"],
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })

# ---------------------------------------------------------
# 🔹 PERMISO POR ROL
# ---------------------------------------------------------
class IsRole(permissions.BasePermission):
    def __init__(self, role):
        self.required_role = role

    def has_permission(self, request, view):
        # SimpleJWT decodifica el token automáticamente,
        # pero los datos custom (como 'role') no van a request.user,
        # así que se pueden tomar de request.auth si querés usarlo más adelante.
        token = request.auth
        if token and hasattr(token, 'payload'):
            return token.payload.get("role") == self.required_role
        return False

# ---------------------------------------------------------
# 🔹 VISTAS PROTEGIDAS
# ---------------------------------------------------------
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # SimpleJWT ya valida el token automáticamente
        token = request.auth
        role = None
        if token and hasattr(token, 'payload'):
            role = token.payload.get("role")

        return Response({
            "message": f"Hola, {request.user.username or 'usuario hardcodeado'}!",
            "role": role or "desconocido"
        })


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsRole("admin")]

    def get(self, request):
        return Response({"message": "Bienvenido, administrador."})


class ClientOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsRole("cliente")]

    def get(self, request):
        return Response({"message": "Bienvenido, cliente."})


class TechnicianOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsRole("tecnico")]

    def get(self, request):
        return Response({"message": "Bienvenido, técnico."})

# ---------------------------------------------------------
# 🔹 USER PROFILE
# ---------------------------------------------------------
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.auth
        role = None
        if token and hasattr(token, 'payload'):
            role = token.payload.get("role")

        return Response({
            "username": getattr(request.user, "username", "hardcoded"),
            "email": getattr(request.user, "email", ""),
            "is_staff": getattr(request.user, "is_staff", False),
            "is_superuser": getattr(request.user, "is_superuser", False),
            "role": role or "desconocido"
        })

# ---------------------------------------------------------
# 🔹 REGISTER
# ---------------------------------------------------------
class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# ---------------------------------------------------------
# 🔹 PRODUCTOS
# ---------------------------------------------------------
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]






