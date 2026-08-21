from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.conf.urls.static import static
from .views import manage_vehicles_mining, edit_vehicle_mining, save_edit_vehicle_mining, select_documents_mining

urlpatterns = [
    path('manage_vehicles_mining',manage_vehicles_mining, name="manage_vehicles_mining"),
    path('edit_vehicle_mining',edit_vehicle_mining, name="edit_vehicle_mining"),
    path('save_edit_vehicle_mining',save_edit_vehicle_mining, name="save_edit_vehicle_mining"),
    path('select_documents_mining',select_documents_mining, name="select_documents_mining"),

]