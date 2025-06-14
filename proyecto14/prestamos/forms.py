from django import forms
from .models import Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ('fecha_inicio', 'fecha_fin')
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_inicio > fecha_fin:
                raise forms.ValidationError('La fecha de fin debe ser posterior a la fecha de inicio.')
        
        return cleaned_data

class ActualizarEstadoPrestamoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Personalizar opciones de estado según el usuario
        if self.user and self.instance:
            if self.user == self.instance.herramienta.propietario:
                # El propietario puede cambiar entre todos los estados
                self.fields['estado'].choices = [
                    ('pendiente', 'Pendiente'),
                    ('aceptado', 'Aceptado'),
                    ('rechazado', 'Rechazado'),
                    ('en_curso', 'En curso'),
                    ('finalizado', 'Finalizado'),
                    ('cancelado', 'Cancelado'),
                ]
            elif self.user == self.instance.prestatario:
                # El prestatario solo puede cancelar o finalizar
                current_estado = self.instance.estado
                if current_estado == 'pendiente':
                    self.fields['estado'].choices = [
                        ('pendiente', 'Pendiente'),
                        ('cancelado', 'Cancelado'),
                    ]
                elif current_estado in ['aceptado', 'en_curso']:
                    self.fields['estado'].choices = [
                        (current_estado, self.instance.get_estado_display()),
                        ('finalizado', 'Finalizado'),
                        ('cancelado', 'Cancelado'),
                    ]
                else:
                    self.fields['estado'].choices = [
                        (current_estado, self.instance.get_estado_display()),
                    ]
    
    class Meta:
        model = Prestamo
        fields = ('estado',)
