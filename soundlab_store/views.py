from django.shortcuts import render

# Create your views here.
# soundlab_store/views.py

from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from django.http import HttpResponse


def home(request):
    return HttpResponse("Bienvenido a SoundLab Store API")



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
