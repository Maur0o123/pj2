from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (Vehiculo, DocumentacionesVehiculo, InformacionTecnicaVehiculo, InfraccionesVehiculo, NuevoKilometraje, NuevaTarjetaCombustible,
                    MarcaSomnolencia, ModeloSomnolencia, AyudaTecnicaVehiculo)
from core.models import Tipo, Marca, Modelo, Ano, Color
from core.utils import get_filtered_queryset
from django.contrib.auth.models import User
from user.models import UsuarioProfile
from core.choices import tipodocumento, tipocombustible
from django.db.models import F
import re

class FormNuevoVehiculo(forms.ModelForm):
    kilometraje_actual = forms.IntegerField(
        required=True,
        label="Kilometraje Actual",
        widget=forms.NumberInput(attrs={'type': 'number', 'min': '0'})
    )
    kilometraje_ultima_mantencion = forms.IntegerField(
        required=True,
        label="Kilometraje Última Mantención General",
        widget=forms.NumberInput(attrs={'type': 'number', 'min': '0'})
    )
    frecuencia_mantenimiento = forms.IntegerField(
        required=True,
        label="Frecuencia de Mantenimiento (Kilómetros)",
        widget=forms.NumberInput(attrs={'type': 'number', 'min': '0'})
    )
    
    def __init__(self, *args, **kwargs):
        es_creacion = kwargs.pop('es_creacion', True)
        ocultar_fechaAdquisicion = kwargs.pop('ocultar_fechaAdquisicion', True)
        ocultar_fechaArriendoInicial = kwargs.pop('ocultar_fechaArriendoInicial', True)
        ocultar_fechaArriendoFinal = kwargs.pop('ocultar_fechaArriendoFinal', True)
        ocultar_fechaInstalacionGps = kwargs.pop('ocultar_fechaInstalacionGps', True)
        ocultar_fechaVencimientoLamina = kwargs.pop('ocultar_fechaVencimientoLamina', True)
        ocultar_fechaVencimientoTransportePrivado = kwargs.pop('ocultar_fechaVencimientoTransportePrivado', True)
        ocultar_fechaInstalacionBarraAntiVuelco = kwargs.pop('ocultar_fechaInstalacionBarraAntiVuelco', True)
        ocultar_fechaCertificadoOperatividad = kwargs.pop('ocultar_fechaCertificadoOperatividad', True)
        ocultar_fechaCertificadoMantencion = kwargs.pop('ocultar_fechaCertificadoMantencion', True)
        ocultar_fechaCertificadoGrua = kwargs.pop('ocultar_fechaCertificadoGrua', True)
        ocultar_fechaVencimientoPermisoCirculacion = kwargs.pop('ocultar_fechaVencimientoPermisoCirculacion', True)
        ocultar_fechaVencimientoRevisionTecnica = kwargs.pop('ocultar_fechaVencimientoRevisionTecnica', True)
        ocultar_fechaVencimientoSeguroObligatorio = kwargs.pop('ocultar_fechaVencimientoSeguroObligatorio', True)
        ocultar_tieneTag = kwargs.pop('ocultar_tieneTag', True)
        ocultar_tarjetaCombustible = kwargs.pop('ocultar_tarjetaCombustible', True)
        tipo_actual = kwargs.pop('tipo_actual', "")
        marca_actual = kwargs.pop('marca_actual', "")
        modelo_actual = kwargs.pop('modelo_actual', "")
        ano_actual = kwargs.pop('ano_actual', "")
        color_actual = kwargs.pop('color_actual', "")
        placaPatente_disabled = kwargs.pop('placaPatente_disabled', False)
        super(FormNuevoVehiculo, self).__init__(*args, **kwargs)
        if not es_creacion:
            del self.fields['kilometraje_actual']
            del self.fields['kilometraje_ultima_mantencion']
            del self.fields['frecuencia_mantenimiento']
        self.fields['fechaInstalacionGps'].label = "Fecha Certificado GPS (Vencimiento)"
        self.fields['fechaInstalacionBarraAntiVuelco'].label = "Fecha Barra AntiVuelco (Vencimiento)"
        self.fields['tenencia'].required = True
        self.fields['tipo'].required = True
        self.fields['marca'].required = True
        self.fields['modelo'].required = True
        self.fields['ano'].required = True
        self.fields['color'].required = True
        self.fields['fechaAdquisicion'].required = False
        self.fields['fechaInstalacionGps'].required = False
        self.fields['fechaVencimientoLamina'].required = False
        self.fields['fechaInstalacionBarraAntiVuelco'].required = False
        self.fields['fechaCertificadoOperatividad'].required = False
        self.fields['fechaCertificadoMantencion'].required = False
        self.fields['fechaCertificadoGrua'].required = False
        self.fields['fechaVencimientoPermisoCirculacion'].required = False
        self.fields['fechaVencimientoRevisionTecnica'].required = False
        self.fields['fechaVencimientoSeguroObligatorio'].required = False
        self.fields['placaPatente'].disabled = placaPatente_disabled
        self.fields['tarjetaCombustible'].widget.attrs['readonly'] = True
        campos_tipo = 'tipo'
        orden_tipo = campos_tipo.split(',')
        self.fields['tipo'].queryset = get_filtered_queryset(Tipo,tipo_actual,orden_tipo)
        campos_marca = 'marca'
        orden_marca = campos_marca.split(',')
        self.fields['marca'].queryset = get_filtered_queryset(Marca,marca_actual,orden_marca)
        campos_modelo = 'modelo'
        orden_modelo = campos_modelo.split(',')
        self.fields['modelo'].queryset = get_filtered_queryset(Modelo,modelo_actual,orden_modelo)
        campos_ano = 'ano'
        orden_ano = campos_ano.split(',')
        self.fields['ano'].queryset = get_filtered_queryset(Ano,ano_actual,orden_ano)
        campos_color = 'color'
        orden_color = campos_color.split(',')
        self.fields['color'].queryset = get_filtered_queryset(Color,color_actual,orden_color)
        if ocultar_fechaAdquisicion:
            self.fields['fechaAdquisicion'].widget = forms.HiddenInput()
        if ocultar_fechaArriendoInicial:
            self.fields['fechaArriendoInicial'].widget = forms.HiddenInput()
        if ocultar_fechaArriendoFinal:
            self.fields['fechaArriendoFinal'].widget = forms.HiddenInput()
        
        if ocultar_fechaInstalacionGps:
            self.fields['fechaInstalacionGps'].widget = forms.HiddenInput()
        if ocultar_fechaVencimientoLamina:
            self.fields['fechaVencimientoLamina'].widget = forms.HiddenInput()
        if ocultar_fechaInstalacionBarraAntiVuelco:
            self.fields['fechaInstalacionBarraAntiVuelco'].widget = forms.HiddenInput()
        if ocultar_tieneTag:
            self.fields['tieneTag'].widget = forms.HiddenInput()
        if ocultar_tarjetaCombustible:
            self.fields['tarjetaCombustible'].widget = forms.HiddenInput()
        if ocultar_fechaVencimientoTransportePrivado:
            self.fields['fechaVencimientoTransportePrivado'].widget = forms.HiddenInput()
        if ocultar_fechaCertificadoOperatividad:
            self.fields['fechaCertificadoOperatividad'].widget = forms.HiddenInput()
        if ocultar_fechaCertificadoMantencion:
            self.fields['fechaCertificadoMantencion'].widget = forms.HiddenInput()
        if ocultar_fechaCertificadoGrua:
            self.fields['fechaCertificadoGrua'].widget = forms.HiddenInput()
        if ocultar_fechaVencimientoPermisoCirculacion:
            self.fields['fechaVencimientoPermisoCirculacion'].widget = forms.HiddenInput()
        if ocultar_fechaVencimientoRevisionTecnica:
            self.fields['fechaVencimientoRevisionTecnica'].widget = forms.HiddenInput()
        if ocultar_fechaVencimientoSeguroObligatorio:
            self.fields['fechaVencimientoSeguroObligatorio'].widget = forms.HiddenInput()
                    
    class Meta: 
        model = Vehiculo
        model._meta.get_field('placaPatente')._unique = True
        model._meta.get_field('numeroMotor')._unique = True
        model._meta.get_field('numeroChasis')._unique = True
        model._meta.get_field('numeroVin')._unique = True
        fields = (
            'placaPatente',
            'rutPropietario',
            'tenencia',
            'fechaAdquisicion',
            'fechaArriendoInicial',
            'fechaArriendoFinal',
            'nombrePropietario',            
            'domicilio',
            'tipo',                  
            'marca',    
            'modelo',  
            'ano',
            'numeroMotor',                
            'numeroChasis',
            'numeroVin',
            'color',
            'tieneTag',
            'tarjetaCombustible',
            'fechaVencimientoLamina',
            'fechaInstalacionBarraAntiVuelco',
            'fechaInstalacionGps',
            'fechaVencimientoTransportePrivado',
            'fechaCertificadoOperatividad',
            'fechaCertificadoMantencion',
            'fechaCertificadoGrua',
            'fechaVencimientoPermisoCirculacion',
            'fechaVencimientoRevisionTecnica',
            'fechaVencimientoSeguroObligatorio',
        )
        widgets = {
            'placaPatente': forms.TextInput(attrs={'type':'text', 'placeholder':'Separa letras de números con Guión'}),
            'rutPropietario': forms.TextInput(attrs={'type':'text', 'placeholder':'Sin puntos ni guión', 'class':'inputs', 'maxlength':'12', 'onkeyup':'formatRutPropietario(this)'}),
            'tipo': forms.Select(attrs={'style': 'text-align:center'}),
            'marca': forms.Select(attrs={'style': 'text-align:center'}),
            'modelo': forms.Select(attrs={'style': 'text-align:center'}),
            'ano': forms.Select(attrs={'style': 'text-align:center'}),
            'color': forms.Select(attrs={'style': 'text-align:center'}),
            'fechaAdquisicion': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaArriendoInicial': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaArriendoFinal': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaInstalacionGps': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),  
            'fechaVencimientoLamina': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaVencimientoTransportePrivado': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaInstalacionBarraAntiVuelco': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaCertificadoOperatividad': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaCertificadoMantencion': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaCertificadoGrua': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaVencimientoPermisoCirculacion': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaVencimientoRevisionTecnica': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaVencimientoSeguroObligatorio': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'tarjetaCombustible': forms.TextInput(attrs={'style': 'text-align:center'}),
        }

