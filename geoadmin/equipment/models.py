from django.db import models
from django.utils import timezone
from core.models import Faena
from administration.managers import AuditableQuerySet

class TipoEquipo(models.Model):
    tipo = models.CharField(max_length=50,unique=True,verbose_name='Tipo Equipo')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self):
        return "{}".format(self.tipo)
    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        db_table = 'equipment_type'
        
class MarcaEquipo(models.Model):
    tipo = models.ForeignKey(TipoEquipo, on_delete=models.CASCADE, null=True)
    marca = models.CharField(max_length=50,verbose_name='Marca - Modelo')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self):
        return "{}".format(self.marca)
    class Meta:
        verbose_name = 'Marca o Modelo'
        verbose_name_plural = 'Marca o Modelos'
        db_table = 'equipment_brand-model'

class NuevoEquipamiento(models.Model):
    tipo = models.ForeignKey(TipoEquipo, on_delete=models.CASCADE, null=True)
    marca = models.ForeignKey(MarcaEquipo, on_delete=models.CASCADE, null=True)
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, null=True)
    area = models.CharField(max_length=50,verbose_name='Área / Ubicación')
    ultimaMantencion = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha última mantención')
    frecuencia = models.IntegerField(null=True, verbose_name='Frecuencia Mantención (Meses)')
    proximaMantencion = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha próxima mantención')
    notasAdicionales = models.CharField(max_length=500,null=True,blank=True,verbose_name='Notas Adicionales')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self):
        return "{}".format(self.area)
    class Meta:
        verbose_name = 'Nuevo Equipo'
        verbose_name_plural = 'Nuevos Equipos'
        db_table = 'equipment_new_equipment'