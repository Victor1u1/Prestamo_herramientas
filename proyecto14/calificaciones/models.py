from django.db import models
from usuarios.models import Usuario
from prestamos.models import Prestamo

class Calificacion(models.Model):
    PUNTAJE_CHOICES = (
        (1, '1 - Muy malo'),
        (2, '2 - Malo'),
        (3, '3 - Regular'),
        (4, '4 - Bueno'),
        (5, '5 - Excelente'),
    )
    
    prestamo = models.ForeignKey(Prestamo, on_delete=models.CASCADE, related_name='calificaciones')
    califica_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='calificaciones_realizadas')
    calificado_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='calificaciones_recibidas')
    puntaje = models.IntegerField(choices=PUNTAJE_CHOICES)
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Calificación de {self.califica_usuario.username} a {self.calificado_usuario.username}"