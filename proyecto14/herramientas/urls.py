from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_herramientas_view, name='lista_herramientas'),
    path('mis-herramientas/', views.mis_herramientas_view, name='mis_herramientas'),
    path('agregar/', views.agregar_herramienta_view, name='agregar_herramienta'),
    path('editar/<int:herramienta_id>/', views.editar_herramienta_view, name='editar_herramienta'),
    path('eliminar/<int:herramienta_id>/', views.eliminar_herramienta_view, name='eliminar_herramienta'),
    path('detalle/<int:herramienta_id>/', views.detalle_herramienta_view, name='detalle_herramienta'),
]
