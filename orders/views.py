from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem
from .serializers import OrderSerializer
from soundlab_store.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    # ================================
    #   QUERIES: Admin ve todo, usuarios ven lo suyo
    # ================================
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().order_by('-created_at')
        return Order.objects.filter(user=user).order_by('-created_at')

    # ================================
    #   CREAR PEDIDOS
    # ================================
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

        # Validación de campos obligatorios
        for field in required_fields:
            if field not in data:
                return Response(
                    {"error": f"Falta el campo {field}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        items = data.get("items")
        if not isinstance(items, list) or len(items) == 0:
            return Response(
                {"error": "Debe haber al menos un ítem en el pedido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear orden vacía inicialmente
        order = Order.objects.create(
            user=user,
            payment_method=data['payment_method'],
            shipping_name=data['shipping_name'],
            shipping_address=data['shipping_address'],
            shipping_city=data['shipping_city'],
            shipping_phone=data['shipping_phone'],
            total=0
        )

        # Crear ítems y calcular total
        total = 0
        for item in items:
            try:
                product = Product.objects.get(id=item['product'])
            except Product.DoesNotExist:
                order.delete()
                return Response(
                    {"error": f"Producto con id {item['product']} no existe"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            quantity = item.get('quantity', 1)
            subtotal = product.price * quantity
            total += subtotal

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=quantity,
                price=product.price,
            )

        order.total = total
        order.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # ================================
    #   ADMIN: actualizar estado
    # ================================
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        # Obtener el pedido
        order = self.get_object()

        # Recibir el nuevo estado desde la solicitud
        new_status = request.data.get("status")

        # Lista de estados válidos
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]

        # Validar que el nuevo estado sea uno de los válidos
        if not new_status:
            return Response(
                {"error": "El campo 'status' es obligatorio"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status not in valid_statuses:
            return Response(
                {"error": f"Estado inválido. Usa uno de: {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Actualizar el estado del pedido
        order.status = new_status
        order.save()

        # Retornar el pedido actualizado
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    # ================================
    #   CORS para OPTIONS
    # ================================
    def options(self, request, *args, **kwargs):
        response = Response(status=200)
        response['Access-Control-Allow-Origin'] = 'https://soundlabstore.netlify.app'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response










