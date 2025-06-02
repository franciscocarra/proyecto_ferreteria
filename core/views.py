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
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

API_URL = "http://127.0.0.1:8001/productos"

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
    try:
        response = requests.get('http://127.0.0.1:8001/productos/')
        response.raise_for_status()
        productos = response.json()

        # Filtro local con "q", si existe
        if query:
            productos = [p for p in productos if query.lower() in p['nombre_producto'].lower()]
    except requests.exceptions.RequestException:
        productos = []
    
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

def editar_producto_api(request, sku):
    """
    1) En GET: obtiene los datos del producto desde la API y los muestra en editar_p.html.
    2) En POST: toma los campos del formulario, arma los query params (incluyendo sku)
       y hace PUT a http://127.0.0.1:8001/productos?sku=...&nombre_producto=... etc.
    """

    # URL base de tu API (sin el SKU en la ruta)
    api_base = 'http://127.0.0.1:8001/productos'

    if request.method == 'POST':
        # Recolectamos todos los campos del formulario
        nombre = request.POST.get('nombre_producto')
        marca = request.POST.get('marca')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        estado = request.POST.get('estado_producto')

        # Aquí armamos el dict que irá en params (query string)
        data = {
            'sku': sku,
            'nombre_producto': nombre,
            'marca': marca,
            'descripcion': descripcion,
            'precio': precio,
            'stock': stock,
            'estado_producto': estado,
        }

        # Hacemos PUT enviando todo como query params
        try:
            respuesta = requests.put(f"{api_base}/{sku}", params=data)
        except requests.RequestException as e:
            return HttpResponse(f"Error de conexión con la API: {e}")

        if respuesta.status_code in (200, 204):
            # Actualización exitosa, volvemos al inventario
            return redirect('inventario')
        else:
            # API devolvió error, mostramos el texto que venga
            return render(request, 'core/bodeguero/editar_p.html', {
                'producto': data,  # para rellenar el formulario con lo que intentó guardarse
                'error': f"Error al actualizar desde la API: {respuesta.text}"
            })

    else:  # GET
        # Obtiene el producto desde la API para llenar el formulario
        try:
            respuesta = requests.get(f"{api_base}/{sku}")
        except requests.RequestException:
            return HttpResponse("Error de conexión al obtener datos del producto.")

        if respuesta.status_code == 200:
            producto = respuesta.json()
            return render(request, 'core/bodeguero/editar_p.html', {
                'producto': producto
            })
        else:
            return render(request, 'core/bodeguero/editar_p.html', {
                'error': "Producto no encontrado en la API."
            })


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


def registro_empleado(request):
    if request.method == 'POST':
        formulario = EmpleadoUserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('Clientes')  # Redirige donde tú quieras
    else:
        formulario = EmpleadoUserCreationForm()

    return render(request, 'core/A_dmin/empleados/crear_e.html', {'form': formulario})

def Clientes(request):
    Usuarios = Usuario.objects.all()
    aux = {
        'lista' : Usuarios
    }

    return render(request, 'core/A_dmin/Cliente/lista_c.html', aux)

<<<<<<< HEAD
def eliminar_usuario(request, id):
    # Obtener el objeto usuario con el id proporcionado
    usuario = get_object_or_404(Usuario, id=id)

    # Eliminar el usuario
    usuario.delete()

    # Redirigir a la lista de usuarios
    return redirect('Clientes')

=======
>>>>>>> 49c5846f5e31eb06b804fe7bd6da4cc78a916c63

