# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from zipfile import ZipFile
from xhtml2pdf import pisa
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from threading import Thread
from core.utils import check_and_convert_pdf
from core.models import Tipo
import os
import datetime
from .models import Vehiculo, OcultarOpcionesVehiculo, DocumentacionesVehiculo, InformacionTecnicaVehiculo
from mining.models import VehiculoAsignado
import time
from messenger.views import notificacion_celery_email
from messenger.utils import notify_group

def create_vehicle_pdf(request,vehiculo):
    opciones = get_object_or_404(OcultarOpcionesVehiculo, tipo_vehiculo=vehiculo.tipo)
    vehiculoDocumentacion = DocumentacionesVehiculo.objects.get(vehiculo_id=vehiculo.id)
    vehiculoInformacion = InformacionTecnicaVehiculo.objects.get(vehiculo_id=vehiculo.id)
    current_datetime = datetime.datetime.now()
    image_paths_dict = {}
    document_fields = [
        'fotografiaFacturaCompra', 'fotografiaPadron', 'fotografiaPermisoCirculacion', 'fotografiaRevisionTecnica', 
        'fotografiaRevisionTecnicaGases', 'fotografiaSeguroObligatorio', 'fotografiaSeguroAutomotriz', 'fotografiaCertificadoGps', 
        'fotografiaCertificadoMantencion', 'fotografiaCertificadoOperatividad', 'fotografiaCertificadoGrua', 
        'fotografiaCertificadoLamina', 'fotografiaDocumentacionMiniBus', 'fotografiaCertificadoBarraAntiVuelco', 
        'fotografiaInteriorTablero', 'fotografiaInteriorCopiloto', 'fotografiaInteriorAtrasPiloto', 
        'fotografiaInteriorAtrasCopiloto', 'fotografiaExteriorFrontis', 'fotografiaExteriorAtras', 
        'fotografiaExteriorPiloto', 'fotografiaExteriorCopiloto'
    ]

    threads = []
    for field in document_fields:
        if getattr(opciones, field) == "Si":
            file_field = getattr(vehiculoDocumentacion, field)
            if file_field:
                file_path = file_field.path
                field_name = vehiculoDocumentacion._meta.get_field(field).verbose_name
                thread = Thread(target=lambda: image_paths_dict.update({field_name: check_and_convert_pdf(file_path)}))
                threads.append(thread)
                thread.start()

    for thread in threads:
        thread.join()

    verbose_names = [
        vehiculoDocumentacion._meta.get_field(field).verbose_name for field in document_fields
    ]
    sorted_image_paths_dict = {field: image_paths_dict[field] for field in verbose_names if field in image_paths_dict}

    perfil = getattr(request.user, 'usuarioprofile', None)
    context = {
        'vehiculo': vehiculo,
        'opciones': opciones,
        'informacion': vehiculoInformacion,
        'documentacion': vehiculoDocumentacion,
        'image_paths_dict': sorted_image_paths_dict,
        'user_role': perfil.seccionVehicular if perfil else 'SIN ASIGNAR',
        'current_datetime': current_datetime,
    }

    template_path = 'pages/pdfs/vehicle_pdf_template.html'
    template = get_template(template_path)
    html = template.render(context)
    filename = f'{vehiculo.placaPatente}-{current_datetime.strftime("%Y%m%d_%H%M%S")}.pdf'
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs_temp', filename)
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    with open(pdf_path, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        if pisa_status.err:
            return None
    return pdf_path

def create_zip_file(pdf_files):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    zip_filename = f'{settings.MEDIA_ROOT}/pdfs_temp_zip/vehiculos_{formatted_datetime}.zip'
    os.makedirs(os.path.dirname(zip_filename), exist_ok=True)
    with ZipFile(zip_filename, 'w') as zipf:
        for pdf_file in pdf_files:
            zipf.write(pdf_file, os.path.basename(pdf_file))
    return zip_filename

@shared_task(bind=True)
def generate_vehicle_pdfs_and_send_email(self):

    
    # Enviar correo electrónico
    notificacion_celery_email()
    time.sleep(60)
    notificacion_celery_email()
    return "done"

@shared_task
def check_documentation_expiry():
    """
    Revisa diariamente los vencimientos de documentos y notifica al grupo correspondiente.
    """
    from .models import Vehiculo
    from django.utils import timezone
    
    vehiculos = Vehiculo.objects.filter(status=True)
    alert_days = [30, 15, 7, 1, 0] # Días de antelación para avisar
    
    for v in vehiculos:
        diffs = v.calculate_days_difference()
        for doc_name, data in diffs.items():
            days = data['dias_diferencia']
            
            # Avisar si faltan los días exactos de la lista o si ya está vencido
            if days in alert_days or days < 0:
                status = "VENCIDO" if days < 0 else (f"vence en {days} días" if days > 0 else "VENCE HOY")
                
                subject = f"ALERTA VENCIMIENTO: {v.placaPatente} - {doc_name}"
                message = (
                    f"Alerta de Documentación Vehicular\n\n"
                    f"Vehículo: {v.placaPatente} ({v.tipo})\n"
                    f"Documento: {doc_name}\n"
                    f"Fecha Vencimiento: {data['fecha_vencimiento'].strftime('%d/%m/%Y')}\n"
                    f"Estado: {status}\n\n"
                    f"Por favor, gestionar la renovación lo antes posible.\n"
                    f"Más información en www.geoadmin.cl"
                )
                notify_group("admin_vehiculos_maquinaria", subject, message)
    
    return "Proceso de revisión de vencimientos completado."
