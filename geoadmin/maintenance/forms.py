from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import NuevaSolicitudMantenimiento, NuevaSolicitudMantenimientoMaquinaria
from core.models import Tipo, Marca, Modelo, Ano, Color, TipoFallaVehiculo
from core.utils import get_filtered_queryset
from vehicle.models import Vehiculo
from machine.models import Maquinaria
from django_select2.forms import Select2MultipleWidget

class FormNuevaSolicitudMantenimiento(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        vehiculos = kwargs.pop('vehiculos', None)
        vehiculo_actual = kwargs.pop('vehiculo_actual', "")
        super(FormNuevaSolicitudMantenimiento, self).__init__(*args, **kwargs)    
        self.fields['solicitante'].label = "Nombre Solicitante"
        self.fields['turno'].label = "Turno (solo si corresponde)"  
        self.fields['solicitante'].disabled = True
        self.fields['turno'].required = False
        self.fields['kilometraje'].required = True
        #self.fields['avisoJefatura'].required = True
        self.fields['problemas'].required = True
        campos = 'placaPatente'
        orden = campos.split(',')
        #self.fields['vehiculo'].queryset = get_filtered_queryset(Vehiculo,vehiculo_actual,orden)
        if vehiculos is not None:
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(id__in=[v.id for v in vehiculos]).order_by(*orden)
        else:
            self.fields['vehiculo'].queryset = Vehiculo.objects.none()
    
    class Meta: 
        model = NuevaSolicitudMantenimiento
        fields = (
                'solicitante',
                'telefono',
                'turno',
                'vehiculo',
                'kilometraje',                
                #'avisoJefatura',
                'problemas',
                'comentario',
        )
        widgets = {
            'solicitante': forms.TextInput(attrs={'type':'text'}),
            'telefono': forms.TextInput(attrs={'type':'text'}),
            'vehiculo': forms.Select(attrs={'style': 'text-align:center'}),
            'turno': forms.Select(attrs={'style': 'text-align:center'}),
            'kilometraje': forms.TextInput(attrs={'type':'number'}),
            'comentario': forms.Textarea(attrs={'type':'text', 'rows':2}),
            'problemas': Select2MultipleWidget(attrs={'style': 'width: 50%', 'rows':10}),
        }

class FormEditSolicitudMantenimiento(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        vehiculos = kwargs.pop('vehiculos', None)
        vehiculo_actual = kwargs.pop('vehiculo_actual', "")
        super(FormEditSolicitudMantenimiento, self).__init__(*args, **kwargs)
        self.fields['solicitante'].label = "Nombre Solicitante"
        self.fields['turno'].label = "Turno (solo si corresponde)"  
        self.fields['solicitante'].disabled = True
        self.fields['turno'].required = False
        self.fields['problemas'].required = False
        self.fields['kilometraje'].required = True
        #self.fields['avisoJefatura'].required = True
        campos = 'placaPatente'
        orden = campos.split(',')
        #self.fields['vehiculo'].queryset = get_filtered_queryset(Vehiculo,vehiculo_actual,orden)
        vehiculos.append(vehiculo_actual)
        if vehiculos is not None:
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(id__in=[v.id for v in vehiculos]).order_by(*orden)
        else:
            self.fields['vehiculo'].queryset = Vehiculo.objects.none()
    
    class Meta: 
        model = NuevaSolicitudMantenimiento
        fields = (
                'solicitante',
                'telefono',
                'turno',
                'vehiculo',
                'kilometraje',                
                #'avisoJefatura',
                'problemas',
                'comentario',
        )
        widgets = {
            'solicitante': forms.TextInput(attrs={'type':'text'}),
            'telefono': forms.TextInput(attrs={'type':'text'}),
            'vehiculo': forms.Select(attrs={'style': 'text-align:center'}),
            'turno': forms.Select(attrs={'style': 'text-align:center'}),
            'kilometraje': forms.TextInput(attrs={'type':'text'}),
            'comentario': forms.Textarea(attrs={'type':'text', 'rows':2}),
            'problemas': Select2MultipleWidget(attrs={'style': 'width: 50%', 'rows':10}),
        }

class FormProcesarSolicitudMantenimiento(forms.ModelForm):
    def __init__(self, *args, **kwargs):        
        super(FormProcesarSolicitudMantenimiento, self).__init__(*args, **kwargs)        
        self.fields['progreso'].label = "Estado Solicitud"
        self.fields['progreso'].required = True  

    class Meta: 
        model = NuevaSolicitudMantenimiento
        fields = (
                'progreso',
                'empresaMantenimiento',
        )
        
class FormNuevaSolicitudMantenimientoMaquinaria(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        maquinarias = kwargs.pop('maquinarias', None)
        maquinaria_actual = kwargs.pop('maquinaria_actual', "")
        super(FormNuevaSolicitudMantenimientoMaquinaria, self).__init__(*args, **kwargs)
        self.fields['solicitante'].label = "Nombre Solicitante"  
        self.fields['turno'].label = "Turno (solo si corresponde)" 
        self.fields['solicitante'].disabled = True
        self.fields['turno'].required = False
        self.fields['horometro'].required = True
        #self.fields['avisoJefatura'].required = True
        self.fields['problemas'].required = True
        campos = 'maquinaria'
        orden = campos.split(',')
        #self.fields['maquinaria'].queryset = get_filtered_queryset(Maquinaria,maquinaria_actual,orden)
        if maquinarias is not None:
            self.fields['maquinaria'].queryset = Maquinaria.objects.filter(id__in=[v.id for v in maquinarias]).order_by(*orden)
        else:
            self.fields['maquinaria'].queryset = Maquinaria.objects.none()
    
    class Meta: 
        model = NuevaSolicitudMantenimientoMaquinaria
        fields = (
                'solicitante',
                'telefono',
                'turno',
                'maquinaria',
                'horometro',                
                #'avisoJefatura',
                'problemas',
                'comentario',
        )
        widgets = {
            'solicitante': forms.TextInput(attrs={'type':'text'}),
            'telefono': forms.TextInput(attrs={'type':'text'}),
            'maquinaria': forms.Select(attrs={'style': 'text-align:center'}),
            'turno': forms.Select(attrs={'style': 'text-align:center'}),
            'horometro': forms.TextInput(attrs={'type':'text'}),
            'comentario': forms.Textarea(attrs={'type':'text', 'rows':2}),
            'problemas': Select2MultipleWidget(attrs={'style': 'width: 50%', 'rows':10}),
        }

class FormEditSolicitudMantenimientoMaquinaria(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        maquinarias = kwargs.pop('maquinarias', None)
        maquinaria_actual = kwargs.pop('maquinaria_actual', "")
        super(FormEditSolicitudMantenimientoMaquinaria, self).__init__(*args, **kwargs)
        self.fields['solicitante'].label = "Nombre Solicitante"
        self.fields['turno'].label = "Turno (solo si corresponde)" 
        self.fields['solicitante'].disabled = True
        self.fields['turno'].required = False
        self.fields['problemas'].required = False
        self.fields['horometro'].required = True
        #self.fields['avisoJefatura'].required = True
        campos = 'maquinaria'
        orden = campos.split(',')
        #self.fields['maquinaria'].queryset = get_filtered_queryset(Maquinaria,maquinaria_actual,orden)
        maquinarias.append(maquinaria_actual)
        if maquinarias is not None:
            self.fields['maquinaria'].queryset = Maquinaria.objects.filter(id__in=[v.id for v in maquinarias]).order_by(*orden)
        else:
            self.fields['maquinaria'].queryset = Maquinaria.objects.none()
    
    class Meta: 
        model = NuevaSolicitudMantenimientoMaquinaria
        fields = (
                'solicitante',
                'telefono',
                'turno',
                'maquinaria',
                'horometro',                
                #'avisoJefatura',
                'problemas',
                'comentario',
        )
        widgets = {
            'solicitante': forms.TextInput(attrs={'type':'text'}),
            'telefono': forms.TextInput(attrs={'type':'text'}),
            'maquinaria': forms.Select(attrs={'style': 'text-align:center'}),
            'turno': forms.Select(attrs={'style': 'text-align:center'}),
            'horometro': forms.TextInput(attrs={'type':'number'}),
            'comentario': forms.Textarea(attrs={'type':'text', 'rows':2}),
            'problemas': Select2MultipleWidget(attrs={'style': 'width: 50%', 'rows':10}),
        }

class FormProcesarSolicitudMantenimientoMaquinaria(forms.ModelForm):
    def __init__(self, *args, **kwargs):        
        super(FormProcesarSolicitudMantenimientoMaquinaria, self).__init__(*args, **kwargs)        
        self.fields['progreso'].label = "Estado Solicitud"
        self.fields['progreso'].required = True  

    class Meta: 
        model = NuevaSolicitudMantenimientoMaquinaria
        fields = (
                'progreso',
                'empresaMantenimiento',
        )
        