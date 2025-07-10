from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Producto
from django.forms.widgets import DateInput
import random

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    fec_nac = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/AAAA', 'type': 'text'}),
        label='Fecha de nacimiento'
    )

    class Meta:
        model = Usuario
        fields = [
            'rut', 'nombre', 'appaterno', 'apmaterno', 'correo', 
            'genero', 'fec_nac', 'telefono', 'direccion'
        ]

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        # Crear el usuario base de Django
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['correo'],
            first_name=self.cleaned_data['nombre'],
            last_name=f"{self.cleaned_data['appaterno']} {self.cleaned_data['apmaterno']}"
        )
        
        # Obtener o crear tipo cliente
        cliente_tipo, _ = TipoUsuario.objects.get_or_create(descripcion='cliente')

        usuario = super().save(commit=False)
        usuario.tipo = cliente_tipo
        usuario.habilitado = True
        usuario.correo = self.cleaned_data['correo']
        usuario.save()

        # Asignar grupo 'cliente' al usuario de Django
        from django.contrib.auth.models import Group
        group, created = Group.objects.get_or_create(name='cliente')
        user.groups.add(group)

        if commit:
            usuario.save()

        return usuario
    
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


class AdminUserCreationForm(UserCreationForm):
    fec_nac = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=DateInput(attrs={'type': 'text', 'placeholder': 'DD/MM/AAAA'}),
        label='Fecha de nacimiento'
    )

    class Meta:
        model = Usuario
        fields = [
            'rut',          # campo para login, no username
            'nombre',
            'appaterno',
            'apmaterno',
            'correo',
            'genero',
            'fec_nac',
            'telefono',
            'direccion',
            'password1',
            'password2',
        ]

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

class EmpleadoUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    fec_nac = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/AAAA', 'type': 'text'}),
        label='Fecha de nacimiento'
    )

    class Meta:
        model = Usuario
        fields = [
            'rut', 'nombre', 'appaterno', 'apmaterno', 'correo',
            'genero', 'fec_nac', 'telefono', 'direccion'
        ]

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['correo'],
            first_name=self.cleaned_data['nombre'],
            last_name=f"{self.cleaned_data['appaterno']} {self.cleaned_data['apmaterno']}"
        )

        empleado_tipo, _ = TipoUsuario.objects.get_or_create(descripcion=random.choice(['bodeguero', 'vendedor']))

        usuario = super().save(commit=False)
        usuario.tipo = empleado_tipo
        usuario.habilitado = True
        usuario.correo = self.cleaned_data['correo']
        usuario.save()

        from django.contrib.auth.models import Group
        from django import forms
        group, _ = Group.objects.get_or_create(name='empleado')
        user.groups.add(group)

        if commit:
            usuario.save()

        return usuario

    # Agrega un formulario simple para el home con enlaces a login y registro

    class HomeForm(forms.Form):
        pass  # Este formulario puede estar vacío, solo para renderizar el home

    # Puedes usar estos helpers en tu vista/template:
    # En tu template home.html, agrega:
    # <a href="{% url 'login' %}">Iniciar sesión</a>
    # <a href="{% url 'registro' %}">Registrarse</a>