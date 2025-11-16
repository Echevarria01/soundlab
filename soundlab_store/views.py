from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Category, Product, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

# -------------------- Home --------------------
def home(request):
    return HttpResponse("Bienvenido a SoundLab Store API")

# -------------------- Category --------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# -------------------- Product --------------------
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request  # ✅ Necesario para construir la URL completa de imagen
        return context


# -------------------- Order --------------------
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        carrito = data.get('items', [])

        if not carrito:
            return Response({"error": "No se enviaron productos en 'items'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            total = sum(float(item['price']) * int(item['quantity']) for item in carrito)
        except KeyError as e:
            return Response({"error": f"Falta la clave {str(e)} en uno de los items."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Price y quantity deben ser números."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            shipping_name=data.get('shipping_name'),
            shipping_address=data.get('shipping_address'),
            shipping_city=data.get('shipping_city'),
            shipping_phone=data.get('shipping_phone'),
            payment_method=data.get('payment_method'),
            invoice_type=data.get('invoice_type'),
            total=total
        )

        for item in carrito:
            OrderItem.objects.create(
                order=order,
                product_id=item['product'],
                quantity=item['quantity'],
                price=item['price']
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

