from django.urls import path
from . import views

urlpatterns = [
    #----------Plantillas Prevención ----------#
    
    # Listar (Mantenedor)
    path('mantenedor/<str:tipo_slug>/', views.manage_prevencion, name='manage_prevencion'),
    path('capacitaciones/<str:tipo_slug>/', views.manage_capacitaciones, name='manage_capacitaciones'),
    
    # Crear Nuevo
    path('mantenedor/<str:tipo_slug>/nuevo/', views.edit_prevencion, name='create_prevencion'),
    
    # Editar Existente
    path('mantenedor/<str:tipo_slug>/editar/<int:pk>/', views.edit_prevencion, name='edit_prevencion'),
    
    # Eliminar
    path('mantenedor/eliminar/<int:pk>/', views.delete_prevencion, name='delete_prevencion'),

    # crear Nuevo Documento
    path('documento/nuevo/', views.new_documento, name='new_documento'),
    
    # AJAX Endpoints
    path('ajax/load-plantillas/', views.ajax_load_plantillas, name='ajax_load_plantillas'),
    path('ajax/get-structure/', views.ajax_get_structure, name='ajax_get_structure'),
    path('ajax/plantilla-pdf/<int:plantilla_id>/', views.ajax_preview_plantilla_pdf, name='ajax_preview_plantilla_pdf'),
    path('ajax/conteo-trabajadores/', views.ajax_conteo_trabajadores, name='ajax_conteo_trabajadores'),
    path('ajax/autorizadores/sync/', views.ajax_sync_autorizadores_prevencion, name='ajax_sync_autorizadores_prevencion'),
    path('ajax/notificaciones/aprobacion/crear/', views.ajax_create_approval_notification, name='ajax_create_approval_notification'),
    path('ajax/notificaciones/aprobacion/historial/<int:plantilla_id>/', views.ajax_list_approval_history_prevencion, name='ajax_list_approval_history_prevencion'),
    path('ajax/notificaciones/aprobacion/estados/<int:plantilla_id>/', views.ajax_list_approval_status_prevencion, name='ajax_list_approval_status_prevencion'),
    path('ajax/notificaciones/aprobacion/listar/', views.ajax_list_approval_notifications, name='ajax_list_approval_notifications'),
    path('notificaciones/', views.view_all_approval_notifications, name='view_all_approval_notifications'),
    path('notificaciones/aprobacion/<int:pk>/ver/', views.view_review_approval_notification, name='view_review_approval_notification'),
    path('ajax/notificaciones/aprobacion/<int:pk>/resolver/', views.ajax_resolve_approval_notification, name='ajax_resolve_approval_notification'),
    path('ajax/notificaciones/aprobacion/<int:pk>/cancelar/', views.ajax_cancel_approval_notification, name='ajax_cancel_approval_notification'),

    #----------Documentos Prevención ----------#
    
    # View Documento
    path('documento/historial/', views.history_prevencion, name='history_prevencion'),
    path('documento/ver/<int:pk>/', views.view_documento, name='view_documento'),
    path(
        'documento/<int:pk>/resultado/guardar/',
        views.guardar_resultado_capacitacion_documento,
        name='guardar_resultado_capacitacion_documento'
    ),
    path(
        'documento/<int:pk>/resultado/borrador/guardar/',
        views.guardar_borrador_capacitacion_documento,
        name='guardar_borrador_capacitacion_documento'
    ),
    path(
        'documento/finalizar/<int:pk>/',
        views.finalizar_capacitacion_documento,
        name='finalizar_capacitacion_documento'
    ),
    path(
        'documento/<int:documento_id>/difusion/trabajadores/',
        views.documento_difusion_trabajadores,
        name='documento_difusion_trabajadores'
    ),
    path(
        'documento/<int:documento_id>/difusion/trabajadores/agregar/',
        views.add_documento_difusion_trabajador,
        name='add_documento_difusion_trabajador'
    ),
    path(
        'documento/<int:documento_id>/difusion/trabajadores/remover/',
        views.remove_documento_difusion_trabajador,
        name='remove_documento_difusion_trabajador'
    ),
    path(
        'documento/<int:documento_id>/difusion/trabajadores/<int:user_id>/resultado/',
        views.view_resultado_capacitacion_documento,
        name='view_resultado_capacitacion_documento'
    ),
    path('documento/pdf/<int:pk>/', views.documento_pdf_view, name='documento_pdf_view'),
    # Edit Documento
    path('documento/editar/<int:pk>/', views.edit_documento, name='edit_documento'),
    # Delete Documento
    path('documento/eliminar/<int:pk>/', views.delete_documento, name='delete_documento'),

    # Rutas Vigilancia Médica
    path('vigilancia/', views.manage_vigilancia, name='manage_vigilancia'),
    path('egreso/', views.egreso, name='egreso'),
    path('egreso/<int:vigilancia_id>/', views.egreso_detalle, name='egreso_detalle'),
    path('egreso/<int:vigilancia_id>/reintegrar/<int:egreso_id>/', views.reintegrar_vigilancia_trabajador, name='reintegrar_vigilancia_trabajador'),
    path('egreso/vigilancia/<int:pk>/', views.view_vigilancia_egreso, name='view_vigilancia_egreso'),
    path('higiene-ocupacional/evaluacion-cualitativa/', views.higiene_cualitativa, name='higiene_cualitativa'),
    path('higiene-ocupacional/evaluacion-cualitativa/nuevo/', views.new_higiene_cualitativa, name='new_higiene_cualitativa'),
    path('higiene-ocupacional/evaluacion-cualitativa/ver/<int:pk>/', views.view_higiene_cualitativa, name='view_higiene_cualitativa'),
    path('higiene-ocupacional/evaluacion-cualitativa/editar/<int:pk>/', views.edit_higiene_cualitativa, name='edit_higiene_cualitativa'),
    path('higiene-ocupacional/evaluacion-cualitativa/deshabilitar/<int:pk>/', views.disable_higiene_cualitativa, name='disable_higiene_cualitativa'),
    path('higiene-ocupacional/evaluacion-cuantitativa/', views.higiene_cuantitativa, name='higiene_cuantitativa'),
    path('higiene-ocupacional/evaluacion-cuantitativa/nuevo/', views.new_higiene_cuantitativa, name='new_higiene_cuantitativa'),
    path('higiene-ocupacional/evaluacion-cuantitativa/ver/<int:pk>/', views.view_higiene_cuantitativa, name='view_higiene_cuantitativa'),
    path('higiene-ocupacional/evaluacion-cuantitativa/editar/<int:pk>/', views.edit_higiene_cuantitativa, name='edit_higiene_cuantitativa'),
    path('higiene-ocupacional/evaluacion-cuantitativa/deshabilitar/<int:pk>/', views.disable_higiene_cuantitativa, name='disable_higiene_cuantitativa'),
    path('vigilancia/nuevo/', views.new_vigilancia, name='new_vigilancia'),
    path('vigilancia/<int:vigilancia_id>/trabajadores/', views.vigilancia_trabajadores, name='vigilancia_trabajadores'),
    path('vigilancia/<int:vigilancia_id>/trabajadores/agregar/', views.add_vigilancia_trabajadores, name='add_vigilancia_trabajadores'),
    path('vigilancia/<int:vigilancia_id>/trabajadores/nuevo/', views.new_vigilancia_trabajador, name='new_vigilancia_trabajador'),
    path('vigilancia/<int:vigilancia_id>/trabajadores/egresar/', views.egresar_vigilancia_trabajador, name='egresar_vigilancia_trabajador'),
    path('vigilancia/<int:vigilancia_id>/trabajadores/remover/', views.remove_vigilancia_trabajador, name='remove_vigilancia_trabajador'),
    path('vigilancia/opciones/<str:tipo_slug>/', views.manage_vigilancia_option, name='manage_vigilancia_option'),
    path('vigilancia/opciones/<str:tipo_slug>/nuevo/', views.new_vigilancia_option, name='new_vigilancia_option'),
    path('vigilancia/opciones/<str:tipo_slug>/guardar/', views.save_new_vigilancia_option, name='save_new_vigilancia_option'),
    path('vigilancia/opciones/<str:tipo_slug>/estado/', views.status_vigilancia_option, name='status_vigilancia_option'),
    
    # NUEVAS RUTAS
    path('vigilancia/editar/<int:pk>/', views.edit_vigilancia, name='edit_vigilancia'),
    path('vigilancia/ver/<int:pk>/', views.view_vigilancia, name='view_vigilancia'),
    path('vigilancia/estado/<int:pk>/', views.status_vigilancia, name='status_vigilancia'),
    path('vigilancia/eliminar/<int:pk>/', views.delete_vigilancia, name='delete_vigilancia'),
    # PDF de Vigilancia Médica (incluye adjuntos en el mismo documento final).
    path('vigilancia/pdf/<int:pk>/', views.vigilancia_pdf_view, name='vigilancia_pdf_view'),
    
    path('api/buscar-usuario-rut/', views.ajax_search_user_by_rut, name='ajax_search_user_by_rut'),

    path('vigilancia/delete-doc/<int:pk>/', views.delete_vigilancia_doc, name='delete_vigilancia_doc'),
    path('vigilancia/delete-adjunto/<int:pk>/', views.delete_vigilancia_adjunto, name='delete_vigilancia_adjunto'),

    # Ruta para descargar datos crudos de Prevención en Excel.
    path('informes/obtener-datos/', views.export_data_prevencion_view, name='prevencion_export_data'),

    path('documento/delete-evidencia/<int:pk>/', views.delete_documento_evidencia, name='delete_documento_evidencia'),

    path('documento/delete-seccion-evidencia/<int:pk>/<int:indice>/', views.delete_documento_evidencia_seccion, name='delete_documento_evidencia_seccion'),

    path('documento/delete-item-evidencia/<int:pk>/<int:sec_idx>/<int:row_idx>/', views.delete_documento_evidencia_item, name='delete_documento_evidencia_item'),

    path('generar-qr-validacion/<int:doc_id>/', views.generar_qr_validacion, name='generar_qr_validacion'),
    path('estado-validacion/<uuid:token>/', views.chequear_estado_validacion, name='chequear_estado_validacion'),
    path('escanear-carnet/<uuid:token>/', views.vista_escaner_movil, name='vista_escaner_movil'),
    path('procesar-carnet-movil/<uuid:token>/', views.procesar_carnet_movil, name='procesar_carnet_movil'),
    path('reiniciar-validacion/<int:documento_id>/<int:user_id>/', views.reiniciar_validacion_trabajador, name='reiniciar_validacion_trabajador'),
    path('reiniciar-curso-intentos/<int:documento_id>/<int:user_id>/', views.reiniciar_curso_intentos, name='reiniciar_curso_intentos'),

]
