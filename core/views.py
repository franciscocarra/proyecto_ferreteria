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

def calcular_dv(rut_num):
    reversed_digits = map(int, reversed(str(rut_num)))
    factors = [2, 3, 4, 5, 6, 7]
    s = sum(d * factors[i % 6] for i, d in enumerate(reversed_digits))
    remainder = 11 - (s % 11)
    if remainder == 11:
        return '0'
    elif remainder == 10:
        return 'K'
    else:
        return str(remainder)

# Lista de calles y comunas para generar direcciones más variadas
calles = ['Av. Los Leones', 'Calle San Martín', 'Av. Providencia', 'Calle La Florida', 'Calle Pajaritos', 'Av. O’Higgins', 'Calle Bilbao']
comunas = ['Santiago', 'Las Condes', 'La Florida', 'Providencia', 'Maipú', 'Ñuñoa', 'Puente Alto']

def registro(request):
    aux = {'form': CustomUserCreationForm()}

    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()

            # Asignar el grupo "cliente"
            group, created = Group.objects.get_or_create(name='cliente')
            user.groups.add(group)

            # Seleccionar un género aleatorio
            generos = list(Genero.objects.all())
            genero_aleatorio = random.choice(generos) if generos else None

            # Asignar tipo "cliente"
            cliente_tipo, _ = TipoUsuario.objects.get_or_create(descripcion='cliente')

            # Generar RUT aleatorio estilo "21.433.434-6"
            rut_prefix = random.choice(['20', '21'])
            rut_middle = f"{random.randint(100, 999)}{random.randint(100, 999)}"
            rut_num = int(f"{rut_prefix}{rut_middle}")
            dv = calcular_dv(rut_num)
            rut_formateado = f"{rut_prefix}.{rut_middle[:3]}.{rut_middle[3:]}-{dv}"

            # Generar dirección aleatoria realista
            calle = random.choice(calles)
            numero = random.randint(1, 9999)
            comuna = random.choice(comunas)
            direccion_random = f"{calle} {numero}, {comuna}"

            # Generar teléfono aleatorio tipo "+56 9 XXXX XXXX"
            telefono_num = f"{random.randint(5000, 5999)} {random.randint(1000, 9999)}"
            telefono_random = f"+56 9 {telefono_num}"

            # Crear perfil Usuario
            Usuario.objects.create(
                rut=rut_formateado,
                nombre=user.first_name,
                apellido=user.last_name,
                edad=random.randint(18, 65),
                direccion=direccion_random,
                telefono=telefono_random,
                genero=genero_aleatorio,
                tipo=cliente_tipo,
                habilitado=True
            )

            return redirect(to="Usuarios")
        else:
            aux['form'] = formulario

    return render(request, 'core/registro.html', aux)

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

def Usuarios(request):
    Usuarios = Usuario.objects.all()
    aux = {
        'lista' : Usuarios
    }

    return render(request, 'core/Usuarios.html', aux)

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

