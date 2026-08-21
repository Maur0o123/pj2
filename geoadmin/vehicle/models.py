import os
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime
from core.models import Tipo, Ano, Marca, Modelo, Color, OcultarOpcionesVehiculo, ProblemaVehiculo
from core.choices import tipotraccion, opcion, tenencia, estadopago, tipocombustible, tipodocumento

from administration.managers import AuditableQuerySet

class Vehiculo(models.Model):
    placaPatente = models.CharField(max_length=25,unique=True,verbose_name='Placa Patente')
    tenencia = models.CharField(max_length=20,choices=tenencia,null=True,blank=True,verbose_name='Tenencia')
    fechaAdquisicion = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Adquisición')
    fechaArriendoInicial = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Arriendo Inicial')
    fechaArriendoFinal = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Arriendo Final')    
    nombrePropietario = models.CharField(max_length=50,verbose_name='Nombre Propietario')
    rutPropietario = models.CharField(max_length=50,verbose_name='Rut Propietario')
    domicilio = models.CharField(max_length=100,verbose_name='Domicilio')
    tipo = models.ForeignKey(Tipo,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Tipo')
    ano = models.ForeignKey(Ano,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Año')
    marca = models.ForeignKey(Marca,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Marca')
    modelo = models.ForeignKey(Modelo,on_delete=models.CASCADE,null=True,blank=True,verbose_name='Modelo')
    numeroMotor = models.CharField(max_length=25,unique=True,verbose_name='N° Motor')
    numeroChasis = models.CharField(max_length=25,unique=True,verbose_name='N° Chasis')
    numeroVin = models.CharField(max_length=25,unique=True,verbose_name='N° Vin')    
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True, blank=True,verbose_name='Color')
    fechaVencimientoPermisoCirculacion = models.DateTimeField(auto_now=False,null=True, verbose_name='Permiso Circulación (Vencimiento)')
    fechaVencimientoRevisionTecnica = models.DateTimeField(auto_now=False,null=True, verbose_name='Revisión Técnica (Vencimiento)')
    fechaVencimientoSeguroObligatorio = models.DateTimeField(auto_now=False,null=True, verbose_name='Seguro Obligatorio (Vencimiento)')    
    fechaInstalacionGps = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Gps (Instalación)')
    fechaVencimientoLamina = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Lámina (Vencimiento)')
    fechaInstalacionBarraAntiVuelco = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Barra AntiVuelco (Instalación)')
    fechaVencimientoTransportePrivado = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Tranporte Privado (Vencimiento)')
    fechaCertificadoOperatividad = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Certificado Operatividad')
    fechaCertificadoMantencion = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Certificado Mantención')
    fechaCertificadoGrua = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Certificado Grúa')
    fechaVencimientoFacturaCompra = models.DateTimeField(auto_now=False, null=True, blank=True, verbose_name='Vencimiento Factura')
    fechaVencimientoPadron = models.DateTimeField(auto_now=False, null=True, blank=True, verbose_name='Vencimiento Padrón')
    fechaVencimientoRevisionTecnicaGases = models.DateTimeField(auto_now=False, null=True, blank=True, verbose_name='Vencimiento Gases')
    fechaVencimientoSeguroAutomotriz = models.DateTimeField(auto_now=False, null=True, blank=True, verbose_name='Vencimiento Seguro Automotriz')
    tieneTag =  models.CharField(max_length=20,choices=opcion,null=True,blank=True, verbose_name='Tiene Tag Asociado?')
    status = models.BooleanField(null=True, verbose_name='Estado')
    completado = models.IntegerField(null=True,blank=True,default=30,verbose_name='Porcentaje de Completado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    tarjetaCombustible = models.CharField(max_length=100, null=True, blank=True, verbose_name='Tarjeta Combustible')
    fechaVencimientoTraspasoVenta = models.DateTimeField(auto_now=False, null=True, blank=True, verbose_name='Vencimiento Traspaso/Venta')
    problema = models.ForeignKey(ProblemaVehiculo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Motivo de Desactivación')
    
    objects = AuditableQuerySet.as_manager()

    def calcular_completitud_vehiculo(self):
        try:
            ocultar_opciones = OcultarOpcionesVehiculo.objects.get(tipo_vehiculo=self.tipo.tipo)
        except OcultarOpcionesVehiculo.DoesNotExist:
            return 0, 0
        total_campos = 0
        campos_completos = 0
        campos_a_verificar = {
            'fechaInstalacionGps': 'fechaInstalacionGps',
            'fechaVencimientoLamina': 'fechaVencimientoLamina',
            'fechaInstalacionBarraAntiVuelco': 'fechaInstalacionBarraAntiVuelco',
            'fechaVencimientoTransportePrivado': 'fechaVencimientoTransportePrivado',
            'fechaCertificadoOperatividad': 'fechaCertificadoOperatividad',
            'fechaCertificadoMantencion': 'fechaCertificadoMantencion',
            'fechaCertificadoGrua': 'fechaCertificadoGrua',
            'tieneTag': 'tieneTag',
            'tarjetaCombustible': 'tarjetaCombustible',
        }        
        for campo, opcion in campos_a_verificar.items():
            if getattr(ocultar_opciones, opcion).lower() == 'si':
                total_campos += 1
                if getattr(self, campo) not in [None, '', False]:
                    campos_completos += 1                    
        return campos_completos, total_campos
    
    def calculate_days_difference(self):
        today = timezone.now().date()
        dates = {
            'Permiso Circulación (Vencimiento)': self.fechaVencimientoPermisoCirculacion,
            'Revisión Técnica (Vencimiento)': self.fechaVencimientoRevisionTecnica,
            'Seguro Obligatorio (Vencimiento)': self.fechaVencimientoSeguroObligatorio,
            'Fecha Gps (Instalación)': self.fechaInstalacionGps,
            'Fecha Lámina (Vencimiento)': self.fechaVencimientoLamina,
            'Fecha Barra AntiVuelco (Instalación)': self.fechaInstalacionBarraAntiVuelco,
            'Fecha Transporte Privado (Vencimiento)': self.fechaVencimientoTransportePrivado,
            'Fecha Certificado Operatividad': self.fechaCertificadoOperatividad,
            'FechaCertificadoMantencion': self.fechaCertificadoMantencion,
            'FechaCertificadoGrua': self.fechaCertificadoGrua,
        }
        differences = {}
        for key, value in dates.items():
            if value:
                difference = (value.date() - today).days
                differences[key] = {
                    'dias_diferencia': difference,
                    'fecha_vencimiento': value
                }
        return differences
    
    def __str__(self):
        return "{}".format(self.placaPatente)
        
    class Meta:
        verbose_name = 'Vehiculo'
        verbose_name_plural = 'Vehiculos'
        db_table = 'vehicle_profile'
        
class InformacionTecnicaVehiculo(models.Model):
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE)
    tipoTraccion = models.CharField(max_length=10,choices=tipotraccion,null=True,blank=True,verbose_name='Tracción')
    pesoBrutoVehicular = models.IntegerField(null=True,blank=True,verbose_name='Peso Bruto Vehicular (kg)')
    capacidadCarga = models.IntegerField(null=True,blank=True,verbose_name='Capacidad de Carga (kg)')
    tipoNeumatico = models.CharField(max_length=50,null=True,blank=True,verbose_name='Tipo Neumatico')
    tipoAceiteMotor = models.CharField(max_length=50,null=True,blank=True,verbose_name='Tipo Aceite Motor')
    tipoRefrigeranteMotor = models.CharField(max_length=50,null=True,blank=True,verbose_name='Tipo Liquido Refrigerante')
    tipoFiltroAireMotor = models.CharField(max_length=50,null=True,blank=True,verbose_name='Tipo Filtro Aire')
    tipoFiltroCombustible = models.CharField(max_length=50,null=True,blank=True,verbose_name='Tipo Filtro Combustible')
    frecuenciaMantenimiento = models.IntegerField(null=True,blank=True,verbose_name='Frecuencia Mantenimiento(Kilometros)')
    proximoMantenimiento = models.IntegerField(null=True,blank=True,verbose_name='Próximo Mantenimiento(Kilometros)')
    proximoMantenimientoGrua = models.IntegerField(null=True,blank=True,verbose_name='Próximo Mantenimiento(Horómetro)')
    
    objects = AuditableQuerySet.as_manager()
    
    def calcular_completitud_informacion_tecnica(self):
        try:
            ocultar_opciones = OcultarOpcionesVehiculo.objects.get(tipo_vehiculo=self.vehiculo.tipo.tipo)
        except OcultarOpcionesVehiculo.DoesNotExist:
            return 0, 0
        total_campos = 0
        campos_completos = 0
        campos_a_verificar = {
            'tipoTraccion': 'tipoTraccion', 
            'pesoBrutoVehicular': 'pesoBrutoVehicular', 
            'capacidadCarga': 'capacidadCarga',
            'tipoNeumatico': 'tipoNeumatico', 
            'tipoAceiteMotor': 'tipoAceiteMotor',
            'tipoRefrigeranteMotor': 'tipoRefrigeranteMotor', 
            'tipoFiltroAireMotor': 'tipoFiltroAireMotor', 
            'tipoFiltroCombustible': 'tipoFiltroCombustible',
            'frecuenciaMantenimiento': 'frecuenciaMantenimiento',
            'proximoMantenimiento': 'proximoMantenimiento',
            'proximoMantenimientoGrua': 'proximoMantenimientoGrua',
        }        
        for campo, opcion in campos_a_verificar.items():
            if getattr(ocultar_opciones, opcion).lower() == 'si':
                total_campos += 1
                if getattr(self, campo) not in [None, '', False]:
                    campos_completos += 1                    
        return campos_completos, total_campos
    
    def __str__(self) :
        return "{}".format(self.vehiculo)
        
    class Meta:
        verbose_name = 'Información Técnica de Vehiculo'
        verbose_name_plural = 'Información Técnica de Vehiculo'
        db_table = 'vehicle_information' 
        
class MarcaSomnolencia(models.Model):
    marca = models.CharField(max_length=50,verbose_name='Proveedor Dispositivo')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self):
        return "{}".format(self.marca)
        
    class Meta:
        verbose_name = 'Marca Dispositivo'
        verbose_name_plural = 'Marcas Dispositivos'
        db_table = 'vehicle sleepiness_brand'
        
class ModeloSomnolencia(models.Model):
    marca = models.ForeignKey(MarcaSomnolencia, on_delete=models.CASCADE, null=True)
    modelo = models.CharField(max_length=50,verbose_name='Modelo Dispositivo')
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self):
        return "{}".format(self.marca)
        
    class Meta:
        verbose_name = 'Modelo Dispositivo'
        verbose_name_plural = 'Modelos Dispositivos'
        db_table = 'vehicle sleepiness_model'

class AyudaTecnicaVehiculo(models.Model):
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE)
    dispositivo = models.BooleanField(null=True, verbose_name='¿Posee Dispositivo?')
    proveedor = models.ForeignKey(MarcaSomnolencia, on_delete=models.CASCADE,null=True)
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    status = models.BooleanField(null=True, verbose_name='Estado')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self):
        return "{}".format(self.vehiculo)
        
    class Meta:
        verbose_name = 'Ayuda Técnica Vehículo'
        verbose_name_plural = 'Ayudas Técnicas Vehículos'
        db_table = 'vehicle_technical_helps'

