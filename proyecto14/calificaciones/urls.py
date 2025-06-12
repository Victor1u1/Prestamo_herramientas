# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_calificaciones, name='base'),       # lista y búsqueda
    path('calificar/<int:prestamo_id>/', views.calificar_prestamo_view, name='calificar_prestamo'),
    path('mis_calificaciones/', views.mis_calificaciones_view, name='mis_calificaciones'),
    path('usuario/<int:usuario_id>/', views.calificaciones_usuario_view, name='calificaciones_usuario'),
]