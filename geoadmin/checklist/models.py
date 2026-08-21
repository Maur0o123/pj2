import os
from django.db import models
from django.utils import timezone
from core.models import MaterialesSonda, MaterialesCaseta, Sondas, Sondajes
from core.choices import jornada, turno, gemelo
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from administration.managers import AuditableQuerySet

class HistorialMovimientoCaseta(models.Model):
    TIPO_MOVIMIENTO = [
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
        ('MODIFICACION', 'Modificación'),
    ]

    item = models.ForeignKey(MaterialesCaseta, on_delete=models.CASCADE)
    movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    cantidad = models.IntegerField(default=0)
    cantidad_buenos = models.IntegerField(default=0)
    cantidad_malos = models.IntegerField(default=0)
    sondaje = models.CharField(max_length=100, null=True, blank=True)
    numero_sondaje = models.CharField(max_length=100, null=True, blank=True)

    observacion = models.TextField(null=True, blank=True)
    imagen = models.ImageField(upload_to='historial_caseta/', null=True, blank=True)

    creado_por = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    status = models.BooleanField(default=True)
    id_checklist = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f'{self.item} - {self.movimiento} - {self.cantidad}'

class ChecklistMaterialesSonda(models.Model):
    item = models.ForeignKey(MaterialesSonda, on_delete=models.CASCADE, verbose_name='Item')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    agregar = models.IntegerField(default=0, verbose_name='Agregar')
    total = models.IntegerField(default=0, verbose_name='Total')
    cantidad = models.IntegerField(null=True, verbose_name='Cantidad',default=0)
    creador = models.CharField(max_length=50, verbose_name='Creador', null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    jornada = models.CharField(max_length=50, choices=jornada, null=True, verbose_name='Jornada')
    etapa = models.CharField(max_length=50, null=True, verbose_name='Etapa')
    turno = models.CharField(max_length=50, choices=turno, null=True, verbose_name='Turno')
    sonda = models.ForeignKey(Sondas, on_delete=models.CASCADE, null=True, verbose_name='Sonda')
    sondajeCodigo = models.ForeignKey(Sondajes, on_delete=models.CASCADE, null=True, verbose_name='Sondaje')
    sondajeSerie = models.IntegerField(verbose_name="Serie",null=True,validators=[MinValueValidator(3940), MaxValueValidator(4400)] )
    sondajeEstado = models.CharField(max_length=3, choices=gemelo, verbose_name='Gemelo', null=True, blank=True, default='')
    id_checklist = models.BigIntegerField(null=True, verbose_name='ID Checklist')
    fecha_checklist = models.DateTimeField(null=True, verbose_name='Fecha')
    progreso = models.CharField(max_length=50,default='Creado',verbose_name='Progreso',null=True)
    fechacreacion = models.DateTimeField(null=False, default=timezone.now)


    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self):
        return "{} - Cantidad: {}".format(self.item.material, self.cantidad)

    class Meta:
        verbose_name = 'Checklist Material Sonda'
        verbose_name_plural = 'Checklist Materiales Sonda'
        db_table = 'checklist_documentos_materiales_sonda'

    @classmethod
    def crear_checklist(cls, creador):
        materiales = MaterialesSonda.objects.all()
        for material in materiales:
            cls.objects.get_or_create(item=material, creador=creador, defaults={'cantidad': 0})





class ChecklistMaterialesCaseta(models.Model):
    TURNO_CHOICES = [
        ('1', 'A'),
        ('2', 'B'),
    ]
    item = models.ForeignKey(MaterialesCaseta, on_delete=models.CASCADE, verbose_name='Item')
    b = models.IntegerField(null=True, verbose_name='B')
    m = models.IntegerField(null=True, verbose_name='M')
    observacion = models.CharField(max_length=500, null=True, verbose_name='Observaciones')
    fecha_control = models.DateTimeField(null=True, verbose_name='Fecha Control')
    creador = models.CharField(max_length=50, verbose_name='Creador', null=True)
    creador_cargo = models.CharField(max_length=50, verbose_name='Cargo', null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    turno = models.CharField(max_length=50, choices=turno, null=True, verbose_name='Turno')
    id_checklist = models.IntegerField(null=True, verbose_name='ID Checklist')
    fecha_checklist = models.DateTimeField(null=True, verbose_name='Fecha Checklist')
    fecha_revision = models.DateTimeField(null=True, verbose_name='Fecha Revision')
    observaciones_revision = models.CharField(max_length=500, null=True, verbose_name='Observaciones Revision')
    supervisor = models.CharField(max_length=50, null=True, verbose_name='Supervisor')
    fechacreacion = models.DateTimeField(null=False, default=timezone.now)
    nombre_caseta = models.CharField(max_length=100, blank=True, null=True)
    sondaje_asociado = models.CharField(max_length=100, blank=True, null=True)
    numero_sondaje_asociado = models.CharField(max_length=100, blank=True, null=True)
    
    usar_en_reporte = models.BooleanField(
        default=True,
        verbose_name='Utilizar material en reporte'
    )

    objects = AuditableQuerySet.as_manager()

    def generaNombre(instance, filename):
        turno_map = {'1': 'A', '2': 'B'}
        turno_str = turno_map.get(instance.turno, 'SinTurno')

        if instance.fecha_checklist:
            fecha_checklist_str = instance.fecha_checklist.strftime("%Y_%m_%d_%H_%M_%S")
        else:
            fecha_checklist_str = "SinFecha"

        ruta = f'checklist_caseta/{fecha_checklist_str}_{turno_str}'
        extension = os.path.splitext(filename)[1][1:] 
        nombre = f"{instance.item.id}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.{extension}"
        return os.path.join(ruta, nombre)

    fotografiaMaterial = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='checklist_caseta/no-imagen.png', verbose_name='Fotografía del Material')
    
    def __str__(self):
        return "{}".format(self.item.material)

    class Meta:
        verbose_name = 'Checklist Material Caseta'
        verbose_name_plural = 'Checklist Materiales Caseta'
        db_table = 'checklist_documentos_materiales_caseta'

    @classmethod
    def crear_checklist(cls, creador):
        materiales = MaterialesCaseta.objects.all()
        for material in materiales:
            cls.objects.get_or_create(item=material, creador=creador)
            
            
class EstadoEtapasReporteDigital(models.Model):
    id_checklist = models.BigIntegerField(null=True, verbose_name='ID Checklist')
    checklistEntrada = models.BooleanField(null=True, default=True, verbose_name='CheckList Entrada')
    reporteDigital = models.BooleanField(null=True, default=True, verbose_name='Reporte Digital')
    checklistSalida = models.BooleanField(null=True, default=True, verbose_name='CheckList Salida')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de Modificación')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"{self.id_checklist} | Entrada:{self.checklistEntrada} | Reporte:{self.reporteDigital} | Salida:{self.checklistSalida}"

    class Meta:
        verbose_name = 'Estado de Etapas'
        verbose_name_plural = 'Estados de Etapas'
        db_table = 'drilling_reporte_digital_etapas'

class CasetaSondajeAsociado(models.Model):
    id_checklist = models.CharField(max_length=100)
    nombre_caseta = models.CharField(max_length=100, blank=True, null=True)
    sondaje = models.CharField(max_length=100)
    numero_sondaje = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)

    objects = AuditableQuerySet.as_manager()

    class Meta:
        db_table = 'checklist_caseta_sondaje_asociado'
