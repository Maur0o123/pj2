from django import forms
from .models import PlanificacionFaenas, PlanificacionCampanas
from core.models import Faena, Tipo, Campana
from django.db.models import Q

class FormPlanificacionFaenas(forms.ModelForm):

    
    class Meta: 
        model = PlanificacionFaenas
        fields = (
            'cantidad',              
        ) 
        widgets = {
            'cantidad': forms.TextInput(attrs={'class':'textinput form-control', 'type':'number' }),
        }
        
class FormSelectFaena(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        faena_actual = kwargs.pop('faena_actual', "")
        super(FormSelectFaena, self).__init__(*args, **kwargs)
        self.fields['faena'].label = "Seleccione Faena"
        self.fields['faena'].queryset = Faena.objects.filter(status=True).filter(~Q(faena="SIN ASIGNAR")).order_by('faena')
        
    class Meta: 
        model = PlanificacionFaenas
        fields = [
            'faena',                 
        ]
        widgets = {
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
        }

class FormSelectTipo(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        tipo_actual = kwargs.pop('tipo_actual', "")
        super(FormSelectTipo, self).__init__(*args, **kwargs)
        self.fields['tipo'].label = "Seleccione Tipo Vehículo"
        self.fields['tipo'].queryset = Tipo.objects.filter(status=True).order_by('tipo')
        
    class Meta: 
        model = PlanificacionFaenas
        fields = [
            'tipo',                 
        ]
        widgets = {
            'tipo': forms.Select(attrs={'style': 'text-align:center'}),
        }
        

class FormSelectCampana(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        campana_actual = kwargs.pop('campana_actual', "")
        super(FormSelectCampana, self).__init__(*args, **kwargs)
        
        self.fields['campana'].label = "Seleccione Campaña"

        # Sobrescribimos el field con un ModelChoiceField personalizado
        self.fields['campana'] = forms.ModelChoiceField(
            queryset=Campana.objects.all().order_by('campana'),
            label="Seleccione Campaña",
            widget=forms.Select(attrs={'style': 'text-align:center'}),
            empty_label="---------",
        )
        
        # Esta función define cómo se muestran las opciones del select
        self.fields['campana'].label_from_instance = lambda obj: f"{obj.campana} ({obj.anoInicial} - {obj.anoFinal})"

    class Meta: 
        model = PlanificacionCampanas
        fields = ['campana']