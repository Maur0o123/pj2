from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from vehicle.models import Vehiculo, NuevoKilometraje, NuevaTarjetaCombustible
from machine.models import Maquinaria, NuevoHorometro, KitsMaquinariaFaena, HistorialStockKitsMaquinariaFaena
from maintenance.models import NuevaSolicitudMantenimiento, NuevaSolicitudMantenimientoMaquinaria
from user.models import User, UsuarioProfile
from drilling.models import ReportesOperacionales
from inventory.models import Items
from core.models import KitsMaquinaria, ReporteError
from checklist.models import ChecklistMaterialesSonda, ChecklistMaterialesCaseta
from prevencion.models import PrevencionPlantilla, PrevencionDocumento
from administration.middleware import get_current_user
from .utils import notify_group, get_changes_message, notify_multiple_groups

@receiver(pre_save, sender=Vehiculo)
@receiver(pre_save, sender=Maquinaria)
@receiver(pre_save, sender=User)
@receiver(pre_save, sender=ReportesOperacionales)
@receiver(pre_save, sender=Items)
@receiver(pre_save, sender=KitsMaquinaria)
@receiver(pre_save, sender=KitsMaquinariaFaena)
@receiver(pre_save, sender=UsuarioProfile)
@receiver(pre_save, sender=ChecklistMaterialesSonda)
@receiver(pre_save, sender=ChecklistMaterialesCaseta)
@receiver(pre_save, sender=PrevencionPlantilla)
@receiver(pre_save, sender=PrevencionDocumento)
@receiver(pre_save, sender=ReporteError)
def capture_old_state(sender, instance, **kwargs):
    """Guarda el estado anterior del objeto antes de ser modificado."""
    try:
        if instance.pk:
            instance._old_instance = sender.objects.get(pk=instance.pk)
        else:
            instance._old_instance = None
    except sender.DoesNotExist:
        instance._old_instance = None

@receiver(post_save, sender=Vehiculo)
def notify_vehicle_change(sender, instance, created, **kwargs):
    """Notifica cambios detallados en vehículos."""
    user = get_current_user()
    if user and hasattr(user, 'get_full_name'):
        user_name = user.get_full_name() or user.username
    else:
        user_name = "Sistema"
    
    if created:
        subject = f"Nuevo Vehículo Registrado: {instance.placaPatente}"
        message = f"Registro de Vehículo por: {user_name}\n\n"
        message += "Detalle de cambios:\n"
        message += f"- Patente: {instance.placaPatente}\n"
        message += f"- Tipo: {instance.tipo}\n"
        message += f"- Marca: {instance.marca}"
        notify_group('admin_vehiculos_maquinaria', subject, message)
    else:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        if not changes: return

        estado = "Habilitado" if instance.status else "Deshabilitado"
        subject = f"Vehículo Actualizado: {instance.placaPatente}"
        message = f"Se han detectado cambios en el vehículo {instance.placaPatente}.\n\nActualizado por: {user_name}"
        message += changes
        notify_group('admin_vehiculos_maquinaria', subject, message)

@receiver(post_save, sender=User)
def notify_user_change(sender, instance, created, **kwargs):
    """Notifica cambios detallados en usuarios."""
    perfil = getattr(instance, 'usuarioprofile', None)
    
    user = get_current_user()
    if user and hasattr(user, 'get_full_name'):
        user_name = user.get_full_name() or user.username
    else:
        user_name = "Sistema"

    if created:
        subject = f"Nuevo Usuario Creado: {instance.get_full_name()}"
        message = (
            f"Se ha creado un nuevo usuario en la plataforma.\n\n"
            f"Nombre: {instance.get_full_name()}\n"
            f"Email: {instance.email}\n"
        )
        if perfil:
            message += (
                f"\nAccesos por Sección:\n"
                f"- Vehicular: {perfil.seccionVehicular}\n"
                f"- Sondaje: {perfil.seccionSondaje}\n"
                f"- Prevención: {perfil.seccionPrevencion}\n"
                f"- Inventario: {perfil.seccionInventario}\n"
                f"- Administración: {perfil.seccionAdministracion}"
            )
        notify_group('usuarios', subject, message)
    else:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        if not changes: return

        estado = "Activo" if instance.is_active else "Inactivo"
        subject = f"Usuario Modificado: {instance.get_full_name()}"
        message = f"Se han actualizado los datos del usuario {instance.get_full_name()}.\n\nActualizado por: {user_name}"
        message += changes
        notify_group('usuarios', subject, message)
        if perfil:
            message += (
                f"\n\nConfiguración de Secciones Actual:\n"
                f"- Vehicular: {perfil.seccionVehicular}\n"
                f"- Sondaje: {perfil.seccionSondaje}\n"
                f"- Prevención: {perfil.seccionPrevencion}\n"
                f"- Inventario: {perfil.seccionInventario}\n"
                f"- Administración: {perfil.seccionAdministracion}"
            )

