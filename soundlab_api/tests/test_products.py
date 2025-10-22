from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from soundlab_store.models import Product, Category

User = get_user_model()

class ProductTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
        self.category = Category.objects.create(name='Instrumentos')

    def test_create_product(self):
        """
        Verifica que un admin pueda crear un producto.
        """
        self.client.login(username='admin', password='admin123')
        data = {
            "name": "Guitarra eléctrica",
            "description": "Modelo Les Paul",
            "price": 1500,
            "stock": 10,
            "category": self.category.id
        }
        response = self.client.post('/api/products/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name="Guitarra eléctrica").exists())

    def test_list_products(self):
        """
        Verifica que se puedan listar los productos correctamente.
        """
        Product.objects.create(
            name="Batería acústica",
            description="Set de 5 cuerpos",
            price=2500,
            stock=5,
            category=self.category
        )
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Batería acústica", str(response.data))

