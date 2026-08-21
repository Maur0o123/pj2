from django import forms
from core.utils import get_filtered_queryset
from .models import MarcaEquipo, NuevoEquipamiento, TipoEquipo
from core.models import Faena
class FormTipoEquipo(forms.ModelForm):     
    class Meta: 
        model = TipoEquipo
        fields = (
            'tipo',                 
        ) 
        widgets = {
            'tipo': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
class FormMarcaEquipo(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo_actual', "")
        super(FormMarcaEquipo, self).__init__(*args, **kwargs)
        self.fields['marca'].label = "Marca o Modelo del Equipo"
        campos = 'tipo'
        orden = campos.split(',')
        self.fields['tipo'].queryset = get_filtered_queryset(TipoEquipo,tipo, orden)
        
    class Meta: 
        model = MarcaEquipo
        fields = (
            'tipo',
            'marca',                 
        ) 
        widgets = {
            'tipo': forms.Select(attrs={'style': 'text-align:center'}),
            'marca': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }

class FormNuevoEquipamiento(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo_disabled', False)
        marca = kwargs.pop('marca_disabled', False)
        super(FormNuevoEquipamiento, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs['readonly'] = tipo
        self.fields['marca'].widget.attrs['readonly'] = marca
        self.fields['proximaMantencion'].widget.attrs['readonly'] = True
        self.fields['faena'].queryset = Faena.objects.filter(status=True).order_by('id')

    class Meta: 
        model = NuevoEquipamiento
        fields = (
            'tipo',
            'marca',
            'faena',
            'area',
            'ultimaMantencion',
            'frecuencia',
            'proximaMantencion',
            'notasAdicionales',
        ) 
        widgets = {
            'tipo': forms.Select(attrs={'style': 'text-align:center'}),
            'marca': forms.Select(attrs={'style': 'text-align:center'}),
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
            'area': forms.TextInput(attrs={'class':'textinput form-control' }), 
            'ultimaMantencion': forms.DateTimeInput(format='%Y-%m-%d', attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'frecuencia': forms.TextInput(attrs={'class':'textinput form-control','min':1, 'max':99999999, 'type':'Number', }), 
            'proximaMantencion': forms.DateTimeInput(format='%Y-%m-%d', attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'notasAdicionales': forms.Textarea(attrs={'class':'textinput form-control','rows':3})
        }

""" class FormFallaMaquinaria(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        kit = kwargs.pop('kit_actual', "")
        super(FormFallaMaquinaria, self).__init__(*args, **kwargs)
        self.fields['falla'].label = "Falla o incidente"
        campos = 'marcaMaquina'
        orden = campos.split(',')
        self.fields['kitMaquinaria'].queryset = get_filtered_queryset(KitsMaquinaria,kit,orden)
        
    class Meta: 
        model = FallaMaquinaria
        fields = (
            'kitMaquinaria',
            'falla',                 
        ) 
        widgets = {
            'kitMaquinaria': forms.Select(attrs={'style': 'text-align:center'}),
            'falla': forms.TextInput(attrs={'class':'textinput form-control' }), 
        } """
"""         
class FormMarcaMaquinariaSelect(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        super(FormMarcaMaquinariaSelect, self).__init__(*args, **kwargs)
        self.fields['marcaMaquina'].label = "Marca o Modelo"
        queryset = MarcaMaquinaria.objects.all().order_by('-tipo', 'marca')
        choices = [(marca.id, f"{marca.tipo} - {marca.marca}") for marca in queryset]
        self.fields['marcaMaquina'].choices = choices
        self.fields['marcaMaquina'].required = True 
        
    class Meta: 
        model = KitsMaquinaria
        fields = (
            'marcaMaquina',                 
        ) 
        widgets = {
            'marcaMaquina': forms.Select(attrs={'style': 'text-align:center'}),
        } """