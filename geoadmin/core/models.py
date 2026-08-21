import os
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from core.choices import tipotraccion, opcion, secciones, estadorecomendaciones
from datetime import datetime
from .choices import meses
from django.core.validators import MinValueValidator, MaxValueValidator
from administration.managers import AuditableQuerySet

class Genero(models.Model):
    genero = models.CharField(max_length=50,unique=True,verbose_name='Genero')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.genero)
    class Meta:
        verbose_name = 'Genero'
        verbose_name_plural = 'Generos'
        db_table = 'user_genero'

class Ciudad(models.Model):
    ciudad = models.CharField(max_length=50,unique=True,verbose_name='Ciudad')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.ciudad)
    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        db_table = 'user_ciudad'
        
class Nacionalidad(models.Model):
    nacionalidad = models.CharField(max_length=50,unique=True,verbose_name='Nacionalidad')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.nacionalidad)
    class Meta:
        verbose_name = 'Nacionalidad'
        verbose_name_plural = 'Nacionalidades'
        db_table = 'user_nacionalidad'

class Ano(models.Model):
    ano = models.CharField(max_length=50,unique=True,verbose_name='Año')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.ano)
    class Meta:
        verbose_name = 'Año'
        verbose_name_plural = 'Años'
        db_table = 'vehicle_ano'

class Marca(models.Model):
    marca = models.CharField(max_length=50,unique=True,verbose_name='Marca')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.marca)
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        db_table = 'vehicle_marca'

class Modelo(models.Model):
    modelo = models.CharField(max_length=50,unique=True,verbose_name='Modelo')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.modelo)
    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        db_table = 'vehicle_modelo'
        
class Color(models.Model):
    color = models.CharField(max_length=50,unique=True,verbose_name='Color')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.color)
    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colores'
        db_table = 'vehicle_color'
        
class Tipo(models.Model):
    tipo = models.CharField(max_length=50,unique=True,verbose_name='Tipo')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.tipo)
    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'
        db_table = 'vehicle_tipo'
        
@receiver(post_save, sender=Tipo)
def create_informacion_vehiculo(sender, instance, created, **kwargs):
    OcultarOpcionesVehiculo.objects.create(tipo_vehiculo=instance.tipo)

class Faena(models.Model):
    faena = models.CharField(max_length=100,unique=True,verbose_name='Nombre Faena')
    descripcion = models.CharField(max_length=500,verbose_name='Descripción Faena')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.faena)
    class Meta:
        verbose_name = 'Faena'
        verbose_name_plural = 'Faenas'
        db_table = 'mining_profile'
        
class TipoDocumentoFaena(models.Model):
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE)
    documento = models.CharField(max_length=100,verbose_name='Tipo Documento Faena')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{} {}".format(self.faena, self.documento)
    class Meta:
        verbose_name = 'Tipo Documento Faena'
        verbose_name_plural = 'Tipos Documentos Faena'
        db_table = 'mining_document_type'

class EmpresaServicios(models.Model):
    empresa = models.CharField(max_length=100,unique=True,verbose_name='Nombre Empresa')
    descripcion = models.CharField(max_length=500,verbose_name='Descripción')
    direccion = models.CharField(max_length=500,verbose_name='Dirección ')
    rut = models.CharField(max_length=50,verbose_name='Rut')
    telefono = models.IntegerField(null=True, verbose_name='Telefono')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.empresa)
    class Meta:
        verbose_name = 'Empresa de Mantenimiento'
        verbose_name_plural = 'Empresas de Mantenimiento'
        db_table = 'companies_profile'

class EmpresaTipoServicios(models.Model):
    empresa = models.ForeignKey(EmpresaServicios, on_delete=models.CASCADE)
    servicio = models.CharField(max_length=100,null=True,verbose_name='Tipo de Servicio')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.servicio)
    class Meta:
        verbose_name = 'Servicio de Mantenimiento'
        verbose_name_plural = 'Servicios de Mantenimientos'
        db_table = 'companies_maintenance_services'

class CategoriaFallaVehiculo(models.Model):
    categoria = models.CharField(max_length=200,null=True, unique=True, verbose_name='Categoría de Falla')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.categoria)
    class Meta:
        verbose_name = 'Tipo Categoría de Falla'
        verbose_name_plural = 'Tipos Categorías de Fallas'
        db_table = 'vehicle_categories_failure'
        
