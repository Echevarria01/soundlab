from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from soundlab_store.models import Product, Category, Cart

User = get_user_model()

class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass123')
        self.client.login(username='buyer', password='pass123')
        self.category = Category.objects.create(name='Instrumentos')
        self.product = Product.objects.create(
            name='Guitarra Fender',
            description='Stratocaster',
            price=1200,
            stock=10,
            category=self.category
        )

    def test_add_to_cart(self):
        """
        Verifica que un usuario logueado pueda agregar un producto al carrito.
        """
        data = {
            "product_id": self.product.id,
            "quantity": 2
        }
        response = self.client.post('/api/cart/add/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Cart.objects.filter(user=self.user, product=self.product).exists())

