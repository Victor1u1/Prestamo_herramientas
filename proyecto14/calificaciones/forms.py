# forms.py
from django import forms
from .models import Calificacion

class CalificacionForm(forms.ModelForm):
    class Meta:
        model = Calificacion
        fields = ['prestamo', 'califica_usuario', 'calificado_usuario', 'puntaje', 'comentario']
