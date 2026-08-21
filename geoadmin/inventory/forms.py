from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Items, SeccionItems , CategoriaItems, DuracionItems,StockItems,StockEgresoItems
from core.models import Tipo, Marca, Modelo, Ano, Color
from core.utils import get_filtered_queryset
from django.contrib.auth.models import User
from user.models import UsuarioProfile
from django.core.exceptions import ValidationError
from mining.models import Faena
class FormSeccionSelect(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        super(FormSeccionSelect, self).__init__(*args, **kwargs)
        self.fields['seccion'].label = "Seccion"
        queryset = SeccionItems.objects.all().order_by('seccion')
        choices = [(seccion.id, seccion.seccion) for seccion in queryset]
        self.fields['seccion'].choices = choices
        self.fields['seccion'].required = True 
        
    class Meta: 
        model = CategoriaItems
        fields = (
            'seccion',                 
        ) 
        widgets = {
            'seccion': forms.Select(attrs={'style': 'text-align:left'}),
        }

class FormCategorySelect(forms.ModelForm):     
    def __init__(self, *args, **kwargs):
        super(FormCategorySelect, self).__init__(*args, **kwargs)
        self.fields['categoria'].label = "Categoria"
        queryset = CategoriaItems.objects.all().order_by('categoria')
        choices = [(categoria.id, categoria.categoria) for categoria in queryset]
        self.fields['categoria'].choices = choices
        self.fields['categoria'].required = True 
        
    class Meta: 
        model = CategoriaItems
        fields = (
            'categoria',                 
        ) 
        widgets = {
            'categoria': forms.Select(attrs={'style': 'text-align:left'}),
        }

class FormNuevoItem(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        seccion_actual = kwargs.pop('seccion_actual', "")
        super(FormNuevoItem, self).__init__(*args, **kwargs)
        self.fields['item'].label = "Nombre del Item"
        self.fields['codigo_item'].label = "Código Item"
        self.fields['duracion'].label = "Meses de Duracion"

        
        # Filtra para que solo salgan las faenas con status=True (habilitadas)
        #---------------------
        self.fields['categoria'].queryset = CategoriaItems.objects.filter(
            status=True
        ).order_by('categoria')
        self.fields['categoria'].required = True
        # self.fields['duracion'].required = True
        self.fields['descripcion'].required = False
        self.fields['valor_neto'].required = False

    class Meta: 
        model = Items
        fields = (
            'categoria',
            'codigo_item',
            'item',
            'marca',
            'duracion',
            'stock_minimo',
            'stock_maximo', 
            'valor_neto',   
            'descripcion',

        )
        widgets = {
            'categoria': forms.Select(attrs={'type':'text'}),
            'item': forms.TextInput(attrs={'style': 'text-align:left'}),
            'descripcion': forms.Textarea(attrs={'class': 'textinput form-control'}),
            'duracion': forms.Select(attrs={'type':'text'}),
            'stock_minimo': forms.TextInput(attrs={'style': 'text-align:left'}),
            'stock_maximo': forms.TextInput(attrs={'style': 'text-align:left'}),
            'valor_neto': forms.TextInput(attrs={'style': 'text-align:left'}),
            'marca': forms.TextInput(attrs={'style': 'text-align:left'}),
        }

class FormNuevaSeccion(forms.ModelForm):    
    def __init__(self, *args, **kwargs):

        super(FormNuevaSeccion, self).__init__(*args, **kwargs)
        self.fields['seccion'].required = True

    class Meta: 
        model = SeccionItems
        model._meta.get_field('id')._unique = True
        fields = (
            'seccion',                     
        )
        widgets = {
            'seccion': forms.TextInput(attrs={'type':'text'}),         
        }

class FormNuevaCategoria(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        kwargs.pop('seccion_actual', None)
        super(FormNuevaCategoria, self).__init__(*args, **kwargs)

        self.fields['categoria'].label = "Categoría del Item"
        self.fields['categoria'].required = True

    class Meta: 
        model = CategoriaItems
        fields = (
            'categoria',
        )

        widgets = {
            'categoria': forms.TextInput(attrs={'type': 'text'}),
        }

class FormNuevaDuracion(forms.ModelForm):    
    def __init__(self, *args, **kwargs):

        super(FormNuevaDuracion, self).__init__(*args, **kwargs)
        self.fields['duracion'].label = "Numero de meses de duracion para un Item"
        self.fields['duracion'].required = True

    class Meta: 
        model = DuracionItems
        model._meta.get_field('id')._unique = True
        fields = (
            'duracion',                     
        )
        widgets = {
            'duracion': forms.NumberInput(attrs={'type': 'number'}),     
        }


class StockItemsForm(forms.ModelForm):
    class Meta:
        model = StockItems
        fields = '__all__' 
        widgets = {
            'faena': forms.TextInput(attrs={'class': 'form-control'}),
            'seccion': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FormInventarioNuevoIngreso(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(FormInventarioNuevoIngreso, self).__init__(*args, **kwargs)

        # Deshabilitar el campos 
        self.fields['faena'].widget.attrs['readonly'] = True
        self.fields['seccion'].widget.attrs['readonly'] = True
        self.fields['categoria'].widget.attrs['readonly'] = True
        self.fields['item'].widget.attrs['readonly'] = True
        self.fields['cantidad_actual'].widget.attrs['readonly'] = True

        # Hacer que los campos no sean obligatorio
        self.fields['item'].required = False
        self.fields['descripcion'].required = False

    class Meta: 
        model = StockItems
        fields = (
            'faena',
            'seccion',
            'categoria', 
            'item',
            'cantidad_actual',
            'cantidad',
            'descripcion',
        )  
        widgets = {
            'faena': forms.TextInput(attrs={'style': 'text-align:left'}),
            'seccion': forms.TextInput(attrs={'style': 'text-align:left'}),
            'categoria': forms.TextInput(attrs={'style': 'text-align:left'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            "cantidad_actual": forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control','min': '1'}),
            'descripcion': forms.Textarea(attrs={'class': 'textinput form-control', 'cols': 40, 'rows': 3}),
        }


class FormInventarioNuevoAjuste(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(FormInventarioNuevoAjuste, self).__init__(*args, **kwargs)
        self.fields['cantidad'].label = "Cantidad Ajuste"
        # Deshabilitar el campos 
        self.fields['faena'].widget.attrs['readonly'] = True
        self.fields['seccion'].widget.attrs['readonly'] = True
        self.fields['categoria'].widget.attrs['readonly'] = True
        self.fields['item'].widget.attrs['readonly'] = True
        self.fields['cantidad_actual'].widget.attrs['readonly'] = True

        # Hacer que los campos no sean obligatorio
        self.fields['item'].required = False
        self.fields['cantidad_actual'].required = False
    class Meta: 
        model = StockItems
        fields = (
            'faena',
            'seccion',
            'categoria', 
            'item',
            'cantidad_actual',
            'cantidad',
            'descripcion',
        )  
        widgets = {
            'faena': forms.TextInput(attrs={'style': 'text-align:left'}),
            'seccion': forms.TextInput(attrs={'style': 'text-align:left'}),
            'categoria': forms.TextInput(attrs={'style': 'text-align:left'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            "cantidad_actual": forms.NumberInput(attrs={'class': 'form-control',}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'textinput form-control', 'cols': 40, 'rows': 3}),
        }

class FormInventarioNuevoEgreso(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(FormInventarioNuevoEgreso, self).__init__(*args, **kwargs)
        self.fields['cantidad'].label = "Cant. Stock Actual"
        self.fields['cantidad_actual'].label = "Cant. a Entregar"
        
        # Deshabilitar los campos
        self.fields['faena'].widget.attrs['readonly'] = True
        self.fields['seccion'].widget.attrs['readonly'] = True
        self.fields['categoria'].widget.attrs['readonly'] = True
        self.fields['item'].widget.attrs['readonly'] = True
        self.fields['cantidad'].widget.attrs['readonly'] = True
        self.fields['rut_receptor'].widget.attrs['readonly'] = True
        self.fields['cargo_receptor'].widget.attrs['readonly'] = True
        self.fields['nombre_receptor'].widget.attrs['readonly'] = True

        # Hacer que algunos campos no sean obligatorios
        self.fields['descripcion'].required = False
        self.fields['item'].required = False
        self.fields['cantidad'].required = False
        self.fields['rut_receptor'].required = False
        self.fields['cargo_receptor'].required = False
        self.fields['nombre_receptor'].required = False

    class Meta: 
        model = StockEgresoItems
        fields = (
            'faena',
            'seccion',
            'categoria', 
            'item',
            'cantidad',
            'cantidad_actual', 
            'rut_receptor',
            'cargo_receptor',
            'nombre_receptor',
            'descripcion',
        )  
        widgets = {
            'faena': forms.TextInput(attrs={'style': 'text-align:left'}),
            'seccion': forms.TextInput(attrs={'style': 'text-align:left'}),
            'categoria': forms.TextInput(attrs={'style': 'text-align:left'}),
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_actual': forms.NumberInput(attrs={'class': 'form-control'}), 
            'rut_receptor': forms.NumberInput(attrs={'class': 'form-control'}),
            'cargo_receptor': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_receptor': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'cols': 40, 'rows': 3}),
        }
