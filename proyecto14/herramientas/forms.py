from django import forms
from .models import Herramienta

class HerramientaForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ('nombre', 'descripcion', 'estado', 'disponibilidad', 'imagen')
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