@receiver(post_save, sender=UsuarioProfile)
def notify_user_profile_change(sender, instance, created, **kwargs):
    """Notifica cambios en los permisos y secciones del usuario."""
    user_actor = get_current_user()
    
    if user_actor and getattr(user_actor, 'is_authenticated', False) and hasattr(user_actor, 'get_full_name'):
        user_actor_name = user_actor.get_full_name() or user_actor.username
    else:
        user_actor_name = "Sistema / Registro Público"
    
    if not created:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        
        if not changes: 
            return
        estado = "Activo" if instance.user.is_active else "Inactivo"   
        user_target_name = instance.user.get_full_name() or instance.user.username
        subject = f"Permisos de Usuario Modificados: {user_target_name}"
        message = f"Actualización de Permisos por: {user_actor_name}\n\n"
        message += f"Usuario afectado: {user_target_name}\n"
        message += f"Estado de cuenta: {estado}\n"
        message += "\nDetalle de cambios:"
        message += changes
        
        notify_group('usuarios', subject, message)

@receiver(post_save, sender=Maquinaria)
def notify_machine_change(sender, instance, created, **kwargs):
    """Notifica cambios detallados en maquinarias."""
    user = get_current_user()
    if user and hasattr(user, 'get_full_name'):
        user_name = user.get_full_name() or user.username
    else:
        user_name = "Sistema"
    
    if created:
        subject = f"Nueva Maquinaria Registrada: {instance.maquinaria}"
        message = f"Registro de Maquinaria por: {user_name}\n\n"
        message += "Detalle de cambios:\n"
        message += f"- Nombre: {instance.maquinaria}\n"
        message += f"- Tipo: {instance.tipo}\n"
        message += f"- Marca: {instance.marca}"
        notify_group('admin_vehiculos_maquinaria', subject, message)
    else:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        if not changes: return

        subject = f"Maquinaria Actualizada: {instance.maquinaria}"
        message = f"Se han detectado cambios en la maquinaria {instance.maquinaria}.\n\nActualizado por: {user_name}"
        message += changes
        notify_group('admin_vehiculos_maquinaria', subject, message)

@receiver(post_save, sender=ReportesOperacionales)
def notify_drilling_change(sender, instance, created, **kwargs):
    """Notifica cambios detallados en reportes de sondaje."""
    user = get_current_user()
    if user and hasattr(user, 'get_full_name'):
        user_name = user.get_full_name() or user.username
    else:
        user_name = "Sistema"

    if created:
        subject = f"Nuevo Reporte de Sondaje: {instance}"
        message = f"Se ha creado un nuevo reporte operacional de sondaje.\n\nSonda: {instance.sonda}\nSondaje: {instance.sondajeCodigo}\nCreado por: {user_name}"
        notify_group('sondaje_general', subject, message)
    else:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        if not changes: return

        subject = f"Reporte de Sondaje Modificado: {instance}"
        message = f"Se han actualizado los datos del reporte operacional.\n\nActualizado por: {user_name}"
        message += changes
        notify_group('sondaje_general', subject, message)

