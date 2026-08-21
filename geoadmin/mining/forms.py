from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import VehiculoAsignado
from core.models import Faena
from core.utils import get_filtered_queryset

class FormVehiculoAsignacion(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        #faena_disabled = kwargs.pop('faena_disabled', False)
        faena_actual = kwargs.pop('faena_actual', "")
        super(FormVehiculoAsignacion, self).__init__(*args, **kwargs)
        self.fields['creador'].label = "Asignado Por"
        self.fields['faenaAnterior'].label = "Faena Actual"
        self.fields['faena'].label = "Faena Siguiente"
        self.fields['faena'].required = True
        self.fields['fechaInicial'].required = True
        self.fields['fechaInicial'].disabled = True
        self.fields['vehiculo'].disabled = True
        self.fields['faenaAnterior'].disabled = True
        self.fields['creador'].disabled = True
        campos = 'faena'
        orden = campos.split(',')
        self.fields['faena'].queryset = get_filtered_queryset(Faena,faena_actual,orden)
        
    class Meta: 
        model = VehiculoAsignado
        fields = (
            'vehiculo',
            'faenaAnterior',
            'creador',
            'faena',            
            'fechaInicial',
            
        ) 
        widgets = {
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
            'vehiculo': forms.TextInput(attrs={'class':'textinput form-control' }), 
            'creador': forms.TextInput(attrs={'class':'textinput form-control' }), 
            'faenaAnterior': forms.TextInput(attrs={'class':'textinput form-control' }), 
            'fechaInicial': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaFinal': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),


        }