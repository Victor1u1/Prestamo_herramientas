from django.urls import path
from . import views

urlpatterns = [
    path('solicitar/<int:herramienta_id>/', views.solicitar_prestamo_view, name='solicitar_prestamo'),
    path('mis-prestamos/', views.mis_prestamos_view, name='mis_prestamos'),
    path('recibidos/', views.prestamos_recibidos_view, name='prestamos_recibidos'),
    path('actualizar-estado/<int:prestamo_id>/', views.actualizar_estado_prestamo_view, name='actualizar_estado_prestamo'),
    path('cancelar/<int:prestamo_id>/', views.cancelar_prestamo_view, name='cancelar_prestamo'),
    path('finalizar/<int:prestamo_id>/', views.finalizar_prestamo_view, name='finalizar_prestamo'),
]
