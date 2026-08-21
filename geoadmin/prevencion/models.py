from django.db import models
from django.utils import timezone
from core.models import Faena
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from administration.managers import AuditableQuerySet
import uuid

class PrevencionPlantilla(models.Model):
    class TipoRiesgo(models.TextChoices):
        CONDICIONES = 'condiciones', _('Condiciones Generales')
        SILICE = 'silice', _('Silice')
        RUIDO = 'ruido', _('Ruido')
        HIPOBARIA = 'hipobaria', _('Hipobaria')
        PSICOSOCIAL = 'psicosocial', _('Psicosocial')
        TMERT = 'tmert', _('TMERT')
        MMC = 'mmc', _('MMC')
        CHARLAS = 'charlas', _('Charlas')
        INFORMATIVOS = 'informativos', _('Informativos')
        DIFUSIONES = 'difusiones', _('Difusiones')
        CURSOS = 'cursos', _('Cursos')

    class ModoContenido(models.TextChoices):
        ESTRUCTURA = 'estructura', _('Crear Estructura')
        PDF = 'pdf', _('Adjuntar PDF')

    nombre = models.CharField(max_length=200, verbose_name='Nombre de la Plantilla', help_text="Ej: Checklist Silice Faena Norte")
    tipo = models.CharField(max_length=20, choices=TipoRiesgo.choices, verbose_name='Tipo de Riesgo')
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, verbose_name='Faena', related_name='plantillas_prevencion')
    tiempo_estimado_minutos = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Tiempo Estimado (minutos)')
    curso_total_intentos = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Curso: Total intentos')
    curso_porcentaje_aprobacion = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Curso: Porcentaje aprobación')
    modo_contenido = models.CharField(max_length=20, choices=ModoContenido.choices, default=ModoContenido.ESTRUCTURA, verbose_name='Modo de Contenido')
    archivo_pdf = models.FileField(upload_to='prevencion/plantillas_pdf/', blank=True, null=True, verbose_name='PDF de Plantilla')
    estructura = models.JSONField(default=list, verbose_name='Estructura Dinámica')
    autorizadores = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='plantillas_prevencion_autorizadores', verbose_name='Autorizadores')
    autorizacion_incompleta = models.BooleanField(default=False, verbose_name='Autorización Incompleta')
    creador = models.CharField(max_length=50, verbose_name='Creador', null=True)
    status = models.BooleanField(default=True, verbose_name='Activo')
    fechacreacion = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

    class Meta:
        verbose_name = 'Plantilla de Prevención'
        verbose_name_plural = 'Plantillas de Prevención'
        db_table = 'prevencion_plantilla'

class PrevencionNotificacionAprobacion(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', _('Pendiente')
        ACEPTADA = 'aceptada', _('Aceptada')
        RECHAZADA = 'rechazada', _('Rechazada')
        CANCELADA = 'cancelada', _('Cancelada')

    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones_prevencion_recibidas', verbose_name='Destinatario')
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones_prevencion_enviadas', verbose_name='Solicitante')
    plantilla = models.ForeignKey('PrevencionPlantilla', on_delete=models.SET_NULL, null=True, blank=True, related_name='notificaciones_aprobacion', verbose_name='Plantilla')
    tipo_documento = models.CharField(max_length=20, blank=True, default='', verbose_name='Tipo Documento')
    titulo = models.CharField(max_length=200, default='Solicitud de aprobación de títulos', verbose_name='Título')
    descripcion = models.TextField(blank=True, default='', verbose_name='Descripción')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE, verbose_name='Estado')
    leida = models.BooleanField(default=False, verbose_name='Leída')
    fechacreacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha Creación')
    fecha_lectura = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Lectura')
    fecha_respuesta = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Respuesta')
    motivo_rechazo = models.TextField(blank=True, default='', verbose_name='Motivo Rechazo')

    objects = AuditableQuerySet.as_manager()

    class Meta:
        db_table = 'prevencion_notificacion_aprobacion'
        verbose_name = 'Notificación Aprobación Prevención'
        verbose_name_plural = 'Notificaciones Aprobación Prevención'
        ordering = ['-fechacreacion']
        indexes = [
            models.Index(fields=['destinatario', 'estado']),
            models.Index(fields=['solicitante', 'estado']),
        ]

    def __str__(self):
        return f"{self.titulo} -> {self.destinatario}"

