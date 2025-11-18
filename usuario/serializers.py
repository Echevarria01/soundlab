from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

Usuario = get_user_model()

# Serializer para CRUD y perfil
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'rol', 'password', 'is_staff'
        ]
        extra_kwargs = {'password': {'write_only': True}}

# Serializer personalizado para JWT
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['rol'] = user.rol  # agrega el rol al token
        return token

    def validate(self, attrs):
        username_field = self.username_field
        username_input = attrs.get(username_field)

        # También permitir login enviando `email`
        if not username_input and 'email' in attrs:
            username_input = attrs.get('email')

        # Si lo que recibimos parece ser un email → lo convertimos al username real
        if username_input and '@' in str(username_input):
            try:
                usuario = Usuario.objects.get(email__iexact=username_input)
                attrs[username_field] = usuario.username  # asignar username real
            except Usuario.DoesNotExist:
                pass  # dejar que falle con credenciales inválidas

        return super().validate(attrs)






