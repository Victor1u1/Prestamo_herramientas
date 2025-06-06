from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['first_name','last_name','username', 'email', 'direccion', 'telefono', 'password1', 'password2']