class PrevencionNotificacionDocumento(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', _('Pendiente')
        VISTA = 'vista', _('Vista')

    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notificaciones_documento_recibidas', verbose_name='Destinatario')
    documento = models.ForeignKey('PrevencionDocumento', on_delete=models.CASCADE, related_name='notificaciones_documento', verbose_name='Documento')
    tipo_documento = models.CharField(max_length=20, blank=True, default='', verbose_name='Tipo Documento')
    titulo = models.CharField(max_length=200, default='Documento disponible', verbose_name='Título')
    descripcion = models.TextField(blank=True, default='', verbose_name='Descripción')
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE, verbose_name='Estado')
    leida = models.BooleanField(default=False, verbose_name='Leída')
    fechacreacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha Creación')
    fecha_inicio_lectura = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Inicio Lectura')
    fecha_lectura = models.DateTimeField(null=True, blank=True, verbose_name='Fecha Lectura')

    objects = AuditableQuerySet.as_manager()

    class Meta:
        db_table = 'prevencion_notificacion_documento'
        verbose_name = 'Notificación Documento Prevención'
        verbose_name_plural = 'Notificaciones Documento Prevención'
        ordering = ['-fechacreacion', '-id']
        constraints = [
            models.UniqueConstraint(fields=['destinatario', 'documento'], name='uq_prev_notif_documento_destinatario_documento')
        ]
        indexes = [
            models.Index(fields=['destinatario', 'estado']),
            models.Index(fields=['documento', 'estado']),
        ]

    def __str__(self):
        return f"{self.titulo} -> {self.destinatario}"

class PrevencionHistorialAutorizacion(models.Model):
    class Accion(models.TextChoices):
        AGREGADO = 'agregado', _('Agregado')
        ELIMINADO = 'eliminado', _('Eliminado')

    plantilla = models.ForeignKey('PrevencionPlantilla', on_delete=models.CASCADE, related_name='historial_autorizacion', verbose_name='Plantilla')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial_autorizacion_realizado', verbose_name='Usuario que realiza el cambio')
    destinatario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial_autorizacion_destinatario', verbose_name='Trabajador afectado')
    accion = models.CharField(max_length=20, choices=Accion.choices, verbose_name='Acción')
    fechacreacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha Creación')

    objects = AuditableQuerySet.as_manager()

    class Meta:
        db_table = 'prevencion_historial_autorizacion'
        verbose_name = 'Historial de Autorización Prevención'
        verbose_name_plural = 'Historiales de Autorización Prevención'
        ordering = ['-fechacreacion', '-id']
        indexes = [
            models.Index(fields=['plantilla', 'fechacreacion']),
            models.Index(fields=['accion']),
        ]

    def __str__(self):
        return f"{self.plantilla_id} - {self.get_accion_display()}"

class PrevencionDocumento(models.Model):
    plantilla_base = models.ForeignKey('PrevencionPlantilla', on_delete=models.SET_NULL, null=True)
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE)
    contenido = models.JSONField(verbose_name="Contenido Relleno")
    evidencia_general = models.FileField(upload_to='prevencion/evidencias/', blank=True, null=True)
    observacion_general = models.TextField(blank=True, null=True)
    creador = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True, verbose_name="Activo")

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"Reporte #{self.id} - {self.faena}"

class PrevencionDocumentoDifusionTrabajador(models.Model):
    documento = models.ForeignKey(PrevencionDocumento, on_delete=models.CASCADE, related_name='difusion_trabajadores')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_difusion_trabajadores')
    rut_trabajador = models.CharField(max_length=20, verbose_name='RUT')
    nombre_completo = models.CharField(max_length=200, verbose_name='Nombre Completo')
    cargo = models.CharField(max_length=120, blank=True, null=True, verbose_name='Cargo')
    area = models.CharField(max_length=120, blank=True, null=True, verbose_name='Area')
    ges = models.CharField(max_length=120, blank=True, null=True, verbose_name='GES')
    faena = models.ForeignKey(Faena, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_difusion_trabajadores', verbose_name='Faena')
    creado_por = models.CharField(max_length=100, blank=True, null=True, verbose_name='Creador')
    status = models.BooleanField(default=True, verbose_name='Activo')
    fechacreacion = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    motivo_rechazo = models.TextField(blank=True, null=True, verbose_name='Motivo de Rechazo')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"Doc #{self.documento_id} - {self.rut_trabajador}"

    class Meta:
        db_table = 'prevencion_documento_difusion_trabajador'
        verbose_name = 'Difusion Documento Trabajador'
        verbose_name_plural = 'Difusiones Documento Trabajadores'
        constraints = [
            models.UniqueConstraint(fields=['documento', 'user'], name='uq_prev_doc_difusion_documento_user')
        ]

class PrevencionHistorialDifusionTrabajador(models.Model):
    class Accion(models.TextChoices):
        AGREGADO = 'agregado', _('Agregado')
        QUITADO = 'quitado', _('Eliminado')

    documento = models.ForeignKey(PrevencionDocumento, on_delete=models.CASCADE, related_name='historial_difusion_trabajadores', verbose_name='Documento')
    trabajador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial_difusion_trabajador_afectado', verbose_name='Trabajador afectado')
    trabajador_rut = models.CharField(max_length=20, blank=True, default='', verbose_name='RUT Trabajador')
    trabajador_nombre = models.CharField(max_length=200, blank=True, default='', verbose_name='Nombre Trabajador')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='historial_difusion_trabajador_realizado', verbose_name='Realizado por')
    actor_nombre = models.CharField(max_length=200, blank=True, default='', verbose_name='Nombre Actor')
    accion = models.CharField(max_length=20, choices=Accion.choices, verbose_name='Accion')
    fechacreacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha Creacion')

    objects = AuditableQuerySet.as_manager()

    class Meta:
        db_table = 'prevencion_historial_difusion_trabajador'
        verbose_name = 'Historial Difusion Trabajador'
        verbose_name_plural = 'Historiales Difusion Trabajadores'
        ordering = ['-fechacreacion', '-id']
        indexes = [
            models.Index(fields=['documento', 'fechacreacion']),
            models.Index(fields=['accion']),
            models.Index(fields=['trabajador']),
        ]

    def __str__(self):
        return f"Doc #{self.documento_id} - {self.get_accion_display()}"

