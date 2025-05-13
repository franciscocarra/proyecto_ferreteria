from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def producto(request):
    return render(request, 'core/productos.html')