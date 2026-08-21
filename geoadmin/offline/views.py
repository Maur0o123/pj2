from django.shortcuts import render
import json, os
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.http import FileResponse
from django.conf import settings

def service_worker(request):
    file_path = os.path.join(settings.BASE_DIR, 'static/js/service-worker.js')
    return FileResponse(open(file_path, 'rb'), content_type='application/javascript')


def sondajeOffline(request): 
    context = {
    }
    return render(request,'pages/offline/homesondaje.html', context)

def reporteDigitalOffline(request): 
    context = {
    }
    return render(request,'pages/offline/new_reporte_digital.html', context)

def editarReporteDigitalOffline(request): 
    context = {
    }
    return render(request,'pages/offline/edit_reporte_digital.html', context)