class TipoFallaVehiculo(models.Model):
    categoria = models.ForeignKey(CategoriaFallaVehiculo, on_delete=models.CASCADE, null=True)
    falla = models.CharField(max_length=200,null=True,verbose_name='Tipo de Falla')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.falla)
    class Meta:
        verbose_name = 'Tipo de Falla'
        verbose_name_plural = 'Tipos de Fallas'
        db_table = 'vehicle_failure'

class ProblemaVehiculo(models.Model):
    problema = models.CharField(max_length=200, unique=True, verbose_name='Problema')
    creador = models.CharField(max_length=50, verbose_name='Creador', null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False, default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.problema)
    class Meta:
        verbose_name = 'Problema de Vehículo'
        verbose_name_plural = 'Problemas de Vehículos'
        db_table = 'vehicle_problem'

class OcultarOpcionesVehiculo(models.Model):
    tipo_vehiculo = models.CharField(max_length=100,null=True,verbose_name='Tipo de Vehículo')    
    placaPatente = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Patente (Requerido)')
    rutPropietario = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Rut Propietario (Reqquerido)')
    fechaAdquisicion = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Fecha Adquisición (Requerido)')
    nombrePropietario = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Nombre Propietario (Requerido)')    
    domicilio = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Domicilio (Requerido)')
    tipo = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Tipo Vehículo (Requerido)')
    marca = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Marca Vehículo (Requerido)')
    modelo = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Modelo Vehículo (Requerido)')
    ano = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Año Vehículo (Requerido)') 
    numeroMotor = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='N° Motor (Requerido)')
    numeroChasis = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='N° Chasis (Requerido)')
    numeroVin = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name=' N° Vin (Requerido)')
    color = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Color Vehículo (Requerido)')
    fechaVencimientoPermisoCirculacion = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Vencimiento Permiso Circulación (Requerido)')
    fechaVencimientoRevisionTecnica = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Vencimiento Revisión Técnica (Requerido)')
    fechaVencimientoSeguroObligatorio = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Vencimiento Seguro Obligatorio (Requerido)')    
    fechaVencimientoLamina = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Vencimiento Lámina (Opcional)')
    fechaInstalacionBarraAntiVuelco = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Vencimiento Barra AntiVuelco (Opcional)')
    fechaInstalacionGps = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Instalación Gps (Opcional)')
    fechaCertificadoOperatividad = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Certificado Operatividad (Opcional)')
    fechaCertificadoMantencion = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Certificado Mantención (Opcional)')
    fechaCertificadoGrua = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Certificado Grua (Opcional)')
    fechaVencimientoTransportePrivado = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Vencimiento Transporte Privado (Opcional)')
    tieneTag = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Tiene Tag (Opcional)')    
    tipoTraccion = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Tipo Tracción')
    pesoBrutoVehicular = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Peso Bruto Vehicular')
    capacidadCarga = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Capacidad de Carga')
    tipoNeumatico = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Tipo Neumático')
    tipoAceiteMotor = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Tipo Aceite Motor')
    tipoRefrigeranteMotor = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Tipo Refrigerante Motor')
    tipoFiltroAireMotor = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Tipo Filtro Aire Motor')
    tipoFiltroCombustible = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Tipo Filtro Combustible')
    frecuenciaMantenimiento = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Frecuencia de Mantenimiento (Kilometros)')
    proximoMantenimiento = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Proximo Mantenimiento (Kilometros)')
    proximoMantenimientoGrua = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Proximo Mantenimiento Grua (Horómetro)')
    fotografiaFacturaCompra = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Factura de Compra')
    fotografiaPadron = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Padrón Vehicular')
    fotografiaPermisoCirculacion = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Permiso Circulación')
    fotografiaRevisionTecnica =models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Revisión Técnica')
    fotografiaRevisionTecnicaGases = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Revisión Técnica de Gases')
    fotografiaSeguroObligatorio = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Seguro Obligatorio')
    fotografiaSeguroAutomotriz = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Seguro Automotriz')
    fotografiaCertificadoGps = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Certificado GPS')
    fotografiaCertificadoMantencion = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Certificado de Mantención')
    fotografiaCertificadoOperatividad = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Certificado de Operatividad')
    fotografiaCertificadoGrua = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Certificado Grúa')
    fotografiaCertificadoLamina = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Certificado de Lámina')
    fotografiaCertificadoBarraAntiVuelco = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Certificado de Barra AntiVuelco')
    fotografiaDocumentacionMiniBus = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Documentación Transp. Privado')    
    fotografiaInteriorTablero = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Fotografía Interior Tablero')
    fotografiaInteriorCopiloto = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Fotografía Interior Acompañante')
    fotografiaInteriorAtrasPiloto = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Fotografía Interior Atrás Conductor')
    fotografiaInteriorAtrasCopiloto = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Fotografía Interior Atrás Acompanante')    
    fotografiaExteriorFrontis = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Fotografía Exterior Frontis')
    fotografiaExteriorAtras = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Fotografía Exterior Atrás')
    fotografiaExteriorPiloto = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Fotografía Exterior Lado Conductor')
    fotografiaExteriorCopiloto = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Fotografía Exterior Lado Acompañante')
    dispositivosomnolencia = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Dispositivos de Somnolencia')
    tarjetaCombustible = models.CharField(max_length=10,null=True,default="Si",choices=opcion,verbose_name='Tarjeta de Combustible')
    objects = AuditableQuerySet.as_manager()
    def __str__(self) : return "{}".format(self.tipo_vehiculo)
    class Meta:
        verbose_name = 'Ocultar Información de Vehiculo'
        verbose_name_plural = 'Ocultar Información de Vehiculo'
        db_table = 'vehicle_hide_options' 

