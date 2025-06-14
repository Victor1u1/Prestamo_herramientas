from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Prestamo
from .forms import PrestamoForm, ActualizarEstadoPrestamoForm
from herramientas.models import Herramienta

@login_required
def solicitar_prestamo_view(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, id=herramienta_id)
    
    # Verificar que la herramienta esté disponible
    if herramienta.disponibilidad != 'disponible':
        messages.error(request, 'Esta herramienta no está disponible para préstamo.')
        return redirect('detalle_herramienta', herramienta_id=herramienta.id)
    
    # Verificar que el usuario no sea el propietario
    if herramienta.propietario == request.user:
        messages.error(request, 'No puedes solicitar préstamo de tu propia herramienta.')
        return redirect('detalle_herramienta', herramienta_id=herramienta.id)
    
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.herramienta = herramienta
            prestamo.prestatario = request.user
            prestamo.save()
            messages.success(request, 'Solicitud de préstamo enviada correctamente.')
            return redirect('mis_prestamos')
    else:
        form = PrestamoForm()
    
    return render(request, 'prestamos/solicitar_prestamo.html', {'form': form, 'herramienta': herramienta})

@login_required
def mis_prestamos_view(request):
    prestamos = Prestamo.objects.filter(prestatario=request.user).order_by('-fecha_solicitud')
    return render(request, 'prestamos/mis_prestamos.html', {'prestamos': prestamos})

@login_required
def prestamos_recibidos_view(request):
    prestamos = Prestamo.objects.filter(herramienta__propietario=request.user).order_by('-fecha_solicitud')
    return render(request, 'prestamos/prestamos_recibidos.html', {'prestamos': prestamos})

@login_required
def actualizar_estado_prestamo_view(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    # Verificar que el usuario sea el propietario de la herramienta o el prestatario
    if prestamo.herramienta.propietario != request.user and prestamo.prestatario != request.user:
        messages.error(request, 'No tienes permiso para actualizar este préstamo.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ActualizarEstadoPrestamoForm(request.POST, instance=prestamo, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estado del préstamo actualizado correctamente.')
            if prestamo.prestatario == request.user:
                return redirect('mis_prestamos')
            else:
                return redirect('prestamos_recibidos')
    else:
        form = ActualizarEstadoPrestamoForm(instance=prestamo, user=request.user)
    
    return render(request, 'prestamos/actualizar_estado_prestamo.html', {'form': form, 'prestamo': prestamo})

@login_required
def cancelar_prestamo_view(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id, prestatario=request.user)
    
    # Solo se pueden cancelar préstamos pendientes
    if prestamo.estado != 'pendiente':
        messages.error(request, 'Solo puedes cancelar préstamos pendientes.')
        return redirect('mis_prestamos')
    
    if request.method == 'POST':
        prestamo.estado = 'cancelado'
        prestamo.save()
        messages.success(request, 'Solicitud de préstamo cancelada correctamente.')
        return redirect('mis_prestamos')
    
    return render(request, 'prestamos/cancelar_prestamo.html', {'prestamo': prestamo})

@login_required
def finalizar_prestamo_view(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    
    # Verificar que el usuario sea el propietario de la herramienta o el prestatario
    if prestamo.herramienta.propietario != request.user and prestamo.prestatario != request.user:
        messages.error(request, 'No tienes permiso para finalizar este préstamo.')
        return redirect('dashboard')
    
    # Solo se pueden finalizar préstamos en curso o aceptados
    if prestamo.estado not in ['en_curso', 'aceptado']:
        messages.error(request, 'Solo puedes finalizar préstamos en curso o aceptados.')
        if prestamo.prestatario == request.user:
            return redirect('mis_prestamos')
        else:
            return redirect('prestamos_recibidos')
    
    if request.method == 'POST':
        prestamo.estado = 'finalizado'
        prestamo.save()
        messages.success(request, 'Préstamo finalizado correctamente.')
        if prestamo.prestatario == request.user:
            return redirect('mis_prestamos')
        else:
            return redirect('prestamos_recibidos')
    
    return render(request, 'prestamos/finalizar_prestamo.html', {'prestamo': prestamo})
