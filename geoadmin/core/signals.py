from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OcultarOpcionesVehiculo, Tipo
from vehicle.models import Vehiculo, InformacionTecnicaVehiculo, DocumentacionesVehiculo

@receiver(post_save, sender=OcultarOpcionesVehiculo)
def actualizar_vehiculos(sender, instance, **kwargs):
    tipo = Tipo.objects.get(tipo=instance.tipo_vehiculo)
    vehiculos = Vehiculo.objects.filter(tipo=tipo.id)
    for vehiculo in vehiculos:
        completado = calcular_completitud(vehiculo, instance)
        vehiculos.update(completado=completado)

def calcular_completitud(vehiculo, opciones):
    documentacionVehiculo = DocumentacionesVehiculo.objects.get(vehiculo_id=vehiculo.id)
    informacionTecnicaVehiculo = InformacionTecnicaVehiculo.objects.get(vehiculo_id=vehiculo.id)
    campos_completos_vehiculo, total_campos_vehiculo = vehiculo.calcular_completitud_vehiculo()
    campos_completos_informacion, total_campos_informacion = informacionTecnicaVehiculo.calcular_completitud_informacion_tecnica()
    campos_completos_documentacion, total_campos_documentacion = documentacionVehiculo.calcular_completitud_documentaciones()
    campos_completos = 16 + campos_completos_vehiculo + campos_completos_informacion + campos_completos_documentacion
    total_campos = 16 + total_campos_vehiculo + total_campos_informacion + total_campos_documentacion
    porcentaje_completitud = (campos_completos / total_campos) * 100    
    return porcentaje_completitud
