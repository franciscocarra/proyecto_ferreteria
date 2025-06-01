from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
import random
from django.utils.crypto import get_random_string
from .models import Producto
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from .models import Usuario, TipoUsuario

def home(request):
    return render(request, 'core/home.html')

def producto(request):
    return render(request, 'core/productos.html')

def producto2(request):
    return render(request, 'core/productos_2.html')

def contacto(request):
    return render(request, 'core/contacto.html')

def iniciar_session(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Verifica si el usuario es admin (superuser o tiene permisos específicos)
            if user.is_superuser:
                return redirect('administración')  # Asegúrate de que esta URL exista
            else:
                return redirect('home')
        else:
            form.add_error(None, "Usuario o contraseña incorrectos.")
    return render(request, 'core/iniciar_session.html', {'form': form})



def registro(request):
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('iniciar_session')
    else:
        formulario = CustomUserCreationForm()

    return render(request, 'core/registro.html', {'form': formulario})

def logout_view(request):
    logout(request)
    return redirect('home')

def pintura(request):
    return render(request, 'core/pintura.html')

def error_producto(request):
    return render(request, 'core/error_producto.html')

def herramientas(request):
    return render(request, 'core/herramientas.html')

def materiales(request):
    return render(request, 'core/materiales.html')

def carrito(request):
    return render(request, 'core/carrito.html')

def users(request):
    return render(request, 'core/A_dmin/users.html')

def administración(request):
    return render(request, 'core/A_dmin/administración.html')

def bodeguero(request):
    return render(request, 'core/bodeguero/bode.html')

def inventario(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(
            Q(nombre_producto__icontains=query) |
            Q(marca__icontains=query) |
            Q(descripcion__icontains=query)
        )
    else:
        productos = Producto.objects.all()
    
    return render(request, 'core/bodeguero/inventario.html', {'lista_productos': productos})

def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')  # Cambia por la url de tu lista
    else:
        form = ProductoForm()

    return render(request, 'core/bodeguero/crear_p.html', {'form': form})

def eliminar_producto(request, sku):
    producto = get_object_or_404(Producto, sku=sku)
    producto.delete()
    return redirect('inventario')

def editar_producto(request, sku):
    producto = get_object_or_404(Producto, sku=sku)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'core/bodeguero/editar_p.html', {'form': form, 'producto': producto})


def listar_empleados(request):
    tipos_empleado = TipoUsuario.objects.filter(descripcion__in=['vendedor', 'bodeguero'])
    empleados = Usuario.objects.filter(tipo__in=tipos_empleado)
    return render(request, 'core/A_dmin/empleados/lista_e.html', {'lista_empleados': empleados})

def Clientes(request):
    Usuarios = Usuario.objects.all()
    aux = {
        'lista' : Usuarios
    }

    return render(request, 'core/A_dmin/Cliente/lista_c.html', aux)
