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
from django.contrib import messages
from django.contrib.auth.decorators import login_required

API_URL = "http://127.0.0.1:8001/productos"

def home(request):
    return render(request, 'core/home.html')

def producto(request):
    try:
        # Hacemos una petición a la API para obtener todos los productos
        response = requests.get('http://127.0.0.1:8001/productos/')
        response.raise_for_status()  # Lanza un error si la petición falla
        productos = response.json()
    except requests.exceptions.RequestException:
        # Si la API no responde o hay un error, enviamos una lista vacía
        productos = []
    
    # Enviamos la lista de productos al template
    return render(request, 'core/productos.html', {'lista_productos': productos})

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
            if user.is_superuser:
                return redirect('administración')

            # Buscar el usuario personalizado para obtener el tipo
            tipo = None
            try:
                usuario_personalizado = Usuario.objects.get(correo=user.email)
                tipo = usuario_personalizado.tipo.descripcion
            except Usuario.DoesNotExist:
                tipo = None

            if tipo == 'bodeguero':
                return redirect('bodeguero')
            elif tipo == 'vendedor':
                return redirect('home')
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
    cart = request.session.get('cart', {})
    cart_items = []
    total_cart_price = 0

    for sku, item_data in cart.items():
        # --- INICIO DE LA CORRECCIÓN ---
        # 1. Define la variable 'item_total' al principio del bucle.
        item_total = item_data['price'] * item_data['quantity']

        # 2. Ahora puedes usar 'item_total' para agregarlo a la lista de items.
        cart_items.append({
            'sku': sku,
            'name': item_data['name'],
            'price': item_data['price'],
            'quantity': item_data['quantity'],
            'image': item_data.get('image', 'core/img/placeholder.png'),
            'stock': item_data.get('stock', 0),
            'total': item_total  # Se usa aquí
        })
        
        # 3. Y también puedes usar 'item_total' para sumarlo al total general.
        total_cart_price += item_total # El error estaba aquí
        # --- FIN DE LA CORRECCIÓN ---
    
    context = {
        'cart_items': cart_items,
        'total_cart_price': total_cart_price
    }
    return render(request, 'core/carrito.html', context)

@login_required
def add_to_cart(request, sku):
    try:
        response = requests.get(f'http://127.0.0.1:8001/productos/{sku}')
        response.raise_for_status()
        producto_data = response.json()
    except requests.exceptions.RequestException:
        messages.error(request, 'No se pudo obtener la información del producto.')
        return redirect('productos')

    if producto_data.get('stock', 0) > 0:
        cart = request.session.get('cart', {})
        sku_str = str(sku)

        if sku_str in cart:
            # ---> INICIO CAMBIO 1 <---
            # Solo aumenta la cantidad si es menor que el stock
            if cart[sku_str]['quantity'] < cart[sku_str]['stock']:
                cart[sku_str]['quantity'] += 1
            else:
                messages.warning(request, f"No puedes agregar más unidades de este producto. Stock máximo: {cart[sku_str]['stock']}")
            # ---> FIN CAMBIO 1 <---
        else:
            cart[sku_str] = {
                'name': producto_data['nombre_producto'],
                'price': float(producto_data['precio']),
                'quantity': 1,
                'image': 'core/img/productos/producto_1.webp',
                'stock': producto_data['stock'] # <-- AÑADE ESTA LÍNEA
            }
        
        request.session['cart'] = cart
        return redirect('carrito')
    else:
        messages.error(request, 'Este producto no tiene stock disponible.')
        return redirect('productos')

def remove_from_cart(request, sku):
    cart = request.session.get('cart', {})
    sku_str = str(sku)
    if sku_str in cart:
        del cart[sku_str]
        request.session['cart'] = cart
    return redirect('carrito')

def update_cart(request):
    if request.method == 'POST':
        sku = request.POST.get('sku')
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        
        if sku in cart:
            stock_disponible = cart[sku].get('stock', 0)

            # ---> INICIO CAMBIO 2 <---
            # Limita la cantidad al stock disponible
            if quantity > stock_disponible:
                quantity = stock_disponible
                messages.warning(request, f"La cantidad se ha ajustado al stock máximo disponible: {stock_disponible}")

            if quantity > 0:
                cart[sku]['quantity'] = quantity
            else:
                del cart[sku]
            # ---> FIN CAMBIO 2 <---
        
        request.session['cart'] = cart
    return redirect('carrito')

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('carrito')

def users(request):
    return render(request, 'core/A_dmin/users.html')

def administración(request):
    return render(request, 'core/A_dmin/administración.html')

def bodeguero(request):
    return render(request, 'core/bodeguero/bode.html')

def inventario(request):
    try:
        # 1. Obtenemos los productos actuales de la API
        response = requests.get('http://127.0.0.1:8001/productos/')
        response.raise_for_status()
        productos_api = response.json()
        
        # Obtenemos una lista de los SKUs que vienen de la API
        skus_en_api = {prod_api['sku'] for prod_api in productos_api}

        # --- INICIO DE LA NUEVA LÓGICA DE ELIMINACIÓN ---
        
        # 2. Obtenemos los SKUs que tenemos en nuestra base de datos local
        skus_en_db = set(Producto.objects.values_list('sku', flat=True))
        
        # 3. Identificamos los SKUs que hay que borrar
        skus_para_borrar = skus_en_db - skus_en_api
        
        if skus_para_borrar:
            Producto.objects.filter(sku__in=skus_para_borrar).delete()
            print(f"Productos eliminados: {skus_para_borrar}")
            
        # --- FIN DE LA NUEVA LÓGICA DE ELIMINACIÓN ---

        # 4. Sincronizamos (actualizamos o creamos) el resto de los productos
        for prod_api in productos_api:
            Producto.objects.update_or_create(
                sku=prod_api['sku'],
                defaults={
                    'nombre_producto': prod_api['nombre_producto'],
                    'marca': prod_api['marca'],
                    'descripcion': prod_api.get('descripcion', ''),
                    'precio': prod_api['precio'],
                    'stock': prod_api['stock'],
                    'estado_producto': prod_api.get('estado_producto', 'Activo')
                }
            )

    except requests.exceptions.RequestException:
        print("Error: No se pudo conectar con la API de productos.")
    
    # El resto de la vista sigue igual, obteniendo los datos de la BD local
    query = request.GET.get('q')
    lista_productos = Producto.objects.all()

    if query:
        lista_productos = lista_productos.filter(nombre_producto__icontains=query)
    
    return render(request, 'core/bodeguero/inventario.html', {'lista_productos': lista_productos})

def ver_stock_sucursales(request, sku):
    try:
        producto = Producto.objects.get(sku=sku)
        stock_en_sucursales = StockPorSucursal.objects.filter(producto=producto)
    except Producto.DoesNotExist:
        producto = {'nombre_producto': 'Producto no encontrado'}
        stock_en_sucursales = []

    context = {
        'producto': producto,
        'stock_en_sucursales': stock_en_sucursales
    }
    
    return render(request, 'core/bodeguero/ver_stock_sucursales.html', context)

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

def eliminar_usuario(request, id):
    # Obtener el objeto usuario con el id proporcionado
    usuario = get_object_or_404(Usuario, id=id)

    # Eliminar el usuario
    usuario.delete()

    # Redirigir a la lista de usuarios
    return redirect('Clientes')



