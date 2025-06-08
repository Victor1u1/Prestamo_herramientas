from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('registro_herramienta/<int:pk>/', views.registro_herramienta, name='registro_herramienta'),
    path('lista/', views.lista_herramientas, name='lista_herramientas'),
    path('<int:pk>/', views.detalle_herramienta, name='detalle_herramienta'),
    #path('<int:pk>/editar/', views.editar_herramienta, name='editar_herramienta'),
    path('<int:pk>/eliminar/', views.eliminar_herramienta, name='eliminar_herramienta'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
