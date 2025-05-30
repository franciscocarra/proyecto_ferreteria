from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('', views.home, name='home'),
    path('productos', views.producto, name='productos'),
    path('productos_2', views.producto2, name='productos_2'),
    path('contacto', views.contacto, name='contacto'),
    path('iniciar_session/', views.iniciar_session, name='iniciar_session'),
    path('registro/', views.registro, name='registro'),
    path('pintura', views.pintura, name='pintura'),
    path('error_producto', views.error_producto, name='error_producto'),
    path('herramientas', views.herramientas, name='herramientas'),
    path('materiales', views.materiales, name='materiales'),
    path('carrito', views.carrito, name='carrito'),
    path('Usuarios/', views.Usuarios, name='Usuarios'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('administración', views.administración, name='administración'),
]