class PrevencionResultadoCurso(models.Model):
    documento = models.ForeignKey(PrevencionDocumento, on_delete=models.CASCADE, related_name='resultados_curso', verbose_name='Documento')
    trabajador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resultados_curso_prevencion', verbose_name='Trabajador')
    total_preguntas = models.PositiveIntegerField(default=0, verbose_name='Total Preguntas')
    total_correctas = models.PositiveIntegerField(default=0, verbose_name='Total Correctas')
    porcentaje_aprobacion = models.FloatField(default=0, verbose_name='Porcentaje Aprobación')
    intentos_realizados = models.PositiveSmallIntegerField(default=0, verbose_name='Intentos Realizados')
    aprobado = models.BooleanField(default=False, verbose_name='Aprobado')
    detalle_respuestas = models.JSONField(default=list, blank=True, verbose_name='Detalle Respuestas')
    fechacreacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha Actualización')

    objects = AuditableQuerySet.as_manager()

    class Meta:
        db_table = 'prevencion_resultado_curso'
        verbose_name = 'Resultado Curso'
        verbose_name_plural = 'Resultados Curso'
        ordering = ['-updated_at', '-id']
        constraints = [
            models.UniqueConstraint(fields=['documento', 'trabajador'], name='uq_prev_resultado_curso_documento_trabajador')
        ]
        indexes = [
            models.Index(fields=['documento', 'trabajador']),
            models.Index(fields=['trabajador', 'updated_at']),
        ]

    def __str__(self):
        return f"Resultado Curso Doc #{self.documento_id} - Usuario #{self.trabajador_id}"

class PrevencionResultadoCursoIntento(models.Model):
    documento = models.ForeignKey(PrevencionDocumento, on_delete=models.CASCADE, related_name='intentos_curso', verbose_name='Documento')
    trabajador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='intentos_curso_prevencion', verbose_name='Trabajador')
    numero_intento = models.PositiveSmallIntegerField(default=1, verbose_name='Nro Intento')
    total_preguntas = models.PositiveIntegerField(default=0, verbose_name='Total Preguntas')
    total_correctas = models.PositiveIntegerField(default=0, verbose_name='Total Correctas')
    porcentaje_aprobacion = models.FloatField(default=0, verbose_name='Porcentaje Aprobación')
    aprobado = models.BooleanField(default=False, verbose_name='Aprobado')
    detalle_respuestas = models.JSONField(default=list, blank=True, verbose_name='Detalle Respuestas')
    fechacreacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha Intento')
    tiempo_segundos = models.PositiveIntegerField(default=0, verbose_name='Tiempo empleado (segundos)')

    objects = AuditableQuerySet.as_manager()

    class Meta:
        db_table = 'prevencion_resultado_curso_intento'
        verbose_name = 'Intento Resultado Curso'
        verbose_name_plural = 'Intentos Resultado Curso'
        ordering = ['trabajador_id', 'numero_intento', 'id']
        constraints = [
            models.UniqueConstraint(fields=['documento', 'trabajador', 'numero_intento'], name='uq_prev_resultado_curso_intento_documento_trabajador_numero')
        ]
        indexes = [
            models.Index(fields=['documento', 'trabajador', 'numero_intento']),
            models.Index(fields=['trabajador', 'fechacreacion']),
        ]

    def __str__(self):
        return f"Intento {self.numero_intento} - Doc {self.documento_id} - Usuario #{self.trabajador_id}"

