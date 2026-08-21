from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from user.models import User, UsuarioProfile, LicenciasUsuario, Usuario, DocumentacionUsuario, UserInformacionLaboral
from core.models import Ciudad, Nacionalidad, Genero, Faena
from prevencion.models import VigilanciaArea, VigilanciaGes, VigilanciaCargo, VigilanciaTipoContrato, VigilanciaContrato
from django.utils import timezone
#from core.utils import get_filtered_queryset
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        "inactive": "Tu cuenta está pendiente de aprobación. Un administrador debe habilitarla primero.",
    }
    def clean(self):
        username = self.data.get("username")
        password = self.data.get("password")
        if username and password:
            UserModel = get_user_model()
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                user = None
            #credenciales correctas pero usuario inactivo:
            if user and user.check_password(password) and not user.is_active:
                raise ValidationError(self.error_messages["inactive"], code="inactive")
        return super().clean()

def get_filtered_queryset(model, objeto_actual,orden):
    objetos_con_estado = model.objects.filter(status=True)
    if objeto_actual.exists():
        for objeto in objeto_actual:
            if not objeto.status:
                objetos_incluyendo_nuevo = objetos_con_estado | model.objects.filter(pk=objeto.pk)
            else:
                objetos_incluyendo_nuevo = objetos_con_estado
        return objetos_incluyendo_nuevo.order_by(*orden)
    else:
        return objetos_con_estado.order_by(*orden)

class FormRegistro(UserCreationForm):    
    def __init__(self, *args, **kwargs):
        ocultar_password = kwargs.pop('ocultar_password', False)
        ocultar_role = kwargs.pop('ocultar_role', True)
        username_disabled = kwargs.pop('username_disabled', False)
        first_name_disabled = kwargs.pop('first_name_disabled', False)
        last_name_disabled = kwargs.pop('last_name_disabled', False)
        phone_disabled = kwargs.pop('phone_disabled', False)
        email_disabled = kwargs.pop('email_disabled', False)
        role_disabled = kwargs.pop('role_disabled', True)
        super(FormRegistro, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Rut (Usuario)"
        self.fields['first_name'].label = "Nombres"
        self.fields['phone'].label = "Numero Celular"
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].disabled = username_disabled
        self.fields['first_name'].disabled = first_name_disabled
        self.fields['last_name'].disabled = last_name_disabled
        self.fields['phone'].disabled = phone_disabled
        self.fields['email'].disabled = email_disabled
        self.fields['role'].disabled = role_disabled
        self.fields['role'].initial = Usuario.base_role
        if ocultar_role:
            self.fields['role'].widget = forms.HiddenInput()
        if ocultar_password:
            self.fields['password1'].widget = forms.HiddenInput()
            self.fields['password2'].widget = forms.HiddenInput()
    
    class Meta: 
        model = Usuario
        model._meta.get_field('email')._unique = True
        model._meta.get_field('phone')._unique = True
        fields = (
            'username',                
            'password1',
            'password2',             
            'first_name',
            'last_name',              
            'phone',    
            'email',    
            'role',                  
        )
        widgets = {
            'username': forms.TextInput(attrs={'type':'text', 'placeholder':'Sin puntos ni guión', 'class':'inputs', 'name':'username', 'id':'id_username', 'maxlength':'12', 'onkeyup':'formatUsuario(this)'}),
            'email': forms.EmailInput(attrs={'placeholder':'ejemplo@gmail.com'}),
            'phone': forms.TextInput(attrs={'min':100000000, 'max':999999999, 'type':'Number', 'placeholder':'9XXXXXXXX', 'maxlength':'9', 'onkeyup':'formatTelefono(this)'}),
            'password1': forms.PasswordInput(attrs={'placeholder':'Min. 8 caracteres'}),            
        }

