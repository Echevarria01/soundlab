from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from soundlab_store.models import Product
from rest_framework.decorators import action

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        required_fields = [
            'payment_method',
            'shipping_name',
            'shipping_address',
            'shipping_city',
            'shipping_phone',
            'items'
        ]
        for field in required_fields:
            if field not in data:
                return Response({"error": f"Falta el campo {field}"}, status=status.HTTP_400_BAD_REQUEST)

        items = data.get("items")
        if not isinstance(items, list) or len(items) == 0:
            return Response({"error": "Debe haber al menos un ítem en el pedido"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=user,
            payment_method=data['payment_method'],
            shipping_name=data['shipping_name'],
            shipping_address=data['shipping_address'],
            shipping_city=data['shipping_city'],
            shipping_phone=data['shipping_phone'],
            total=0
        )

        total = 0
        for item in items:
            try:
                product = Product.objects.get(id=item['product'])
            except Product.DoesNotExist:
                order.delete()
                return Response({"error": f"Producto con id {item['product']} no existe"}, status=status.HTTP_400_BAD_REQUEST)

            subtotal = product.price * item.get('quantity', 1)
            total += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=item.get('quantity', 1),
                price=product.price,
            )

        order.total = total
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 👇 NUEVO: acción admin para actualizar estado
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")

        valid_statuses = ['pending', 'paid', 'cancelled', 'rejected']
        if new_status not in valid_statuses:
            return Response(
                {"error": "Estado inválido. Usa: pending, paid, cancelled o rejected"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save()
        return Response({"message": f"Estado del pedido #{order.id} cambiado a '{new_status}'"}, status=status.HTTP_200_OK)