class PrevencionPermisoLlenado(models.Model):
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, related_name='permisos_prevencion_llenado')
    plantilla = models.ForeignKey('PrevencionPlantilla', on_delete=models.CASCADE, related_name='permisos_llenado')
    cargos = models.ManyToManyField('VigilanciaCargo', related_name='permisos_llenado', blank=True)
    status = models.BooleanField(default=True, verbose_name='Activo')
    creador = models.CharField(max_length=100, blank=True, null=True, verbose_name='Creador')
    fechacreacion = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"{self.faena} - {self.plantilla}"

    class Meta:
        db_table = 'prevencion_permiso_llenado'
        verbose_name = 'Permiso de Llenado'
        verbose_name_plural = 'Permisos de Llenado'
        constraints = [
            models.UniqueConstraint(fields=['faena', 'plantilla'], name='uq_prevencion_permiso_llenado_faena_plantilla')
        ]

class PrevencionEvidenciaGeneral(models.Model):
    documento = models.ForeignKey(PrevencionDocumento, related_name='evidencias_generales', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='prevencion/evidencias_generales/')
    fechacreacion = models.DateTimeField(default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"Evidencia General Doc {self.documento.id}"

class PrevencionEvidenciaSeccion(models.Model):
    documento = models.ForeignKey(PrevencionDocumento, related_name='evidencias_secciones', on_delete=models.CASCADE)
    indice_seccion = models.IntegerField(help_text="Indice de la sección (0, 1, 2...)")
    archivo = models.FileField(upload_to='prevencion/evidencias_secciones/')
    
    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"Evidencia Doc {self.documento.id} - Seccion {self.indice_seccion}"

class BaseVigilanciaCatalogo(models.Model):
    correlativo = models.PositiveIntegerField(verbose_name='ID Tipo')
    valor = models.CharField(max_length=120, verbose_name='Valor')
    status = models.BooleanField(default=True, verbose_name='Activo')
    creador = models.CharField(max_length=100, blank=True, null=True, verbose_name='Creador')
    fechacreacion = models.DateTimeField(default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ['correlativo', 'id']

    def __str__(self):
        return self.valor

class VigilanciaGes(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_ges'
        verbose_name = 'GES Vigilancia'
        verbose_name_plural = 'GES Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_ges_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_ges_correlativo'),
        ]

class VigilanciaArea(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_area'
        verbose_name = 'Area Vigilancia'
        verbose_name_plural = 'Areas Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_area_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_area_correlativo'),
        ]

class VigilanciaCargo(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_cargo'
        verbose_name = 'Cargo Vigilancia'
        verbose_name_plural = 'Cargos Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_cargo_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_cargo_correlativo'),
        ]

class VigilanciaTipoContrato(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_tipo_contrato'
        verbose_name = 'Tipo de Contrato Vigilancia'
        verbose_name_plural = 'Tipos de Contrato Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_tipo_contrato_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_tipo_contrato_correlativo'),
        ]

class VigilanciaContrato(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_contrato'
        verbose_name = 'Contrato Vigilancia'
        verbose_name_plural = 'Contratos Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_contrato_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_contrato_correlativo'),
        ]

class VigilanciaEvaluacionRiesgo(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_evaluacion_riesgo'
        verbose_name = 'Evaluacion de Riesgo Vigilancia'
        verbose_name_plural = 'Evaluaciones de Riesgo Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_eval_riesgo_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_eval_riesgo_correlativo'),
        ]

class VigilanciaExposicion(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_exposicion'
        verbose_name = 'Exposicion Vigilancia'
        verbose_name_plural = 'Exposiciones Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_exposicion_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_exposicion_correlativo'),
        ]

class VigilanciaNivelRiesgo(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_nivel_riesgo'
        verbose_name = 'Nivel de Riesgo Vigilancia'
        verbose_name_plural = 'Niveles de Riesgo Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_nivel_riesgo_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_nivel_riesgo_correlativo'),
        ]

class VigilanciaGradoExposicion(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_grado_exposicion'
        verbose_name = 'Grado de Exposicion Vigilancia'
        verbose_name_plural = 'Grados de Exposicion Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_grado_exposicion_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_grado_exposicion_correlativo'),
        ]

class VigilanciaNivelSeguimiento(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_nivel_seguimiento'
        verbose_name = 'Nivel de Seguimiento Vigilancia'
        verbose_name_plural = 'Niveles de Seguimiento Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_nivel_seguimiento_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_nivel_seguimiento_correlativo'),
        ]

class VigilanciaEstado(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_vigilancia_estado'
        verbose_name = 'Estado Vigilancia'
        verbose_name_plural = 'Estados Vigilancia'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prevencion_vigilancia_estado_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prevencion_vigilancia_estado_correlativo'),
        ]

class DocumentoCharla(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_documento_charla'
        verbose_name = 'Charla'
        verbose_name_plural = 'Charlas'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prev_doc_charla_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prev_doc_charla_correlativo'),
        ]

class DocumentoInformativo(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_documento_informativo'
        verbose_name = 'Informativo'
        verbose_name_plural = 'Informativos'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prev_doc_informativo_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prev_doc_informativo_correlativo'),
        ]

