from django.db import models
from datetime import date

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

class Usuario(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=40)
    appaterno = models.CharField(max_length=60)
    apmaterno = models.CharField(max_length=60)
    correo = models.EmailField(max_length=100)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    fec_nac = models.DateField()  # fecha de nacimiento
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=100)
    habilitado = models.BooleanField(default=True)
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    def edad(self):
        hoy = date.today()
        años = hoy.year - self.fec_nac.year
        if (hoy.month, hoy.day) < (self.fec_nac.month, self.fec_nac.day):
            años -= 1
        return años

    def __str__(self):
        return f"{self.nombre} {self.appaterno} {self.apmaterno}"
    
class Producto(models.Model):
    sku = models.AutoField(primary_key=True)  # ID autoincremental
    nombre_producto = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    estado_producto = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nombre_producto} ({self.marca})"
