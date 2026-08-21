from django.db import models
from django.utils import timezone
from core.models import Faena, Tipo, Campana, Programa
from vehicle.models import Vehiculo
from core.choices import meses
from administration.managers import AuditableQuerySet

class PlanificacionFaenas(models.Model):
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    mes = models.CharField(max_length=15,choices=meses,null=True,blank=True,verbose_name='Meses')
    cantidad = models.IntegerField(null=True,blank=True,verbose_name='Valor')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()

    def __str__(self) :
        return "{} {}".format(self.faena, self.tipo)
    class Meta:
        verbose_name = 'Planificación por Faena y Tipo de Vehículo'
        verbose_name_plural = 'Planificación por Faena y Tipo de Vehículos'
        db_table = 'planning_minning_type' 

class PlanificacionCampanas(models.Model):
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE,verbose_name='Campañas')
    mes = models.CharField(max_length=15,choices=meses,null=True,blank=True,verbose_name='Meses')
    plan = models.IntegerField(null=True,blank=True,verbose_name='Plan')
    realMensual = models.IntegerField(null=True,blank=True,verbose_name='Real Mensual')
    acumuladoPlan = models.IntegerField(null=True,blank=True,verbose_name='Acumulado Plan')
    acumuladoReal = models.IntegerField(null=True,blank=True,verbose_name='Acumulado Real')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()

    def __str__(self) :
        return "{} {}".format(self.campana, self.tipo)
    class Meta:
        verbose_name = 'Planificación de Campaña'
        verbose_name_plural = 'Planificación de Campañas'
        db_table = 'planning_drilling' 

class PlanificacionPrograma(models.Model):
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, verbose_name='Campañas')
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, verbose_name='Programas')
    mes = models.CharField(max_length=15, choices=meses, null=True, blank=True, verbose_name='Meses')
    ano = models.IntegerField(null=True, blank=True, verbose_name='Año')
    plan = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Plan')
    realMensual = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Real Mensual')
    acumuladoPlan = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Acumulado Plan')
    acumuladoReal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Acumulado Real')
    fechacreacion = models.DateTimeField(null=False, default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{} {}".format(self.programa, self.plan)

    class Meta:
        verbose_name = 'Planificación de Programa'
        verbose_name_plural = 'Planificación de Programas'
        db_table = 'planning_drilling_program'