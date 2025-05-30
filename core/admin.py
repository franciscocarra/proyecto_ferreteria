from django.contrib import admin
from django.contrib.auth.models import User
from .models import Usuario, Genero, TipoUsuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['rut', 'nombre', 'apellido', 'tipo', 'habilitado']
    list_filter = ['tipo', 'habilitado']

admin.site.register(Genero)
admin.site.register(TipoUsuario)
