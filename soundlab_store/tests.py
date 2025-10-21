from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Product, Category

Usuario = get_user_model()

class PruebasDeProductos(APITestCase):
    def setUp(self):
        """
        Se ejecuta antes de cada prueba.
        Crea un usuario administrador y una categoría de ejemplo.
        """
        self.admin_user = Usuario.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.category = Category.objects.create(name='Instrumentos')

    def test_crear_producto_como_admin(self):
        """
        Verifica que un usuario administrador pueda crear un producto.
        """
        # Iniciar sesión como administrador
        self.client.login(username='admin', password='admin123')

        # Datos del nuevo producto
        datos = {
            "name": "Guitarra eléctrica",
            "description": "Modelo Les Paul",
            "price": 1500,
            "stock": 10,
            "category": self.category.id
        }

        # La URL real es /api/products/
        respuesta = self.client.post('/api/products/', datos, format='json')

        # Comprobar que la creación fue exitosa
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name="Guitarra eléctrica").exists())

    def test_listar_productos(self):
        """
        Verifica que se puedan listar los productos correctamente.
        """
        # Crear un producto de prueba
        Product.objects.create(
            name="Batería acústica",
            description="Set de 5 cuerpos",
            price=2500,
            stock=5,
            category=self.category
        )

        # La URL real es /api/products/
        respuesta = self.client.get('/api/products/')

        # Comprobar que la respuesta sea correcta
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertIn("Batería acústica", str(respuesta.data))


class PruebasDeUsuarios(APITestCase):
    def test_registro_de_usuario(self):
        """
        Verifica que se pueda registrar un nuevo usuario.
        """
        datos = {
            "username": "nuevo_usuario",
            "email": "nuevo@test.com",
            "password": "clave123",
        }

        respuesta = self.client.post('/api/usuario/register/', datos, format='json')

        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Usuario.objects.filter(username="nuevo_usuario").exists())

    def test_login_de_usuario(self):
        """
        Verifica que un usuario pueda iniciar sesión correctamente.
        """
        # Crear un usuario
        Usuario.objects.create_user(username="test_login", password="clave123")

        datos_login = {
            "username": "test_login",
            "password": "clave123",
        }

        respuesta = self.client.post('/api/usuario/login/', datos_login, format='json')

        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertIn('token', respuesta.data)  # si usás JWT o token auth
