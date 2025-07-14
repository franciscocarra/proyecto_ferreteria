from django.db import models
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
import random

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

    

    

