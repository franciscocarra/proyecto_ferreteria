from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout


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
            return redirect('home')  # O donde quieras que vaya
        else:
            form.add_error(None, "Usuario o contraseña incorrectos.")
    return render(request, 'core/iniciar_session.html', {'form': form})

def registro(request):
    aux = {'form': CustomUserCreationForm()}

    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()

            # Crear el grupo 'cliente' si no existe
            group, created = Group.objects.get_or_create(name='cliente')
            user.groups.add(group)

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


