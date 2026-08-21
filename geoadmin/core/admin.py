from django.contrib import admin
from .models import Ciudad, Nacionalidad, Genero, Ano, Marca, Modelo, Color, Tipo, Faena

class CiudadAdmin(admin.ModelAdmin):
    list_display = [
        'ciudad',
        ]
    def get_queryset(self, request):
        return super(CiudadAdmin, self).get_queryset(request).order_by('id', )
    

class NacionalidadAdmin(admin.ModelAdmin):
    list_display = [
        'nacionalidad',
        ]
    def get_queryset(self, request):
        return super(NacionalidadAdmin, self).get_queryset(request).order_by('id', )
    
class GeneroAdmin(admin.ModelAdmin):
    list_display = [
        'genero',
        ]
    def get_queryset(self, request):
        return super(GeneroAdmin, self).get_queryset(request).order_by('id', )
    
class AnoAdmin(admin.ModelAdmin):
    list_display = [
        'ano',
        ]
    def get_queryset(self, request):
        return super(AnoAdmin, self).get_queryset(request).order_by('id', )

class MarcaAdmin(admin.ModelAdmin):
    list_display = [
        'marca',
        ]
    def get_queryset(self, request):
        return super(MarcaAdmin, self).get_queryset(request).order_by('id', )
    
class ModeloAdmin(admin.ModelAdmin):
    list_display = [
        'modelo',
        ]
    def get_queryset(self, request):
        return super(ModeloAdmin, self).get_queryset(request).order_by('id', )
    
class ColorAdmin(admin.ModelAdmin):
    list_display = [
        'color',
        ]
    def get_queryset(self, request):
        return super(ColorAdmin, self).get_queryset(request).order_by('id', )   

class TipoAdmin(admin.ModelAdmin):
    list_display = [
        'tipo',
        ]
    def get_queryset(self, request):
        return super(TipoAdmin, self).get_queryset(request).order_by('id', )   
    
admin.site.register(Faena)
