from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Maquinaria, NuevoHorometro, HistorialStockKitsMaquinariaFaena, KitsMaquinariaFaena
from core.models import Faena, TipoMaquinaria, MarcaMaquinaria, KitsMaquinaria
from core.utils import get_filtered_queryset

class FormMaquinaria(forms.ModelForm):
    horometro_actual = forms.IntegerField(label='Horómetro Actual', required=True)
    horometro_ultima_mantencion = forms.IntegerField(label='Horómetro Última Mantención Completa', required=True)

    def __init__(self, *args, **kwargs):
        es_creacion = kwargs.pop('es_creacion', True)
        faena_disabled = kwargs.pop('faena_disabled', False)
        faena_actual = kwargs.pop('faena_actual', "")
        marca_actual = kwargs.pop('marca_actual', "")
        tipo_actual = kwargs.pop('tipo_actual', "")
        super(FormMaquinaria, self).__init__(*args, **kwargs)
        if not es_creacion:
            self.fields.pop('horometro_actual')
            self.fields.pop('horometro_ultima_mantencion')
        self.fields['faena'].required = True
        self.fields['marca'].required = True
        self.fields['tipo'].required = True
        self.fields['faena'].disabled = faena_disabled
        campos_faena = 'faena'
        orden_faena = campos_faena.split(',')
        self.fields['faena'].queryset = get_filtered_queryset(Faena,faena_actual,orden_faena)#.exclude(faena="SIN ASIGNAR")
        campos_tipo = 'tipo'
        orden_tipo = campos_tipo.split(',')
        self.fields['tipo'].queryset = get_filtered_queryset(TipoMaquinaria,tipo_actual,orden_tipo)
        campos_marca = 'marca'
        orden_marca = campos_marca.split(',')
        self.fields['marca'].queryset = get_filtered_queryset(MarcaMaquinaria,marca_actual,orden_marca)
        
    class Meta: 
        model = Maquinaria
        fields = (
            'maquinaria',
            'descripcion',
            'fechaAdquisicion',
            'tipo',
            'marca',
            'faena',
            'frecuenciaMantenimiento'
        ) 
        widgets = {
            'fechaAdquisicion': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'tipo': forms.Select(attrs={'style': 'text-align:center'}),
            'marca': forms.Select(attrs={'style': 'text-align:center'}),
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
            'maquinaria': forms.TextInput(attrs={'class':'textinput form-control' }),
            'frecuenciaMantenimiento': forms.TextInput(attrs={'type':'number'}),
        }

class FormNuevoHorometro(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        maquinarias = kwargs.pop('maquinarias', None)
        maquinaria = kwargs.pop('maquinaria_actual', "")
        super(FormNuevoHorometro, self).__init__(*args, **kwargs)
        self.fields['horometro'].required = True
        campos = 'maquinaria'
        orden = campos.split(',')
        #self.fields['maquinaria'].queryset = get_filtered_queryset(Maquinaria,maquinaria, orden)
        if maquinarias is not None:
            self.fields['maquinaria'].queryset = Maquinaria.objects.filter(id__in=[v.id for v in maquinarias]).order_by(*orden)
        else:
            self.fields['maquinaria'].queryset = Maquinaria.objects.none()
        
    class Meta: 
        model = NuevoHorometro
        fields = (
            'maquinaria',
            'horometro',                 
        ) 
        widgets = {
            'maquinaria': forms.Select(attrs={'style': 'text-align:center'}),
            'horometro': forms.TextInput(attrs={'class':'textinput form-control', 'type':'number' }),
        }


class FormNuevoKitReparacionFaena(forms.ModelForm):
    
    class Meta: 
        model = KitsMaquinariaFaena
        fields = (
            'faena', 
            'kitMaquinaria'
        )
        widgets = {
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
            'kitMaquinaria': forms.Select(attrs={'style': 'text-align:center'}),
        }

    def __init__(self, *args, **kwargs):
        super(FormNuevoKitReparacionFaena, self).__init__(*args, **kwargs)
        self.fields['faena'].queryset = Faena.objects.exclude(faena='SIN ASIGNAR').order_by('faena')
        
        # Se restringe el QuerySet para listar solo Kits de Maquinaria con estado activo (status=True),
        # garantizando que solo se asignen recursos habilitados a las faenas operativas.
        self.fields['kitMaquinaria'].queryset = KitsMaquinaria.objects.filter(status=True).select_related('marcaMaquina__tipo').order_by('nombreKit')
        
        # Personaliza las etiquetas del select
        self.fields['kitMaquinaria'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(instance):
        return f"{instance.nombreKit} - {instance.marcaMaquina.marca} ({instance.marcaMaquina.tipo.tipo})"
    
class FormEditKitsMaquinariaFaena(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormEditKitsMaquinariaFaena, self).__init__(*args, **kwargs)
        self.fields['faena'].disabled = True
        self.fields['kitMaquinaria'].disabled = True
        self.fields['stockActual'].disabled = True
        self.fields['kitMaquinaria'].label = "Kit Reparación Maquinaria"

    class Meta:
        model = HistorialStockKitsMaquinariaFaena
        fields = (
            'kitMaquinaria',
            'faena',
            'stockActual',
        )
        widgets = {
            'kitMaquinaria': forms.Select(attrs={'style': 'text-align:center'}),
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
            'stockMovimiento': forms.TextInput(attrs={'class':'textinput form-control', 'type':'number' }),
            'stockActual': forms.TextInput(attrs={'class':'textinput form-control', 'type':'number' }),
            'descripcion': forms.TextInput(attrs={'class':'textinput form-control' }),
        }

        
class FormEditKitsMaquinariaFaenaAdd(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormEditKitsMaquinariaFaenaAdd, self).__init__(*args, **kwargs)
        self.fields['descripcion'].required = True
        self.fields['stockMovimiento'].required = True 
        self.fields['stockMovimiento'].label = "Cantidad"

    class Meta:
        model = HistorialStockKitsMaquinariaFaena
        fields = (
            'stockMovimiento',
            'descripcion',
        )
        widgets = {
            'stockMovimiento': forms.TextInput(attrs={'class':'textinput form-control', 'type':'number' }),
            'descripcion': forms.TextInput(attrs={'class':'textinput form-control' }),
        }