from django.contrib import admin
from django.contrib.auth.models import User
from .models import Usuario, Genero, TipoUsuario, Producto, Sucursal, StockPorSucursal


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'apellido_completo', 'tipo', 'habilitado']
    list_filter = ['tipo', 'habilitado']

    def apellido_completo(self, obj):
        return f"{obj.appaterno} {obj.apmaterno}"
    apellido_completo.short_description = 'Apellido'

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

admin.site.register(Genero)
admin.site.register(TipoUsuario)