from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from core.choices import turno, gemelo, opcion
from user.models import Usuario
from core.models import (Sondas, Sondajes, Diametros, TipoTerreno, Orientacion, DetalleControlHorario, Perforistas, 
                        CantidadAgua, Aditivos, LargoBarra)
from administration.managers import AuditableQuerySet

class ReportesOperacionales(models.Model):
    turno = models.CharField(max_length=50, choices=turno, verbose_name='Turno')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    fechaedicion = models.DateTimeField(null=True,default=timezone.now)
    controlador = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name='Controlador')
    perforista = models.ForeignKey(Perforistas, on_delete=models.CASCADE, verbose_name='Perforista')
    sonda = models.ForeignKey(Sondas, on_delete=models.CASCADE, null=True, verbose_name='Sonda')
    sondajeCodigo = models.ForeignKey(Sondajes, on_delete=models.CASCADE, null=True, verbose_name='Sondaje')
    sondajeSerie = models.IntegerField(verbose_name="Serie",null=True,validators=[MinValueValidator(3940), MaxValueValidator(4400)] )
    sondajeEstado =  models.CharField(max_length=3, choices=gemelo, verbose_name='Gemelo', null=True, blank=True, default='')
    metroInicial = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Metro Inicial")
    metroFinal = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Metro Final")
    totalPerforado = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Total Perforado")
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    progreso = models.CharField(max_length=50,default='Creado',verbose_name='Progreso',null=True)
    correlativo = models.IntegerField(verbose_name="Correlativo",null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    id_checklist = models.BigIntegerField(null=True, verbose_name='ID Checklist')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{} {} {}".format(self.sonda, self.sondajeCodigo, self.sondajeSerie)
    
    class Meta:
        verbose_name = 'Reporte Digital Operacional'
        verbose_name_plural = 'Reportes Digitales Operacionales'
        db_table = 'drilling_reporte_digital_operacional'
    
class DetallesPerforaciones(models.Model):
    reporte = models.ForeignKey(ReportesOperacionales, on_delete=models.CASCADE)
    diametros = models.ForeignKey(Diametros, on_delete=models.CASCADE, null=True)
    perforado = models.DecimalField(max_digits=5, decimal_places=2)
    desde = models.DecimalField(max_digits=5, decimal_places=2)
    hasta = models.DecimalField(max_digits=5, decimal_places=2)
    recuperacion = models.DecimalField(max_digits=5, decimal_places=2)
    porcentajeRecuperacion = models.DecimalField(max_digits=5, decimal_places=2)
    barra = models.IntegerField()
    largoBarra = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    totalHtas = models.DecimalField(max_digits=5, decimal_places=2)
    contra = models.DecimalField(max_digits=5, decimal_places=2)
    tipoTerreno = models.ForeignKey(TipoTerreno, on_delete=models.CASCADE, null=True)
    orientacion = models.ForeignKey(Orientacion, on_delete=models.CASCADE, null=True)
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    status = models.BooleanField(null=True, verbose_name='Estado')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.reporte)
    
    class Meta:
        verbose_name = 'Reporte Digital Perforación'
        verbose_name_plural = 'Reportes Digitales Perforaciones'
        db_table = 'drilling_reporte_digital_perforaciones'

class ControlesHorarios(models.Model):
    reporte = models.ForeignKey(ReportesOperacionales, on_delete=models.CASCADE)
    posicion = models.IntegerField()
    inicio = models.TimeField(verbose_name="Hora Inicio")
    final = models.TimeField(verbose_name="Hora final")
    total = models.TimeField(verbose_name="Total Horas")
    detalleControlHorario = models.ForeignKey(DetalleControlHorario, on_delete=models.CASCADE, null=True, verbose_name="Detalle Control Horario")
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    status = models.BooleanField(null=True, verbose_name='Estado')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.reporte)
    
    class Meta:
        verbose_name = 'Reporte Digital Control Horario'
        verbose_name_plural = 'Reportes Digitales Control Horario'
        db_table = 'drilling_reporte_digital_control_horario'