@receiver(post_save, sender=Items)
def notify_inventory_change(sender, instance, created, **kwargs):
    """Notifica cambios detallados en items de inventario."""
    user = get_current_user()
    if user and hasattr(user, 'get_full_name'):
        user_name = user.get_full_name() or user.username
    else:
        user_name = "Sistema"

    if created:
        subject = f"Nuevo Item en Inventario: {instance.item}"
        message = f"Se ha registrado un nuevo item en el inventario.\n\nNombre: {instance.item}\nSección: {instance.seccion}\nCategoría: {instance.categoria}\nCreado por: {user_name}"
        notify_group('registro_equipos', subject, message)
    else:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        if not changes: return

        subject = f"Item de Inventario Modificado: {instance.item}"
        message = f"Se han detectado cambios en el item de inventario.\n\nActualizado por: {user_name}"
        message += changes
        notify_group('registro_equipos', subject, message)

@receiver(post_save, sender=KitsMaquinaria)
def notify_kits_change(sender, instance, created, **kwargs):
    """Notifica cambios detallados en kits de maquinaria con formato estandarizado."""
    user = get_current_user()
    user_name = user.get_full_name() or user.username if user else "Sistema"
    
    if created:
        subject = f"Nuevo Kit de Reparación: {instance.nombreKit}"
        message = f"Registro de Kit por: {user_name}\n\n"
        message += "Detalle de cambios:\n"
        message += f"- Nombre: {instance.nombreKit}\n"
        message += f"- Marca/Modelo: {instance.marcaMaquina}\n"
        message += f"- Stock Mínimo: {instance.stockMinimo}\n"
        message += f"- Stock Máximo: {instance.stockMaximo}"
        notify_group('mantenimiento_sistema', subject, message)
    else:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        if not changes: return

        subject = f"Kit de Reparación Actualizado: {instance.nombreKit}"
        message = f"Actualización de Kit por: {user_name}\n\n"
        message += changes
        notify_group('mantenimiento_sistema', subject, message)

@receiver(post_save, sender=KitsMaquinariaFaena)
def notify_kit_faena_change(sender, instance, created, **kwargs):
    """Notifica la asignación de un kit a una faena con formato estandarizado."""
    user = get_current_user()
    user_name = user.get_full_name() or user.username if user else "Sistema"
    
    if created:
        subject = f"Kit Asignado a Faena: {instance.kitMaquinaria.nombreKit}"
        message = f"Asignación de Kit por: {user_name}\n\n"
        message += "Detalle de cambios:\n"
        message += f"- Kit: {instance.kitMaquinaria.nombreKit}\n"
        message += f"- Faena: {instance.faena}"
        notify_group('registro_equipos', subject, message)

@receiver(post_save, sender=HistorialStockKitsMaquinariaFaena)
def notify_stock_kit_change(sender, instance, created, **kwargs):
    """Notifica el movimiento de stock de un kit enfocándose solo en lo modificado."""
    if created:
        user_name = instance.creador or "Sistema"
        subject = f"Movimiento de Stock: {instance.kitMaquinaria.kitMaquinaria.nombreKit} ({instance.faena})"
        
        message = f"Ajuste de Stock por: {user_name}\n\n"
        message += "Detalle de cambios:\n"
        message += f"- Movimiento: {instance.stockMovimiento} unidades\n"
        message += f"- Stock Actual: {instance.stockActual}\n"
        if instance.descripcion:
            message += f"- Descripción: {instance.descripcion}"
        
        notify_group('registro_equipos', subject, message)
@receiver(post_save, sender=NuevoKilometraje)
def notify_kilometraje_new(sender, instance, created, **kwargs):
    """Notifica el registro de un nuevo kilometraje."""
    if created:
        try:
            subject = f"Nuevo Kilometraje: {instance.vehiculo} ({instance.kilometraje} KM)"
            message = f"Nuevo Kilometraje Registrado\n\nVehículo: {instance.vehiculo}\nKilometraje: {instance.kilometraje} KM\nRegistrado por: {instance.creador}"
            notify_group('mantenimiento_km_horometros', subject, message)
        except Exception as e:
            print(f"Error al enviar notificación de kilometraje: {e}")

