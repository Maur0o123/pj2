from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from .views import (manage_machines, new_machine, cargar_marca_por_tipo, save_new_machine, status_machine, edit_machine_profile, 
                    save_edit_machine_profile, machine_pdf_view, new_horometro_register, save_new_horometro_register,
                    manage_machines_kits_repair, new_machines_kits_repair, save_new_machines_kits_repair, edit_machines_kits_repair,
                    status_machines_kits_repair, save_edit_machines_kits_repair)

urlpatterns = [
    path('manage_machines',manage_machines, name="manage_machines"),
    path('new_machine',new_machine, name="new_machine"),
    path('save_new_machine',save_new_machine, name="save_new_machine"),
    path('status_machine',status_machine, name="status_machine"),
    path('edit_machine_profile',edit_machine_profile, name="edit_machine_profile"),
    path('save_edit_machine_profile',save_edit_machine_profile, name="save_edit_machine_profile"),
    path('cargar_marca_por_tipo',cargar_marca_por_tipo, name="cargar_marca_por_tipo"),
    path('machine_pdf_view',machine_pdf_view, name="machine_pdf_view"),
    path('new_horometro_register',new_horometro_register, name="new_horometro_register"),
    path('save_new_horometro_register',save_new_horometro_register, name="save_new_horometro_register"),
    path('manage_machines_kits_repair',manage_machines_kits_repair, name="manage_machines_kits_repair"),
    path('new_machines_kits_repair',new_machines_kits_repair, name="new_machines_kits_repair"),
    path('save_new_machines_kits_repair',save_new_machines_kits_repair, name="save_new_machines_kits_repair"),
    path('edit_machines_kits_repair',edit_machines_kits_repair, name="edit_machines_kits_repair"),
    path('status_machines_kits_repair',status_machines_kits_repair, name="status_machines_kits_repair"),
    path('save_edit_machines_kits_repair',save_edit_machines_kits_repair, name="save_edit_machines_kits_repair"),
]