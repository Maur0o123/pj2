from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (Genero, Ciudad, Nacionalidad, Ano, Marca, Modelo, Color, Tipo, Faena, TipoDocumentoFaena, EmpresaServicios, 
                    EmpresaTipoServicios, TipoFallaVehiculo, OcultarOpcionesVehiculo, CategoriaFallaVehiculo, TipoDocumentoFaenaGeneral,
                    TipoMaquinaria, MarcaMaquinaria, KitsMaquinaria, FallaMaquinaria, FechasImportantes, ReporteError, AyudaManuales,
                    Sondas, Sondajes, Diametros, TipoTerreno, Orientacion, DetalleControlHorario, Corona, Escareador, CantidadAgua,
                    Aditivos, Casing, Zapata, LargoBarra, Recomendacion, Perforistas, MaterialesSonda, MaterialesCaseta, Campana, Programa,
                    RecomendacionAjuste, RecomendacionFinal, ProblemaVehiculo)
from .utils import get_filtered_queryset
from user.models import UsuarioProfile
from django.db import models
from django.db.models import Q
from core.models import Sondajes, Recomendacion, Sondas
from drilling.models import ReportesOperacionales

class FormGenero(forms.ModelForm):   
    class Meta: 
        model = Genero
        fields = (
            'genero',                         
        ) 
        widgets = {
            'genero': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }

