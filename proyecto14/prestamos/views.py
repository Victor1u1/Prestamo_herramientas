from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from herramientas.models import Herramienta
from .models import Prestamo
from .forms import PrestamoForm
from django.contrib import messages
from django.shortcuts import redirect

def inicio_prestamos(request):
    return render(request, 'prestamos/inicio.html')

@login_required
def solicitar_prestamo(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, id=herramienta_id)
    
    # Evitar solicitar si está prestada
    if herramienta.disponibilidad != 'disponible':
        messages.error(request, "La herramienta no está disponible.")
        return redirect('herramientas:lista_herramientas')  
    
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamos = form.save(commit=False)
            prestamos.herramienta = herramienta
            prestamos.prestatario = request.user
            prestamos.estado = 'pendiente'
            prestamos.save()
            messages.success(request, "Solicitud enviada.")
            return redirect('prestamos:mis_prestamos')  # Ajusta esta vista
    else:
        form = PrestamoForm()

    return render(request, 'prestamos/solicitar.html', {'form': form, 'herramienta': herramienta})

@login_required
def mis_prestamos(request):
    prestamos = Prestamo.objects.filter(prestatario=request.user)
    return render(request, 'prestamos/prestamo.html', {'prestamos': prestamos})

@login_required
def gestionar_prestamos_recibidos(request):
    prestamos = Prestamo.objects.filter(herramienta__propietario=request.user, estado='pendiente')
    return render(request, 'prestamos/recibidos.html', {'prestamos': prestamos})

@login_required
def cambiar_estado_prestamo(request, prestamo_id, nuevo_estado):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id, herramienta__propietario=request.user)
    if nuevo_estado in ['aceptado', 'rechazado', 'cancelado', 'finalizado']:
        prestamo.estado = nuevo_estado
        prestamo.save()
        messages.success(request, f"Préstamo {nuevo_estado}.")
    return redirect('prestamos:gestionar_prestamos_recibidos')
