import bcrypt
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Persona

class PersonaAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        """
        Este método se ejecuta cuando un usuario intenta iniciar sesión.
        """
        try:
            # 1. Busca a la persona en tu tabla `persona` usando el correo (que llega como 'username')
            persona = Persona.objects.get(correo=username)

            # 2. Compara la contraseña que ingresó el usuario con la que está en Oracle
            # Usamos bcrypt, igual que en tu API de Node.js
            if bcrypt.checkpw(password.encode('utf-8'), persona.contraseña.encode('utf-8')):
                # 3. Si la contraseña es correcta, busca o crea un usuario en la tabla `auth_user` de Django.
                #    Esto es necesario para que las sesiones de Django funcionen.
                user, created = User.objects.get_or_create(
                    username=persona.correo,
                    defaults={
                        'email': persona.correo,
                        'first_name': persona.nombre,
                        'last_name': persona.appaterno
                    }
                )
                return user # Devuelve el usuario de Django para iniciar la sesión
            
        except Persona.DoesNotExist:
            return None # Si no se encuentra la persona, no se autentica

    def get_user(self, user_id):
        """
        Este método es usado por Django para obtener el usuario durante la sesión.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None