from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from .views import (new_maintenance_request, save_new_maintenance_request, manage_maintenance_request, edit_maintenance_request, 
                    save_edit_maintenance_request, status_maintenance_request, new_maintenance_machine_request, save_new_maintenance_machine_request,
                    manage_maintenance_machine_request, edit_maintenance_machine_request, save_edit_maintenance_machine_request, maintenance_pdf_view,
                    maintenance_machine_pdf_view, view_maintenance_readonly)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('new_maintenance_request',new_maintenance_request, name="new_maintenance_request"),
    path('save_new_maintenance_request',save_new_maintenance_request, name="save_new_maintenance_request"),
    path('manage_maintenance_request',manage_maintenance_request, name="manage_maintenance_request"),
    path('edit_maintenance_request',edit_maintenance_request, name="edit_maintenance_request"),
    path('save_edit_maintenance_request',save_edit_maintenance_request, name="save_edit_maintenance_request"),
    path('status_maintenance_request',status_maintenance_request, name="status_maintenance_request"),
    path('new_maintenance_machine_request',new_maintenance_machine_request, name="new_maintenance_machine_request"),
    path('save_new_maintenance_machine_request',save_new_maintenance_machine_request, name="save_new_maintenance_machine_request"),
    path('manage_maintenance_machine_request',manage_maintenance_machine_request, name="manage_maintenance_machine_request"),
    path('edit_maintenance_machine_request',edit_maintenance_machine_request, name="edit_maintenance_machine_request"),
    path('save_edit_maintenance_machine_request',save_edit_maintenance_machine_request, name="save_edit_maintenance_machine_request"),
    path('maintenance_pdf_view',maintenance_pdf_view, name="maintenance_pdf_view"),
    path('maintenance_machine_pdf_view',maintenance_machine_pdf_view, name="maintenance_machine_pdf_view"),
    path('view_maintenance_readonly/', view_maintenance_readonly, name='view_maintenance_readonly'),
]