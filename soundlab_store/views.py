from django.shortcuts import render

# Create your views here.
# soundlab_store/views.py

from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.http import HttpResponse
from soundlab_store.views import home

def home(request):
    return HttpResponse("¡Hola! Esta es la página de inicio.")


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
