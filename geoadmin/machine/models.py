import os
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime
from core.models import TipoMaquinaria, MarcaMaquinaria, Faena, KitsMaquinaria
from administration.managers import AuditableQuerySet

class Maquinaria(models.Model):
    maquinaria = models.CharField(max_length=50,unique=True,verbose_name='Nombre Maquinaria')
    descripcion = models.CharField(max_length=200,verbose_name='Descripción')
    fechaAdquisicion = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Adquisición')
    tipo = models.ForeignKey(TipoMaquinaria,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Tipo')
    marca = models.ForeignKey(MarcaMaquinaria,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Marca')
    faena = models.ForeignKey(Faena,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Faena')
    frecuenciaMantenimiento = models.IntegerField(null=True,blank=True,verbose_name='Frecuencia Mantenimiento(Horas)')
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()
    
    def generaNombre(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        maquinaria = instance.Maquinaria.maquinaria.upper()
        ruta = f'documentacion_maquinaria/{maquinaria}' 
        fecha =datetime.now().strftime("%Y%m%d_%H%M%S") 
        nombre = "{}.{}".format(fecha,extension)
        return os.path.join(ruta,nombre)           
    fotografia = models.ImageField(upload_to=generaNombre,null=True,blank=True,default='base/no-imagen.png')
    
    def __str__(self):
        return "{}".format(self.maquinaria)
    class Meta:
        verbose_name = 'Maquinaria'
        verbose_name_plural = 'Maquinarias'
        db_table = 'machine_profile'

class MaquinariaFaena(models.Model):
    maquinaria = models.ForeignKey(Maquinaria,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Maquinaria')
    faena = models.ForeignKey(Faena,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Faena')
    status = models.BooleanField(null=True, verbose_name='Estado')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self):
        return "{}".format(self.maquinaria)
    class Meta:
        verbose_name = 'Maquinaria Faena'
        verbose_name_plural = 'Maquinarias Faenas'
        db_table = 'mining_machines'

class NuevoHorometro(models.Model):
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.CASCADE)
    horometro = models.IntegerField(null=True,blank=True,verbose_name='Horómetro Actual')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    origen = models.CharField(max_length=30,null=True,blank=True,verbose_name='Origen')
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self) :
        return "{}".format(self.maquinaria)
    class Meta:
        verbose_name = 'Horómetro Maquinaria'
        verbose_name_plural = 'Horómetros Maquinarias'
        db_table = 'machine_horometres_registers' 
        
class KitsMaquinariaFaena(models.Model):
    kitMaquinaria = models.ForeignKey(KitsMaquinaria, on_delete=models.CASCADE, null=True)
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, null=True)
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self) :
        return "{}".format(self.kitMaquinaria)
    class Meta:
        verbose_name = 'Kit Maquinaria por Faena'
        verbose_name_plural = 'Kits Maquinarias por Faenas'
        db_table = 'machine_kits_machine_mining'
        constraints = [
            models.UniqueConstraint(fields=['faena', 'kitMaquinaria'], name='unique_faena_kitMaquinaria')
        ]
        
class HistorialStockKitsMaquinariaFaena(models.Model):
    kitMaquinaria = models.ForeignKey(KitsMaquinariaFaena, on_delete=models.CASCADE, null=True)
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, null=True)
    stockMovimiento = models.IntegerField(null=True,blank=True,verbose_name='Movimiento') 
    stockActual = models.IntegerField(null=True,blank=True,verbose_name='Stock Actual')
    descripcion = models.CharField(max_length=200,null=True,blank=True,verbose_name='Descripción')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self) :
        return "{}".format(self.kitMaquinaria)
    class Meta:
        verbose_name = 'Historial Stock Kit Maquinaria'
        verbose_name_plural = 'Historial Stock Kits Maquinarias'
        db_table = 'machine_kits_stock_history'