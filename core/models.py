from django.db import models
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
import random
from django.conf import settings

class ExampleModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Genero(models.Model):
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return self.descripcion

class TipoUsuario(models.Model):
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return self.descripcion

class Persona(models.Model):
    # Los nombres de los campos deben coincidir EXACTAMENTE con las columnas de tu tabla en Oracle
    rut = models.CharField(max_length=12, primary_key=True) # El RUT es la clave primaria
    nombre = models.CharField(max_length=40)
    appaterno = models.CharField(max_length=60)
    apmaterno = models.CharField(max_length=60)
    correo = models.EmailField(max_length=100)
    contraseña = models.CharField(max_length=60) # Campo para la contraseña hasheada por Node.js
    genero = models.CharField(max_length=1)
    fec_nac = models.DateField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    tipo_persona = models.CharField(max_length=20)

    class Meta:
        managed = False      # ¡MUY IMPORTANTE! Le dice a Django que no gestione esta tabla.
        db_table = 'persona' # El nombre exacto de tu tabla en Oracle.
    
class Producto(models.Model):
    sku = models.AutoField(primary_key=True)  # ID autoincremental
    nombre_producto = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    estado_producto = models.CharField(max_length=10)
    imagen_url = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_producto} ({self.marca})"
    
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class StockPorSucursal(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    class Meta:
        unique_together = ('producto', 'sucursal')

    def __str__(self):
        return f"{self.producto.nombre_producto} en {self.sucursal.nombre}: {self.cantidad}"


# --- NUEVA LÓGICA DE SEÑAL QUE SE AGREGA ---
@receiver(post_save, sender=Producto)
def distribuir_stock(sender, instance, **kwargs):
    sucursales = Sucursal.objects.all()
    stock_total = instance.stock
    num_sucursales = sucursales.count()

    if num_sucursales > 0:
        try:
            with transaction.atomic():
                StockPorSucursal.objects.filter(producto=instance).delete()

                if stock_total > 0:
                    distribucion = [0] * num_sucursales
                    for _ in range(stock_total):
                        indice_al_azar = random.randint(0, num_sucursales - 1)
                        distribucion[indice_al_azar] += 1
                    
                    nuevos_stocks = []
                    for i, sucursal in enumerate(sucursales):
                        if distribucion[i] > 0:
                            nuevos_stocks.append(
                                StockPorSucursal(
                                    producto=instance,
                                    sucursal=sucursal,
                                    cantidad=distribucion[i]
                                )
                            )
                    StockPorSucursal.objects.bulk_create(nuevos_stocks)
        except Exception as e:
            print(f"Error al distribuir el stock: {e}")

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    # Vinculamos la venta al usuario autenticado de Django
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    total = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True) # Se guarda la fecha y hora automáticamente
    
    # Datos que sacamos de la respuesta de Transbank
    orden_compra = models.CharField(max_length=100, unique=True, null=True)
    codigo_autorizacion = models.CharField(max_length=100, null=True)
    tipo_tarjeta = models.CharField(max_length=50, null=True)
    ultimos_digitos_tarjeta = models.CharField(max_length=4, null=True)

    def __str__(self):
        # Aseguramos que el usuario y su persona existan antes de acceder a sus atributos
        cliente_nombre = "Usuario Desconocido"
        if self.usuario and hasattr(self.usuario, 'persona'):
            cliente_nombre = f"{self.usuario.persona.nombre} {self.usuario.persona.appaterno}"
        elif self.usuario:
            cliente_nombre = self.usuario.username
            
        return f"Venta #{self.id} - Cliente: {cliente_nombre} - Total: ${self.total}"

# --- MODELO PARA CADA LÍNEA DE PRODUCTO DE LA VENTA ---
class DetalleVenta(models.Model):
    # Vinculamos el detalle a una Venta específica
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    # Vinculamos el detalle a un Producto específico
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField() # Guardamos el precio al momento de la compra

    def __str__(self):
        # Ya incluía el nombre del producto, lo hacemos más explícito
        producto_nombre = self.producto.nombre_producto if self.producto else "Producto Desconocido"
        return f"Detalle de Venta #{self.venta.id} - Producto: {producto_nombre} - Cantidad: {self.cantidad}"

    

    

