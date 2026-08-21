import os
from django.db import models
from datetime import datetime
from django.utils import timezone
import json
from core.choices import turno, opcion, progreso
from core.models import TipoFallaVehiculo, Faena, EmpresaServicios, FallaMaquinaria
from user.models import Usuario
from machine.models import Maquinaria
from vehicle.models import Vehiculo
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from administration.managers import AuditableQuerySet

class NuevaSolicitudMantenimiento(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name='Nombre Usuario')
    telefono = models.IntegerField(null=True, verbose_name='Telefono')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE,null=True,verbose_name='Patente')
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE,null=True,verbose_name='Faena')
    patente = models.CharField(max_length=50, verbose_name='Patente', null=True)
    kilometraje = models.IntegerField(null=True,blank=True,verbose_name='Kilometraje')
    progreso = models.CharField(max_length=50,choices=progreso,null=True,blank=True, default=1,verbose_name='Progreso Solicitud')
    empresaMantenimiento = models.ForeignKey(EmpresaServicios, on_delete=models.CASCADE,null=True,blank=True,verbose_name='Empresa Servicios')
    turno = models.CharField(max_length=20,choices=turno,null=True,blank=True,verbose_name='Turno')
    problemas = models.ManyToManyField(TipoFallaVehiculo, through='SolicitudMantenimientoProblemas')
    comentario = models.CharField(max_length=1000,null=True,verbose_name='Comentarios Adicionales')
    avisoJefatura =  models.CharField(max_length=20,choices=opcion,null=True,blank=True, verbose_name='Aviso a su Jefatura Directa?')
    status = models.BooleanField(null=True, verbose_name='Estado')    
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def generaNombre(instance, filename):
        extension = os.path.splitext(filename)[1][1:]
        vehiculo_placaPatente = instance.patente.upper()
        solicitud_fecha = instance.fechacreacion.strftime('%Y-%m-%d')
        solicitud_hora = instance.fechacreacion.strftime('%H-%M-%S')
        ruta = f'documentacion_mantenimientos/{vehiculo_placaPatente}/{solicitud_fecha}/{solicitud_hora}' 
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S") 
        nombre = "{}.{}".format(fecha, extension)
        return os.path.join(ruta, nombre)

    fotografiaUno = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='base/no-imagen2.png')
    fotografiaDos = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='base/no-imagen2.png')
    fotografiaTres = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='base/no-imagen2.png')
    
    def __str__(self):
        return ', '.join(problema.falla for problema in self.problemas.all())
    
    class Meta:
        verbose_name = 'Registro de Mantenimiento'
        verbose_name_plural = 'Registros de Mantenimientos'
        db_table = 'maintenance_register'
        
class HistorialSolicitudMantenimiento(models.Model):
    solicitud = models.ForeignKey(NuevaSolicitudMantenimiento, on_delete=models.CASCADE,verbose_name='Solicitud')
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name='Nombre Usuario')
    progreso = models.CharField(max_length=50,choices=progreso,null=True,blank=True,verbose_name='Progreso Solicitud')
    empresaMantenimiento = models.ForeignKey(EmpresaServicios, on_delete=models.CASCADE,null=True,blank=True,verbose_name='Empresa Servicios')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.progreso)
    
    class Meta:
        verbose_name = 'Historial Registro de Mantenimiento'
        verbose_name_plural = 'Historial Registros de Mantenimientos'
        db_table = 'maintenance_register_history'

@receiver(post_save, sender=NuevaSolicitudMantenimiento)
def create_historial_solicitud_mantenimiento(sender, instance, created, **kwargs):
    if created:
        HistorialSolicitudMantenimiento.objects.create(
            solicitud=instance,
            solicitante=instance.solicitante,
            progreso=instance.progreso
        )
        
class SolicitudMantenimientoProblemas(models.Model):
    fallaVehiculo = models.ForeignKey(TipoFallaVehiculo, on_delete=models.CASCADE,verbose_name='Falla Vehiculo')
    solicitudMantenimiento = models.ForeignKey(NuevaSolicitudMantenimiento, on_delete=models.CASCADE,verbose_name='Solicitud Mantenimiento')
    valorServicio =  models.IntegerField(null=True,blank=True,verbose_name='Valor Servicio')
    descripcion = models.CharField(max_length=100,null=True,verbose_name='Descripción')
    
    objects = AuditableQuerySet.as_manager()

