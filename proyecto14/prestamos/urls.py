from django.urls import path
from . import views

app_name = 'prestamos'

urlpatterns = [
    path('', views.inicio_prestamos, name='inicio_prestamos'),  # ← inicio
    path('solicitar/<int:herramienta_id>/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('prestamo/', views.mis_prestamos, name='mis_prestamos'),
    path('recibidos/', views.gestionar_prestamos_recibidos, name='gestionar_prestamos_recibidos'),
    path('cambiar_estado/<int:prestamo_id>/<str:nuevo_estado>/', views.cambiar_estado_prestamo, name='cambiar_estado_prestamo'),
]
