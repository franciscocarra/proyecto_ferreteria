from django.contrib import admin
from django.contrib.auth.models import User
# La corrección está aquí: Eliminamos 'Usuario' de la importación.
from .models import Genero, TipoUsuario, Producto, Sucursal, StockPorSucursal

# El registro de Usuario/Persona se mantiene comentado, ya que no es necesario
# para que la autenticación funcione.

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('sku', 'nombre_producto', 'marca', 'stock')
    # No hacemos editable el stock aquí porque viene de la API
    readonly_fields = ('sku', 'nombre_producto', 'marca', 'stock', 'precio', 'descripcion', 'estado_producto')

    def has_add_permission(self, request):
        # Deshabilita el botón de "Añadir producto" en el admin,
        # ya que los productos vienen de la API.
        return False

# Personaliza cómo se ve la lista de Sucursales
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion')

# Registra los modelos en el panel de administrador
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(StockPorSucursal)

# Se descomentan estas líneas para que puedas gestionar Género y TipoUsuario desde el admin
admin.site.register(Genero)
admin.site.register(TipoUsuario)