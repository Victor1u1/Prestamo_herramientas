from django.contrib import admin
from .models import Herramienta

@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'propietario', 'estado', 'disponibilidad', 'fecha_registro')
    list_filter = ('estado', 'disponibilidad', 'fecha_registro')
    search_fields = ('nombre', 'descripcion', 'propietario__username', 'propietario__email')
    ordering = ('-fecha_registro',)
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'propietario')
        }),
        ('Estado y disponibilidad', {
            'fields': ('estado', 'disponibilidad')
        }),
    )
    
    def has_module_permission(self, request):
        return request.user.is_authenticated and request.user.is_admin
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.is_admin
    
    def has_add_permission(self, request):
        return request.user.is_authenticated and request.user.is_admin
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.is_admin
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_authenticated and request.user.is_admin
