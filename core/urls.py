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
    path('users', views.users, name='users'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('administración', views.administración, name='administración'),
    path('bodeguero', views.bodeguero, name='bodeguero'),
    path('inventario', views.inventario, name='inventario'),
    path('productos/registrar/', views.registrar_producto, name='registrar_producto'),
    path('producto/eliminar/<int:sku>/', views.eliminar_producto, name='producto_eliminar'),
    path('productos/editar/<int:sku>/', views.editar_producto, name='producto_editar'),
    path('empleados/', views.listar_empleados, name='lista_empleados'),
    path('registro_empleado/', views.registro_empleado, name='registro_empleado'),
    path('Clientes/', views.Clientes, name='Clientes'),
<<<<<<< HEAD
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
=======
>>>>>>> 49c5846f5e31eb06b804fe7bd6da4cc78a916c63
    path('editar_producto_api/<str:sku>/', views.editar_producto_api, name='editar_producto_api'),
    

]

