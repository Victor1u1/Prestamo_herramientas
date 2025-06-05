from django.db import models
from usuarios.models import Usuario
from django.utils import timezone
import os

def imagen_herramienta_path(instance, filename):
    # Obtener la extensión del archivo original
    ext = filename.split('.')[-1]
    # Crear un nombre de archivo único con fecha y hora
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    # Generar el nuevo nombre: nombre-herramienta_fecha_hora.extensión
    filename = f"{instance.nombre.replace(' ', '_').lower()}_{timestamp}.{ext}"
    # Devolver la ruta completa
    return os.path.join('herramientas', filename)

class Herramienta(models.Model):
    ESTADO_CHOICES = (
        ('nuevo', 'Nuevo'),
        ('bueno', 'Buen estado'),
        ('regular', 'Estado regular'),
        ('malo', 'Mal estado'),
    )
    
    DISPONIBILIDAD_CHOICES = (
        ('disponible', 'Disponible'),
        ('prestada', 'Prestada'),
        ('mantenimiento', 'En mantenimiento'),
        ('inactiva', 'Inactiva'),
    )
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='bueno')
    disponibilidad = models.CharField(max_length=15, choices=DISPONIBILIDAD_CHOICES, default='disponible')
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='herramientas')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to=imagen_herramienta_path, null=True, blank=True, help_text="Imagen de la herramienta")
    
    def __str__(self):
        return f"{self.nombre} - {self.propietario.username}"
