from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from soundlab_store.models import Product, Category, Cart, Order, OrderItem

User = get_user_model()

class OrderTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='buyer', password='pass123')
        self.client.login(username='buyer', password='pass123')
        self.category = Category.objects.create(name='Instrumentos')
        self.product = Product.objects.create(
            name='Bajo eléctrico',
            description='Precision Bass',
            price=900,
            stock=5,
            category=self.category
        )
        Cart.objects.create(user=self.user, product=self.product, quantity=2)

    def test_create_order_from_cart(self):
        """
        Verifica que se cree correctamente un pedido a partir del carrito.
        """
        response = self.client.post('/api/orders/create_from_cart/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        order = Order.objects.get(user=self.user)
        self.assertTrue(OrderItem.objects.filter(order=order).exists())

