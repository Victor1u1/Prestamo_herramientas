from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Herramienta
from .forms import HerramientaForm

from prestamos.forms import PrestamoForm

def lista_herramientas(request):
    query = request.GET.get('q', '')  
    if query:
        herramientas = Herramienta.objects.filter(nombre__icontains=query)
    else:
        herramientas = Herramienta.objects.all()
    return render(request, 'herramientas/lista.html', {'herramientas': herramientas, 'query': query})

@login_required
def detalle_herramienta(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)

    if herramienta.disponibilidad != 'disponible':
        messages.warning(request, "Esta herramienta no está disponible para préstamo.")

    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.herramienta = herramienta
            prestamo.prestatario = request.user
            prestamo.estado = 'pendiente'
            prestamo.save()
            messages.success(request, "Solicitud de préstamo enviada correctamente.")
            return redirect('prestamos:mis_prestamos')
    else:
        form = PrestamoForm()

    return render(request, 'herramientas/detalle.html', {'herramienta': herramienta, 'form': form})

def crear_herramienta(request):
    if request.method == 'POST':
        form = HerramientaForm(request.POST, request.FILES)  # para imagenes es importante request.FILES
        if form.is_valid():
            herramienta = form.save(commit=False)
            herramienta.propietario = request.user  # asignar el usuario logueado como propietario
            herramienta.save()
            return render(request, 'herramientas/crear.html')

    else:
        form = HerramientaForm()
    return render(request, 'herramientas/crear.html', {'form': form})
