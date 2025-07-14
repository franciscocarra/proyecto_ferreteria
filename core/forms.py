from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Producto
from django.forms.widgets import DateInput
import random


from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'marca', 'descripcion', 'precio', 'stock', 'estado_producto', 'imagen_url']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control'}),
        }