class DetalleAditivos(models.Model):
    reporte = models.ForeignKey(ReportesOperacionales, on_delete=models.CASCADE)
    aditivo = models.ForeignKey(Aditivos, on_delete=models.CASCADE, null=True, verbose_name="Aditivos")
    cantidad = models.IntegerField( verbose_name="Cantidad",validators=[MinValueValidator(0), MaxValueValidator(1000)] )
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    status = models.BooleanField(null=True, verbose_name='Estado')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.reporte)
    
    class Meta:
        verbose_name = 'Reporte Digital Aditivo'
        verbose_name_plural = 'Reportes Digitales Aditivos'
        db_table = 'drilling_reporte_digital_aditivos'
        
class Insumos(models.Model):
    reporte = models.ForeignKey(ReportesOperacionales, on_delete=models.CASCADE)
    corona = models.CharField(max_length=50, null=True, verbose_name='Corona')
    escareador = models.CharField(max_length=50, null=True, verbose_name='Escariador')
    cantidadAgua = models.ForeignKey(CantidadAgua, on_delete=models.CASCADE, null=True, verbose_name="Agua (lts)")
    casing = models.CharField(max_length=50, null=True, verbose_name='Casing')
    zapata = models.CharField(max_length=50, null=True, verbose_name='Zapata')
    status = models.BooleanField(null=True, verbose_name='Estado')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.reporte)
    
    class Meta:
        verbose_name = 'Reporte Digital Insumo'
        verbose_name_plural = 'Reportes Digitales Insumos'
        db_table = 'drilling_reporte_digital_insumos'

class LongitudPozos(models.Model):
    reporte = models.ForeignKey(ReportesOperacionales, on_delete=models.CASCADE)
    largoBarril = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Largo del Barril (mts)",validators=[MinValueValidator(2.00), MaxValueValidator(5.50)] )
    largoBarra = models.DecimalField(null=True, max_digits=5, decimal_places=2, verbose_name="Largo Barra (mts)",validators=[MinValueValidator(0.00), MaxValueValidator(9.00)] )
    puntoMuerto = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Punto Muerto (mts)",validators=[MinValueValidator(0.00), MaxValueValidator(5.00)] )
    restoBarra = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Resto de Barra (mts)")
    numeroBarras = models.IntegerField(verbose_name="Numero de Barras")
    longitudPozo = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Longitud Pozo (mts)")
    htaEnPozo = models.CharField(max_length=50, choices=opcion, default='Si', verbose_name='Hta. en el Pozo')
    mtsDeHta = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name="Mts. de Hta.")
    profundidadHta = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name="Profundidad ala que queda (mts)")
    status = models.BooleanField(null=True, verbose_name='Estado')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.reporte)
    
    class Meta:
        verbose_name = 'Reporte Digital Longitud'
        verbose_name_plural = 'Reportes Digitales Longitud'
        db_table = 'drilling_reporte_digital_longitud'
    
class ObservacionesReportes(models.Model):
    reporte = models.ForeignKey(ReportesOperacionales, on_delete=models.CASCADE)
    observaciones = models.TextField(max_length=1000, null=True, verbose_name="Observaciones")
    status = models.BooleanField(null=True, verbose_name='Estado')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.reporte)
    
    class Meta:
        verbose_name = 'Reporte Digital Observacion'
        verbose_name_plural = 'Reportes Digitales Observaciones'
        db_table = 'drilling_reporte_digital_observaciones'


class ParticipantesPerforacion(models.Model):
    reporte = models.ForeignKey(ReportesOperacionales, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Trabajador')
    fechacreacion = models.DateTimeField(null=False, default=timezone.now)
    status = models.BooleanField(null=True, verbose_name='Estado')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"{self.reporte} - {self.trabajador}"

    class Meta:
        verbose_name = 'Participante de Perforación'
        verbose_name_plural = 'Participantes de Perforación'
        db_table = 'drilling_reporte_digital_participantes'

class DocumentosReportesPerforaciones(models.Model):
    reporte = models.CharField(max_length=200, verbose_name='Tipo Reporte')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    archivo = models.FileField(upload_to='reportes_avance/') 
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    status = models.BooleanField(null=True, verbose_name='Estado')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.reporte)
    
    class Meta:
        verbose_name = 'Documento Reporte Perforacion'
        verbose_name_plural = 'Documentos Reportes Perforaciones'
        db_table = 'drilling_documents_report_drilling'