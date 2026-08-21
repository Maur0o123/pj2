from django import forms

class FormVigilanciaOpcion(forms.Form):
    valor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'textinput form-control'})
    )


# Formulario para seleccionar rango de fechas en la exportación de Prevención.
class ExportDataPrevencionForm(forms.Form):
    fecha_inicio = forms.DateField(
        label='Fecha Inicial',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    fecha_final = forms.DateField(
        label='Fecha Final',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
