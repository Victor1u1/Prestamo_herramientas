from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Calificacion
from .forms import CalificacionForm
from prestamos.models import Prestamo
from django.db.models import Avg



@login_required
def calificar_prestamo_view(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    # Verificar que el préstamo esté finalizado
    if prestamo.estado != 'finalizado':
        messages.error(request, 'Solo puedes calificar préstamos finalizados.')
        return redirect('mis_prestamos' if prestamo.prestatario == request.user else 'prestamos_recibidos')
    
    # Verificar que el usuario sea parte del préstamo
    if request.user != prestamo.prestatario and request.user != prestamo.herramienta.propietario:
        messages.error(request, 'No tienes permiso para calificar este préstamo.')
        return redirect('dashboard')
    
    # Determinar quién califica a quién
    if request.user == prestamo.prestatario:
        califica_usuario = request.user
        calificado_usuario = prestamo.herramienta.propietario
    else:
        califica_usuario = request.user
        calificado_usuario = prestamo.prestatario
    
    # Verificar si ya existe una calificación
    calificacion_existente = Calificacion.objects.filter(
        prestamo=prestamo,
        califica_usuario=califica_usuario
    ).first()
    
    if calificacion_existente:
        messages.error(request, 'Ya has calificado este préstamo.')
        return redirect('mis_prestamos' if prestamo.prestatario == request.user else 'prestamos_recibidos')
    
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.prestamo = prestamo
            calificacion.califica_usuario = califica_usuario
            calificacion.calificado_usuario = calificado_usuario
            calificacion.save()
            messages.success(request, 'Calificación enviada correctamente.')
            return redirect('mis_prestamos' if prestamo.prestatario == request.user else 'prestamos_recibidos')
    else:
        form = CalificacionForm()
    
    return render(request, 'calificaciones/calificar_prestamo.html', {
        'form': form,
        'prestamo': prestamo,
        'calificado_usuario': calificado_usuario
    })
    
@login_required
def mis_calificaciones_view(request):
    calificaciones_recibidas = Calificacion.objects.filter(calificado_usuario=request.user).order_by('-fecha')
    return render(request, 'calificaciones/mis_calificaciones.html', {'calificaciones': calificaciones_recibidas})

@login_required
def calificaciones_usuario_view(request, usuario_id):
    from usuarios.models import Usuario
    usuario = get_object_or_404(Usuario, id=usuario_id)
    calificaciones = Calificacion.objects.filter(calificado_usuario=usuario).order_by('-fecha')
    
    # Calcular promedio de calificaciones
    promedio = calificaciones.aggregate(promedio=Avg('puntaje'))['promedio'] or 0
    
    return render(request, 'calificaciones/calificaciones_usuario.html', {
        'usuario': usuario,
        'calificaciones': calificaciones,
        'promedio': round(promedio, 1)
    })