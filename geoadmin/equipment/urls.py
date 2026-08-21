from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from .views import (manage_types_equipment, new_type_equipment, save_new_type_equipment, status_type_equipment, manage_brands_equipment, new_brand_equipment,
                    save_new_brand_equipment, status_brand_equipment, manage_equipments, new_equipment, save_new_equipment, status_equipment, edit_equipment,
                    save_edit_equipment, cargar_marcas_por_tipo)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('manage_types_equipment', manage_types_equipment, name="manage_types_equipment"),
    path('new_type_equipment', new_type_equipment, name="new_type_equipment"),
    path('save_new_type_equipment', save_new_type_equipment, name="save_new_type_equipment"),
    path('status_type_equipment', status_type_equipment, name="status_type_equipment"),
    path('manage_brands_equipment', manage_brands_equipment, name="manage_brands_equipment"),
    path('new_brand_equipment', new_brand_equipment, name="new_brand_equipment"),
    path('save_new_brand_equipment', save_new_brand_equipment, name="save_new_brand_equipment"),
    path('status_brand_equipment', status_brand_equipment, name="status_brand_equipment"),
    path('manage_equipments', manage_equipments, name="manage_equipments"),
    path('new_equipment', new_equipment, name="new_equipment"),
    path('save_new_equipment', save_new_equipment, name="save_new_equipment"),    
    path('status_equipment', status_equipment, name="status_equipment"),
    path('edit_equipment', edit_equipment, name="edit_equipment"),
    path('save_edit_equipment', save_edit_equipment, name="save_edit_equipment"),
    path('cargar_marcas_por_tipo', cargar_marcas_por_tipo, name="cargar_marcas_por_tipo"),
]