@receiver(post_save, sender=NuevoHorometro)
def notify_horometro_new(sender, instance, created, **kwargs):
    """Notifica el registro de un nuevo horómetro."""
    if created:
        try:
            subject = f"Nuevo Horómetro: {instance.maquinaria} ({instance.horometro} Hrs)"
            message = f"Nuevo Horómetro Registrado\n\nMaquinaria: {instance.maquinaria}\nHorómetro: {instance.horometro} Hrs\nRegistrado por: {instance.creador}"
            notify_group('mantenimiento_km_horometros', subject, message)
        except Exception as e:
            print(f"Error al enviar notificación de horómetro: {e}")

@receiver(post_save, sender=NuevaTarjetaCombustible)
def notify_fuel_card_new(sender, instance, created, **kwargs):
    """Notifica el registro o actualización de una tarjeta de combustible."""
    if created:
        try:
            # Buscar si existe una tarjeta anterior para el mismo vehículo para saber si es edición
            previous_card = NuevaTarjetaCombustible.objects.filter(
                vehiculo=instance.vehiculo
            ).exclude(pk=instance.pk).order_by('-pk').first()

            if previous_card:
                # Es una edición/modificación
                changes = get_changes_message(previous_card, instance)
                if not changes:
                    return

                subject = f"Tarjeta de Combustible Modificada: {instance.patente}"
                message = (
                    f"Se han actualizado los datos de la tarjeta de combustible para el vehículo {instance.patente}.\n\n"
                    f"Actualizado por: {instance.creador}"
                    f"{changes}"
                )
            else:
                # Es un nuevo registro
                subject = f"Tarjeta de Combustible Registrada: {instance.patente}"
                # Manejar campos que pueden ser None para que no se vea feo o falle
                vencimiento_str = instance.fechaVencimiento.strftime('%d/%m/%Y') if instance.fechaVencimiento else "No especificado"
                faena_str = str(instance.faena) if instance.faena else "Sin asignar"
                
                message = (
                    f"Se ha registrado una nueva tarjeta de combustible en el sistema.\n\n"
                    f"Vehículo: {instance.patente}\n"
                    f"Tipo Vehículo: {instance.tipoVehiculo}\n"
                    f"Propietario: {instance.nombrePropietario}\n"
                    f"N° Tarjeta: {instance.numeroTarjeta}\n"
                    f"Tipo Documento: {instance.tipoDocumento}\n"
                    f"Tipo Combustible: {instance.tipoCombustible}\n"
                    f"Vencimiento: {vencimiento_str}\n"
                    f"Faena: {faena_str}\n"
                    f"Registrado por: {instance.creador}"
                )

            # Notificar a ambos grupos de forma unificada para evitar destinatarios duplicados
            notify_multiple_groups(['admin_vehiculos_maquinaria', 'mantenimiento_km_horometros'], subject, message)
        except Exception as e:
            print(f"Error al enviar notificación de tarjeta: {e}")



@receiver(post_save, sender=PrevencionPlantilla)
def notify_capacitacion_change(sender, instance, created, **kwargs):
    """Notifica cambios limpios en Plantillas/Capacitaciones."""
    user = get_current_user()
    user_name = user.get_full_name() or user.username if user else "Sistema"

    if created:
        subject = f"Nueva Plantilla/Capacitación: {instance.nombre}"
        message = f"Creación por: {user_name}\n\n"
        message += "Detalle de cambios:\n"
        message += f"- Nombre: {instance.nombre}\n"
        message += f"- Tipo: {instance.get_tipo_display() if hasattr(instance, 'get_tipo_display') else getattr(instance, 'tipo', '')}"
        notify_group('prevencion_general', subject, message)
    else:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        if not changes: return

        subject = f"Capacitación/Plantilla Actualizada: {instance.nombre}"
        message = f"Actualización por: {user_name}\n\n"
        message += changes
        notify_group('prevencion_general', subject, message)