class NuevaSolicitudMantenimientoMaquinaria(models.Model):
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name='Nombre Usuario')
    telefono = models.IntegerField(null=True, verbose_name='Telefono')
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.CASCADE,null=True,verbose_name='Nombre Maquinaria')
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE,null=True,verbose_name='Faena')
    horometro = models.IntegerField(null=True,blank=True,verbose_name='Horómetro')
    progreso = models.CharField(max_length=50,choices=progreso,null=True,blank=True, default=1,verbose_name='Progreso Solicitud')
    empresaMantenimiento = models.ForeignKey(EmpresaServicios, on_delete=models.CASCADE,null=True,blank=True,verbose_name='Empresa Servicios')
    turno = models.CharField(max_length=20,choices=turno,null=True,blank=True,verbose_name='Turno')
    problemas = models.ManyToManyField(FallaMaquinaria, through='SolicitudMantenimientoProblemasMaquinaria')
    comentario = models.CharField(max_length=1000,null=True,verbose_name='Comentarios Adicionales')
    avisoJefatura =  models.CharField(max_length=20,choices=opcion,null=True,blank=True, verbose_name='Aviso a su Jefatura Directa?')
    status = models.BooleanField(null=True, verbose_name='Estado')    
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def generaNombre(instance, filename):
        extension = os.path.splitext(filename)[1][1:]
        maquinaria_nombre = instance.maquinaria.maquinaria.upper()
        solicitud_fecha = instance.fechacreacion.strftime('%Y-%m-%d')
        solicitud_hora = instance.fechacreacion.strftime('%H-%M-%S')
        ruta = f'documentacion_mantenimientos_maquinaria/{maquinaria_nombre}/{solicitud_fecha}/{solicitud_hora}' 
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S") 
        nombre = "{}.{}".format(fecha, extension)
        return os.path.join(ruta, nombre)

    fotografiaUno = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='base/no-imagen2.png')
    fotografiaDos = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='base/no-imagen2.png')
    
    def __str__(self):
        return ', '.join(problema.falla for problema in self.problemas.all())
    
    class Meta:
        verbose_name = 'Registro de Mantenimiento Maquinaria'
        verbose_name_plural = 'Registros de Mantenimientos Maquinarias'
        db_table = 'maintenance_register_machines'
        
class HistorialSolicitudMantenimientoMaquinaria(models.Model):
    solicitud = models.ForeignKey(NuevaSolicitudMantenimientoMaquinaria, on_delete=models.CASCADE,verbose_name='Solicitud Maquinaria')
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name='Nombre Usuario')
    progreso = models.CharField(max_length=50,choices=progreso,null=True,blank=True,verbose_name='Progreso Solicitud')
    empresaMantenimiento = models.ForeignKey(EmpresaServicios, on_delete=models.CASCADE,null=True,blank=True,verbose_name='Empresa Servicios')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{}".format(self.progreso)
    
    class Meta:
        verbose_name = 'Historial Registro de Mantenimiento Maquinaria'
        verbose_name_plural = 'Historial Registros de Mantenimientos Maquinarias'
        db_table = 'maintenance_register_history_machines'

@receiver(post_save, sender=NuevaSolicitudMantenimientoMaquinaria)
def create_historial_solicitud_mantenimiento_maquinaria(sender, instance, created, **kwargs):
    if created:
        HistorialSolicitudMantenimientoMaquinaria.objects.create(
            solicitud=instance,
            solicitante=instance.solicitante,
            progreso=instance.progreso
        )
        
class SolicitudMantenimientoProblemasMaquinaria(models.Model):
    fallaMaquinaria = models.ForeignKey(FallaMaquinaria, on_delete=models.CASCADE,verbose_name='Falla Maquinaria')
    solicitudMantenimiento = models.ForeignKey(NuevaSolicitudMantenimientoMaquinaria, on_delete=models.CASCADE,verbose_name='Solicitud Mantenimiento')
    valorServicio =  models.IntegerField(null=True,blank=True,verbose_name='Valor Servicio')
    descripcion = models.CharField(max_length=100,null=True,verbose_name='Descripción')

    objects = AuditableQuerySet.as_manager()

class Mantenimiento(models.Model):
    progreso_choices = (
        ('1', 'Solicitud'),
        ('2', 'En Mantención'),
        ('3', 'Segunda Revisión'),
        ('4', 'Terminada'),
        ('5', 'Anulada'),
    )

    progreso = models.CharField(max_length=1, choices=progreso_choices)

    objects = AuditableQuerySet.as_manager()

    @classmethod
    def get_nombre_progreso(cls, numero):
        return dict(cls.progreso_choices).get(numero, 'Desconocido')