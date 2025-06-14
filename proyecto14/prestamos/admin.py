from django.contrib import admin
from .models import Prestamo

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('herramienta', 'prestatario', 'propietario_herramienta', 'fecha_solicitud', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_solicitud', 'fecha_inicio', 'fecha_fin')
    search_fields = ('herramienta__nombre', 'prestatario__username', 'herramienta__propietario__username')
    ordering = ('-fecha_solicitud',)
    date_hierarchy = 'fecha_solicitud'
    
    fieldsets = (
        ('Información del préstamo', {
            'fields': ('herramienta', 'prestatario')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )
    
    readonly_fields = ('fecha_solicitud',)
    
    def propietario_herramienta(self, obj):
        return obj.herramienta.propietario.username
    propietario_herramienta.short_description = 'Propietario'
    
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