@receiver(post_save, sender=PrevencionDocumento)
def notify_documento_change(sender, instance, created, **kwargs):
    """Notifica cambios limpios en Documentación."""
    user = get_current_user()
    user_name = user.get_full_name() or user.username if user else "Sistema"

    plantilla_nombre = instance.plantilla_base.nombre if instance.plantilla_base else "Documento Genérico"

    if created:
        subject = f"Nuevo Documento Registrado: {plantilla_nombre}"
        message = f"Creación por: {user_name}\n\n"
        message += "Detalle de cambios:\n"
        message += f"- Plantilla Base: {plantilla_nombre}\n"
        message += f"- Faena: {instance.faena}"
        notify_group('prevencion_general', subject, message)
    else:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        if not changes: return

        subject = f"Documento Actualizado: {plantilla_nombre}"
        message = f"Actualización por: {user_name}\n\n"
        message += changes
        notify_group('prevencion_general', subject, message)

@receiver(post_save, sender=NuevaSolicitudMantenimientoMaquinaria)
def notify_machine_maintenance_new(sender, instance, created, **kwargs):
    """Notifica el registro de un nuevo mantenimiento de maquinaria."""
    if created:
        try:
            creador = instance.solicitante.get_full_name() or instance.solicitante.username
            subject = f"Nuevo Mantenimiento Maquinaria: {instance.maquinaria}"
            message = (
                f"Nuevo Mantenimiento Maquinaria Registrado\n\n"
                f"Maquinaria: {instance.maquinaria}\n"
                f"Horómetro: {instance.horometro} Hrs\n"
                f"Registrado por: {creador}"
            )
            notify_group('mantenimiento_km_horometros', subject, message)
        except Exception as e:
            print(f"Error al enviar notificación de mantenimiento maquinaria: {e}")

@receiver(post_save, sender=NuevaSolicitudMantenimiento)
def notify_vehicle_maintenance_new(sender, instance, created, **kwargs):
    """Notifica el registro de un nuevo mantenimiento de vehículo."""
    if created:
        try:
            creador = instance.solicitante.get_full_name() or instance.solicitante.username
            subject = f"Nuevo Mantenimiento: {instance.vehiculo}"
            message = (
                f"Nuevo Mantenimiento Registrado\n\n"
                f"Vehículo: {instance.vehiculo}\n"
                f"Patente: {instance.patente}\n"
                f"Kilometraje: {instance.kilometraje} KM\n"
                f"Registrado por: {creador}"
            )
            notify_group('mantenimiento_km_horometros', subject, message)
        except Exception as e:
            print(f"Error al enviar notificación de mantenimiento vehicular: {e}")

@receiver(post_save, sender=ReporteError)
def notify_error_change(sender, instance, created, **kwargs):
    """Notifica reportes de error al equipo técnico."""
    user = get_current_user()
    
    # Manejar caso en el que el usuario viene de get_current_user o del propio modelo
    if user and hasattr(user, 'get_full_name'):
        user_name = user.get_full_name() or user.username
    elif hasattr(instance, 'usuario'):
        user_name = str(instance.usuario)
    else:
        user_name = "Sistema"

    titulo_error = getattr(instance, 'tituloError', getattr(instance, 'titulo', str(instance.id)))

    if created:
        subject = f"NUEVO REPORTE DE ERROR: {titulo_error}"
        message = f"Reporte enviado por: {user_name}\n\n"
        message += "Detalle de cambios:\n"
        message += f"- Título: {titulo_error}\n"
        if hasattr(instance, 'prioridad'):
            message += f"- Prioridad: {instance.prioridad}\n"
        if hasattr(instance, 'estado'):
            message += f"- Estado: {instance.estado}"
        notify_group('mantenimiento_sistema', subject, message)
    else:
        old = getattr(instance, '_old_instance', None)
        changes = get_changes_message(old, instance)
        if not changes: return

        subject = f"Actualización Error: {titulo_error}"
        message = f"Actualización de Error por: {user_name}\n\n"
        message += changes
        notify_group('mantenimiento_sistema', subject, message)
