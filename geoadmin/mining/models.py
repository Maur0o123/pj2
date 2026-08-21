import os
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime
from core.models import Tipo, Ano, Marca, Modelo, Color, Faena
from core.choices import tipotraccion, cantidadpuertas
from vehicle.models import Vehiculo
from administration.managers import AuditableQuerySet

class VehiculoAsignado(models.Model):
    vehiculo = models.ForeignKey(Vehiculo,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Vehículo')
    faena = models.ForeignKey(Faena,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Faena Actual')
    faenaAnterior = models.CharField(max_length=50,verbose_name='Faena Anterior',null=True)
    fechaInicial = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha inicial Traspaso')
    fechaFinal = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Final Traspaso')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.vehiculo)
    
    class Meta:
        verbose_name = 'Vehiculo en Faena'
        verbose_name_plural = 'Vehiculos en Faena'
        db_table = 'mining_vehicles'
        
class DocumentoPorFaena(models.Model):
    faena = models.CharField(max_length=100, verbose_name='Faena', null=True)
    patente = models.CharField(max_length=50, verbose_name='Patente', null=True)
    tipoDocumento = models.CharField(max_length=100, verbose_name='Tipo Documento', null=True)
    fechaVencimiento = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Vencimiento')
    creador = models.CharField(max_length=50, verbose_name='Creador', null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False, default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def generaNombre(instance, filename):
        extension = os.path.splitext(filename)[1][1:]
        vehiculo_placaPatente = instance.patente.upper()
        vehiculo_faena = instance.faena.upper()
        ruta = f'documentacion_vehiculo_faena/{vehiculo_placaPatente}/{vehiculo_faena}' 
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S") 
        nombre = "{}.{}".format(fecha, extension)
        return os.path.join(ruta, nombre)

    documento = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png')

    def __str__(self):
        return "{} {}".format(self.faena, self.documento)

    class Meta:
        verbose_name = 'Documento por Faena'
        verbose_name_plural = 'Documentos por Faena'
        db_table = 'mining_documents'