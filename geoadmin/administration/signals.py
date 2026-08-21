from django.db.models.signals import pre_save, post_save, post_delete
from .models import HistorialCambio
from .middleware import get_current_user
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import MaterialesSonda, MaterialesCaseta
import inspect

from vehicle.models import (
    Vehiculo, InformacionTecnicaVehiculo, DocumentacionesVehiculo,
    InfraccionesVehiculo, NuevoKilometraje, NuevaTarjetaCombustible,
    AyudaTecnicaVehiculo, MarcaSomnolencia, ModeloSomnolencia,
    HistorialDocumentacionVehiculo
)

from user.models import (
    User, Usuario, UsuarioProfile, UserInformacionLaboral, 
    LicenciasUsuario, DocumentacionUsuario
)

from core.models import (
    Genero, Ciudad, Nacionalidad, Ano, Marca, Modelo, Color, Tipo,
    Faena, TipoDocumentoFaena, EmpresaServicios, EmpresaTipoServicios,
    CategoriaFallaVehiculo, TipoFallaVehiculo, ProblemaVehiculo,
    OcultarOpcionesVehiculo, TipoDocumentoFaenaGeneral, TipoMaquinaria,
    MarcaMaquinaria, KitsMaquinaria, FallaMaquinaria, FechasImportantes,
    ReporteError, AyudaManuales, Sondas, Sondajes, Diametros, TipoTerreno,
    Orientacion, Perforistas, DetalleControlHorario, Corona, Escareador,
    CantidadAgua, Aditivos, Casing, Zapata, LargoBarra, Campana, Programa,
    Recomendacion, RecomendacionAjuste, RecomendacionFinal, MaterialesSonda,
    MaterialesCaseta
)

from prevencion.models import (
    PrevencionPlantilla, PrevencionNotificacionAprobacion, PrevencionNotificacionDocumento,
    PrevencionHistorialAutorizacion, PrevencionDocumento, PrevencionDocumentoDifusionTrabajador,
    PrevencionHistorialDifusionTrabajador, PrevencionResultadoCurso, PrevencionResultadoCursoIntento,
    PrevencionPermisoLlenado, PrevencionEvidenciaGeneral, PrevencionEvidenciaSeccion,
    VigilanciaGes, VigilanciaArea, VigilanciaCargo, VigilanciaTipoContrato, VigilanciaContrato,
    VigilanciaEvaluacionRiesgo, VigilanciaExposicion, VigilanciaNivelRiesgo, VigilanciaGradoExposicion,
    VigilanciaNivelSeguimiento, VigilanciaEstado, DocumentoCharla, DocumentoInformativo,
    DocumentoDifusion, DocumentoCurso, HigieneCualitativa, HigieneCuantitativa, Vigilancia,
    VigilanciaMedica, Egreso, EgresoAdjuntoHistorico, VigilanciaAdjunto, PrevencionEvidenciaItem, ValidacionDobleFactor
)

from planning.models import (
    PlanificacionFaenas, PlanificacionCampanas, PlanificacionPrograma
)

from mining.models import (
    VehiculoAsignado, DocumentoPorFaena
)

from maintenance.models import (
    NuevaSolicitudMantenimiento, HistorialSolicitudMantenimiento,
    SolicitudMantenimientoProblemas, NuevaSolicitudMantenimientoMaquinaria,
    HistorialSolicitudMantenimientoMaquinaria, SolicitudMantenimientoProblemasMaquinaria,
    Mantenimiento
)

from machine.models import (
    Maquinaria, MaquinariaFaena, NuevoHorometro,
    KitsMaquinariaFaena, HistorialStockKitsMaquinariaFaena
)

from inventory.models import (
    SeccionItems, CategoriaItems, DuracionItems, Items,
    StockItems, StockItemsHistorico, StockEgresoItems
)

from equipment.models import (
    TipoEquipo, MarcaEquipo, NuevoEquipamiento
)

from drilling.models import (
    ReportesOperacionales, DetallesPerforaciones, ControlesHorarios,
    DetalleAditivos, Insumos, LongitudPozos, ObservacionesReportes,
    ParticipantesPerforacion, DocumentosReportesPerforaciones
)

from checklist.models import (
    ChecklistMaterialesSonda, ChecklistMaterialesCaseta,
    EstadoEtapasReporteDigital, HistorialMovimientoCaseta, CasetaSondajeAsociado,
)