class DocumentoDifusion(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_documento_difusion'
        verbose_name = 'Difusion'
        verbose_name_plural = 'Difusiones'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prev_doc_difusion_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prev_doc_difusion_correlativo'),
        ]

class DocumentoCurso(BaseVigilanciaCatalogo):
    class Meta:
        db_table = 'prevencion_documento_curso'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        constraints = [
            models.UniqueConstraint(fields=['valor'], name='uq_prev_doc_curso_valor'),
            models.UniqueConstraint(fields=['correlativo'], name='uq_prev_doc_curso_correlativo'),
        ]

class HigieneCualitativa(models.Model):
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, related_name='higiene_cualitativa')
    codigo = models.CharField(max_length=80, unique=True, verbose_name='Codigo')
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    fecha = models.DateField(verbose_name='Fecha')
    estado = models.CharField(max_length=120, verbose_name='Estado')
    contrato = models.CharField(max_length=120, blank=True, null=True, verbose_name='Contrato')
    informe_tecnico = models.TextField(verbose_name='Informe Tecnico')
    documento = models.FileField(upload_to='prevencion/higiene_cualitativa/', verbose_name='Documento')
    creador = models.CharField(max_length=100, blank=True, null=True, verbose_name='Creador')
    status = models.BooleanField(default=True, verbose_name='Activo')
    fechacreacion = models.DateTimeField(default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        db_table = 'prevencion_higiene_cualitativa'
        verbose_name = 'Higiene Ocupacional Cualitativa'
        verbose_name_plural = 'Higiene Ocupacional Cualitativa'

class HigieneCuantitativa(models.Model):
    AGENTE_CHOICES = (
        ('silice', 'Silice Respirable'),
        ('ruido', 'Ruido Ocupacional'),
        ('hipobaria', 'Hipobaria'),
        ('vibraciones', 'Vibraciones'),
        ('radiaciones', 'Radiaciones Ionizantes'),
        ('humos', 'Humos Metálicos'),
    )

    DETALLE_LABELS = {
        'evaluacion_riesgo': 'Evaluacion de Riesgo',
        'nivel_riesgo': 'Nivel de Riesgo',
        'nivel_seguimiento': 'Nivel Seguimiento',
        'grado_exposicion': 'Grado Exposicion',
        'exposicion': 'Exposicion',
    }

    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, related_name='higiene_cuantitativa')
    cualitativa = models.ForeignKey(HigieneCualitativa, on_delete=models.CASCADE, related_name='cuantitativas')
    codigo = models.CharField(max_length=80, unique=True, verbose_name='Codigo Cuantitativa')
    nombre = models.CharField(max_length=200, verbose_name='Nombre Cuantitativa')
    fecha = models.DateField(verbose_name='Fecha')
    area = models.CharField(max_length=120, verbose_name='Area')
    ges = models.CharField(max_length=120, verbose_name='GES')
    informe_tecnico = models.TextField(verbose_name='Informe Tecnico', blank=True, null=True)
    documento = models.FileField(upload_to='prevencion/higiene_cuantitativa/', verbose_name='Documento', blank=True, null=True)
    agente = models.CharField(max_length=30, choices=AGENTE_CHOICES, blank=True, null=True, verbose_name='Agente')
    agente_detalle = models.JSONField(default=dict, blank=True, verbose_name='Seleccion de Agente')
    creador = models.CharField(max_length=100, blank=True, null=True, verbose_name='Creador')
    status = models.BooleanField(default=True, verbose_name='Activo')
    fechacreacion = models.DateTimeField(default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def agente_texto(self):
        if not self.agente: return '-'
        return dict(self.AGENTE_CHOICES).get(self.agente, self.agente)

    @property
    def agente_detalle_texto(self):
        if not self.agente_detalle or not isinstance(self.agente_detalle, dict): return '-'
        partes = []
        for key, value in self.agente_detalle.items():
            if value in (None, ''): continue
            label = self.DETALLE_LABELS.get(key, key.replace('_', ' ').title())
            partes.append(f"{label}: {value}")
        return ' | '.join(partes) if partes else '-'

    @property
    def nivel_riesgo_texto(self):
        if not self.agente_detalle or not isinstance(self.agente_detalle, dict): return ''
        return str(self.agente_detalle.get('nivel_riesgo') or '')

    class Meta:
        db_table = 'prevencion_higiene_cuantitativa'
        verbose_name = 'Higiene Ocupacional Cuantitativa'
        verbose_name_plural = 'Higiene Ocupacional Cuantitativa'

class Vigilancia(models.Model):
    cuantitativa = models.ForeignKey(HigieneCuantitativa, on_delete=models.CASCADE, related_name='vigilancias')
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, related_name='vigilancias')
    codigo = models.CharField(max_length=80, verbose_name='Codigo Vigilancia')
    nombre = models.CharField(max_length=200, verbose_name='Nombre Vigilancia')
    area = models.CharField(max_length=120, blank=True, default='', verbose_name='Area')
    ges = models.CharField(max_length=120, blank=True, default='', verbose_name='GES')
    snapshot_inicializado = models.BooleanField(default=False, verbose_name='Snapshot Inicializado')
    creador = models.CharField(max_length=100, blank=True, null=True, verbose_name='Creador')
    status = models.BooleanField(default=True, verbose_name='Activo')
    fechacreacion = models.DateTimeField(default=timezone.now)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        db_table = 'prevencion_vigilancia'
        verbose_name = 'Vigilancia Medica'
        verbose_name_plural = 'Vigilancias Medicas'
        constraints = [
            models.UniqueConstraint(fields=['codigo'], name='uq_prevencion_vigilancia_codigo'),
        ]

