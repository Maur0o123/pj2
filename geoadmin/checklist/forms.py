from django import forms
from core.choices import jornada, turno, gemelo
from django.utils import timezone
from core.models import Sondas, Sondajes

class ChecklistMaterialesSondaEntradaForm(forms.Form):
    fecha_checklist_entrada = forms.DateTimeField(
        label="Fecha Checklist",
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    turno_entrada = forms.ChoiceField(choices=turno, label="Turno", widget=forms.Select(attrs={'class': 'form-control'}))
    jornada_entrada = forms.ChoiceField(choices=jornada, label="Jornada", initial='1', disabled=True, widget=forms.Select(attrs={'class': 'form-control'})) #forzamos siempre salida (1) y deshabilitamos el choice
    sonda_entrada = forms.ModelChoiceField(queryset=Sondas.objects.filter(status=True), label="Sonda", widget=forms.Select(attrs={'class': 'form-control'}))
    sondaje_entrada = forms.ModelChoiceField(queryset=Sondajes.objects.filter(status=True), label="Sondaje", widget=forms.Select(attrs={'class': 'form-control'}))
    serie_entrada = forms.CharField(
        label="N° Sondaje",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'height: 2.375rem;'})
    )
    estado_entrada = forms.ChoiceField(choices=[('', '---------')] + list(gemelo), label="Gemelo", widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    
    def __init__(self, *args, **kwargs):
        modo_edicion = kwargs.pop('modo_edicion', False) #modo edicion false por defecto para "crear nuevo reporte"
        super().__init__(*args, **kwargs)

        if modo_edicion: #solo si modo edicion es true
            for nombre in ['turno_entrada', 'sonda_entrada', 'sondaje_entrada', 'serie_entrada', 'estado_entrada']:
                if nombre in self.fields:
                    self.fields[nombre].disabled = True

class ChecklistMaterialesSondaSalidaForm(forms.Form):
    fecha_checklist_salida = forms.DateTimeField(
        label="Fecha Checklist",
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    turno_salida = forms.ChoiceField(choices=turno, label="Turno", widget=forms.Select(attrs={'class': 'form-control'}))
    jornada_salida = forms.ChoiceField(choices=jornada, label="Jornada", initial='2', disabled=True, widget=forms.Select(attrs={'class': 'form-control'})) #forzamos siempre salida (2) y deshabilitamos el choice
    sonda_salida = forms.ModelChoiceField(queryset=Sondas.objects.filter(status=True), label="Sonda", widget=forms.Select(attrs={'class': 'form-control'}))
    sondaje_salida = forms.ModelChoiceField(queryset=Sondajes.objects.filter(status=True), label="Sondaje", widget=forms.Select(attrs={'class': 'form-control'}))
    serie_salida = forms.CharField(
        label="N° Sondaje",
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'height: 2.375rem;'})
    )
    estado_salida = forms.ChoiceField(choices=[('', '---------')] + list(gemelo), label="Gemelo", widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    
    def __init__(self, *args, **kwargs):
        modo_edicion = kwargs.pop('modo_edicion', False)
        super().__init__(*args, **kwargs)

        if modo_edicion:
            for nombre in ['turno_salida', 'sonda_salida', 'sondaje_salida', 'serie_salida', 'estado_salida']:
                if nombre in self.fields:
                    self.fields[nombre].widget.attrs['readonly'] = 'readonly'
    
class ChecklistMaterialesCasetaFormTop(forms.Form):
    fecha_checklist = forms.DateTimeField(
        label="Fecha Checklist",
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    turno = forms.ChoiceField(choices=turno, label="Turno", widget=forms.Select(attrs={'class': 'form-control'}))
    responsable = forms.CharField(label="Responsable", widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}))
    cargo = forms.CharField(label="Cargo", widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}))
    


class ChecklistMaterialesCasetaFormBottom(forms.Form):
    fecha_revision = forms.DateTimeField(
        label="Fecha Revisión",
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={'readonly': 'readonly', 'class': 'form-control'})
    )
    supervisor = forms.CharField(label="Supervisor", widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control'}))
    observaciones = forms.CharField(label="Observaciones", required=False, widget=forms.Textarea(attrs={'class': 'form-control',  'cols': '40', 'rows': '5'}))
