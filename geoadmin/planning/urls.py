from django.urls import path, include
from .views import (new_planning_select_mining, view_planning_mining, view_planning_type, edit_planning_mining, get_planning_mining, 
                    get_planning_type, update_planning_value, new_planning_drilling, edit_drilling_program, update_drilling_program)

urlpatterns = [
    path('new_planning_select_mining',new_planning_select_mining, name="new_planning_select_mining"),
    path('view_planning_mining',view_planning_mining, name="view_planning_mining"),
    path('view_planning_type',view_planning_type, name="view_planning_type"),
    path('edit_planning_mining',edit_planning_mining, name="edit_planning_mining"),
    path('get_planning_mining',get_planning_mining, name="get_planning_mining"),
    path('get_planning_type',get_planning_type, name="get_planning_type"),
    path('update_planning_value',update_planning_value, name="update_planning_value"),
    path('new_planning_drilling',new_planning_drilling, name="new_planning_drilling"),
    path('edit_drilling_program',edit_drilling_program, name="edit_drilling_program"),
    path('update_drilling_program',update_drilling_program, name="update_drilling_program"),
]