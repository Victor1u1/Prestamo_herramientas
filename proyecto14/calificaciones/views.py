# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Calificacion
from .forms import CalificacionForm

def inicio_calificacion(request):
    return render(request, 'calificaciones/inicio.html')

def listar_calificaciones(request):
    calificaciones = Calificacion.objects.all()
    return render(request, 'calificaciones/listar_calificaciones.html', {'calificaciones': calificaciones})


def crear_calificacion(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_calificaciones')
    else:
        form = CalificacionForm()
    return render(request, 'calificaciones/crear_calificacion.html', {'form': form})

def detalle_calificacion(request, pk):
    calificacion = get_object_or_404(Calificacion, pk=pk)
    return render(request, 'calificaciones/detalle_calificacion.html', {'calificacion': calificacion})