class TipoDocumentoFaenaGeneral(models.Model):
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE)
    nombredocumento = models.CharField(max_length=100,null=True,verbose_name='Tipo Documento Faena')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    fechacaducidad = models.DateField(null=True, blank=True, verbose_name='Fecha de Caducidad')
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{} {}".format(self.faena, self.nombredocumento)
    def generaNombre(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        faena = instance.faena.faena.upper()
        ruta = f'documentacion_general_faena/{faena}' 
        fecha =datetime.now().strftime("%Y%m%d_%H%M%S") 
        nombre = "{}.{}".format(fecha,extension)
        return os.path.join(ruta,nombre)
    archivodocumento = models.ImageField(upload_to=generaNombre,null=True,blank=True,default='base/no-imagen.png')
    class Meta:
        verbose_name = 'Tipo Documento Faena'
        verbose_name_plural = 'Tipos Documentos Faena'
        db_table = 'mining_document_type_general'
        
class TipoMaquinaria(models.Model):
    tipo = models.CharField(max_length=50,unique=True,verbose_name='Tipo Máquinaria')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.tipo)
    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        db_table = 'machine_type'
        
class MarcaMaquinaria(models.Model):
    tipo = models.ForeignKey(TipoMaquinaria, on_delete=models.CASCADE, null=True)
    marca = models.CharField(max_length=50,verbose_name='Marca o Modelo')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.marca)
    class Meta:
        verbose_name = 'Marca o Modelo'
        verbose_name_plural = 'Marca o Modelos'
        db_table = 'machine_model'

class KitsMaquinaria(models.Model):
    marcaMaquina = models.ForeignKey(MarcaMaquinaria, on_delete=models.CASCADE, null=True)
    nombreKit = models.CharField(max_length=50,verbose_name='Kit de Reparación')
    stockMinimo = models.IntegerField(null=True, verbose_name='Stock Minimo')
    stockMaximo = models.IntegerField(null=True, verbose_name='Stock Máximo')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.nombreKit)
    class Meta:
        verbose_name = 'Marca o Modelo'
        verbose_name_plural = 'Marca o Modelos'
        db_table = 'machine_kit_machine'
        
class FallaMaquinaria(models.Model):
    kitMaquinaria = models.ForeignKey(KitsMaquinaria, on_delete=models.CASCADE, null=True)
    falla = models.CharField(max_length=50,verbose_name='Tipo de Falla')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.falla)
    class Meta:
        verbose_name = 'Falla en Máquina'
        verbose_name_plural = 'Fallas en Máquinas'
        db_table = 'machine_failure'
        