class FormCiudad(forms.ModelForm):   
    class Meta: 
        model = Ciudad
        fields = (
            'ciudad',                 
        ) 
        widgets = {
            'ciudad': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
class FormNacionalidad(forms.ModelForm):   
    class Meta: 
        model = Nacionalidad
        fields = (
            'nacionalidad',                 
        ) 
        widgets = {
            'nacionalidad': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
class FormAno(forms.ModelForm):   
    class Meta: 
        model = Ano
        fields = (
            'ano',                 
        ) 
        widgets = {
            'ano': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
class FormMarca(forms.ModelForm):   
    class Meta: 
        model = Marca
        fields = (
            'marca',                 
        ) 
        widgets = {
            'marca': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }

class FormModelo(forms.ModelForm):   
    class Meta: 
        model = Modelo
        fields = (
            'modelo',                 
        ) 
        widgets = {
            'modelo': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
class FormColor(forms.ModelForm):   
    class Meta: 
        model = Color
        fields = (
            'color',                 
        ) 
        widgets = {
            'color': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }

class FormTipo(forms.ModelForm):   
    class Meta: 
        model = Tipo
        fields = (
            'tipo',                 
        ) 
        widgets = {
            'tipo': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }

class FormNuevaFaena(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        faena_disabled = kwargs.pop('faena_disabled', False)
        super(FormNuevaFaena, self).__init__(*args, **kwargs)
        self.fields['descripcion'].required = False 
        self.fields['descripcion'].label = "Descriçión de la Faena (Opcional)"
        self.fields['faena'].disabled = faena_disabled
        
    class Meta: 
        model = Faena
        fields = (
            'faena',
            'descripcion',               
        ) 
        widgets = {
            'faena': forms.TextInput(attrs={'class':'textinput form-control' }), 
            'descripcion': forms.Textarea(attrs={'class':'textinput form-control' }), 
        }
        
class FormTipoDocumentoFaena(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        #faena_disabled = kwargs.pop('faena_disabled', False)
        faena_actual = kwargs.pop('faena_actual', "")
        super(FormTipoDocumentoFaena, self).__init__(*args, **kwargs)
        #self.fields['descripcion'].required = False 
        #self.fields['descripcion'].label = "Descriçión de la Faena (Opcional)"
        #self.fields['faena'].disabled = faena_disabled
        campos = 'faena'
        orden = campos.split(',')
        self.fields['faena'].queryset = get_filtered_queryset(Faena,faena_actual,orden).exclude(faena="SIN ASIGNAR")
        
    class Meta: 
        model = TipoDocumentoFaena
        fields = (
            'faena',
            'documento',               
        ) 
        widgets = {
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
            'documento': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
class FormNuevaEmpresaServicios(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        empresa_disabled = kwargs.pop('empresa_disabled', False)
        rut_disabled = kwargs.pop('rut_disabled', False)
        super(FormNuevaEmpresaServicios, self).__init__(*args, **kwargs)
        self.fields['descripcion'].required = False
        self.fields['descripcion'].label = "Descripción de la Empresa (Opcional)"
        self.fields['empresa'].disabled = empresa_disabled
        self.fields['rut'].disabled = rut_disabled
        
    class Meta: 
        model = EmpresaServicios
        fields = (
            'empresa',
            'rut',
            'telefono',
            'direccion',
            'descripcion',               
        ) 
        widgets = {
            'empresa': forms.TextInput(attrs={'class':'textinput form-control' }), 
            'descripcion': forms.Textarea(attrs={'class':'textinput form-control' }), 
            'rut': forms.TextInput(attrs={'type':'text', 'placeholder':'Sin puntos ni guión', 'class':'inputs', 'maxlength':'12', 'onkeyup':'formatRutEmpresa(this)'}),
            'telefono': forms.TextInput(attrs={'min':100000000, 'max':999999999, 'type':'Number', 'placeholder':'9XXXXXXXX', 'maxlength':'9', 'onkeyup':'formatTelefono(this)'}),
        }
        
class FormEmpresaTipoServicios(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop('empresa_actual', "")
        super(FormEmpresaTipoServicios, self).__init__(*args, **kwargs)
        self.fields['servicio'].label = "Tipo de Servicio"
        campos = 'empresa'
        orden = campos.split(',')
        self.fields['empresa'].queryset = get_filtered_queryset(EmpresaServicios,empresa,orden)
        
    class Meta: 
        model = EmpresaTipoServicios
        fields = (
            'empresa',
            'servicio',
        ) 
        widgets = {
            'empresa': forms.Select(attrs={'style': 'text-align:center'}),
            'servicio': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
class FormTipoFallaVehiculo(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        categoria = kwargs.pop('categoria_actual', "")
        super(FormTipoFallaVehiculo, self).__init__(*args, **kwargs)
        self.fields['falla'].label = "Tipo de Falla"
        campos = 'categoria'
        orden = campos.split(',')
        self.fields['categoria'].queryset = get_filtered_queryset(CategoriaFallaVehiculo,categoria,orden)
    
    def clean_falla(self):
        falla = self.cleaned_data.get('falla', '')
        return falla.strip().title()
        
    class Meta: 
        model = TipoFallaVehiculo
        fields = (
            'categoria',
            'falla',                 
        ) 
        widgets = {
            'categoria': forms.Select(attrs={'style': 'text-align:center'}),
            'falla': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
class FormCategoriaFallaVehiculo(forms.ModelForm):
    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria', '')
        return categoria.strip().title()
     
    class Meta: 
        model = CategoriaFallaVehiculo
        fields = (
            'categoria',                 
        ) 
        widgets = {
            'categoria': forms.TextInput(attrs={'class':'textinput form-control' }), 
        } 
        
class FormOcultarOpcionesVehiculoAdicional(forms.ModelForm):     
    class Meta: 
        model = OcultarOpcionesVehiculo
        fields = (
                
            'fechaVencimientoLamina',
            'fechaInstalacionBarraAntiVuelco',
            'fechaInstalacionGps',
            'fechaVencimientoTransportePrivado',
            'fechaCertificadoOperatividad',
            'fechaCertificadoMantencion',
            'fechaCertificadoGrua',
            'tieneTag',
            'tarjetaCombustible',
        ) 
        widgets = {
        }
        
class FormOcultarOpcionesVehiculoTecnica(forms.ModelForm):     
    class Meta: 
        model = OcultarOpcionesVehiculo
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
        }
        
class FormOcultarOpcionesVehiculoDocumentacion(forms.ModelForm):     
    class Meta: 
        model = OcultarOpcionesVehiculo
        fields = (
            'fotografiaFacturaCompra',
            'fotografiaPadron',
            'fotografiaPermisoCirculacion',
            'fotografiaRevisionTecnica',
            'fotografiaRevisionTecnicaGases',
            'fotografiaSeguroObligatorio',
            'fotografiaSeguroAutomotriz',
            'fotografiaCertificadoGps',
            'fotografiaCertificadoMantencion',
            'fotografiaCertificadoOperatividad',
            'fotografiaCertificadoGrua',
            'fotografiaCertificadoLamina',
            'fotografiaCertificadoBarraAntiVuelco',
            'fotografiaDocumentacionMiniBus',
        ) 
        widgets = {
        }
        
class FormOcultarOpcionesVehiculoInterior(forms.ModelForm):     
    class Meta: 
        model = OcultarOpcionesVehiculo
        fields = (
            'fotografiaInteriorTablero',
            'fotografiaInteriorCopiloto',
            'fotografiaInteriorAtrasPiloto',
            'fotografiaInteriorAtrasCopiloto',
        ) 
        widgets = {
        }
        
class FormOcultarOpcionesVehiculoExterior(forms.ModelForm):     
    class Meta: 
        model = OcultarOpcionesVehiculo
        fields = (
            'fotografiaExteriorFrontis',
            'fotografiaExteriorAtras',
            'fotografiaExteriorPiloto',
            'fotografiaExteriorCopiloto',
        ) 
        widgets = {
        }
        
class FormTipoDocumentoFaenaGeneral(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        nombredocumento_disabled = kwargs.pop('nombredocumento_disabled', False)
        faena_disabled = kwargs.pop('faena_disabled', False)
        faena_actual = kwargs.pop('faena_actual', "")
        super(FormTipoDocumentoFaenaGeneral, self).__init__(*args, **kwargs)
        self.fields['nombredocumento'].disabled = nombredocumento_disabled
        self.fields['faena'].disabled = faena_disabled
        campos = 'faena'
        orden = campos.split(',')
        self.fields['faena'].queryset = get_filtered_queryset(Faena,faena_actual,orden).exclude(faena="SIN ASIGNAR")
        
    class Meta: 
        model = TipoDocumentoFaenaGeneral
        fields = (
            'faena',
            'nombredocumento',
            'fechacaducidad',
        ) 
        widgets = {
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
            'nombredocumento': forms.TextInput(attrs={'class':'textinput form-control' }), 
            'fechacaducidad': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class FormTipoMaquinaria(forms.ModelForm):     
    class Meta: 
        model = TipoMaquinaria
        fields = (
            'tipo',                 
        ) 
        widgets = {
            'tipo': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
class FormMarcaMaquinaria(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        tipo = kwargs.pop('tipo_actual', "")
        super(FormMarcaMaquinaria, self).__init__(*args, **kwargs)
        self.fields['marca'].label = "Marca o Modelo de la Maquinaria"
        campos = 'tipo'
        orden = campos.split(',')
        self.fields['tipo'].queryset = get_filtered_queryset(TipoMaquinaria,tipo, orden)
        
    class Meta: 
        model = MarcaMaquinaria
        fields = (
            'tipo',
            'marca',                 
        ) 
        widgets = {
            'tipo': forms.Select(attrs={'style': 'text-align:center'}),
            'marca': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }

class FormKitReparacion(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        marca = kwargs.pop('marca_actual', "")
        marcaMaquina_disabled = kwargs.pop('marcaMaquina_disabled', False)
        nombreKit_disabled = kwargs.pop('nombreKit_disabled', False)
        super(FormKitReparacion, self).__init__(*args, **kwargs)
        self.fields['nombreKit'].label = "Nombre del Kit de Reparación"
        self.fields['marcaMaquina'].label = "Marca (Tipo)"
        self.fields['marcaMaquina'].disabled = marcaMaquina_disabled
        self.fields['nombreKit'].disabled = nombreKit_disabled
        campos = '-tipo' + ',' + 'marca'
        orden = campos.split(',')
        
        # Filtra el QuerySet para listar únicamente Marcas de Maquinaria activas (status=True),
        # evitando la selección de registros deshabilitados.
        queryset = get_filtered_queryset(MarcaMaquinaria, marca, orden).filter(status=True)
        
        choices = [(marca.id, f"{marca.tipo} - {marca.marca}") for marca in queryset]
        self.fields['marcaMaquina'].choices = choices
        
    class Meta: 
        model = KitsMaquinaria
        fields = (
            'marcaMaquina',
            'nombreKit',
            'stockMinimo',
            'stockMaximo',
        ) 
        widgets = {
            'marcaMaquina': forms.Select(attrs={'style': 'text-align:center'}),
            'nombreKit': forms.TextInput(attrs={'class':'textinput form-control' }), 
            'stockMinimo': forms.TextInput(attrs={'class':'textinput form-control','min':1, 'max':99999999, 'type':'Number', }), 
            'stockMaximo': forms.TextInput(attrs={'class':'textinput form-control','min':1, 'max':99999999, 'type':'Number', }), 
        }

class FormFallaMaquinaria(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        kit = kwargs.pop('kit_actual', "")
        super(FormFallaMaquinaria, self).__init__(*args, **kwargs)
        self.fields['falla'].label = "Falla o incidente"
        campos = 'marcaMaquina'
        orden = campos.split(',')

        # Filtra el QuerySet para listar únicamente Kits activos (status=True),
        # evitando la selección de registros deshabilitados.
        self.fields['kitMaquinaria'].queryset = get_filtered_queryset(KitsMaquinaria, kit, orden).filter(status=True)
        
    class Meta: 
        model = FallaMaquinaria
        fields = (
            'kitMaquinaria',
            'falla',                 
        ) 
        widgets = {
            'kitMaquinaria': forms.Select(attrs={'style': 'text-align:center'}),
            'falla': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }
        
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
        }
        
class FormNuevaFechasImportantes(forms.ModelForm):  
    class Meta: 
        model = FechasImportantes
        fields = (
            'fechaVencimiento',
            'descripcion',
        ) 
        widgets = {
            'descripcion': forms.TextInput(attrs={'class':'textinput form-control' }),
        }

class FormReporteError(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormReporteError, self).__init__(*args, **kwargs)
        self.fields['detalle'].label = "Detalla claramente como se produjo el problema (sección, hora aproximada, etc...)"
        
    class Meta: 
        model = ReporteError
        fields = (
            'descripcion',
            'detalle',
        ) 
        widgets = {
            'detalle': forms.Textarea(attrs={'class':'textinput form-control' }), 
        }

class FormAyudaManuales(forms.ModelForm):
        
    class Meta: 
        model = AyudaManuales
        fields = (
            'seccion',
            'nombredocumento',
        )
        
class FormSeleccionSeccion(forms.ModelForm):
    seccion_select = forms.ChoiceField(
        choices=[],
        required=True,
        label="Opciones",
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'text-align:center; width: 100%;'})
    )

    class Meta:
        model = UsuarioProfile
        fields = ()

    def __init__(self, *args, **kwargs):
        usuario_profile = kwargs.pop('usuario_profile', None)
        super(FormSeleccionSeccion, self).__init__(*args, **kwargs)
        opciones = []
        accesos_nulos = [None, '', 'No', 'SIN ASIGNAR']

        if usuario_profile:
            if usuario_profile.seccionAdministracion not in accesos_nulos:
                opciones.append(('administracion', 'Administración'))
            if usuario_profile.seccionVehicular not in accesos_nulos:
                opciones.append(('vehicular', 'Registro Vehicular'))
            if usuario_profile.seccionSondaje not in accesos_nulos:
                opciones.append(('sondaje', 'Sondajes'))
            if usuario_profile.seccionPrevencion not in accesos_nulos:
                opciones.append(('prevencion', 'Prevención de Riesgos'))
            if usuario_profile.seccionInventario not in accesos_nulos:
                opciones.append(('inventario', 'Inventario'))
                
        self.fields['seccion_select'].choices = opciones
        
class FormSondas(forms.ModelForm):
        
    class Meta: 
        model = Sondas
        fields = (
            'sonda',
        )

class FormSondajes(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        faena_actual = kwargs.pop('faena_actual', "")
        super(FormSondajes, self).__init__(*args, **kwargs)
        campos = 'faena'
        orden = campos.split(',')
        self.fields['faena'].queryset = get_filtered_queryset(Faena,faena_actual,orden).exclude(faena="SIN ASIGNAR")
            
    class Meta: 
        model = Sondajes
        model._meta.get_field('sondaje')._unique = True
        fields = (
            'faena',
            'sondaje',
            )
        
class FormDiametros(forms.ModelForm):
                
    class Meta: 
        model = Diametros
        fields = (
            'diametro',
        )

class FormTipoTerreno(forms.ModelForm):

    class Meta: 
        model = TipoTerreno
        fields = (
            'tipoTerreno',
        )

class FormOrientacion(forms.ModelForm):

    class Meta: 
        model = Orientacion
        fields = (
            'orientacion',
        )

class FormDetalleControlHorario(forms.ModelForm):

    class Meta: 
        model = DetalleControlHorario
        fields = (
            'detalle',
        )

class FormCorona(forms.ModelForm):
    
    class Meta: 
        model = Corona
        fields = (
            'corona',
        )

class FormEscareador(forms.ModelForm):
    
    class Meta: 
        model = Escareador
        fields = (
            'escareador',
        )
        
class FormCantidadAgua(forms.ModelForm):
    
    class Meta: 
        model = CantidadAgua
        fields = (
            'cantidadAgua',
        )

class FormAditivos(forms.ModelForm):
    
    class Meta: 
        model = Aditivos
        fields = (
            'aditivo',
        )
        
class FormCasing(forms.ModelForm):
    
    class Meta: 
        model = Casing
        fields = (
            'casing',
        )

class FormZapata(forms.ModelForm):
    
    class Meta: 
        model = Zapata
        fields = (
            'zapata',
        )

class FormLargoBarra(forms.ModelForm):
    
    class Meta: 
        model = LargoBarra
        fields = (
            'largoBarra',
        )

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
class CampanaChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Aquí definimos el formato: "NombreFaena - NombreCampaña"
        return f"{obj.faena} - {obj.campana}"

class FormRecomendaciones(forms.ModelForm):
    # Definimos explícitamente el campo usando la clase personalizada
    campana = CampanaChoiceField(
        queryset=Campana.objects.all().order_by('faena__faena', 'campana'), # Ordenamos por Faena y luego Campaña
        widget=forms.Select(attrs={'style': 'text-align:center'}),
        label="Campaña"
    )

    class Meta:
        model = Recomendacion
        fields = (
            'campana',
            'programa',
            'recomendacion',
            'pozo',
            'sonda',
            'fecha_inicio',
            'sector', 
            'azimut',
            'inclinacion',
            'este',
            'norte',
            'cota',
            'manteo',
            'largo_programado',
            'largo_real',
            'estado',
        )

        widgets = {
            # 'campana': ... (Ya no es necesario definirlo aquí porque lo definimos arriba)
            'programa': forms.Select(attrs={'style': 'text-align:center'}),
            'fecha_inicio': forms.DateTimeInput(attrs={'style': 'text-align:center', 'type': 'date', 'min': "1920-01-01"}),
            'azimut': forms.NumberInput(attrs={'min': 0, 'max': 360, 'step': 1}),
        }

    def __init__(self, *args, **kwargs):
        campana_disabled = kwargs.pop('campana_disabled', False)
        programa = kwargs.pop('programa_disabled', False)
        super().__init__(*args, **kwargs)

        # 1. Obtenemos todos los reportes aprobados y activos
        reportes_aprobados = ReportesOperacionales.objects.filter(
            progreso='Aprobado',
            status=1  # <--- Agregamos esta condición
        ).select_related('sondajeCodigo').order_by('sondajeCodigo__sondaje', 'sondajeSerie')

        # 2. Creamos los identificadores disponibles
        identificadores_disponibles = set()
        for r in reportes_aprobados:
            identificador = f"{r.sondajeCodigo.sondaje}-{r.sondajeSerie}"
            
            if r.sondajeEstado: 
                identificador += f"{r.get_sondajeEstado_display()}"
                
            identificadores_disponibles.add(identificador)

        # Mostrar solo pozos que no tengan ninguna recomendacion activa
        query_ocupados = Recomendacion.objects.filter(status=True).exclude(pozo__isnull=True).exclude(pozo__exact='')
        if self.instance and self.instance.pk:
            query_ocupados = query_ocupados.exclude(pk=self.instance.pk)
            
        pozos_con_recomendacion = set(
            (pozo or "").strip()
            for pozo in query_ocupados.values_list('pozo', flat=True)
            if pozo
        )
        
        # 4. Filtramos los pozos disponibles
        pozos_finales = list(identificadores_disponibles - pozos_con_recomendacion)
        
        # SEGURIDAD: Si editamos, forzamos que el pozo actual esté en la lista final
        if self.instance and self.instance.pk and self.instance.pozo:
            if self.instance.pozo not in pozos_finales:
                pozos_finales.append(self.instance.pozo)
                
        pozos_finales.sort()

        # 5. Asignamos al Select
        opciones_pozo = [('', '---------')] + [(p, p) for p in pozos_finales]
        
        # Configuraciones adicionales de los campos
        self.fields['campana'].widget.attrs['readonly'] = campana_disabled
        self.fields['programa'].widget.attrs['readonly'] = programa
        self.fields['azimut'].initial = None
        self.fields['largo_real'].widget.attrs['readonly'] = True
        self.fields['largo_real'].initial = 0
        self.fields['azimut'].required = True
        self.fields['largo_programado'].required = True
        self.fields['largo_real'].required = False
        self.fields['este'].required = True
        self.fields['norte'].required = True
        self.fields['cota'].required = True
        self.fields['manteo'].required = False
        self.fields['manteo'].widget = forms.HiddenInput()
        self.fields['largo_real'].widget = forms.HiddenInput()
        
        self.fields['pozo'].widget = forms.Select(choices=opciones_pozo)
        
        # Nueva recomendacion: la sonda se determina por pozo via JS/AJAX (solo una opcion)
        if not (self.instance and self.instance.pk):
            pozo_seleccionado = (self.data.get('pozo') if self.data else None) or self.initial.get('pozo')
            sonda_predeterminada_id = self._obtener_sonda_predeterminada_por_pozo(pozo_seleccionado)
            if sonda_predeterminada_id:
                self.fields['sonda'].queryset = Sondas.objects.filter(id=sonda_predeterminada_id)
            else:
                self.fields['sonda'].queryset = Sondas.objects.none()
        else:
            recomendaciones_ocupadas = Recomendacion.objects.filter(status=True).exclude(Q(id=self.instance.id) | Q(estado__in=[1,4]))
            sondas_usadas = recomendaciones_ocupadas.values_list('sonda_id', flat=True)
            queryset = Sondas.objects.exclude(id__in=sondas_usadas)

            if self.instance and self.instance.sonda:
                queryset = Sondas.objects.filter(Q(id=self.instance.sonda.id) | ~Q(id__in=sondas_usadas))

            self.fields['sonda'].queryset = queryset.order_by('sonda')

    def _obtener_sonda_predeterminada_por_pozo(self, pozo_string):
        if not pozo_string:
            return None

        try:
            partes = str(pozo_string).rsplit('-', 1)
            if len(partes) < 2:
                return None

            codigo_sondaje = partes[0]
            serie_gemelo_str = partes[1]
            gemelo_letra = None
            serie_sondaje = serie_gemelo_str

            if serie_gemelo_str and not serie_gemelo_str[-1].isdigit():
                gemelo_letra = serie_gemelo_str[-1].upper()
                serie_sondaje = serie_gemelo_str[:-1]

            filtros = {
                'sondajeCodigo__sondaje': codigo_sondaje,
                'sondajeSerie': serie_sondaje,
                'progreso': 'Aprobado',
                'status': True,
            }

            if gemelo_letra:
                mapa_gemelo = {'A': '1', 'B': '2'}
                gemelo_id = mapa_gemelo.get(gemelo_letra)
                if not gemelo_id:
                    return None
                filtros['sondajeEstado'] = gemelo_id
            else:
                filtros['sondajeEstado__in'] = ['', None]

            ultimo_reporte = ReportesOperacionales.objects.filter(**filtros).order_by('-fechacreacion').first()
            if ultimo_reporte and ultimo_reporte.sonda_id:
                return ultimo_reporte.sonda_id
        except Exception:
            return None

        return None

    def clean_azimut(self):
        """ Validación en backend: azimut debe estar entre 0 y 360. """
        azimut = self.cleaned_data.get('azimut')
        if azimut is not None:
            try:
                azimut = int(azimut)
                if azimut < 0 or azimut > 360:
                    raise forms.ValidationError("El azimut debe estar entre 0 y 360.")
            except ValueError:
                raise forms.ValidationError("El azimut debe ser un número entero válido.")
        return azimut

    def clean(self):
        """Validación general para asegurar que los campos obligatorios tengan valores."""
        cleaned_data = super().clean()
        campos_obligatorios = ['recomendacion', 'pozo', 'sonda', 'fecha_inicio', 'sector', 'inclinacion']
        for campo in campos_obligatorios:
            if not cleaned_data.get(campo):
                self.add_error(campo, f"Este campo es obligatorio.")
        return cleaned_data

class FormRecomendacionesAjuste(forms.ModelForm):
        
    class Meta:
        model = RecomendacionAjuste
        fields = (
            'azimutAjuste',
            'esteAjuste', 
            'norteAjuste',
            'cotaAjuste',
            'manteoAjuste',
        )
        widgets = {
            'azimutAjuste': forms.NumberInput(attrs={'min': 0, 'max': 360, 'step': 1}),
        }
        
class FormRecomendacionesFinal(forms.ModelForm):
        
    class Meta:
        model = RecomendacionFinal
        fields = (
            'esteFinal', 
            'norteFinal',
            'cotaFinal',
            'fechaFinal',
        )
        widgets = {
            'fechaFinal': forms.DateTimeInput(attrs={'style': 'text-align:center', 'type': 'date', 'min': "1920-01-01"}),
        }


class FormPerforista(forms.ModelForm):
    
    class Meta: 
        model = Perforistas
        fields = (
            'perforista',
        )

class FormMaterialesSonda(forms.ModelForm):
    
    class Meta: 
        model = MaterialesSonda
        fields = (
            'material',
        )

class FormMaterialesCaseta(forms.ModelForm):
    
    class Meta: 
        model = MaterialesCaseta
        fields = (
            'material',
        )

class FormCampana(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        faena_actual = kwargs.pop('faena_actual', "")
        super(FormCampana, self).__init__(*args, **kwargs)
        campos = 'faena'
        orden = campos.split(',')
        self.fields['faena'].queryset = get_filtered_queryset(Faena,faena_actual,orden).exclude(faena="SIN ASIGNAR")
    class Meta: 
        model = Campana
        fields = (
            'campana',
            'faena',
            'metros',
            'anoInicial',
            'anoFinal',
        ) 
        widgets = {
            'marca': forms.TextInput(attrs={'class':'textinput form-control' }),
            'anoInicial': forms.NumberInput(attrs={'class':'textinput form-control' }),
            'anoFinal': forms.NumberInput(attrs={'class':'textinput form-control' }),
            
        }
    
class FormPrograma(forms.ModelForm):
    # Definimos explícitamente el campo usando la clase personalizada
    campana = CampanaChoiceField(
        queryset=Campana.objects.none(),  # Se llena en el __init__
        widget=forms.Select(attrs={'style': 'text-align:center'}),
        label="Campaña"
    )

    def __init__(self, *args, **kwargs):
        campana_actual = kwargs.pop('campana_actual', "")
        super(FormPrograma, self).__init__(*args, **kwargs)
        campos = 'campana'
        orden = campos.split(',')
        self.fields['campana'].queryset = get_filtered_queryset(Campana, campana_actual, orden)
        
    class Meta: 
        model = Programa
        fields = (
            'campana',
            'programa',
            'metros',
        ) 
        widgets = {
            #  'campana': ... (Ya no es necesario definirlo aquí porque lo definimos en la clase personalizada)
            'programa': forms.TextInput(attrs={'class':'textinput form-control' }),
            'metros': forms.NumberInput(attrs={'class':'textinput form-control' }),
        }

class FormProblemaVehiculo(forms.ModelForm):   
    class Meta: 
        model = ProblemaVehiculo
        fields = (
            'problema',                 
        ) 
        widgets = {
            'problema': forms.TextInput(attrs={'class':'textinput form-control' }), 
        }