from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
    def test_user_registration(self):
        """
        Verifica que se pueda registrar un nuevo usuario.
        """
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = self.client.post('/api/usuario/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        """
        Verifica que un usuario pueda iniciar sesión correctamente.
        """
        User.objects.create_user(username='testuser', password='testpass123')
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post('/api/usuario/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Si usás JWT o Token Auth