class FechasImportantes(models.Model):
    descripcion = models.CharField(max_length=50,verbose_name='Descripción Fecha')
    fechaVencimiento =  models.CharField(max_length=20,null=True,choices=meses,verbose_name='Mes de Vencimiento')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.descripcion)
    class Meta:
        verbose_name = 'Fecha Importante'
        verbose_name_plural = 'Fechas Importantes'
        db_table = 'vehicle_important_dates'

class ReporteError(models.Model):
    creador = models.CharField(max_length=50,verbose_name='Usuario',null=True)
    descripcion = models.CharField(max_length=50,verbose_name='Descripción')
    detalle = models.CharField(max_length=500,verbose_name='Detalle del Error')
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.descripcion)
    class Meta:
        verbose_name = 'Reporte de Error'
        verbose_name_plural = 'Reporte de Errores'
        db_table = 'report_errors'

class AyudaManuales(models.Model):
    seccion = models.CharField(max_length=100,choices=secciones,verbose_name='Sección')
    nombredocumento = models.CharField(max_length=100,null=True,verbose_name='Nombre Documento')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{} {}".format(self.seccion, self.nombredocumento)
    def generaNombre(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        seccion = instance.seccion.upper()
        ruta = f'ayuda_manuales/{seccion}' 
        fecha =datetime.now().strftime("%Y%m%d_%H%M%S") 
        nombre = "{}.{}".format(fecha,extension)
        return os.path.join(ruta,nombre)
    archivodocumento = models.ImageField(upload_to=generaNombre,null=True,blank=True,default='base/no-imagen.png')
    class Meta:
        verbose_name = 'Documento Ayuda y Manual '
        verbose_name_plural = 'Documentos Ayuda y Manuales'
        db_table = 'documents_help_manuals'
        
class Sondas(models.Model):
    sonda = models.CharField(max_length=100,null=True,verbose_name='Sonda')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.sonda)
    class Meta:
        verbose_name = 'Sonda Minera'
        verbose_name_plural = 'Sondas Mineras'
        db_table = 'drilling_probe'
        
class Sondajes(models.Model):
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, null=True)
    sondaje = models.CharField(max_length=100,null=True,verbose_name='Sondajes')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.sondaje)
    class Meta:
        verbose_name = 'Sondaje Minero'
        verbose_name_plural = 'Sondajes Mineros'
        db_table = 'drilling_drilling'

class Diametros(models.Model):
    diametro = models.CharField(max_length=100,null=True,verbose_name='Diametro')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.diametro)
    class Meta:
        verbose_name = 'Diametro'
        verbose_name_plural = 'Diametros'
        db_table = 'drilling_diameter'

class TipoTerreno(models.Model):
    tipoTerreno = models.CharField(max_length=100,null=True,verbose_name='Tipo Terreno')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.tipoTerreno)
    class Meta:
        verbose_name = 'Tipo Terreno'
        verbose_name_plural = 'Tipo Terrenos'
        db_table = 'drilling_land_type'
        
class Orientacion(models.Model):
    orientacion = models.CharField(max_length=100,null=True,verbose_name='Orientacion')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.orientacion)
    class Meta:
        verbose_name = 'Orientacion'
        verbose_name_plural = 'Orientaciones'
        db_table = 'drilling_orientation'

class Perforistas(models.Model):
    perforista = models.CharField(max_length=100,null=True,verbose_name='Perforista')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.perforista)
    class Meta:
        verbose_name = 'Perforista'
        verbose_name_plural = 'Perforistas'
        db_table = 'drilling_perforista'
        
class DetalleControlHorario(models.Model):
    detalle = models.CharField(max_length=100,null=True,verbose_name='Detalle')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.detalle)
    class Meta:
        verbose_name = 'Detalle Control Horario'
        verbose_name_plural = 'Detalles Control Horario'
        db_table = 'drilling_details'

class Corona(models.Model):
    corona = models.CharField(max_length=100,null=True,verbose_name='Corona')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.corona)
    class Meta:
        verbose_name = 'Corona'
        verbose_name_plural = 'Coronas'
        db_table = 'drilling_corona'
        
