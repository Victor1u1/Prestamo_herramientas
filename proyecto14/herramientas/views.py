from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegistroHerramientaForm
from .models import Herramienta
from usuarios.models import Usuario
# Create your views here.

@login_required
def registro_herramienta(request, pk):
    propietario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        form = RegistroHerramientaForm(request.POST, request.FILES)
        if form.is_valid():
            herramienta = form.save(commit=False)
            herramienta.propietario = request.user
            herramienta.save()
            return redirect('lista_herramientas')
    else:
        form = RegistroHerramientaForm()
    
    return render(request, 'herramientas/registro_herramienta.html', {'form': form})

@login_required
def lista_herramientas(request):
    herramientas_propias = Herramienta.objects.filter(propietario=request.user) #herramientas del usuario logeado
    herramientas_otras = Herramienta.objects.exclude(propietario=request.user) #herramietas de otros usuarios
    
    context = {
        'herramientas_propias': herramientas_propias,
        'herramientas_otras': herramientas_otras,
        'es_propietario': True  # Para controlar qué botones mostrar en la plantilla
    }
    
    return render(request, 'herramientas/lista_herramientas.html', context)

def detalle_herramienta(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    es_propietario = herramienta.propietario == request.user
    
    context = {
        'herramienta': herramienta,
        'es_propietario': es_propietario
    }
    
    return render(request, 'herramientas/detalle_herramienta.html', context)

def editar_herramienta(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    
    # Verificar que el usuario es el propietario
    if herramienta.propietario != request.user:
        return redirect('detalle_herramienta', pk=pk)
    
    if request.method == 'POST':
        form = RegistroHerramientaForm(request.POST, request.FILES, instance=herramienta)
        if form.is_valid():
            form.save()
            return redirect('detalle_herramienta', pk=pk)
    else:
        form = RegistroHerramientaForm(instance=herramienta)
    
    return render(request, 'herramientas/editar_herramienta.html', {'form': form})

def eliminar_herramienta(request, pk):
    herramienta = get_object_or_404(Herramienta, pk=pk)
    
    # Verificar que el usuario es el propietario
    if herramienta.propietario != request.user:
        return redirect('detalle_herramienta', pk=pk)
    
    if request.method == 'POST':
        herramienta.delete()
        return redirect('lista_herramientas')
    
    return render(request, 'herramientas/confirmar_eliminar.html', {'herramienta': herramienta})
