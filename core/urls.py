from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos', views.producto, name='productos'),
    path('contacto', views.contacto, name='contacto'),
    path('iniciar_session', views.iniciar_session, name='iniciar_session'),
    path('registro', views.registro, name='registro'),
    path('pintura', views.pintura, name='pintura'),
]