class Escareador(models.Model):
    escareador = models.CharField(max_length=100,null=True,verbose_name='Escareador')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.escareador)
    class Meta:
        verbose_name = 'Escareador'
        verbose_name_plural = 'Escareadores'
        db_table = 'drilling_escareador'
        
class CantidadAgua(models.Model):
    cantidadAgua = models.IntegerField(null=True,verbose_name='Litros Agua')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.cantidadAgua)
    class Meta:
        verbose_name = 'Litros Agua'
        verbose_name_plural = 'Litros Agua'
        db_table = 'drilling_cant_water'

class Aditivos(models.Model):
    aditivo = models.CharField(max_length=100,null=True,verbose_name='Aditivo')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.aditivo)
    class Meta:
        verbose_name = 'Aditivo'
        verbose_name_plural = 'Aditivos'
        db_table = 'drilling_aditivos'
        
class Casing(models.Model):
    casing = models.CharField(max_length=100,null=True,verbose_name='Casing')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.casing)
    class Meta:
        verbose_name = 'Casing'
        verbose_name_plural = 'Casing'
        db_table = 'drilling_casing'

class Zapata(models.Model):
    zapata = models.CharField(max_length=100,null=True,verbose_name='Zapata')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.zapata)
    class Meta:
        verbose_name = 'Zapata'
        verbose_name_plural = 'Zapatas'
        db_table = 'drilling_zapata'

class LargoBarra(models.Model):
    largoBarra = models.IntegerField(null=True,verbose_name='Largo Barra (Mts)')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.largoBarra)
    class Meta:
        verbose_name = 'Largo Barra'
        verbose_name_plural = 'Largo Barras'
        db_table = 'drilling_largo_barra'

class Campana(models.Model):
    campana = models.CharField(max_length=100,null=True,verbose_name='Campaña')
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, null=True, verbose_name='Faena')
    anoInicial = models.IntegerField(null=True,verbose_name='Año Inicial')
    anoFinal = models.IntegerField(verbose_name='Año Final',null=True)
    metros = models.IntegerField(null=True,verbose_name='Metros Planificados (Mts)')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.campana)
    class Meta:
        verbose_name = 'Campaña'
        verbose_name_plural = 'Campañas'
        db_table = 'drilling_campaing'
    
class Programa(models.Model):
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, null=True, verbose_name='Campaña')
    programa = models.CharField(max_length=100,null=True,verbose_name='Programa')
    metros = models.IntegerField(null=True,verbose_name='Metros Planificados (Mts)')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.programa)
    class Meta:
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'
        db_table = 'drilling_program'
        unique_together = ('campana', 'programa')
        
class Recomendacion(models.Model):
    campana = models.ForeignKey(Campana, on_delete=models.CASCADE, null=True, verbose_name='Campaña')
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, null=True, verbose_name='Programa')
    recomendacion = models.CharField(max_length=50, null=True, verbose_name='Recomendación')
    pozo = models.CharField(max_length=50, null=True, verbose_name='Pozo')
    sonda = models.ForeignKey(Sondas, on_delete=models.CASCADE, null=True, verbose_name='Sonda', related_name="recomendaciones")
    fecha_inicio = models.DateTimeField(auto_now=False,null=True, verbose_name='Fecha de Inicio')
    sector = models.CharField(max_length=50, null=True, verbose_name='Sector')
    azimut = models.IntegerField(null=True, verbose_name='Azimut', validators=[MinValueValidator(0), MaxValueValidator(360)])
    inclinacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name='Inclinación')
    largo_programado = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Largo Programado')
    largo_real = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Largo Real')
    este = models.DecimalField(max_digits=12, decimal_places=3, null=True, verbose_name='Este')
    norte = models.DecimalField(max_digits=12, decimal_places=3, null=True, verbose_name='Norte')
    cota = models.DecimalField(max_digits=10, decimal_places=3, null=True, verbose_name='Cota')
    manteo = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Manteo')
    estado = models.CharField(max_length=100,choices=estadorecomendaciones,null=True, verbose_name='Estado')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    fechaUpdateEstado = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def format_decimal(self, value):
        if value is not None: return '{:g}'.format(float(value))
        return None
    def __str__(self):
        largo_real_formatted = int(self.largo_real) if self.largo_real == int(self.largo_real) else self.largo_real
        return f"{self.recomendacion} - Largo Real: {largo_real_formatted}"
    class Meta:
        verbose_name = 'Recomendacion'
        verbose_name_plural = 'Recomendaciones'
        db_table = 'drilling_recommendation'

