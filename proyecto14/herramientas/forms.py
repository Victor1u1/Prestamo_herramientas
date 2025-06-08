from django import forms
from .models import Herramienta
from django.core.validators import FileExtensionValidator

class RegistroHerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['imagen', 'nombre', 'descripcion', 'estado', 'disponibilidad']
        
    imagen = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',
            'accept': 'image/*'
        }),
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])
        ]
    )
    nombre = forms.CharField(
        max_length=100,
        label="Herramienta",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre de la herramienta'
        })
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describa la herramienta...'
        }),
        label="Descripción"
    )
    estado = forms.ChoiceField(
        choices=Herramienta.ESTADO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )