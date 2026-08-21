from django.db import models
from django.utils import timezone

class HistorialCambio(models.Model):
    rut_usuario = models.CharField(max_length=20, null=True, blank=True, verbose_name='RUT')
    nombre_usuario = models.CharField(max_length=200, null=True, blank=True, verbose_name='Nombre Completo')
    rol_usuario = models.CharField(max_length=100, null=True, blank=True, verbose_name='Rol')
    
    fecha_modificacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Modificación')
    
    seccion = models.CharField(max_length=100, verbose_name='Sección del Sistema')
    modelo_afectado = models.CharField(max_length=100, verbose_name='Modelo/Formulario')
    registro_id = models.IntegerField(verbose_name='ID del Registro')

    accion = models.CharField(max_length=20, default='Editado', verbose_name='Acción')
    nombre_registro = models.CharField('Registro Afectado', max_length=255, null=True, blank=True)
    
    campo_modificado = models.CharField(max_length=100, verbose_name='Campo')
    valor_anterior = models.TextField(null=True, blank=True, verbose_name='Valor Anterior')
    valor_nuevo = models.TextField(null=True, blank=True, verbose_name='Valor Nuevo')

    class Meta:
        verbose_name = 'Historial de Cambio'
        verbose_name_plural = 'Historiales de Cambios'
        db_table = 'admin_audit_log'
        ordering = ['-fecha_modificacion']

    def __str__(self):
        return f"{self.fecha_modificacion} - {self.nombre_usuario} ({self.modelo_afectado})"
    
def obtener_rol_seccion_formateado(user, app_label):
    if not user or not getattr(user, 'is_authenticated', False):
        return 'N/A'
    
    nombres_secciones = {
        'vehicle': 'Vehicular',
        'user': 'Usuario',
        'prevencion': 'Prevención',
        'drilling': 'Perforación',
        'planning': 'Planificación', 
        'mining': 'Minería', 
        'maintenance': 'Mantención',
        'machine': 'Maquinaria', 
        'inventory': 'Inventario', 
        'equipment': 'Equipos',
        'documentation': 'Documentos',
        'core': 'General',
        'checklist': 'Checklist'
    }
    nombre_seccion = nombres_secciones.get(app_label, app_label.capitalize())
    
    mapa_perfil = {
        'vehicle': 'seccionVehicular',
        'drilling': 'seccionSondaje',
        'prevencion': 'seccionPrevencion',
        'inventory': 'seccionInventario',
        'user': 'seccionAdministracion',
        'core': 'seccionAdministracion',
        'planning': 'seccionAdministracion',
        'mining': 'seccionAdministracion',
        'maintenance': 'seccionAdministracion',
        'machine': 'seccionAdministracion',
        'equipment': 'seccionAdministracion',
        'documentation': 'seccionAdministracion',
        'checklist': 'seccionAdministracion',
    }
    rol_seccion = 'Sin Asignar'
    
    try:
        if hasattr(user, 'usuarioprofile'):
            campo_perfil = mapa_perfil.get(app_label)
            if campo_perfil:
                rol_obtenido = getattr(user.usuarioprofile, campo_perfil, None)
                if rol_obtenido:
                    rol_seccion = rol_obtenido
    except Exception:
        pass
        
    rol_formateado = rol_seccion.title() if isinstance(rol_seccion, str) else str(rol_seccion)
    
    return f"{rol_formateado} ({nombre_seccion})"