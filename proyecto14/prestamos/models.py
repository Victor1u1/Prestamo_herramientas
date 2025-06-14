from django.db import models
from usuarios.models import Usuario
from herramientas.models import Herramienta

class Prestamo(models.Model):
    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
        ('en_curso', 'En curso'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )
    
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE, related_name='prestamos')
    prestatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestamos_solicitados')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    
    def __str__(self):
        return f"{self.herramienta.nombre} - {self.prestatario.username} ({self.estado})"
    
    def save(self, *args, **kwargs):
        # Si el préstamo es aceptado, actualizar la disponibilidad de la herramienta
        if self.estado == 'aceptado':
            self.herramienta.disponibilidad = 'prestada'
            self.herramienta.save()
        # Si el préstamo es finalizado o cancelado, actualizar la disponibilidad de la herramienta
        elif self.estado in ['finalizado', 'cancelado'] and self.pk:
            self.herramienta.disponibilidad = 'disponible'
            self.herramienta.save()
        
        super().save(*args, **kwargs)
