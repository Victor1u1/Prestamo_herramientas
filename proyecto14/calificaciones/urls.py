# urls.py
from django.urls import path
from .views import listar_calificaciones, crear_calificacion, detalle_calificacion
from . import views

urlpatterns = [

    path('', views.inicio_calificacion, name='inicio_calificacion'),  # Página de inicio
    path('crear/', crear_calificacion, name='crear_calificacion'),
    path('detalle/<int:pk>/', views.detalle_calificacion, name='detallecalificacion'),
    
]
