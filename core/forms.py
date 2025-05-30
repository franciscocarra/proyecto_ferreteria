from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        # Asignar tipo 'cliente' automáticamente
        cliente_tipo = TipoUsuario.objects.get_or_create(descripcion='cliente')[0]
        user.tipo_usuario = cliente_tipo  # Guardar esta referencia para crear el modelo Usuario luego
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


class AdminUserCreationForm(UserCreationForm):
    rut = forms.CharField(max_length=12)
    nombre = forms.CharField(max_length=40)
    apellido = forms.CharField(max_length=40)
    edad = forms.IntegerField()
    direccion = forms.CharField(max_length=60)
    telefono = forms.CharField(max_length=20)
    genero = forms.ModelChoiceField(queryset=Genero.objects.all())
    tipo = forms.ModelChoiceField(queryset=TipoUsuario.objects.all())

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        # Guardar los campos adicionales en self.cleaned_data para la vista
        user.extra_data = {
            'rut': self.cleaned_data['rut'],
            'nombre': self.cleaned_data['nombre'],
            'apellido': self.cleaned_data['apellido'],
            'edad': self.cleaned_data['edad'],
            'direccion': self.cleaned_data['direccion'],
            'telefono': self.cleaned_data['telefono'],
            'genero': self.cleaned_data['genero'],
            'tipo': self.cleaned_data['tipo']
        }
        return user