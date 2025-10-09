from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')  # columnas que se ven
    search_fields = ('name',)                     # barra de búsqueda
    list_filter = ('category',)                   # filtros laterales


# Personalización del encabezado del panel
admin.site.site_header = "SoundLab Admin"
admin.site.site_title = "SoundLab Panel"
admin.site.index_title = "Administración de la tienda"
