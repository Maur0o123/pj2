from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import DataPerforacionesListView, SaveReporteOperacionalAPI, VehiculosListView, VehiculoskilometrajesListView, VehiculosFaenasListView, SaveReporteMaterialesSonda
from .views import VehiculoskilometrajesListViewDemo,DashboardVehiculos, token_obtain_pair
from .views import DashboardInventarioVehiculo,DashboardInventarioSondaje, DashboardInventarioPrevencion, DashboardSondas 
from .views import SaveReport,ReadReport_v1, ReadReport_v0, SelectorReport
from .views import ReporteAvanceCampana
from .views import DashboardSondajeTotalAPI
from .views import DashboardSondajeDiarioAPI
from .views import DashboardPrevencionReportesAPI, DashboardVigilanciaMedicaAPI

app_name = 'api'
urlpatterns = [
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', token_obtain_pair, name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/data_perforaciones/', DataPerforacionesListView.as_view(), name='data_perforaciones'),
    path('api/save_reporte_operacional/', SaveReporteOperacionalAPI.as_view(), name='save_reporte_operacional_api'),
    path('api/save_reporte_materiales_sonda/', SaveReporteMaterialesSonda.as_view(), name='save_reporte_materiales_sonda'),
    path('api/vehiculos/', VehiculosListView.as_view(), name='vehiculos'),
    path('api/vehiculos_kilometrajes/', VehiculoskilometrajesListView.as_view(), name='vehiculos_kilometrajes'),
    path('api/vehiculos_faenas/', VehiculosFaenasListView.as_view(), name='vehiculos_faenas'),
    path('api/vehiculos_kilometrajes_demo/', VehiculoskilometrajesListViewDemo.as_view(), name='vehiculos_kilometrajesDemo'),
    path('api/dashboardVehiculos/', DashboardVehiculos.as_view(), name='vehiculos_kilometrajesDemo'), 
    path('api/dashboardInventarioVehiculo/', DashboardInventarioVehiculo.as_view(), name='dashboardInventarioVehiculo'),
    path('api/dashboardInventarioSondaje/', DashboardInventarioSondaje.as_view(), name='dashboardInventarioSondaje'),
    path('api/dashboardInventarioPrevencion/', DashboardInventarioPrevencion.as_view(), name='dashboardInventarioPrevencion'),
    path('api/dashboardSondas/', DashboardSondas.as_view(), name='dashboardSondas'),
    path('api/save_report/', SaveReport.as_view(), name='save_report'), 
    #path('api/read_report/', ReadReport_v0.as_view(), name='read_report'), # VERSION SIN OPTIMIZAR
    path('api/read_report/', ReadReport_v1.as_view(), name='read_report'),  # VERSION OPTIMIZADA 12-nov-2025
    path('api/selector_report/', SelectorReport.as_view(), name='selector_report'), 
    path('api/reporte_avance_campana/', ReporteAvanceCampana.as_view(), name='reporte_avance_campana'),
    path('api/dashboard_sondaje_total/', DashboardSondajeTotalAPI.as_view(), name='dashboard_sondaje_total'),
    path('api/dashboard_sondaje_diario/', DashboardSondajeDiarioAPI.as_view(), name='dashboard_sondaje_diario'),
    path('api/dashboard_prevencion_reportes/', DashboardPrevencionReportesAPI.as_view(), name='dashboard_prevencion_reportes'),
    path('api/dashboard_vigilancia_medica/', DashboardVigilanciaMedicaAPI.as_view(), name='dashboard_vigilancia_medica'),

]
