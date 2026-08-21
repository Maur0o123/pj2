from django.urls import path, include
from .views import (view_general_mining_documents, select_massive_vehicles, request_massive_vehicle_pdf, generar_excel, generar_pdf,
                    manage_report_drilling, report_drilling_general)

urlpatterns = [
    path('view_general_mining_documents',view_general_mining_documents, name="view_general_mining_documents"),
    path('select_massive_vehicles',select_massive_vehicles, name="select_massive_vehicles"),
    path('request_massive_vehicle_pdf',request_massive_vehicle_pdf, name="request_massive_vehicle_pdf"),
    path('generar_excel/', generar_excel, name="generar_excel"),
    path('generar_pdf/', generar_pdf, name="generar_pdf"),
    path('manage_report_drilling',manage_report_drilling, name="manage_report_drilling"),
    path('report_drilling_general',report_drilling_general, name="report_drilling_general"),
]