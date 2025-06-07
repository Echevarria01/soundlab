from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Administrador(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Instrumento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50)  # ejemplo: cuerda, viento, percusión
    marca = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.instrumento.nombre} - ${self.precio}"

class Orden(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)  # ejemplo: pendiente, pagada, enviada

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente.nombre}"

class Pago(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    metodo_pago = models.CharField(max_length=50)  # ejemplo: tarjeta, transferencia
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pago de Orden #{self.orden.id}"

class Carrito(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.cliente.nombre}"

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.instrumento.nombre}"

class OrdenDetalle(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.instrumento.nombre} en Orden #{self.orden.id}"