class FormInformacionTecnica(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        super(FormInformacionTecnica, self).__init__(*args, **kwargs)
        self.fields['tipoTraccion'].required = False
        self.fields['pesoBrutoVehicular'].required = False
        self.fields['capacidadCarga'].required = False
        self.fields['tipoNeumatico'].required = False
        self.fields['tipoAceiteMotor'].required = False
        self.fields['tipoRefrigeranteMotor'].required = False
        self.fields['tipoFiltroAireMotor'].required = False
        self.fields['tipoFiltroCombustible'].required = False
        self.fields['proximoMantenimiento'].required = False
        self.fields['proximoMantenimientoGrua'].required = False
        
    class Meta: 
        model = InformacionTecnicaVehiculo
        fields = (
                'tipoTraccion',
                'pesoBrutoVehicular',
                'capacidadCarga',
                'tipoNeumatico',
                'tipoAceiteMotor',
                'tipoRefrigeranteMotor',
                'tipoFiltroAireMotor',
                'tipoFiltroCombustible',
                'frecuenciaMantenimiento',
                'proximoMantenimiento',
                'proximoMantenimientoGrua',
        )
        widgets = {
            'pesoBrutoVehicular': forms.TextInput(attrs={'type':'number'}),
            'capacidadCarga': forms.TextInput(attrs={'type':'number'}),
            'tipoNeumatico': forms.TextInput(attrs={'type':'text'}),
            'tipoAceiteMotor': forms.TextInput(attrs={'type':'text'}),
            'tipoRefrigeranteMotor': forms.TextInput(attrs={'type':'text'}),
            'tipoFiltroAireMotor': forms.TextInput(attrs={'type':'text'}),
            'tipoFiltroCombustible': forms.TextInput(attrs={'type':'text'}),
            'frecuenciaMantenimiento': forms.TextInput(attrs={'type':'number'}),
            'proximoMantenimiento': forms.TextInput(attrs={'type':'number'}),
            'proximoMantenimientoGrua': forms.TextInput(attrs={'type':'number'}),
        }
        
class FormMarcaSomnolencia(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormMarcaSomnolencia, self).__init__(*args, **kwargs)
        self.fields['marca'].label = "Proveedor del Equipo"
        
    class Meta: 
        model = MarcaSomnolencia
        fields = (
            'marca',
        )
        widgets = {
            'marca': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }

class FormModeloSomnolencia(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        marca = kwargs.pop('marca_actual', "")
        super(FormModeloSomnolencia, self).__init__(*args, **kwargs)
        self.fields['modelo'].label = "Modelo del Equipo"
        self.fields['marca'].label = "Proveedor del Dispositivo"
        campos = 'marca'
        orden = campos.split(',')
        self.fields['marca'].queryset = get_filtered_queryset(MarcaSomnolencia,marca, orden)
        
    class Meta: 
        model = ModeloSomnolencia
        fields = (
            'marca',
            'modelo',
        )
        widgets = {
            'marca': forms.Select(attrs={'style': 'text-align:center'}),
            'modelo': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }

class FormAyudaTecnicaVehiculo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormAyudaTecnicaVehiculo, self).__init__(*args, **kwargs)
        self.fields['proveedor'].queryset = MarcaSomnolencia.objects.filter(status=True)
    class Meta: 
        model = AyudaTecnicaVehiculo
        fields = (
            'dispositivo',
            'proveedor',
        )
    
class FormDocumentacionVehiculo(forms.ModelForm):    

    class Meta: 
        model = DocumentacionesVehiculo
        fields = (        
            'fotografiaPadron',
            'fotografiaPermisoCirculacion',
            'fotografiaRevisionTecnica',
            'fotografiaRevisionTecnicaGases',
            'fotografiaSeguroObligatorio',
            'fotografiaCertificadoGps',
            'fotografiaCertificadoOperatividad',
            'fotografiaCertificadoMantencion',
            'fotografiaCertificadoGrua',
            'fotografiaCertificadoVarios',
        ) 
        widgets = {
        }

class FormDocumentacionVehiculoExterior(forms.ModelForm):    

    class Meta: 
        model = DocumentacionesVehiculo
        fields = (        
            'fotografiaExteriorFrontis',
            'fotografiaExteriorAtras',
            'fotografiaExteriorPiloto',
            'fotografiaExteriorCopiloto', 
        ) 
        widgets = {
        }

class FormDocumentacionVehiculointerior(forms.ModelForm):    

    class Meta: 
        model = DocumentacionesVehiculo
        fields = (        
            'fotografiaInteriorTablero',
            'fotografiaInteriorCopiloto',
            'fotografiaInteriorAtrasPiloto',
            'fotografiaInteriorAtrasCopiloto',               
        ) 
        widgets = {
        }

class FormInfraccionesVehiculo(forms.ModelForm):
    
    class Meta:
        model = InfraccionesVehiculo
        fields = (
            
            'infraccion',
            'fechaInfraccion',
            'ciudadInfraccion',
            'estadoPagoInfraccion',
            'valorInfraccion',
        )
        widgets = {
            'fechaInfraccion': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'infraccion': forms.Textarea(attrs={'class':'textinput form-control' }),
            'valorInfraccion': forms.TextInput(attrs={'min':0, 'type':'text', 'maxlength':'10', 'class':'cambiarNumero'}),
        }

class FormNuevoKilometraje(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        vehiculos = kwargs.pop('vehiculos', None)
        vehiculo = kwargs.pop('vehiculo_actual', "")
        super(FormNuevoKilometraje, self).__init__(*args, **kwargs)
        self.fields['kilometraje'].required = True
        campos = 'placaPatente'
        orden = campos.split(',')
        if vehiculos is not None:
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(id__in=[v.id for v in vehiculos]).order_by(*orden)
        else:
            self.fields['vehiculo'].queryset = Vehiculo.objects.none()
    
    class Meta: 
        model = NuevoKilometraje
        fields = (
            'vehiculo',
            'kilometraje',                 
        ) 
        widgets = {
            'vehiculo': forms.Select(attrs={'style': 'text-align:center'}),
            'kilometraje': forms.TextInput(attrs={'class':'textinput form-control', 'type':'number' }),
        }

class FormNuevaFuelCards(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super(FormNuevaFuelCards, self).__init__(*args, **kwargs)

        self.fields['vehiculo'].queryset = Vehiculo.objects.exclude(tipo__in=[7, 13])

        self.fields['vehiculo'].label = "Placa Patente"

        self.fields['tipoVehiculo'].widget.attrs['readonly'] = True
        self.fields['nombrePropietario'].widget.attrs['readonly'] = True
        self.fields['rutPropietario'].widget.attrs['readonly'] = True
        self.fields['faena'].widget.attrs['readonly'] = True
        self.fields['tipoDocumento'].required = True
        self.fields['tipoCombustible'].required = True
        self.fields['numeroTarjeta'].required = True
        self.fields['fechaVencimiento'].required = True

    class Meta:
        model = NuevaTarjetaCombustible
        fields = (
            'vehiculo',
            'faena',
            'tipoVehiculo',
            'nombrePropietario',
            'rutPropietario',
            'tipoDocumento',
            'tipoCombustible',
            'numeroTarjeta',
            'fechaVencimiento',
        )
        widgets = {
            'vehiculo': forms.Select(attrs={'style': 'text-align:center'}),
            'numeroTarjeta': forms.TextInput(attrs={'class': 'textinput form-control', 'type': 'number'}),
            'fechaVencimiento': forms.DateTimeInput(
                format='%Y-%m-%d', attrs={'style': 'text-align:center', 'type': 'date', 'min': '1920-01-01'}
            ),
        }