from rest_framework import serializers
from .models import Category, Product, Order, OrderItem
import urllib.parse

# -------------------- CATEGORY --------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# -------------------- PRODUCT --------------------
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock', 'image']

    def get_image(self, obj):
        if not obj.image:
            return None
        # Codifica la URL para que funcione con espacios y caracteres especiales
        image_url = f"/img/productos/{obj.image}"
        return urllib.parse.quote(image_url, safe="/")  # safe="/" mantiene las barras


# -------------------- ORDER ITEM --------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


# -------------------- ORDER --------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['total']