class DocumentacionesVehiculo(models.Model):
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE)
    def generaNombre(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        vehiculo_placaPatente = instance.vehiculo.placaPatente.upper()
        ruta = f'documentacion_vehiculo/{vehiculo_placaPatente}' 
        fecha =datetime.now().strftime("%Y%m%d_%H%M%S") 
        nombre = "{}.{}".format(fecha,extension)
        return os.path.join(ruta,nombre)           
    fotografiaPadron = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Padrón Vehicular")
    fotografiaPermisoCirculacion = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Permiso de Circulación")
    fotografiaRevisionTecnica = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Revisión Técnica")
    fotografiaRevisionTecnicaGases = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Revisión Técnica de Gases")
    fotografiaSeguroObligatorio = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Seguro Obligatorio")
    fotografiaCertificadoGps = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Certificado GPS")
    fotografiaCertificadoVarios = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Certificados Varios")
    fotografiaCertificadoMantencion = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Certificado de Mantención")
    fotografiaCertificadoOperatividad = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Certificado de Operatividad")
    fotografiaCertificadoGrua = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Certificado de Grúa")
    fotografiaFacturaCompra = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Factura de Compra")
    fotografiaSeguroAutomotriz = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Seguro Automotriz")
    fotografiaCertificadoLamina = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Certificado de Lámina")
    fotografiaDocumentacionMiniBus = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Documentación Transp. Privado")
    fotografiaCertificadoBarraAntiVuelco = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Certificado de Barra AntiVuelco")
    fotografiaInteriorTablero = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen-vehiculo.png', verbose_name="Fotografía Interior Tablero")
    fotografiaInteriorCopiloto = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen-vehiculo.png', verbose_name="Fotografía Interior Acompañante")
    fotografiaInteriorAtrasPiloto = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen-vehiculo.png', verbose_name="Fotografía Interior Atrás Conductor")
    fotografiaInteriorAtrasCopiloto = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen-vehiculo.png', verbose_name="Fotografía Interior Atrás Acompañante")
    fotografiaExteriorFrontis = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen-vehiculo.png', verbose_name="Fotografía Exterior Frontis")
    fotografiaExteriorAtras = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen-vehiculo.png', verbose_name="Fotografía Exterior Atrás")
    fotografiaExteriorPiloto = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen-vehiculo.png', verbose_name="Fotografía Exterior Lado Conductor")
    fotografiaExteriorCopiloto = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen-vehiculo.png', verbose_name="Fotografía Exterior Lado Acompañante")
    fotografiaTraspasoVenta = models.ImageField(upload_to=generaNombre, null=True, blank=True, default='documentacion_vehiculo/no-imagen.png', verbose_name="Traspaso/Venta")
    
    objects = AuditableQuerySet.as_manager()
    
    def calcular_completitud_documentaciones(self):
        try:
            ocultar_opciones = OcultarOpcionesVehiculo.objects.get(tipo_vehiculo=self.vehiculo.tipo.tipo)
        except OcultarOpcionesVehiculo.DoesNotExist:
            return 0, 0
        total_campos = 0
        campos_completos = 0
        campos_a_verificar = {
            'fotografiaPadron': 'fotografiaPadron', 
            'fotografiaPermisoCirculacion': 'fotografiaPermisoCirculacion', 
            'fotografiaRevisionTecnica': 'fotografiaRevisionTecnica',
            'fotografiaRevisionTecnicaGases': 'fotografiaRevisionTecnicaGases', 
            'fotografiaSeguroObligatorio': 'fotografiaSeguroObligatorio',
            'fotografiaCertificadoGps': 'fotografiaCertificadoGps',
            'fotografiaCertificadoMantencion': 'fotografiaCertificadoMantencion',
            'fotografiaCertificadoOperatividad': 'fotografiaCertificadoOperatividad',
            'fotografiaCertificadoGrua': 'fotografiaCertificadoGrua',
            'fotografiaFacturaCompra': 'fotografiaFacturaCompra', 
            'fotografiaSeguroAutomotriz': 'fotografiaSeguroAutomotriz',
            'fotografiaCertificadoLamina': 'fotografiaCertificadoLamina',
            'fotografiaDocumentacionMiniBus': 'fotografiaDocumentacionMiniBus',
            'fotografiaCertificadoBarraAntiVuelco': 'fotografiaCertificadoBarraAntiVuelco',
            'fotografiaInteriorTablero': 'fotografiaInteriorTablero',
            'fotografiaInteriorCopiloto': 'fotografiaInteriorCopiloto',
            'fotografiaInteriorAtrasPiloto': 'fotografiaInteriorAtrasPiloto',
            'fotografiaInteriorAtrasCopiloto': 'fotografiaInteriorAtrasCopiloto',
            'fotografiaExteriorFrontis': 'fotografiaExteriorFrontis',
            'fotografiaExteriorAtras': 'fotografiaExteriorAtras',
            'fotografiaExteriorPiloto': 'fotografiaExteriorPiloto',
            'fotografiaExteriorCopiloto': 'fotografiaExteriorCopiloto',
        }        
        for campo, opcion in campos_a_verificar.items():
            if getattr(ocultar_opciones, opcion).lower() == 'si':
                total_campos += 1
                if getattr(self, campo) not in [None, 'documentacion_vehiculo/no-imagen-vehiculo.png', 'documentacion_vehiculo/no-imagen.png']:
                    campos_completos += 1                    
        return campos_completos, total_campos
    
    def __str__(self) :
        return "{}".format(self.vehiculo)
        
    class Meta:
        verbose_name = 'Documentacion Vehiculo'
        verbose_name_plural = 'Documentacion Vehiculos'
        db_table = 'vehicle_documentation' 
        
@receiver(post_save, sender=Vehiculo)
def create_documentacion_vehiculo(sender, instance, created, **kwargs):
    if created:
        DocumentacionesVehiculo.objects.create(vehiculo=instance)    
    
@receiver(post_save, sender=Vehiculo)
def create_informacion_vehiculo(sender, instance, created, **kwargs):
    if created:
        InformacionTecnicaVehiculo.objects.create(vehiculo=instance)

class InfraccionesVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fechaInfraccion = models.DateTimeField(auto_now=False,null=True,blank=True,verbose_name='Fecha Infracción')
    infraccion = models.CharField(max_length=1000,null=True,blank=True,verbose_name='Detalle Infraccion')
    ciudadInfraccion = models.CharField(max_length=30,null=True,blank=True,verbose_name='Ciudad / Lugar')
    estadoPagoInfraccion = models.CharField(max_length=10,choices=estadopago,null=True,blank=True,verbose_name='Estado del Pago')
    valorInfraccion = models.IntegerField(null=True,blank=True,verbose_name='Valor')

    objects = AuditableQuerySet.as_manager()

    def __str__(self) :
        return "{}".format(self.vehiculo)
        
    class Meta:
        verbose_name = 'Información Infracción y Multas'
        verbose_name_plural = 'Información Infracciones y Multas'
        db_table = 'vehicle_penalty' 
        
class NuevoKilometraje(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    kilometraje = models.IntegerField(null=True,blank=True,verbose_name='Kilometraje Actual')
    fechacreacion = models.DateTimeField(null=False,default=timezone.now)
    creador = models.CharField(max_length=50,verbose_name='Creador',null=True)
    origen = models.CharField(max_length=30,null=True,blank=True,verbose_name='Origen')
    
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self) :
        return "{}".format(self.vehiculo)
        
    class Meta:
        verbose_name = 'Kilometraje Vehicular'
        verbose_name_plural = 'Kilometrajes Vehicular'
        db_table = 'vehicle_kilometres_registers'

class NuevaTarjetaCombustible(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    numeroTarjeta = models.BigIntegerField(null=True, blank=True, verbose_name='Número Tarjeta')
    patente = models.CharField(max_length=30, null=True, blank=True, verbose_name='Patente')
    tipoVehiculo = models.CharField(max_length=50, null=True, blank=True, verbose_name='Tipo de Vehículo')
    nombrePropietario = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre Propietario')
    rutPropietario = models.CharField(max_length=30, null=True, blank=True, verbose_name='Rut Propietario')
    tipoDocumento = models.CharField(max_length=20, choices=[(v, v) for k, v in tipodocumento], null=True, blank=True, verbose_name='Tipo Documento') 
    tipoCombustible = models.CharField(max_length=20, choices=[(v, v) for k, v in tipocombustible], null=True, blank=True, verbose_name='Tipo Combustible') 
    fechaVencimiento = models.DateTimeField(auto_now=False, null=True, blank=True, verbose_name='Fecha Vencimiento')
    fechacreacion = models.DateTimeField(null=False, default=timezone.now)
    faena = models.CharField(max_length=100, null=True, blank=True, verbose_name='Faena')
    actual = models.BooleanField(default=True, verbose_name="Registro Actual")
    status = models.BooleanField(null=True, verbose_name='Estado')
    creador = models.CharField(max_length=50, verbose_name='Creador', null=True)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{} {}".format(self.vehiculo, self.numeroTarjeta)
        
    class Meta:
        verbose_name = 'Tarjeta de Combustible'
        verbose_name_plural = 'Tarjetas de Combustible'
        db_table = 'vehicle_fuel_cards' 

class HistorialDocumentacionVehiculo(models.Model):
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE)
    documento_modificado = models.CharField(max_length=100, verbose_name='Documento Modificado')
    accion = models.CharField(max_length=50, verbose_name='Acción')
    archivo = models.CharField(max_length=500, null=True, blank=True, verbose_name='Ruta del Archivo')
    creador = models.CharField(max_length=100, verbose_name='Usuario', null=True)
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de Vencimiento')
    fechacreacion = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f"{self.vehiculo.placaPatente} - {self.documento_modificado} - {self.accion}"

    class Meta:
        verbose_name = 'Historial de Documentación'
        verbose_name_plural = 'Historiales de Documentación'
        db_table = 'vehicle_documentation_history'