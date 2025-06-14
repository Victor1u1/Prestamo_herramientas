from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Herramienta
from .forms import HerramientaForm

@login_required
def lista_herramientas_view(request):
    herramientas = Herramienta.objects.all()
    return render(request, 'herramientas/lista_herramientas.html', {'herramientas': herramientas})

@login_required
def mis_herramientas_view(request):
    herramientas = Herramienta.objects.filter(propietario=request.user)
    return render(request, 'herramientas/mis_herramientas.html', {'herramientas': herramientas})

@login_required
def agregar_herramienta_view(request):
    if request.method == 'POST':
        form = HerramientaForm(request.POST, request.FILES)
        if form.is_valid():
            herramienta = form.save(commit=False)
            herramienta.propietario = request.user
            herramienta.save()
            messages.success(request, 'Herramienta agregada correctamente.')
            return redirect('mis_herramientas')
    else:
        form = HerramientaForm()
    return render(request, 'herramientas/agregar_herramienta.html', {'form': form})

@login_required
def editar_herramienta_view(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, id=herramienta_id, propietario=request.user)
    
    if request.method == 'POST':
        form = HerramientaForm(request.POST, request.FILES, instance=herramienta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Herramienta actualizada correctamente.')
            return redirect('mis_herramientas')
    else:
        form = HerramientaForm(instance=herramienta)
    
    return render(request, 'herramientas/editar_herramienta.html', {'form': form, 'herramienta': herramienta})

@login_required
def eliminar_herramienta_view(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, id=herramienta_id, propietario=request.user)
    
    if request.method == 'POST':
        herramienta.delete()
        messages.success(request, 'Herramienta eliminada correctamente.')
        return redirect('mis_herramientas')
    
    return render(request, 'herramientas/eliminar_herramienta.html', {'herramienta': herramienta})

@login_required
def detalle_herramienta_view(request, herramienta_id):
    herramienta = get_object_or_404(Herramienta, id=herramienta_id)
    return render(request, 'herramientas/detalle_herramienta.html', {'herramienta': herramienta})
