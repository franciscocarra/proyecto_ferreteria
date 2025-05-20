from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def producto(request):
    return render(request, 'core/productos.html')

def contacto(request):
    return render(request, 'core/contacto.html')

def iniciar_session(request):
    return render(request, 'core/iniciar_session.html')

def registro(request):
    return render(request, 'core/registro.html')

def pintura(request):
    return render(request, 'core/pintura.html')