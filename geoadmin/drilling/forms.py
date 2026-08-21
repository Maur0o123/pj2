from django import forms
from .models import ReportesOperacionales, DetallesPerforaciones, ControlesHorarios, Insumos, DetalleAditivos, LongitudPozos, ObservacionesReportes
from core.models import Perforistas, Sondas, Sondajes
from core.choices import gemelo
from user.models import User
import unicodedata


def _normalizar_nombre_persona(valor):
    texto = " ".join((valor or "").split()).strip()
    if not texto:
        return ""
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(ch for ch in texto if not unicodedata.combining(ch))
    return texto.casefold()

class FormReportesOperacionales(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        disabled_sondaje_codigo = kwargs.pop('disabled_sondaje_codigo', False)
        disabled_reporte_detalle_perforacion = kwargs.pop('disabled_reporte_detalle_perforacion', False)
        super(FormReportesOperacionales, self).__init__(*args, **kwargs)
        self.fields['fechacreacion'].widget.attrs['readonly'] = True
        self.fields['metroInicial'].widget.attrs['readonly'] = True
        self.fields['metroFinal'].widget.attrs['readonly'] = True
        self.fields['totalPerforado'].widget.attrs['readonly'] = True
        self.fields['controlador'].widget.attrs['readonly'] = True
        self.fields['sondajeCodigo'].widget.attrs['readonly'] = disabled_sondaje_codigo
        self.fields['sonda'].widget.attrs['readonly'] = disabled_sondaje_codigo
        self.fields['sondajeSerie'].widget.attrs['readonly'] = disabled_sondaje_codigo
        self.fields['sondajeEstado'].widget.attrs['readonly'] = disabled_sondaje_codigo
        self.fields['turno'].widget.attrs['readonly'] = disabled_sondaje_codigo
        self.fields['sondajeSerie'].label = "N° Sondaje"
        self.fields['sondajeEstado'].label = "Gemelo"
        self.fields['perforista'].required = True
        self.fields['sondajeCodigo'].required = True
        self.fields['sondajeSerie'].required = True
        self.fields['sondajeEstado'].required = False

        self.fields['sondajeEstado'].required = False

        usuarios_perforistas = User.objects.filter(
            role='PERFORISTA',
            is_active=True
        ).only('first_name', 'last_name')

        nombres_unicos = []
        claves_vistas = set()

        for usuario in usuarios_perforistas:
            nombre = " ".join(
                parte.strip()
                for parte in [usuario.first_name or '', usuario.last_name or '']
                if parte and parte.strip()
            )

            clave = _normalizar_nombre_persona(nombre)

            if not clave or clave in claves_vistas:
                continue

            claves_vistas.add(clave)
            nombres_unicos.append((clave, nombre))

        nombres_unicos = []
        claves_vistas = set()
        for usuario in usuarios_perforistas:
            nombre = " ".join(
                parte.strip()
                for parte in [usuario.first_name or '', usuario.last_name or '']
                if parte and parte.strip()
            )
            clave = _normalizar_nombre_persona(nombre)
            if not clave or clave in claves_vistas:
                continue
            claves_vistas.add(clave)
            nombres_unicos.append((clave, nombre))

        if not nombres_unicos:
            self.fields['perforista'].queryset = Perforistas.objects.none()
        else:
            perforistas_activos = list(Perforistas.objects.filter(status=True))
            perforistas_por_clave = {}
            for perforista in perforistas_activos:
                clave = _normalizar_nombre_persona(perforista.perforista)
                if clave and clave not in perforistas_por_clave:
                    perforistas_por_clave[clave] = perforista

            ids_permitidos = []
            for clave, nombre in nombres_unicos:
                perforista = perforistas_por_clave.get(clave)
                if not perforista:
                    perforista = Perforistas.objects.create(
                        perforista=nombre,
                        creador='Sistema',
                        status=True,
                    )
                    perforistas_por_clave[clave] = perforista
                ids_permitidos.append(perforista.id)

            self.fields['perforista'].queryset = Perforistas.objects.filter(
                status=True,
                id__in=ids_permitidos
            ).order_by('perforista')

        self.fields['sonda'].queryset = Sondas.objects.filter(status=True)
        self.fields['sondajeCodigo'].queryset = Sondajes.objects.filter(status=True)
        
    class Meta: 
        model = ReportesOperacionales
        fields = (
            'fechacreacion',
            'perforista',
            'metroInicial',
            'turno',
            'sonda',
            'metroFinal',
            'controlador',
            'sondajeCodigo',
            'sondajeSerie',
            'sondajeEstado',
            'totalPerforado',
        )
        widgets = {
            'fechacreacion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class':'form-control'}),
            'perforista': forms.Select(attrs={'class':'form-control'}),
            'metroInicial': forms.NumberInput(attrs={'class':'form-control'}),
            'turno': forms.Select(attrs={'class':'form-control'}),
            'sonda': forms.Select(attrs={'class':'form-control'}),
            'metroFinal': forms.NumberInput(attrs={'class':'form-control'}),
            'controlador': forms.TextInput(attrs={'type':'text', 'class':'form-control'}),
            'sondajeCodigo': forms.Select(attrs={'class':'form-control new-td'}),
            'sondajeSerie': forms.NumberInput(attrs={'class':'form-control new-td', 'min':3940, 'max':4400, 'style':'height: 2.375rem;'}),
            'sondajeEstado': forms.Select(attrs={'class':'form-control'}),
            'totalPerforado': forms.NumberInput(attrs={'class':'form-control'}),

        }