def obtener_rol_exacto_seccion(user, app_label):
    try:
        perfil = user.usuarioprofile
    except:
        return "SIN ASIGNAR"

    seccion_visual = None
    for frame_record in inspect.stack():
        req = frame_record[0].f_locals.get('request')
        if req and hasattr(req, 'session'):
            seccion_visual = req.session.get('seccion')
            break

    secciones_dict = {
        'vehicular': ('Registro Vehicular', perfil.seccionVehicular),
        'sondaje': ('Sondajes', perfil.seccionSondaje),
        'prevencion': ('Prevención', perfil.seccionPrevencion),
        'inventario': ('Inventario', perfil.seccionInventario),
        'administracion': ('Administración', perfil.seccionAdministracion),
    }

    if seccion_visual and seccion_visual in secciones_dict:
        nombre_sec, rol_sec = secciones_dict[seccion_visual]
        if rol_sec not in [None, '', 'SIN ASIGNAR', 'No']:
            return f"{rol_sec} ({nombre_sec})"

    app_label = str(app_label).lower()
    mapeo_app = {
        'vehicle': 'vehicular', 'maintenance': 'vehicular', 'machine': 'vehicular',
        'drilling': 'sondaje', 'planning': 'sondaje', 'checklist': 'sondaje', 'mining': 'sondaje',
        'prevencion': 'prevencion',
        'inventory': 'inventario', 'equipment': 'inventario',
        'user': 'administracion', 'core': 'administracion', 'administration': 'administracion'
    }

    seccion_db = mapeo_app.get(app_label, 'administracion')
    nombre_sec_db, rol_sec_db = secciones_dict.get(seccion_db, ('Administración', "SIN ASIGNAR"))

    if rol_sec_db not in [None, '', 'SIN ASIGNAR', 'No']:
        return f"{rol_sec_db} ({nombre_sec_db})"

    for key, (nombre, valor) in secciones_dict.items():
        if valor not in [None, '', 'SIN ASIGNAR', 'No']:
            return f"{valor} ({nombre})"

    return "SIN ASIGNAR"


MODELOS_A_AUDITAR = [
    Vehiculo, InformacionTecnicaVehiculo, DocumentacionesVehiculo,
    InfraccionesVehiculo, NuevoKilometraje, NuevaTarjetaCombustible,
    AyudaTecnicaVehiculo, MarcaSomnolencia, ModeloSomnolencia,
    HistorialDocumentacionVehiculo,
    User, Usuario, UsuarioProfile, UserInformacionLaboral, 
    LicenciasUsuario, DocumentacionUsuario,
    Genero, Ciudad, Nacionalidad, Ano, Marca, Modelo, Color, Tipo,
    Faena, TipoDocumentoFaena, EmpresaServicios, EmpresaTipoServicios,
    CategoriaFallaVehiculo, TipoFallaVehiculo, ProblemaVehiculo,
    OcultarOpcionesVehiculo, TipoDocumentoFaenaGeneral, TipoMaquinaria,
    MarcaMaquinaria, KitsMaquinaria, FallaMaquinaria, FechasImportantes,
    ReporteError, AyudaManuales, Sondas, Sondajes, Diametros, TipoTerreno,
    Orientacion, Perforistas, DetalleControlHorario, Corona, Escareador,
    CantidadAgua, Aditivos, Casing, Zapata, LargoBarra, Campana, Programa,
    Recomendacion, RecomendacionAjuste, RecomendacionFinal, MaterialesSonda,
    MaterialesCaseta,
    PrevencionPlantilla, PrevencionNotificacionAprobacion, PrevencionNotificacionDocumento,
    PrevencionHistorialAutorizacion, PrevencionDocumento, PrevencionDocumentoDifusionTrabajador,
    PrevencionHistorialDifusionTrabajador, PrevencionResultadoCurso, PrevencionResultadoCursoIntento,
    PrevencionPermisoLlenado, PrevencionEvidenciaGeneral, PrevencionEvidenciaSeccion,
    VigilanciaGes, VigilanciaArea, VigilanciaCargo, VigilanciaTipoContrato, VigilanciaContrato,
    VigilanciaEvaluacionRiesgo, VigilanciaExposicion, VigilanciaNivelRiesgo, VigilanciaGradoExposicion,
    VigilanciaNivelSeguimiento, VigilanciaEstado, DocumentoCharla, DocumentoInformativo,
    DocumentoDifusion, DocumentoCurso, HigieneCualitativa, HigieneCuantitativa, Vigilancia,
    VigilanciaMedica, Egreso, EgresoAdjuntoHistorico, VigilanciaAdjunto, PrevencionEvidenciaItem,
    PlanificacionFaenas, PlanificacionCampanas, PlanificacionPrograma,
    VehiculoAsignado, DocumentoPorFaena,
    NuevaSolicitudMantenimiento, HistorialSolicitudMantenimiento,
    SolicitudMantenimientoProblemas, NuevaSolicitudMantenimientoMaquinaria,
    HistorialSolicitudMantenimientoMaquinaria, SolicitudMantenimientoProblemasMaquinaria,
    Mantenimiento,
    Maquinaria, MaquinariaFaena, NuevoHorometro,
    KitsMaquinariaFaena, HistorialStockKitsMaquinariaFaena,
    SeccionItems, CategoriaItems, DuracionItems, Items,
    StockItems, StockItemsHistorico, StockEgresoItems,
    TipoEquipo, MarcaEquipo, NuevoEquipamiento,
    ReportesOperacionales, DetallesPerforaciones, ControlesHorarios,
    DetalleAditivos, Insumos, LongitudPozos, ObservacionesReportes,
    ParticipantesPerforacion, DocumentosReportesPerforaciones,
    ChecklistMaterialesSonda, ChecklistMaterialesCaseta,
    EstadoEtapasReporteDigital, HistorialMovimientoCaseta, CasetaSondajeAsociado, ValidacionDobleFactor
]

