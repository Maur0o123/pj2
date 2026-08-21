from django.urls import path, include
from .views import sondajeOffline, service_worker
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('sondajeOffline/', sondajeOffline, name='ondajeOffline'),
    path('service-worker.js', service_worker, name='service-worker'),
]