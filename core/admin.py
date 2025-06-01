from django.contrib import admin
from django.contrib.auth.models import User
from .models import Usuario, Genero, TipoUsuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'apellido_completo', 'tipo', 'habilitado']
    list_filter = ['tipo', 'habilitado']

    def apellido_completo(self, obj):
        return f"{obj.appaterno} {obj.apmaterno}"
    apellido_completo.short_description = 'Apellido'

admin.site.register(Genero)
admin.site.register(TipoUsuario)