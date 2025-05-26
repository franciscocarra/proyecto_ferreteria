from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def producto(request):
    return render(request, 'core/productos.html')

def producto2(request):
    return render(request, 'core/productos_2.html')

def contacto(request):
    return render(request, 'core/contacto.html')

def iniciar_session(request):
    return render(request, 'core/iniciar_session.html')

def registro(request):
    return render(request, 'core/registro.html')

def pintura(request):
    return render(request, 'core/pintura.html')

def error_producto(request):
    return render(request, 'core/error_producto.html')