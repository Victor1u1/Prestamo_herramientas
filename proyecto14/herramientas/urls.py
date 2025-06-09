# herramientas/urls.py

from django.urls import path
from . import views

app_name = 'herramientas'

urlpatterns = [
    path('', views.lista_herramientas, name='lista_herramientas'),       # lista y búsqueda
    path('crear/', views.crear_herramienta, name='crear_herramienta'),    # formulario para crear
    path('<int:pk>/', views.detalle_herramienta, name='detalle_herramienta'),  # detalle
    path('herramienta/<int:pk>/editar/', views.editar_herramienta, name='editar_herramienta'),
    path('herramienta/<int:pk>/eliminar/', views.eliminar_herramienta, name='eliminar_herramienta'),
]