class VigilanciaMedica(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='vigilancias')
    cuantitativa = models.ForeignKey(HigieneCuantitativa, on_delete=models.SET_NULL, null=True, blank=True, related_name='vigilancias_medicas')
    vigilancia = models.ForeignKey(Vigilancia, on_delete=models.SET_NULL, null=True, blank=True, related_name='fichas')
    rut_trabajador = models.CharField(max_length=20, verbose_name="RUT")
    nombre_completo = models.CharField(max_length=200)
    genero_texto = models.CharField(max_length=50, blank=True, null=True, verbose_name="Género")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha Nacimiento")
    edad = models.IntegerField(blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    faena = models.ForeignKey(Faena, on_delete=models.SET_NULL, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True, verbose_name="Fecha de Ingreso")
    antiguedad_anos = models.IntegerField(default=0, verbose_name="Años")
    antiguedad_meses = models.IntegerField(default=0, verbose_name="Meses")
    antiguedad_dias = models.IntegerField(default=0, verbose_name="Días")
    tipo_contrato = models.CharField(max_length=100, blank=True, null=True)
    fecha_retiro = models.DateField(blank=True, null=True, verbose_name="Fecha Retiro o Desvinculación")
    ges = models.CharField(max_length=100, blank=True, null=True, verbose_name="GES")
    silice_eval_riesgo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Evaluación Riesgo Sílice")
    silice_nivel_riesgo = models.CharField(max_length=100, blank=True, null=True)
    silice_grado_expo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Grado Exposición")
    silice_fecha_radio = models.DateField(blank=True, null=True, verbose_name="Fecha Radiografía")
    silice_fecha_vence = models.DateField(blank=True, null=True, verbose_name="Fecha Vencimiento")
    silice_vigencia = models.CharField(max_length=50, blank=True, null=True)
    silice_obs = models.TextField(blank=True, null=True, verbose_name="Observaciones Sílice")
    ruido_eval_riesgo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Evaluación Riesgo Ruido")
    ruido_nivel_seguimiento = models.CharField(max_length=100, blank=True, null=True)
    ruido_grado_expo = models.CharField(max_length=100, blank=True, null=True)
    ruido_fecha_audio = models.DateField(blank=True, null=True, verbose_name="Fecha Audiometría")
    ruido_fecha_vence = models.DateField(blank=True, null=True)
    ruido_vigencia = models.CharField(max_length=50, blank=True, null=True)
    ruido_obs = models.TextField(blank=True, null=True)
    hipo_exposicion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Exposición Hipobaria")
    hipo_fecha_hemo = models.DateField(blank=True, null=True, verbose_name="Fecha Hemoglobina")
    hipo_fecha_vence = models.DateField(blank=True, null=True)
    hipo_vigencia = models.CharField(max_length=50, blank=True, null=True)
    hipo_obs = models.TextField(blank=True, null=True)
    vibra_eval_riesgo = models.CharField(max_length=100, blank=True, null=True)
    vibra_exposicion = models.CharField(max_length=100, blank=True, null=True)
    vibra_fecha_vence = models.DateField(blank=True, null=True, verbose_name="Fecha Vencimiento Vibraciones")
    vibra_vigencia = models.CharField(max_length=50, blank=True, null=True)
    rad_exposicion = models.CharField(max_length=100, blank=True, null=True)
    rad_fecha_vence = models.DateField(blank=True, null=True, verbose_name="Fecha Vencimiento Radiaciones")
    rad_vigencia = models.CharField(max_length=50, blank=True, null=True)
    humos_eval_riesgo = models.CharField(max_length=100, blank=True, null=True)
    humos_exposicion = models.CharField(max_length=100, blank=True, null=True)
    humos_fecha_vence = models.DateField(blank=True, null=True, verbose_name="Fecha Vencimiento Humos")
    humos_vigencia = models.CharField(max_length=50, blank=True, null=True)
    fecha_incidente = models.DateField(default=timezone.now, null=True, verbose_name="Fecha Incidente")
    organismo_administrador = models.CharField(max_length=100, default='ACHS', verbose_name="Organismo")
    clinica = models.CharField(max_length=100, blank=True, null=True, verbose_name="Clínica / Lugar")
    observacion_general = models.TextField(blank=True, null=True)
    documento_adjunto = models.FileField(upload_to='prevencion/vigilancia_medica/', blank=True, null=True)
    creado_por = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    egresado = models.BooleanField(default=False)
    fecha_egreso = models.DateTimeField(blank=True, null=True)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"{self.rut_trabajador} - {self.nombre_completo}"

    @property
    def fecha_vencimiento(self):
        fechas = [
            self.silice_fecha_vence, self.ruido_fecha_vence, self.hipo_fecha_vence,
            self.vibra_fecha_vence, self.rad_fecha_vence, self.humos_fecha_vence,
        ]
        fechas_validas = [fecha for fecha in fechas if fecha]
        if not fechas_validas: return None
        return min(fechas_validas)

    @property
    def estado_gestion(self):
        campos_obligatorios = [
            self.rut_trabajador, self.nombre_completo, self.genero_texto, 
            self.fecha_nacimiento, self.edad, self.area, self.cargo, self.faena,
            self.fecha_ingreso, self.tipo_contrato, self.ges,
            self.silice_eval_riesgo, self.silice_nivel_riesgo, self.silice_grado_expo, 
            self.silice_fecha_radio, self.silice_fecha_vence, self.silice_vigencia,
            self.ruido_eval_riesgo, self.ruido_nivel_seguimiento, self.ruido_grado_expo, 
            self.ruido_fecha_audio, self.ruido_fecha_vence, self.ruido_vigencia,
            self.hipo_exposicion, self.hipo_fecha_hemo, self.hipo_fecha_vence, self.hipo_vigencia,
            self.vibra_eval_riesgo, self.vibra_exposicion, self.rad_exposicion,
            self.humos_eval_riesgo, self.humos_exposicion
        ]
        for campo in campos_obligatorios:
            if campo is None or campo == "": return "INCOMPLETO"
        if not self.tiene_adjuntos: return "COMPLETO_SIN_EVIDENCIA"
        return "COMPLETO"

    @property
    def tiene_adjuntos(self):
        prefetched_adjuntos = getattr(self, '_prefetched_objects_cache', {}).get('adjuntos_vigilancia')
        tiene_adjuntos_nuevos = bool(prefetched_adjuntos) if prefetched_adjuntos is not None else self.adjuntos_vigilancia.exists()
        return bool(self.documento_adjunto or tiene_adjuntos_nuevos)

    class Meta:
        db_table = 'prevencion_vigilancia_ficha'
        verbose_name = 'Vigilancia Medica (Ficha)'
        verbose_name_plural = 'Vigilancias Medicas (Fichas)'

class Egreso(models.Model):
    ficha_origen = models.ForeignKey(VigilanciaMedica, on_delete=models.SET_NULL, null=True, blank=True, related_name='egresos_historial')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='egresos')
    cuantitativa = models.ForeignKey(HigieneCuantitativa, on_delete=models.SET_NULL, null=True, blank=True, related_name='egresos')
    vigilancia = models.ForeignKey(Vigilancia, on_delete=models.SET_NULL, null=True, blank=True, related_name='egresos')
    rut_trabajador = models.CharField(max_length=20, verbose_name="RUT")
    nombre_completo = models.CharField(max_length=200)
    genero_texto = models.CharField(max_length=50, blank=True, null=True, verbose_name="Genero")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha Nacimiento")
    edad = models.IntegerField(blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    faena = models.ForeignKey(Faena, on_delete=models.SET_NULL, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True, verbose_name="Fecha de Ingreso")
    antiguedad_anos = models.IntegerField(default=0, verbose_name="Anos")
    antiguedad_meses = models.IntegerField(default=0, verbose_name="Meses")
    antiguedad_dias = models.IntegerField(default=0, verbose_name="Dias")
    tipo_contrato = models.CharField(max_length=100, blank=True, null=True)
    fecha_retiro = models.DateField(blank=True, null=True, verbose_name="Fecha Retiro o Desvinculacion")
    ges = models.CharField(max_length=100, blank=True, null=True, verbose_name="GES")
    silice_eval_riesgo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Evaluacion Riesgo Silice")
    silice_nivel_riesgo = models.CharField(max_length=100, blank=True, null=True)
    silice_grado_expo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Grado Exposicion")
    silice_fecha_radio = models.DateField(blank=True, null=True, verbose_name="Fecha Radiografia")
    silice_fecha_vence = models.DateField(blank=True, null=True, verbose_name="Fecha Vencimiento")
    silice_vigencia = models.CharField(max_length=50, blank=True, null=True)
    silice_obs = models.TextField(blank=True, null=True, verbose_name="Observaciones Silice")
    ruido_eval_riesgo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Evaluacion Riesgo Ruido")
    ruido_nivel_seguimiento = models.CharField(max_length=100, blank=True, null=True)
    ruido_grado_expo = models.CharField(max_length=100, blank=True, null=True)
    ruido_fecha_audio = models.DateField(blank=True, null=True, verbose_name="Fecha Audiometria")
    ruido_fecha_vence = models.DateField(blank=True, null=True)
    ruido_vigencia = models.CharField(max_length=50, blank=True, null=True)
    ruido_obs = models.TextField(blank=True, null=True)
    hipo_exposicion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Exposicion Hipobaria")
    hipo_fecha_hemo = models.DateField(blank=True, null=True, verbose_name="Fecha Hemoglobina")
    hipo_fecha_vence = models.DateField(blank=True, null=True)
    hipo_vigencia = models.CharField(max_length=50, blank=True, null=True)
    hipo_obs = models.TextField(blank=True, null=True)
    vibra_eval_riesgo = models.CharField(max_length=100, blank=True, null=True)
    vibra_exposicion = models.CharField(max_length=100, blank=True, null=True)
    vibra_fecha_vence = models.DateField(blank=True, null=True, verbose_name="Fecha Vencimiento Vibraciones")
    vibra_vigencia = models.CharField(max_length=50, blank=True, null=True)
    rad_exposicion = models.CharField(max_length=100, blank=True, null=True)
    rad_fecha_vence = models.DateField(blank=True, null=True, verbose_name="Fecha Vencimiento Radiaciones")
    rad_vigencia = models.CharField(max_length=50, blank=True, null=True)
    humos_eval_riesgo = models.CharField(max_length=100, blank=True, null=True)
    humos_exposicion = models.CharField(max_length=100, blank=True, null=True)
    humos_fecha_vence = models.DateField(blank=True, null=True, verbose_name="Fecha Vencimiento Humos")
    humos_vigencia = models.CharField(max_length=50, blank=True, null=True)
    fecha_incidente = models.DateField(default=timezone.now, null=True, verbose_name="Fecha Incidente")
    organismo_administrador = models.CharField(max_length=100, default='ACHS', verbose_name="Organismo")
    clinica = models.CharField(max_length=100, blank=True, null=True, verbose_name="Clinica / Lugar")
    observacion_general = models.TextField(blank=True, null=True)
    documento_adjunto = models.FileField(upload_to='prevencion/egreso/', blank=True, null=True)
    documento_adjunto_cargado_at = models.DateTimeField(blank=True, null=True)
    creado_por = models.CharField(max_length=100, blank=True, null=True)
    fecha_egreso = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"Egreso {self.rut_trabajador} - {self.nombre_completo}"

    class Meta:
        db_table = 'prevencion_egreso'
        verbose_name = 'Egreso'
        verbose_name_plural = 'Egresos'
        ordering = ['-fecha_egreso', '-id']

class EgresoAdjuntoHistorico(models.Model):
    egreso = models.ForeignKey(Egreso, related_name='adjuntos_historicos', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='prevencion/egreso/')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = AuditableQuerySet.as_manager()

    class Meta:
        db_table = 'prevencion_egreso_adjunto_historico'
        verbose_name = 'Adjunto Historico Egreso'
        verbose_name_plural = 'Adjuntos Historicos Egreso'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"Adjunto historico {self.id} - Egreso {self.egreso_id}"

class VigilanciaAdjunto(models.Model):
    vigilancia = models.ForeignKey(VigilanciaMedica, related_name='adjuntos_vigilancia', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='prevencion/vigilancia_medica/')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = AuditableQuerySet.as_manager()

    class Meta:
        db_table = 'prevencion_vigilancia_adjunto'
        verbose_name = 'Adjunto Vigilancia'
        verbose_name_plural = 'Adjuntos Vigilancia'
        ordering = ['id']

    def __str__(self):
        return f"Adjunto {self.id} - Vigilancia {self.vigilancia_id}"

class PrevencionEvidenciaItem(models.Model):
    documento = models.ForeignKey(PrevencionDocumento, related_name='evidencias_items', on_delete=models.CASCADE)
    indice_seccion = models.IntegerField(help_text="Índice de la sección (0, 1, 2...)")
    indice_fila = models.IntegerField(help_text="Índice de la fila/ítem (0, 1, 2...)")
    archivo = models.FileField(upload_to='prevencion/evidencias_items/')
    objects = AuditableQuerySet.as_manager()
    
    def __str__(self):
        return f"Evidencia Doc {self.documento.id} - Sec {self.indice_seccion} - Item {self.indice_fila}"
    
class ValidacionDobleFactor(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    documento_id = models.IntegerField()
    rut_esperado = models.CharField(max_length=12)
    validado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    en_uso = models.BooleanField(default=False)

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"Token {self.token} - Validado: {self.validado}"