class FormRegistroExtra(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        ciudad_disabled = kwargs.pop('ciudad_disabled', False)
        nacionalidad_disabled = kwargs.pop('nacionalidad_disabled', False)
        genero_disabled = kwargs.pop('genero_disabled', False)
        fechanacimiento_disabled = kwargs.pop('fechanacimiento_disabled', False)
        fechacedulavencimiento_disabled = kwargs.pop('fechacedulavencimiento_disabled', False)
        faena_disabled = kwargs.pop('faena_disabled', False)
        ciudad_actual = kwargs.pop('ciudad_actual', "")
        nacionalidad_actual = kwargs.pop('nacionalidad_actual', "")
        genero_actual = kwargs.pop('genero_actual', "")
        faena_actual = kwargs.pop('faena_actual', "")
        super(FormRegistroExtra, self).__init__(*args, **kwargs)
        self.fields['ciudad'].required = False
        self.fields['nacionalidad'].required = False
        self.fields['genero'].required = False
        self.fields['fechaNacimiento'].required = False
        self.fields['fechaCedulaVencimiento'].required = False
        self.fields['faena'].required = True
        self.fields['ciudad'].disabled = ciudad_disabled
        self.fields['nacionalidad'].disabled = nacionalidad_disabled
        self.fields['genero'].disabled = genero_disabled
        self.fields['fechaNacimiento'].disabled = fechanacimiento_disabled
        self.fields['fechaCedulaVencimiento'].disabled = fechacedulavencimiento_disabled
        self.fields['faena'].disabled = faena_disabled
        campos_ciudad = 'ciudad'
        orden_ciudad = campos_ciudad.split(',')
        self.fields['ciudad'].queryset = get_filtered_queryset(Ciudad,ciudad_actual, orden_ciudad)
        campos_nacionalidad = 'nacionalidad'
        orden_nacionalidad = campos_nacionalidad.split(',')
        self.fields['nacionalidad'].queryset = get_filtered_queryset(Nacionalidad,nacionalidad_actual,orden_nacionalidad)
        campos_genero = 'genero'
        orden_genero = campos_genero.split(',')
        self.fields['genero'].queryset = get_filtered_queryset(Genero,genero_actual, orden_genero)
        campos_faena = 'faena'
        orden_faena = campos_faena.split(',')
        self.fields['faena'].queryset = get_filtered_queryset(Faena,faena_actual,orden_faena)
    
    class Meta: 
        model = UsuarioProfile
        fields = (         
            'ciudad',
            'nacionalidad', 
            'genero',         
            'fechaNacimiento',
            'fechaCedulaVencimiento',
            'faena',
        )
        widgets = {
            'ciudad': forms.Select(attrs={'style': 'text-align:center'}),
            'nacionalidad': forms.Select(attrs={'style': 'text-align:center'}),
            'genero': forms.Select(attrs={'style': 'text-align:center'}),
            'faena': forms.Select(attrs={'style': 'text-align:center'}),
            'fechaNacimiento': forms.DateTimeInput(attrs={'class':'datetimeinput form-control','style': 'text-align:center','type':'date', 'min':"1920-01-01"}),   
            'fechaCedulaVencimiento': forms.DateTimeInput(attrs={'class':'datetimeinput form-control','style': 'text-align:center','type':'date', 'min':"1920-01-01"}),           
        }

class FormRegistroSeccion(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        seccionVehicular = kwargs.pop('seccionVehicular_disabled', False)
        seccionSondaje = kwargs.pop('seccionSondaje_disabled', False)
        seccionPrevencion = kwargs.pop('seccionPrevencion_disabled', False)
        seccionInventario = kwargs.pop('seccionInventario_disabled', False)
        seccionAdministracion = kwargs.pop('seccionAdministracion_disabled', False)
        super(FormRegistroSeccion, self).__init__(*args, **kwargs)
        
        self.fields['seccionVehicular'].label = "Registro Vehicular"
        self.fields['seccionSondaje'].label = "Sondaje"
        self.fields['seccionPrevencion'].label = "Prevención de Riesgos"
        self.fields['seccionInventario'].label = "Inventario"
        self.fields['seccionAdministracion'].label = "Administración"
        
        for campo in ('seccionVehicular', 'seccionSondaje', 'seccionPrevencion', 'seccionInventario', 'seccionAdministracion'):
            self.fields[campo].required = False 
            
            self.fields[campo].widget.attrs.update({
                'class': 'form-control form-control-sm',
                'style': 'width: 100%;',
            })
           
            if hasattr(self.fields[campo], 'choices'):
                choices = [(k, v) for k, v in self.fields[campo].choices if k != '']
                
                if campo == 'seccionVehicular':
                    choices = [(k, v) for k, v in choices if k not in ['PERFORISTA', 'CONTROLADOR', 'PREVENCIONISTA']]
                
                if campo == 'seccionSondaje':
                    choices = [(k, v) for k, v in choices if k != 'PREVENCIONISTA']
                
                if campo == 'seccionPrevencion':
                    choices = [(k, v) for k, v in choices if k not in ['JEFE MANTENCION', 'CONTROLADOR', 'PERFORISTA']]
                
                if campo in ['seccionInventario', 'seccionAdministracion']:
                    choices = [(k, v) for k, v in choices if k in ['ADMINISTRADOR', 'BASE DATOS', 'SIN ASIGNAR']]
                
                self.fields[campo].choices = choices
      
            if not self.initial.get(campo):
                self.initial[campo] = 'SIN ASIGNAR'

        self.fields['seccionVehicular'].disabled = seccionVehicular
        self.fields['seccionSondaje'].disabled = seccionSondaje
        self.fields['seccionPrevencion'].disabled = seccionPrevencion
        self.fields['seccionInventario'].disabled = seccionInventario
        self.fields['seccionAdministracion'].disabled = seccionAdministracion
        
    class Meta:
        model = UsuarioProfile
        fields = (
            'seccionVehicular',
            'seccionSondaje',
            'seccionPrevencion',
            'seccionInventario',
            'seccionAdministracion',
        )
    
class FormRegistroInformacionLaboral(forms.ModelForm):
    # Formulario de la nueva tabla user_informacion_laboral.
    # Sus combos se alimentan desde los mantenedores de Prevención > Vigilancia.
    def __init__(self, *args, **kwargs):
        area_disabled = kwargs.pop('area_disabled', False)
        ges_disabled = kwargs.pop('ges_disabled', False)
        cargo_disabled = kwargs.pop('cargo_disabled', False)
        tipo_contrato_disabled = kwargs.pop('tipo_contrato_disabled', False)
        contrato_disabled = kwargs.pop('contrato_disabled', False)
        fecha_ingreso_disabled = kwargs.pop('fecha_ingreso_disabled', False)
        fecha_desvinculacion_disabled = kwargs.pop('fecha_desvinculacion_disabled', False)
        area_actual = kwargs.pop('area_actual', None)
        ges_actual = kwargs.pop('ges_actual', None)
        cargo_actual = kwargs.pop('cargo_actual', None)
        tipo_contrato_actual = kwargs.pop('tipo_contrato_actual', None)
        contrato_actual = kwargs.pop('contrato_actual', None)
        super(FormRegistroInformacionLaboral, self).__init__(*args, **kwargs)

        self.fields['area'].required = False
        self.fields['ges'].required = False
        self.fields['cargo'].required = False
        self.fields['tipo_contrato'].required = False
        self.fields['contrato'].required = False
        self.fields['fechaIngreso'].required = False
        self.fields['fechaDesvinculacion'].required = False

        self.fields['area'].disabled = area_disabled
        self.fields['ges'].disabled = ges_disabled
        self.fields['cargo'].disabled = cargo_disabled
        self.fields['tipo_contrato'].disabled = tipo_contrato_disabled
        self.fields['contrato'].disabled = contrato_disabled
        self.fields['fechaIngreso'].disabled = fecha_ingreso_disabled
        self.fields['fechaDesvinculacion'].disabled = fecha_desvinculacion_disabled

        self.fields['area'].queryset = get_filtered_queryset(VigilanciaArea, area_actual, ['correlativo', 'id'])
        self.fields['ges'].queryset = get_filtered_queryset(VigilanciaGes, ges_actual, ['correlativo', 'id'])
        self.fields['cargo'].queryset = get_filtered_queryset(VigilanciaCargo, cargo_actual, ['correlativo', 'id'])
        self.fields['tipo_contrato'].queryset = get_filtered_queryset(
            VigilanciaTipoContrato,
            tipo_contrato_actual,
            ['correlativo', 'id']
        )
        self.fields['contrato'].queryset = get_filtered_queryset(
            VigilanciaContrato,
            contrato_actual,
            ['correlativo', 'id']
        )

    class Meta:
        model = UserInformacionLaboral
        fields = (
            'area',
            'ges',
            'cargo',
            'tipo_contrato',
            'contrato',
            'fechaIngreso',
            'fechaDesvinculacion',
        )
        widgets = {
            'area': forms.Select(attrs={'style': 'text-align:center'}),
            'ges': forms.Select(attrs={'style': 'text-align:center'}),
            'cargo': forms.Select(attrs={'style': 'text-align:center'}),
            'tipo_contrato': forms.Select(attrs={'style': 'text-align:center'}),
            'contrato': forms.Select(attrs={'style': 'text-align:center'}),
            'fechaIngreso': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fechaDesvinculacion': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }


class FormRegistroLicenciasUsuarioFecha(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        fechalicenciavencimiento_disabled = kwargs.pop('fechalicenciavencimiento_disabled', False)
        fechalicenciainternavencimiento_disabled = kwargs.pop('fechalicenciainternavencimiento_disabled', False)
        super(FormRegistroLicenciasUsuarioFecha, self).__init__(*args, **kwargs)
        self.fields['fechaLicenciaVencimiento'].label = "Licencia (Vencimiento)"
        self.fields['fechaLicenciaInternaVencimiento'].label = "Licencia Interna (Vencimiento)"
        self.fields['fechaLicenciaVencimiento'].required = False
        self.fields['fechaLicenciaInternaVencimiento'].required = False
        self.fields['fechaLicenciaVencimiento'].disabled = fechalicenciavencimiento_disabled
        self.fields['fechaLicenciaInternaVencimiento'].disabled = fechalicenciainternavencimiento_disabled
    
    class Meta: 
        model = LicenciasUsuario
        fields = (
            'fechaLicenciaVencimiento',
            'fechaLicenciaInternaVencimiento',    
        ) 
        widgets = {
            'fechaLicenciaVencimiento': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
            'fechaLicenciaInternaVencimiento': forms.DateTimeInput(attrs={'style': 'text-align:center','type':'date', 'min':"1920-01-01"}),
        }
        
class FormRegistroLicenciasUsuarioNoProfesionales(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        licenciaclaseb_disabled= kwargs.pop('licenciaclaseb_disabled', False)
        licenciaclasec_disabled= kwargs.pop('licenciaclasec_disabled', False)
        licenciaclased_disabled= kwargs.pop('licenciaclased_disabled', False)
        licenciaclasee_disabled= kwargs.pop('licenciaclasee_disabled', False)
        licenciaclasef_disabled= kwargs.pop('licenciaclasef_disabled', False)        
        super(FormRegistroLicenciasUsuarioNoProfesionales, self).__init__(*args, **kwargs)
        self.fields['licenciaClaseB'].required = False       
        self.fields['licenciaClaseC'].required = False    
        self.fields['licenciaClaseD'].required = False 
        self.fields['licenciaClaseE'].required = False
        self.fields['licenciaClaseF'].required = False 
        self.fields['licenciaClaseB'].disabled = licenciaclaseb_disabled 
        self.fields['licenciaClaseC'].disabled = licenciaclasec_disabled
        self.fields['licenciaClaseD'].disabled = licenciaclased_disabled
        self.fields['licenciaClaseE'].disabled = licenciaclasee_disabled
        self.fields['licenciaClaseF'].disabled = licenciaclasef_disabled
    
    class Meta: 
        model = LicenciasUsuario
        fields = (          
            'licenciaClaseB',                    
            'licenciaClaseC',     
            'licenciaClaseD',     
            'licenciaClaseE',     
            'licenciaClaseF',     
        ) 
        widgets = {
        }
        
class FormRegistroLicenciasUsuarioProfesionales(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        licenciaclasea1_disabled= kwargs.pop('licenciaclasea1_disabled', False)
        licenciaclasea2_disabled= kwargs.pop('licenciaclasea2_disabled', False)
        licenciaclasea3_disabled= kwargs.pop('licenciaclasea3_disabled', False)
        licenciaclasea4_disabled= kwargs.pop('licenciaclasea4_disabled', False)
        licenciaclasea5_disabled= kwargs.pop('licenciaclasea5_disabled', False)
        super(FormRegistroLicenciasUsuarioProfesionales, self).__init__(*args, **kwargs)
        self.fields['licenciaClaseA1'].required = False
        self.fields['licenciaClaseA2'].required = False
        self.fields['licenciaClaseA3'].required = False
        self.fields['licenciaClaseA4'].required = False
        self.fields['licenciaClaseA5'].required = False
        self.fields['licenciaClaseA1'].disabled = licenciaclasea1_disabled 
        self.fields['licenciaClaseA2'].disabled = licenciaclasea2_disabled
        self.fields['licenciaClaseA3'].disabled = licenciaclasea3_disabled
        self.fields['licenciaClaseA4'].disabled = licenciaclasea4_disabled
        self.fields['licenciaClaseA5'].disabled = licenciaclasea5_disabled
    
    class Meta: 
        model = LicenciasUsuario
        fields = (            
            'licenciaClaseA1',                    
            'licenciaClaseA2',  
            'licenciaClaseA3', 
            'licenciaClaseA4', 
            'licenciaClaseA5', 
        ) 
        widgets = {
        }

class FormRegistroLicenciasUsuarioProfesionalesAntiguas(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        licenciaclasea1antigua_disabled= kwargs.pop('licenciaclasea1antigua_disabled', False)
        licenciaclasea2antigua_disabled= kwargs.pop('licenciaclasea2antigua_disabled', False)
        super(FormRegistroLicenciasUsuarioProfesionalesAntiguas, self).__init__(*args, **kwargs)
        self.fields['licenciaClaseA1Antigua'].required = False
        self.fields['licenciaClaseA2Antigua'].required = False
        self.fields['licenciaClaseA1Antigua'].disabled = licenciaclasea1antigua_disabled 
        self.fields['licenciaClaseA2Antigua'].disabled = licenciaclasea2antigua_disabled
    
    class Meta: 
        model = LicenciasUsuario
        fields = (        
            'licenciaClaseA1Antigua',
            'licenciaClaseA2Antigua',
        ) 
        widgets = {
        }

class FormDocumentacionUsuario(forms.ModelForm):    

    class Meta: 
        model = DocumentacionUsuario
        fields = (        
            'fotografiaUsuario',
            'fotografiaCedula',
            'fotografiaLicencia',
            'fotografiaLicenciaInterna',
        ) 
        widgets = {
        }
