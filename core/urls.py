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
    path('olvidar_contrasena/', views.olvidar_contrasena, name='olvidar_contrasena'),
    path('pintura', views.pintura, name='pintura'),
    path('error_producto', views.error_producto, name='error_producto'),
    path('herramientas', views.herramientas, name='herramientas'),
    path('materiales', views.materiales, name='materiales'),
    path('carrito/', views.carrito, name='carrito'),
    path('add/<int:sku>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:sku>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('iniciar-pago/', views.iniciar_pago, name='iniciar_pago'),
    path('confirmar-pago/', views.confirmar_pago, name='confirmar_pago'),
    path('users', views.users, name='users'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('administracion/', views.administracion, name='administracion'),
    path('bodeguero', views.bodeguero, name='bodeguero'),
    path('inventario', views.inventario, name='inventario'),
    path('producto/<int:sku>/sucursales/', views.ver_stock_sucursales, name='ver_stock_sucursales'),
    path('productos/registrar/', views.registrar_producto, name='registrar_producto'),
    path('producto/eliminar/<int:sku>/', views.eliminar_producto, name='producto_eliminar'),
    path('productos/editar/<int:sku>/', views.editar_producto, name='producto_editar'),
    path('empleados/', views.listar_empleados, name='lista_empleados'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('agregar-usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar_producto_api/<str:sku>/', views.editar_producto_api, name='editar_producto_api'),
    path('contador/', views.contador, name='contador'),
    path('contador/ventas/', views.ventas, name='ventas'),
    path('contador/reportes/ventas/', views.reporte_ventas, name='reporte_ventas'),
    path('contador/reportes/ventas/pdf/', views.descargar_reporte_pdf, name='descargar_reporte_pdf'),
    path('contador/reportes/ventas/excel/', views.descargar_reporte_excel, name='descargar_reporte_excel'),

    
    

]

