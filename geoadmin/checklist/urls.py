from django.urls import path, include
from .views import (save_checklist_materiales_sonda_entrada, save_checklist_materiales_sonda_salida, 
                    edit_checklist_materiales_sonda, manage_checklist_materiales_sonda, 
                    save_edit_checklist_materiales_sonda_entrada,save_edit_checklist_materiales_sonda_salida, 
                    new_checklist_materiales_caseta, edit_checklist_materiales_caseta, manage_checklist_materiales_caseta, 
                    save_edit_checklist_materiales_caseta, asociar_sondaje_caseta,desasociar_sondaje_caseta,obtener_casetas_disponibles,
                    asociar_sondaje_caseta_desde_reporte,obtener_materiales_caseta_por_id,cambiar_usar_material_reporte)

urlpatterns = [
    path('save_checklist_materiales_sonda_entrada', save_checklist_materiales_sonda_entrada, name="save_checklist_materiales_sonda_entrada"),
    path('save_checklist_materiales_sonda_salida', save_checklist_materiales_sonda_salida, name="save_checklist_materiales_sonda_salida"),
    path('edit_checklist_materiales_sonda', edit_checklist_materiales_sonda, name='edit_checklist_materiales_sonda'),
    path('manage_checklist_materiales_sonda', manage_checklist_materiales_sonda, name="manage_checklist_materiales_sonda"),
    path('save_edit_checklist_materiales_sonda_entrada', save_edit_checklist_materiales_sonda_entrada, name="save_edit_checklist_materiales_sonda_entrada"),
    path('save_edit_checklist_materiales_sonda_salida', save_edit_checklist_materiales_sonda_salida, name="save_edit_checklis_materiales_sonda_salida"),
    path('asociar_sondaje_caseta/',asociar_sondaje_caseta,name='asociar_sondaje_caseta'),
    path('new_checklist_materiales_caseta', new_checklist_materiales_caseta, name="new_checklist_materiales_caseta"),
    path('edit_checklist_materiales_caseta', edit_checklist_materiales_caseta, name='edit_checklist_materiales_caseta'),
    path('manage_checklist_materiales_caseta', manage_checklist_materiales_caseta, name="manage_checklist_materiales_caseta"),
    path('save_edit_checklist_materiales_caseta', save_edit_checklist_materiales_caseta, name="save_edit_checklist_materiales_caseta"),
    path('desasociar_sondaje_caseta/',desasociar_sondaje_caseta,name='desasociar_sondaje_caseta'),
    path('obtener_casetas_disponibles/',obtener_casetas_disponibles,name='obtener_casetas_disponibles'),
    path('asociar_sondaje_caseta_desde_reporte/',asociar_sondaje_caseta_desde_reporte,name='asociar_sondaje_caseta_desde_reporte'),
    path('obtener_materiales_caseta_por_id/',obtener_materiales_caseta_por_id,name='obtener_materiales_caseta_por_id'),
    path('cambiar-usar-material-reporte/',cambiar_usar_material_reporte,name='cambiar_usar_material_reporte'),

    
]