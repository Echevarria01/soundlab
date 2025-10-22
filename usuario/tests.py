from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioTests(APITestCase):
    def test_registro_usuario(self):
        """Prueba que un usuario se registre correctamente"""
        url = reverse('register')  # necesitaremos definir este name en urls.py
        data = {
            "username": "testuser",
            "password": "12345",
            "email": "test@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Usuario.objects.filter(username="testuser").exists())

    def test_login_usuario(self):
        """Prueba que el login funcione correctamente"""
        user = Usuario.objects.create_user(username="testuser", password="12345")
        url = reverse('login')
        data = {"username": "testuser", "password": "12345"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Inicio de sesión exitoso", response.data["message"])

    def test_login_invalido(self):
        """Prueba que no se pueda loguear con datos incorrectos"""
        url = reverse('login')
        data = {"username": "usernoexiste", "password": "wrongpass"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