class FormDetallesPerforaciones(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormDetallesPerforaciones, self).__init__(*args, **kwargs)
        self.fields['desde'].widget.attrs['readonly'] = True
        self.fields['hasta'].widget.attrs['readonly'] = True
        self.fields['porcentajeRecuperacion'].widget.attrs['readonly'] = True
        
    class Meta: 
        model = DetallesPerforaciones
        fields = '__all__'

class FormControlesHorarios(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormControlesHorarios, self).__init__(*args, **kwargs)
        self.fields['total'].widget.attrs['readonly'] = True

    class Meta:
        model = ControlesHorarios
        fields = (
            'inicio',
            'final',
            'total',
            'detalleControlHorario',
        )
        widgets = {
            'inicio': forms.TextInput(attrs={'class': 'tempus-dominus', 'autocomplete': 'off'}),
            'final': forms.TextInput(attrs={'class': 'tempus-dominus', 'autocomplete': 'off'}),
        }

class FormInsumos(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormInsumos, self).__init__(*args, **kwargs)
        self.fields['corona'].required = False
        self.fields['escareador'].required = False
        self.fields['cantidadAgua'].required = False
        self.fields['casing'].required = False
        self.fields['zapata'].required = False
        self.fields['casing'].label = "Casing (mts)"
    
    class Meta: 
        model = Insumos
        fields = (
            'corona',
            'escareador',
            'cantidadAgua',
            'casing',
            'zapata',
        )
        widgets = {
            'casing': forms.NumberInput(attrs={'class':'form-control'}),

        }

class FormAditivos(forms.ModelForm):   
    class Meta: 
        model = DetalleAditivos
        fields = (
            'aditivo',
            'cantidad',
        )
        widgets = {
            'aditivo': forms.Select(attrs={'class':'form-control', 'autocomplete':"off"}),
            'cantidad': forms.NumberInput(attrs={'class':'form-control', 'autocomplete':"off"}),
        }

class FormLongitudPozos(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormLongitudPozos, self).__init__(*args, **kwargs)
        self.fields['restoBarra'].widget.attrs['readonly'] = True
        self.fields['numeroBarras'].widget.attrs['readonly'] = True
        self.fields['longitudPozo'].widget.attrs['readonly'] = True
        self.fields['largoBarril'].required = False
        #self.fields['largoBarra'].required = False
        self.fields['puntoMuerto'].required = False
        self.fields['restoBarra'].required = False
        self.fields['numeroBarras'].required = False
        self.fields['longitudPozo'].required = False
        self.fields['htaEnPozo'].required = True
        self.fields['htaEnPozo'].label = "Queda Hta. en el Pozo"
        self.fields['mtsDeHta'].label = "Metros de Hta"
        self.fields['profundidadHta'].label = "Profundidad a la que queda (mts)"
        
    class Meta: 
        model = LongitudPozos
        fields = (
            'largoBarril',
            #'largoBarra',
            'puntoMuerto',
            'restoBarra',
            'numeroBarras',
            'longitudPozo',
            'htaEnPozo',
            'mtsDeHta',
            'profundidadHta',
        )
        widgets = {
            'largoBarril': forms.NumberInput(attrs={'min': 2.0, 'max': 5.5}),
            'puntoMuerto': forms.NumberInput(attrs={'min': 0.1, 'max': 5.0}),
            'htaEnPozo': forms.Select(attrs={'class':'form-control'}),
            'mtsDeHta': forms.NumberInput(attrs={'min': 0.0}),
            'profundidadHta': forms.NumberInput(attrs={'min': 0.0}),
            #'largoBarra': forms.NumberInput(attrs={'min': 0.0, 'max': 9.0}),
        }


class FormObservacionesReportes(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormObservacionesReportes, self).__init__(*args, **kwargs)
        self.fields['observaciones'].label = ""
        self.fields['observaciones'].required = False
        
    class Meta: 
        model = ObservacionesReportes
        fields = (
            'observaciones',
        )
# Formulario para exportar datos
class ExportDataForm(forms.Form):
    fecha_inicio = forms.DateTimeField(
        label='Fecha Inicial',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=True
    )
    fecha_final = forms.DateTimeField(
        label='Fecha Final',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        required=True
    )
