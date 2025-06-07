from django.contrib import admin
from .models import Cliente, Administrador, Instrumento, Producto, Orden, Pago, Carrito, CarritoItem, OrdenDetalle

admin.site.register(Cliente)
admin.site.register(Administrador)
admin.site.register(Instrumento)
admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(Pago)
admin.site.register(Carrito)
admin.site.register(CarritoItem)
admin.site.register(OrdenDetalle)
