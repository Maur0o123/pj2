from django.urls import path
from .views import dashboard_global

urlpatterns = [
    path('dashboard/', dashboard_global, name='dashboardAdministracion'),
]