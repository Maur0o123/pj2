from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django import forms
from .models import User, Usuario, UsuarioProfile, LicenciasUsuario, DocumentacionUsuario, UserInformacionLaboral

class UserAdmin(AuthUserAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'phone',
        'role',
        'is_active',
        'last_login',        
    ]
    def get_queryset(self, request):
        return super(UserAdmin, self).get_queryset(request).order_by('username', )
    
class UsuarioProfileAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(UsuarioProfileAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'telefono':
            formfield.widget = forms.TextInput(attrs={'col': 1})
        return formfield 
    
    list_display = [
        'user',
        'fechaNacimiento',
        'fechaCedulaVencimiento',        
    ]
    def get_queryset(self, request):
        return super(UsuarioProfileAdmin, self).get_queryset(request).order_by('user', )

class LicenciasUsuarioAdmin(admin.ModelAdmin):    
    list_display = [
        'user',
        'fechaLicenciaVencimiento',        
    ]
    def get_queryset(self, request):
        return super(LicenciasUsuarioAdmin, self).get_queryset(request).order_by('user', )

class DocumentacionUsuarioAdmin(admin.ModelAdmin):    
    list_display = [
        'user',
        'fotografiaUsuario',
        'fotografiaCedula',
        'fotografiaLicencia',        
    ]
    def get_queryset(self, request):
        return super(DocumentacionUsuarioAdmin, self).get_queryset(request).order_by('user', )


class UserInformacionLaboralAdmin(admin.ModelAdmin):
    # Admin para gestionar/validar manualmente la información laboral por usuario.
    list_display = [
        'user',
        'area',
        'ges',
        'cargo',
        'tipo_contrato',
        'fechaIngreso',
        'fechaDesvinculacion',
    ]
    def get_queryset(self, request):
        return super(UserInformacionLaboralAdmin, self).get_queryset(request).order_by('user')
            
admin.site.register(User,UserAdmin)
admin.site.register(UsuarioProfile,UsuarioProfileAdmin)
admin.site.register(LicenciasUsuario, LicenciasUsuarioAdmin)
admin.site.register(DocumentacionUsuario, DocumentacionUsuarioAdmin)
admin.site.register(UserInformacionLaboral, UserInformacionLaboralAdmin)
