from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.conf.urls.static import static
from .views import (new_vehicle, manage_vehicles, save_new_vehicle, status_vehicle, edit_vehicle_profile, save_edit_vehicle_profile, hide_options_vehicle, save_penalty,
                    new_kilometraje_register, save_new_kilometraje_register, vehicle_pdf_view, report_vehicles_kilometrajes, report_vehicles_general, report_vehicles_camionetas_faenas,
                    report_vehicles_camionetas_ano, report_vehicles_faenas, manage_fuel_cards, new_fuel_cards, save_new_fuel_cards, status_fuel_cards, edit_fuel_card, save_edit_fuel_card, cargar_informacion_vehiculo,
                    fuel_cards_pdf_view, manage_brand_sleepiness, new_brand_sleepiness, save_new_brand_sleepiness, status_brand_sleepiness, edit_brand_sleepiness, save_edit_brand_sleepiness,
                    manage_model_sleepiness, new_model_sleepiness, save_new_model_sleepiness, status_model_sleepiness, edit_model_sleepiness, save_edit_model_sleepiness,
                    manage_vehicles_por_faena, manage_vehicles_por_tipo, update_penalty)


urlpatterns = [
    path('new_vehicle',new_vehicle, name="new_vehicle"),
    path('manage_vehicles',manage_vehicles, name="manage_vehicles"),
    path('save_new_vehicle',save_new_vehicle, name="save_new_vehicle"),
    path('status_vehicle',status_vehicle, name="status_vehicle"),
    path('edit_vehicle_profile',edit_vehicle_profile, name="edit_vehicle_profile"),
    path('save_edit_vehicle_profile',save_edit_vehicle_profile, name="save_edit_vehicle_profile"),
    path('manage_fuel_cards',manage_fuel_cards, name="manage_fuel_cards"),
    path('new_fuel_cards',new_fuel_cards, name="new_fuel_cards"),
    path('save_new_fuel_cards',save_new_fuel_cards, name="save_new_fuel_cards"),
    path('status_fuel_cards',status_fuel_cards, name="status_fuel_cards"),
    path('edit_fuel_card/<int:card_id>/', edit_fuel_card, name='edit_fuel_card'),
    path('save_edit_fuel_card/<int:card_id>/', save_edit_fuel_card, name='save_edit_fuel_card'),
    path('cargar_informacion_vehiculo',cargar_informacion_vehiculo, name="cargar_informacion_vehiculo"),
    path('fuel_cards_pdf_view',fuel_cards_pdf_view, name="fuel_cards_pdf_view"),
    path('hide_options_vehicle',hide_options_vehicle, name="hide_options_vehicle"),
    path('save_penalty',save_penalty, name="save_penalty"),    
    path('new_kilometraje_register',new_kilometraje_register, name="new_kilometraje_register"),
    path('save_new_kilometraje_register',save_new_kilometraje_register, name="save_new_kilometraje_register"),
    path('vehicle_pdf_view',vehicle_pdf_view, name="vehicle_pdf_view"),
    path('report_vehicles_kilometrajes',report_vehicles_kilometrajes, name="report_vehicles_kilometrajes"),
    path('report_vehicles_general',report_vehicles_general, name="report_vehicles_general"),
    path('report_vehicles_camionetas_faenas',report_vehicles_camionetas_faenas, name="report_vehicles_camionetas_faenas"),
    path('report_vehicles_camionetas_ano',report_vehicles_camionetas_ano, name="report_vehicles_camionetas_ano"),
    path('report_vehicles_faenas',report_vehicles_faenas, name="report_vehicles_faenas"),
    
    path('manage_brand_sleepiness',manage_brand_sleepiness, name="manage_brand_sleepiness"),
    path('new_brand_sleepiness',new_brand_sleepiness, name="new_brand_sleepiness"),
    path('save_new_brand_sleepiness',save_new_brand_sleepiness, name="save_new_brand_sleepiness"),
    path('status_brand_sleepiness',status_brand_sleepiness, name="status_brand_sleepiness"),
    path('edit_brand_sleepiness',edit_brand_sleepiness, name="edit_brand_sleepiness"),
    path('save_edit_brand_sleepiness',save_edit_brand_sleepiness, name="save_edit_brand_sleepiness"),
    path('manage_model_sleepiness',manage_model_sleepiness, name="manage_model_sleepiness"),
    path('new_model_sleepiness',new_model_sleepiness, name="new_model_sleepiness"),
    path('save_new_model_sleepiness',save_new_model_sleepiness, name="save_new_model_sleepiness"),
    path('status_model_sleepiness',status_model_sleepiness, name="status_model_sleepiness"),
    path('edit_model_sleepiness',edit_model_sleepiness, name="edit_model_sleepiness"),
    path('save_edit_model_sleepiness',save_edit_model_sleepiness, name="save_edit_model_sleepiness"),
    path('manage_vehicles_por_faena',manage_vehicles_por_faena, name="manage_vehicles_por_faena"),
    path('manage_vehicles_por_tipo',manage_vehicles_por_tipo, name="manage_vehicles_por_tipo"),
    path('update_penalty/',update_penalty, name='update_penalty'),
]