from django.urls import path, include
from .views import (new_reporte_digital, save_reporte_digital, obtener_metro_inicial, manage_mis_reportes_digitales, manage_revisar_reportes_digitales,
                    progreso_reporte_digital, progreso_reporte_digital_corregir, progreso_reporte_digital_aprobar, manage_todos_reportes_digitales,
                    editar_reporte_digital, save_editar_reporte_digital, obtener_estado_sonda, reporte_digital_pdf_view, manage_mis_reportes_digitales_eliminados
                    ,eliminar_reporte_digital_action, export_data_view, get_ultima_sonda_por_pozo,obtener_stock_por_sondaje,obtener_materiales_caseta_por_sondaje)

urlpatterns = [
    path('new_reporte_digital', new_reporte_digital, name="new_reporte_digital"),
    path('save_reporte_digital', save_reporte_digital, name="save_reporte_digital"),    
    path('obtener-metro-inicial/', obtener_metro_inicial, name='obtener_metro_inicial'),
    path('manage_mis_reportes_digitales', manage_mis_reportes_digitales, name='manage_mis_reportes_digitales'),
    path('manage_revisar_reportes_digitales', manage_revisar_reportes_digitales, name='manage_revisar_reportes_digitales'),
    path('manage_todos_reportes_digitales', manage_todos_reportes_digitales, name='manage_todos_reportes_digitales'),
    path('progreso_reporte_digital', progreso_reporte_digital, name='progreso_reporte_digital'),
    path('progreso_reporte_digital_corregir', progreso_reporte_digital_corregir, name='progreso_reporte_digital_corregir'),
    path('progreso_reporte_digital_aprobar', progreso_reporte_digital_aprobar, name='progreso_reporte_digital_aprobar'),
    path('editar_reporte_digital', editar_reporte_digital, name='editar_reporte_digital'),
    path('save_editar_reporte_digital', save_editar_reporte_digital, name='save_editar_reporte_digital'),
    path('obtener-estado-sonda/', obtener_estado_sonda, name='obtener_estado_sonda'),
    path('reporte_digital_pdf_view', reporte_digital_pdf_view, name='reporte_digital_pdf_view'),
    path('manage_mis_reportes_digitales_eliminados', manage_mis_reportes_digitales_eliminados, name='manage_mis_reportes_digitales_eliminados'),
    path('eliminar_reporte_digital_action', eliminar_reporte_digital_action, name='eliminar_reporte_digital_action'),
    path('export_data', export_data_view, name='export_data'),
    path('get_ultima_sonda/', get_ultima_sonda_por_pozo, name='get_ultima_sonda_por_pozo'),
    path('obtener_stock_por_sondaje/', obtener_stock_por_sondaje, name='obtener_stock_por_sondaje'),
    path('obtener_materiales_caseta_por_sondaje/',obtener_materiales_caseta_por_sondaje,name='obtener_materiales_caseta_por_sondaje'),
]