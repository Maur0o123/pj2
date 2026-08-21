from django import forms
from vehicle.models import Vehiculo
from core.models import Faena, Tipo
from core.utils import get_filtered_queryset
from mining.models import VehiculoAsignado


class FormSelectFaena(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        faena_actual = kwargs.pop('faena_actual', "")
        super(FormSelectFaena, self).__init__(*args, **kwargs)
        self.fields['faena'].label = "Seleccione Faena"
        faenas_queryset = Faena.objects.all().order_by('faena')
        choices = [(None, 'Todas las faenas')] + list(faenas_queryset.values_list('id', 'faena'))
        self.fields['faena'].choices = choices
        
    class Meta: 
        model = VehiculoAsignado
        fields = [
            'faena',                 
        ]
        widgets = {
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
        }

class FormSelectTipo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSelectTipo, self).__init__(*args, **kwargs)
        tipos_queryset = Tipo.objects.all().order_by('tipo')
        choices = [(None, 'Todos los tipos')] + list(tipos_queryset.values_list('id', 'tipo'))
        self.fields['tipo'].choices = choices
        self.fields['status'].choices = [
            ('', 'Todos'),
            (True, 'Habilitados'),  
            (False, 'Deshabilitados'),  
        ]

    class Meta: 
        model = Vehiculo
        fields = (
            'tipo',
            'status',
        ) 
        widgets = {
            'tipo': forms.Select(attrs={'style': 'text-align:center'}),
        }