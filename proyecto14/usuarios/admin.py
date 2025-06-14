from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'direccion', 'telefono', 'fecha_registro', 'is_active')
    list_filter = ('rol', 'is_active', 'is_staff', 'fecha_registro')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'direccion')
    ordering = ('-fecha_registro',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('direccion', 'telefono', 'rol', 'is_admin')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('email', 'direccion', 'telefono', 'rol')
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
