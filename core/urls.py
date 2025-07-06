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
    path('carrito/', views.carrito, name='carrito'),
    path('add/<int:sku>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:sku>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('users', views.users, name='users'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('administración', views.administración, name='administración'),
    path('bodeguero', views.bodeguero, name='bodeguero'),
    path('inventario', views.inventario, name='inventario'),
    path('producto/<int:sku>/sucursales/', views.ver_stock_sucursales, name='ver_stock_sucursales'),
    path('productos/registrar/', views.registrar_producto, name='registrar_producto'),
    path('producto/eliminar/<int:sku>/', views.eliminar_producto, name='producto_eliminar'),
    path('productos/editar/<int:sku>/', views.editar_producto, name='producto_editar'),
    path('empleados/', views.listar_empleados, name='lista_empleados'),
    path('registro_empleado/', views.registro_empleado, name='registro_empleado'),
    path('Clientes/', views.Clientes, name='Clientes'),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar_producto_api/<str:sku>/', views.editar_producto_api, name='editar_producto_api'),
    

]