class RecomendacionAjuste(models.Model):
    recomendacionAjuste = models.ForeignKey(Recomendacion, on_delete=models.CASCADE, null=True, verbose_name='Recomendación')
    azimutAjuste = models.IntegerField(null=True, verbose_name='Azimut', validators=[MinValueValidator(0), MaxValueValidator(360)])
    esteAjuste = models.DecimalField(max_digits=12, decimal_places=3, null=True, verbose_name='Este')
    norteAjuste = models.DecimalField(max_digits=12, decimal_places=3, null=True, verbose_name='Norte')
    cotaAjuste = models.DecimalField(max_digits=10, decimal_places=3, null=True, verbose_name='Cota')
    manteoAjuste = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name='Manteo')
    statusAjuste = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacionAjuste = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.recomendacionAjuste)
    class Meta:
        verbose_name = 'Recomendacion Ajuste'
        verbose_name_plural = 'Recomendaciones Ajustes'
        db_table = 'drilling_recommendation_ajuste'

class RecomendacionFinal(models.Model):
    recomendacionFinal = models.ForeignKey(Recomendacion, on_delete=models.CASCADE, null=True, verbose_name='Recomendación')
    esteFinal = models.DecimalField(max_digits=12, decimal_places=3, null=True, verbose_name='Este')
    norteFinal = models.DecimalField(max_digits=12, decimal_places=3, null=True, verbose_name='Norte')
    cotaFinal = models.DecimalField(max_digits=10, decimal_places=3, null=True, verbose_name='Cota')
    fechaFinal = models.DateTimeField(auto_now=False,null=True, verbose_name='Fecha')
    statusFinal = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacionFinal = models.DateTimeField(null=False,default=timezone.now)
    objects = AuditableQuerySet.as_manager()
    def __str__(self): return "{}".format(self.recomendacionFinal)
    class Meta:
        verbose_name = 'Recomendacion Final'
        verbose_name_plural = 'Recomendaciones Finales'
        db_table = 'drilling_recommendation_final'

class MaterialesSonda(models.Model):
    material = models.CharField(max_length=100, null=True, verbose_name='Material')
    creador = models.CharField(max_length=50, verbose_name='Creador', null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False, default=timezone.now)
    objects = AuditableQuerySet.as_manager()

    def save(self, *args, **kwargs):
        sincronizar = kwargs.pop('sincronizar', True)

        super().save(*args, **kwargs)

        if sincronizar and self.material:
            obj, created = MaterialesCaseta.objects.get_or_create(
                material=self.material,
                defaults={
                    'creador': self.creador,
                    'status': self.status,
                }
            )

            if not created and obj.status != self.status:
                obj.status = self.status
                obj.creador = self.creador
                obj.save(sincronizar=False)

    def __str__(self):
        return "{}".format(self.material)

    class Meta:
        verbose_name = 'Material Sonda'
        verbose_name_plural = 'Materiales Sonda'
        db_table = 'checklist_materiales_sonda'


class MaterialesCaseta(models.Model):
    material = models.CharField(max_length=100, null=True, verbose_name='Material')
    creador = models.CharField(max_length=50, verbose_name='Creador', null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False, default=timezone.now)
    objects = AuditableQuerySet.as_manager()

    def save(self, *args, **kwargs):
        sincronizar = kwargs.pop('sincronizar', True)

        super().save(*args, **kwargs)

        if sincronizar and self.material:
            obj, created = MaterialesSonda.objects.get_or_create(
                material=self.material,
                defaults={
                    'creador': self.creador,
                    'status': self.status,
                }
            )

            if not created and obj.status != self.status:
                obj.status = self.status
                obj.creador = self.creador
                obj.save(sincronizar=False)

    def __str__(self):
        return "{}".format(self.material)

    class Meta:
        verbose_name = 'Material Caseta'
        verbose_name_plural = 'Materiales Caseta'
        db_table = 'checklist_materiales_caseta'