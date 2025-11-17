from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    description = serializers.CharField(source='product.description', read_only=True)  # Añadimos la descripción

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'description']  # Incluir descripción



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'user_name',
            'created_at',
            'payment_method',
            'status',
            'shipping_name',
            'shipping_address',
            'shipping_city',
            'shipping_phone',
            'total',
            'items',
        ]
        read_only_fields = ['user', 'status', 'created_at', 'total']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        order = Order.objects.create(user=user, **validated_data)

        total = 0
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']

            subtotal = product.price * quantity
            total += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                price=product.price
            )

        order.total = total
        order.save()

        return order