CAMPOS_IGNORADOS = ['id', 'password', 'last_login']

def preparar_auditoria(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    instance._cambios_detectados = []
    
    for field in instance._meta.fields:
        if field.name in CAMPOS_IGNORADOS:
            continue

        field_name = field.name
        old_value = getattr(old_instance, field_name)
        new_value = getattr(instance, field_name)

        if str(old_value) != str(new_value):
            val_ant = str(old_value)
            
            if sender._meta.app_label == 'vehicle' and '-' in val_ant and len(val_ant) >= 10:
                val_ant = val_ant[:7]

            instance._cambios_detectados.append({
                'campo': field.verbose_name or field_name,
                'valor_anterior': val_ant,
                'field_name': field_name
            })

def ejecutar_auditoria(sender, instance, created, **kwargs):
    user = get_current_user()
    if not user or not user.is_authenticated:
        return

    instance_final = sender.objects.get(pk=instance.pk)

    if created:
        detalles_campos = []
        for field in instance_final._meta.fields:
            if field.name in CAMPOS_IGNORADOS: 
                continue
                
            val = getattr(instance_final, field.name)
            
            if val not in [None, '', 'documentacion_vehiculo/no-imagen.png', 'documentacion_vehiculo/no-imagen-vehiculo.png', 'documentacion_usuario/no-avatar.png', 'documentacion_usuario/no-imagen.png', 'base/no-imagen.png', 'base/no-imagen2.png', 'inventario_item/no-imagen-item.png', 'checklist_caseta/no-imagen.png']:
                if val is True:
                    val_str = "Habilitado"
                elif val is False:
                    val_str = "Deshabilitado"
                elif sender._meta.app_label == 'vehicle' and '-' in str(val) and len(str(val)) >= 10:
                    val_str = str(val)[:7]
                else:
                    val_str = val
                detalles_campos.append(f"• {field.verbose_name or field.name}: {val_str}")
        
        if detalles_campos:
            HistorialCambio.objects.create(
                rut_usuario=user.username,
                nombre_usuario=f"{user.first_name} {user.last_name}",
                rol_usuario=obtener_rol_exacto_seccion(user, sender._meta.app_label),
                seccion=sender._meta.app_label,
                modelo_afectado=sender.__name__,
                registro_id=instance.pk,
                nombre_registro=f"{sender._meta.verbose_name.title()} ({str(instance_final)})",
                accion='Creado',
                campo_modificado='Registro Completo',
                valor_anterior='-',
                valor_nuevo="\n".join(detalles_campos)
            )
        return

    cambios = getattr(instance, '_cambios_detectados', [])
    for c in cambios:
        val_raw = getattr(instance_final, c['field_name'])
        valor_nuevo_final = str(val_raw)
        
        if sender._meta.app_label == 'vehicle' and '-' in valor_nuevo_final and len(valor_nuevo_final) >= 10:
            valor_nuevo_final = valor_nuevo_final[:7]

        HistorialCambio.objects.create(
            rut_usuario=user.username,
            nombre_usuario=f"{user.first_name} {user.last_name}",
            rol_usuario=obtener_rol_exacto_seccion(user, sender._meta.app_label),
            seccion=sender._meta.app_label,
            modelo_afectado=sender.__name__,
            registro_id=instance.pk,
            nombre_registro=f"{sender._meta.verbose_name.title()} ({str(instance_final)})",
            accion='Editado',
            campo_modificado=c['campo'],
            valor_anterior=c['valor_anterior'],
            valor_nuevo=valor_nuevo_final
        )

def auditar_delete(sender, instance, **kwargs):
    user = get_current_user()
    if not user or not user.is_authenticated:
        return

    HistorialCambio.objects.create(
        rut_usuario=user.username,
        nombre_usuario=f"{user.first_name} {user.last_name}",
        rol_usuario=obtener_rol_exacto_seccion(user, sender._meta.app_label),
        seccion=sender._meta.app_label,
        modelo_afectado=sender.__name__,
        registro_id=instance.pk,
        nombre_registro=f"{sender._meta.verbose_name.title()} ({str(instance)})",
        accion='Eliminado',
        campo_modificado='Registro Completo',
        valor_anterior=str(instance),
        valor_nuevo='-'
    )

for modelo in MODELOS_A_AUDITAR:
    pre_save.connect(preparar_auditoria, sender=modelo)
    post_save.connect(ejecutar_auditoria, sender=modelo)
    post_delete.connect(auditar_delete, sender=modelo)