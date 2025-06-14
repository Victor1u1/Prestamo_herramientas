from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=False)
    nombre = forms.CharField(max_length=100)
    direccion = forms.CharField(max_length=255)
    telefono = forms.CharField(max_length=20)
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre', 'direccion', 'telefono', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nombre']
        user.direccion = self.cleaned_data['direccion']
        user.telefono = self.cleaned_data['telefono']
        if commit:
            user.save()
        return user

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'direccion', 'telefono')
