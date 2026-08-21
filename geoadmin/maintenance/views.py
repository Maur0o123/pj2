from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import (FormNuevaSolicitudMantenimiento, FormEditSolicitudMantenimiento, FormProcesarSolicitudMantenimiento, FormNuevaSolicitudMantenimientoMaquinaria, 
                    FormProcesarSolicitudMantenimientoMaquinaria, FormEditSolicitudMantenimientoMaquinaria)
from .models import (NuevaSolicitudMantenimiento, HistorialSolicitudMantenimiento, SolicitudMantenimientoProblemas, NuevaSolicitudMantenimientoMaquinaria, 
                    HistorialSolicitudMantenimientoMaquinaria, SolicitudMantenimientoProblemasMaquinaria, Mantenimiento)
from core.models import TipoFallaVehiculo, EmpresaServicios, FallaMaquinaria
from core.choices import progreso
from machine.models import Maquinaria, MaquinariaFaena, NuevoHorometro, KitsMaquinariaFaena, HistorialStockKitsMaquinariaFaena, KitsMaquinaria
from django.contrib import messages
from vehicle.models import Vehiculo, NuevoKilometraje
from user.models import Usuario, UsuarioProfile
from core.utils import procesar_fotografia_dos, procesar_fotografia, extension_archivo, check_and_convert_pdf
from django.utils.datastructures import MultiValueDictKeyError
from mining.models import VehiculoAsignado
from django.template.loader import get_template
from xhtml2pdf import pisa
import datetime
import os
from django.http import JsonResponse
from django.conf import settings
from messenger.views import (notificacion_nuevo_mantenimiento_vehiculos_email_sms, notificacion_update_mantenimiento_vehiculos_email_sms, 
                            notificacion_nuevo_mantenimiento_maquinaria_email_sms, notificacion_update_mantenimiento_maquinaria_email_sms,notificacion_jefe_mantencion_stock_minimo_kit_email_sms)
from collections import Counter
from django.db import transaction
from django.template.loader import render_to_string
from core.decorators import vehicular_basico_required, vehicular_avanzado_required

@login_required
@vehicular_avanzado_required
def view_maintenance_readonly(request):
    if request.method == 'GET':
        solicitud_id = request.GET.get('solicitud_id')
        try:
            solicitud = NuevaSolicitudMantenimiento.objects.get(id=solicitud_id)
            problemas = SolicitudMantenimientoProblemas.objects.filter(solicitudMantenimiento=solicitud)
            historiales = HistorialSolicitudMantenimiento.objects.filter(solicitud=solicitud).order_by('-fechacreacion')

            context = {
                'solicitud': solicitud,
                'problemas': problemas,
                'historiales': historiales,
                'choicesprogreso': progreso,
            }

            html = render_to_string('pages/maintenance/maintenance_readonly_modal.html', context, request=request)
            
            return JsonResponse({'success': True, 'html': html})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@login_required
@vehicular_basico_required
def new_maintenance_request(request):
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    if usuario.faena.faena == "SIN ASIGNAR":
        vehiculos = list(Vehiculo.objects.filter(status=True).order_by('-placaPatente'))
    else:
        asignados = VehiculoAsignado.objects.filter(faena=usuario.faena, status=True).order_by('-vehiculo')
        vehiculos = [asignado.vehiculo for asignado in asignados]
        
    context = {
        'formnuevasolicitud': FormNuevaSolicitudMantenimiento(initial={
            'solicitante': request.user.first_name+" "+request.user.last_name,
            'telefono': request.user.phone,
            'vehiculo': vehiculos,
            },
            vehiculos=vehiculos,
        ),
        'solicitante_id': request.user.id,
        'sidebar': 'new_maintenance_request',
        'sidebarmain': 'system_vehicles', 
    }
    return render(request,'pages/maintenance/new_maintenance_request.html', context)

@login_required
@vehicular_basico_required
def save_new_maintenance_request(request):     
    if request.method == 'POST':
        vehiculo = Vehiculo.objects.get(id=request.POST['vehiculo'])
        solicitante = Usuario.objects.get(id=request.POST['solicitante_id'])
        ids_problemas = request.POST.getlist('problemas')
        problemas = TipoFallaVehiculo.objects.filter(id__in=ids_problemas)
        problemasList = TipoFallaVehiculo.objects.filter(id__in=ids_problemas).values_list('falla', flat=True)
        toggle_Uno = request.POST.get('toggle-Uno', 'no')
        toggle_Dos = request.POST.get('toggle-Dos', 'no')
        toggle_Tres = request.POST.get('toggle-Tres', 'no')
        
        fotografiaUno = procesar_fotografia_dos(toggle_Uno, 'fotografiaUno', 'base/no-imagen2.png', request)
        fotografiaDos = procesar_fotografia_dos(toggle_Dos, 'fotografiaDos', 'base/no-imagen2.png', request)
        fotografiaTres = procesar_fotografia_dos(toggle_Tres, 'fotografiaTres', 'base/no-imagen2.png', request)
        vehiculoFaena = VehiculoAsignado.objects.get(vehiculo=request.POST['vehiculo'], status=True)
            
        mantenimiento = NuevaSolicitudMantenimiento(
                solicitante = solicitante,
                telefono = request.POST['telefono'],
                turno = request.POST['turno'],
                vehiculo = vehiculo,
                patente = vehiculo.placaPatente,
                kilometraje = request.POST['kilometraje'],   
                avisoJefatura = 'Si',
                comentario = request.POST['comentario'],
                faena = vehiculoFaena.faena,
                fotografiaUno = fotografiaUno,
                fotografiaDos = fotografiaDos,
                fotografiaTres = fotografiaTres,
                status = True,
                progreso = 1,
            )
        mantenimiento.save()    
        mantenimiento.problemas.set(problemas)
        
        registro = NuevoKilometraje(
            vehiculo = vehiculo,
            kilometraje = request.POST['kilometraje'],
            creador = request.user.first_name+" "+request.user.last_name,
            origen = "Mantención"
        )
        registro.save()
        
        estado_progreso = Mantenimiento.get_nombre_progreso('1')
        notificacion_nuevo_mantenimiento_vehiculos_email_sms(request, mantenimiento, problemasList, estado_progreso, "creado")        
        messages.success(request, 'Solicitud Realizada con Exito', extra_tags='')
        return redirect('new_maintenance_request')
    else:
        return redirect('new_maintenance_request') 

@login_required
@vehicular_avanzado_required
def manage_maintenance_request(request):
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    if usuario.faena.faena == "SIN ASIGNAR":
        solicitudes = NuevaSolicitudMantenimiento.objects.all().order_by('-fechacreacion')
    else:
        solicitudes = NuevaSolicitudMantenimiento.objects.filter(faena=usuario.faena).order_by('-fechacreacion')

    context = {
        'solicitudes': solicitudes,
        'choicesprogreso': progreso,
        'sidebar': 'manage_maintenance_request',
        'sidebarmain': 'system_vehicles', 
    }
    return render(request,'pages/maintenance/manage_maintenance_request.html', context)

@login_required
@vehicular_avanzado_required
def edit_maintenance_request(request):
    try:
        request.session['origen_id'] = request.POST['origen_id']            
    except MultiValueDictKeyError:
        request.session['origen_id'] = request.session['origen_id']
    try:
        request.session['edit_solicitud_id'] = request.POST['solicitud_id']            
    except MultiValueDictKeyError:
        request.session['edit_solicitud_id'] = request.session['edit_solicitud_id']
    solicitud = NuevaSolicitudMantenimiento.objects.get(id=request.session['edit_solicitud_id'])
    historial = list(HistorialSolicitudMantenimiento.objects.filter(solicitud=solicitud).order_by('-fechacreacion'))
    problemas_solicitud = list(SolicitudMantenimientoProblemas.objects.filter(solicitudMantenimiento=solicitud)) 
    problemas_seleccionados = solicitud.problemas.all().values_list('pk', flat=True)
    vehiculo_actual = Vehiculo.objects.get(placaPatente=solicitud.vehiculo.placaPatente)
    urlFotografiaUno = solicitud.fotografiaUno
    urlFotografiaDos = solicitud.fotografiaDos
    urlFotografiaTres = solicitud.fotografiaTres
    extensionFotografiaUno = extension_archivo(urlFotografiaUno)
    extensionFotografiaDos = extension_archivo(urlFotografiaDos)
    extensionFotografiaTres = extension_archivo(urlFotografiaTres)
    
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    if usuario.faena.faena == "SIN ASIGNAR":
        vehiculos = list(Vehiculo.objects.filter(status=True).order_by('-placaPatente'))
    else:
        asignados = VehiculoAsignado.objects.filter(faena=usuario.faena, status=True).order_by('-vehiculo')
        vehiculos = [asignado.vehiculo for asignado in asignados]
    
    context = {
        'formeditsolicitud': FormEditSolicitudMantenimiento(initial={
            'solicitante': solicitud.solicitante.first_name+" "+solicitud.solicitante.last_name,
            'telefono': solicitud.telefono,
            'vehiculo': solicitud.vehiculo.id,
            'problemas': problemas_seleccionados,
            'kilometraje': solicitud.kilometraje,
            'turno': solicitud.turno,
            'comentario': solicitud.comentario,
            },
            vehiculo_actual=vehiculo_actual,
            vehiculos=vehiculos,
        ),
        'formprocesarsolicitud': FormProcesarSolicitudMantenimiento(initial={
            'progreso': solicitud.progreso,
            'empresaMantenimiento': solicitud.empresaMantenimiento,
            },
        ),
        'origen': request.session['origen_id'],
        'solicitud': solicitud,
        'historiales': historial,
        'choicesprogreso': progreso,
        'problemas': problemas_solicitud,
        'fotografiaUno': solicitud.fotografiaUno,
        'fotografiaDos': solicitud.fotografiaDos,
        'fotografiaTres': solicitud.fotografiaTres,
        'extensionFotografiaUno': extensionFotografiaUno,
        'extensionFotografiaDos': extensionFotografiaDos,
        'extensionFotografiaTres': extensionFotografiaTres,
        'sidebar': 'manage_maintenance_request',
        'sidebarmain': 'system_vehicles', 
    }
    return render(request,'pages/maintenance/edit_maintenance_request.html', context)

@login_required
@vehicular_avanzado_required
def save_edit_maintenance_request(request):     
    if request.method == 'POST':
        if request.POST['empresaMantenimiento'] == "":
            empresaMantenimiento = None
        else:
            empresaMantenimiento = EmpresaServicios.objects.get(id=request.POST['empresaMantenimiento'])
        
        vehiculo = Vehiculo.objects.get(id=request.POST['vehiculo'])
        NuevaSolicitudMantenimiento.objects.filter(id=request.POST['solicitud_id']).update(
            telefono = request.POST['telefono'],
            turno = request.POST['turno'],
            vehiculo = request.POST['vehiculo'],
            kilometraje = request.POST['kilometraje'],
            comentario = request.POST['comentario'],
            progreso = request.POST['progreso'],
            empresaMantenimiento = empresaMantenimiento,
            patente=vehiculo.placaPatente,
        )
        
        solicitud = get_object_or_404(NuevaSolicitudMantenimiento, id=request.POST['solicitud_id'])
        problemas_seleccionados = request.POST.getlist('problemas')
        problemasList = TipoFallaVehiculo.objects.filter(id__in=problemas_seleccionados).values_list('falla', flat=True)
        solicitud.problemas.set(problemas_seleccionados)
       
        historial_mas_reciente = HistorialSolicitudMantenimiento.objects.filter(solicitud=solicitud).order_by('-fechacreacion').first()
        if int(historial_mas_reciente.progreso) != int(request.POST['progreso']) or historial_mas_reciente.empresaMantenimiento != empresaMantenimiento :
            historial = HistorialSolicitudMantenimiento(
                solicitud = solicitud,
                solicitante = request.user,
                progreso = request.POST['progreso'],
                empresaMantenimiento = empresaMantenimiento,
            )
            historial.save()
        
        for nombre_campo, valor in request.POST.items():
            if nombre_campo.startswith('valorServicio'):
                numero = nombre_campo.split('valorServicio')[1]
                if valor=="":
                    valor="0"
                try:
                    valorInt =int(valor.replace(".", ""))
                    SolicitudMantenimientoProblemas.objects.filter(id=numero).update(valorServicio=valorInt)
                except:
                    messages.error(request, 'Valor Servicio Excede el Máximo', extra_tags='')
                    return redirect('edit_maintenance_request') 
                    
            if nombre_campo.startswith('descripcion'):
                numero = nombre_campo.split('descripcion')[1]
                SolicitudMantenimientoProblemas.objects.filter(id=numero).update(descripcion=valor)
                
        estado_progreso = Mantenimiento.get_nombre_progreso(request.POST['progreso'])
        notificacion_update_mantenimiento_vehiculos_email_sms(request, solicitud, problemasList, estado_progreso, "actualizado")
        messages.success(request, 'Solicitud Actualizada con Exito', extra_tags='')
        return redirect('manage_maintenance_request') 
    else:
        messages.error(request, 'Solicitud no Procesada', extra_tags='')
        return redirect('edit_maintenance_request') 
    
@login_required
@vehicular_avanzado_required
def status_maintenance_request(request):
    if request.method == 'POST': 
        solicitud = NuevaSolicitudMantenimiento.objects.get(id=request.POST['solicitud_id'])
        if (solicitud.status): 
            NuevaSolicitudMantenimiento.objects.filter(id=request.POST['solicitud_id']).update(status=False)  
            messages.success(request, 'Estado de Solicitud ha cambiado a Terminada')             
        else:            
            NuevaSolicitudMantenimiento.objects.filter(id=request.POST['solicitud_id']).update(status=True) 
            messages.success(request, 'Estado de Solicitud ha cambiado a Activa')  
        return redirect('manage_maintenance_request')
    else:
        return redirect('manage_maintenance_request') 

@login_required
@vehicular_avanzado_required
def new_maintenance_machine_request(request):
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    if usuario.faena.faena == "SIN ASIGNAR":
        maquinas = list(Maquinaria.objects.filter(status=True).order_by('-maquinaria')) 
    else:
        maquinas = list(Maquinaria.objects.filter(faena=usuario.faena, status=True).order_by('-maquinaria')) 

    listamaquinarias = Maquinaria.objects.filter(status=True).order_by('maquinaria')
    datamaquinarias = [{'id': maquinaria.id, 'nombre': maquinaria.maquinaria, 'marca': maquinaria.marca.id} for maquinaria in listamaquinarias]
    listaproblemas = FallaMaquinaria.objects.filter(status=True).order_by('falla')
    dataproblemas = [{'id': problema.id, 'falla': problema.falla, 'marca': problema.kitMaquinaria.marcaMaquina.id if problema.kitMaquinaria else None} for problema in listaproblemas]
    context = {
        'formnuevasolicitud': FormNuevaSolicitudMantenimientoMaquinaria(initial={
            'solicitante': request.user.first_name+" "+request.user.last_name,
            'telefono': request.user.phone,
            'maquinaria': maquinas,
            },
            maquinarias = maquinas,
        ),
        'listaproblemas': dataproblemas,
        'listamaquinarias': datamaquinarias,
        'solicitante_id': request.user.id,
        'sidebar': 'new_maintenance_machine_request',
        'sidebarmain': 'system_machines', 
    }
    return render(request,'pages/maintenance/new_maintenance_machine_request.html', context)

@login_required
@vehicular_avanzado_required
def save_new_maintenance_machine_request(request):     
    if request.method == 'POST':
        maquinaria = Maquinaria.objects.get(id=request.POST['maquinaria'])
        solicitante = Usuario.objects.get(id=request.POST['solicitante_id'])
        ids_problemas = request.POST.getlist('problemas')
        problemas = FallaMaquinaria.objects.filter(id__in=ids_problemas)
        problemasList = FallaMaquinaria.objects.filter(id__in=ids_problemas).values_list('falla', flat=True)
        toggle_Uno = request.POST.get('toggle-Uno', 'no')
        toggle_Dos = request.POST.get('toggle-Dos', 'no')
        
        fotografiaUno = procesar_fotografia_dos(toggle_Uno, 'fotografiaUno', 'base/no-imagen2.png', request)
        fotografiaDos = procesar_fotografia_dos(toggle_Dos, 'fotografiaDos', 'base/no-imagen2.png', request)
        maquinariaFaena = MaquinariaFaena.objects.get(maquinaria=request.POST['maquinaria'], status=True)
            
        mantenimiento = NuevaSolicitudMantenimientoMaquinaria(
                solicitante = solicitante,
                telefono = request.POST['telefono'],
                maquinaria = maquinaria,
                faena = maquinariaFaena.faena,                
                horometro = request.POST['horometro'],   
                progreso = 1,
                turno = request.POST['turno'],
                comentario = request.POST['comentario'],
                avisoJefatura = 'Si',
                fotografiaUno = fotografiaUno,
                fotografiaDos = fotografiaDos,
                status = True,
            )
        mantenimiento.save()
        mantenimiento.problemas.set(problemas)
        
        existe_mantencion_mayor = problemas.filter(falla='Mantención mayor').exists()
        if existe_mantencion_mayor:
            origen = "Mantención mayor"
        else:
            origen = "Mantención"
        
        registro = NuevoHorometro(
                maquinaria = maquinaria,
                horometro = request.POST['horometro'],
                creador = request.user.first_name+" "+request.user.last_name,
                origen = origen,
            )
        registro.save()
        
        estado_progreso = Mantenimiento.get_nombre_progreso('1')
        notificacion_nuevo_mantenimiento_maquinaria_email_sms(request, mantenimiento, problemasList, estado_progreso, "creado")
        messages.success(request, 'Solicitud Realizada con Exito', extra_tags='')
        return redirect('new_maintenance_machine_request')
    else:
        return redirect('new_maintenance_machine_request') 

@login_required
@vehicular_avanzado_required
def manage_maintenance_machine_request(request):
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    if usuario.faena.faena == "SIN ASIGNAR":
        solicitudes = NuevaSolicitudMantenimientoMaquinaria.objects.all().order_by('-fechacreacion')
    else:
        solicitudes = NuevaSolicitudMantenimientoMaquinaria.objects.filter(faena=usuario.faena).order_by('-fechacreacion')

    context = {
        'solicitudes': solicitudes,
        'choicesprogreso': progreso,
        'sidebar': 'manage_maintenance_machine_request',
        'sidebarmain': 'system_machines', 
    }
    return render(request,'pages/maintenance/manage_maintenance_machine_request.html', context)

@login_required
@vehicular_avanzado_required
def edit_maintenance_machine_request(request):
    try:
        request.session['origen_id'] = request.POST['origen_id']            
    except MultiValueDictKeyError:
        request.session['origen_id'] = request.session['origen_id']
    try:
        request.session['edit_solicitud_id'] = request.POST['solicitud_id']            
    except MultiValueDictKeyError:
        request.session['edit_solicitud_id'] = request.session['edit_solicitud_id']
    solicitud = NuevaSolicitudMantenimientoMaquinaria.objects.get(id=request.session['edit_solicitud_id'])
    historial = list(HistorialSolicitudMantenimientoMaquinaria.objects.filter(solicitud=solicitud).order_by('-fechacreacion'))
    problemas_solicitud = list(SolicitudMantenimientoProblemasMaquinaria.objects.filter(solicitudMantenimiento=solicitud)) 
    problemas_seleccionados = solicitud.problemas.all().values_list('pk', flat=True)
    maquinaria_actual = Maquinaria.objects.get(maquinaria=solicitud.maquinaria.maquinaria)
    urlFotografiaUno = solicitud.fotografiaUno
    urlFotografiaDos = solicitud.fotografiaDos
    extensionFotografiaUno = extension_archivo(urlFotografiaUno)
    extensionFotografiaDos = extension_archivo(urlFotografiaDos)
    
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    if usuario.faena.faena == "SIN ASIGNAR":
        maquinas = list(Maquinaria.objects.filter(status=True).order_by('-maquinaria')) 
    else:
        maquinas = list(Maquinaria.objects.filter(faena=usuario.faena, status=True).order_by('-maquinaria')) 
    
    context = {
        'formeditsolicitud': FormEditSolicitudMantenimientoMaquinaria(initial={
            'solicitante': solicitud.solicitante.first_name+" "+solicitud.solicitante.last_name,
            'telefono': solicitud.telefono,
            'maquinaria': solicitud.maquinaria.id,
            'problemas': problemas_seleccionados,
            'horometro': solicitud.horometro,
            'turno': solicitud.turno,
            'comentario': solicitud.comentario,
            },
            maquinaria_actual=maquinaria_actual,
            maquinarias=maquinas,
        ),
        'formprocesarsolicitud': FormProcesarSolicitudMantenimientoMaquinaria(initial={
            'progreso': solicitud.progreso,
            'empresaMantenimiento': solicitud.empresaMantenimiento,
            },
        ),
        'origen': request.session['origen_id'],
        'solicitud': solicitud,
        'historiales': historial,
        'choicesprogreso': progreso,
        'problemas': problemas_solicitud,
        'fotografiaUno': solicitud.fotografiaUno,
        'fotografiaDos': solicitud.fotografiaDos,
        'extensionFotografiaUno': extensionFotografiaUno,
        'extensionFotografiaDos': extensionFotografiaDos,
        'sidebar': 'manage_maintenance_machine_request',
        'sidebarmain': 'system_machines', 
    }
    return render(request,'pages/maintenance/edit_maintenance_machine_request.html', context)

@login_required
@vehicular_avanzado_required
def save_edit_maintenance_machine_request(request):     
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        solicitud = get_object_or_404(NuevaSolicitudMantenimientoMaquinaria, id=solicitud_id)

        historial_mas_reciente = HistorialSolicitudMantenimientoMaquinaria.objects.filter(solicitud=solicitud).order_by('-fechacreacion').first()
        progreso_antiguo_id = str(historial_mas_reciente.progreso) if historial_mas_reciente else "1"
        progreso_nuevo_id = str(request.POST['progreso'])

        # Se implementa un bloque de validación previa para asegurar la integridad del inventario.
        # Antes de procesar la solicitud, se verifica si el cambio de estado implica consumo de stock ('Terminado').
        # El sistema valida la disponibilidad física y el estado administrativo del Kit en la faena antes de permitir el cierre.
        if progreso_nuevo_id == '4' and progreso_antiguo_id != '4':
            
            maquinaria_id = request.POST.get('maquinaria')
            maquinaria_obj = Maquinaria.objects.get(id=maquinaria_id)
            
            maquinaria_faena = MaquinariaFaena.objects.filter(maquinaria=maquinaria_obj, status=True).first()
            faena_solicitud = maquinaria_faena.faena if maquinaria_faena else None

            if not faena_solicitud:
                messages.error(request, "La maquinaria no tiene Faena asignada. No se puede validar el stock.", extra_tags='')
                return redirect('edit_maintenance_machine_request')

            problemas_ids = request.POST.getlist('problemas')
            problemas_qs = FallaMaquinaria.objects.filter(id__in=problemas_ids)

            kits_necesarios = Counter() 
            for problema in problemas_qs:
                if problema.kitMaquinaria:
                    kits_necesarios[problema.kitMaquinaria.id] += 1

            errores_detectados = []
            
            for kit_id, cantidad_necesaria in kits_necesarios.items():
                kit_obj = KitsMaquinaria.objects.get(id=kit_id)
                
                kit_en_faena = KitsMaquinariaFaena.objects.filter(
                    kitMaquinaria=kit_obj, 
                    faena=faena_solicitud
                ).first()

                if not kit_en_faena:
                    errores_detectados.append(f"{kit_obj.nombreKit} (No asignado a esta Faena)")
                    continue

                if not kit_en_faena.status:
                    errores_detectados.append(f"{kit_obj.nombreKit} (DESHABILITADO EN FAENA)")
                    continue

                ultimo_mov = HistorialStockKitsMaquinariaFaena.objects.filter(kitMaquinaria=kit_en_faena).order_by('-fechacreacion').first()
                stock_actual = ultimo_mov.stockActual if ultimo_mov else 0
                
                if stock_actual < cantidad_necesaria:
                    mensaje = f"{kit_obj.nombreKit} (Necesitas: {cantidad_necesaria}, Hay: {stock_actual})"
                    errores_detectados.append(mensaje)

            if errores_detectados:
                lista_texto = ", ".join(errores_detectados)
                messages.error(request, f"NO SE PUEDE TERMINAR: {lista_texto}", extra_tags='')
                return redirect('edit_maintenance_machine_request') 

        # Se encapsula la operación de guardado dentro de una transacción atómica (ACID).
        # Esto garantiza que si ocurre un error durante el descuento de stock o la actualización,
        # se reviertan todos los cambios para evitar inconsistencias en la base de datos.
        try:
            with transaction.atomic():
                if request.POST['empresaMantenimiento'] == "":
                    empresaMantenimiento = None
                else:
                    empresaMantenimiento = EmpresaServicios.objects.get(id=request.POST['empresaMantenimiento'])
                    
                NuevaSolicitudMantenimientoMaquinaria.objects.filter(id=solicitud_id).update(
                    telefono = request.POST['telefono'],
                    turno = request.POST['turno'],
                    maquinaria = request.POST['maquinaria'],
                    horometro = request.POST['horometro'],
                    comentario = request.POST['comentario'],
                    progreso = request.POST['progreso'],
                    empresaMantenimiento = empresaMantenimiento,
                )
                  
                solicitud.refresh_from_db() 

                problemas_seleccionados = request.POST.getlist('problemas')
                problemasList = FallaMaquinaria.objects.filter(id__in=problemas_seleccionados).values_list('falla', flat=True)
                solicitud.problemas.set(problemas_seleccionados)
                
                fotografiaSolicitud = solicitud
                toggle_Uno = request.POST.get('toggle-Uno', 'no')
                procesar_fotografia(fotografiaSolicitud, toggle_Uno, 'fotografiaUno', 'base/no-imagen2.png', request)
                toggle_Dos = request.POST.get('toggle-Dos', 'no')
                procesar_fotografia(fotografiaSolicitud, toggle_Dos, 'fotografiaDos', 'base/no-imagen2.png', request)
    
                fotografiaSolicitud.save()
                
                if progreso_antiguo_id != progreso_nuevo_id or (historial_mas_reciente and historial_mas_reciente.empresaMantenimiento != empresaMantenimiento):
                    HistorialSolicitudMantenimientoMaquinaria.objects.create(
                        solicitud = solicitud,
                        solicitante = request.user,
                        progreso = progreso_nuevo_id,
                        empresaMantenimiento = empresaMantenimiento,
                    )
                     
                    maquina_obj = solicitud.maquinaria
                    maquina_faena_obj = MaquinariaFaena.objects.filter(maquinaria=maquina_obj, status=True).first()
                    faena_solicitud = maquina_faena_obj.faena if maquina_faena_obj else None
            
                    nombre_progreso_nuevo = Mantenimiento.get_nombre_progreso(progreso_nuevo_id)

                    # LOGICA OPTIMIZADA: Agrupación de Kits antes de descontar/devolver
                    # Evita duplicidad en el bucle y asegura descuentos masivos correctos.
                    kits_agrupados = {}
                    for problema in solicitud.problemas.all():
                        if problema.kitMaquinaria:
                            k_id = problema.kitMaquinaria.id
                    
                            if k_id not in kits_agrupados:
                                kits_agrupados[k_id] = {
                                    'cantidad': 0,
                                    'kit_obj': problema.kitMaquinaria,
                                    'fallas': set()
                                }
                            kits_agrupados[k_id]['cantidad'] += 1
                            kits_agrupados[k_id]['fallas'].add(problema.falla)

                    # Lógica de descuento automático de inventario al terminar la mantención.
                    if progreso_nuevo_id == '4' and progreso_antiguo_id != '4':
                        if faena_solicitud:
                            kits_procesados_nombres = []
                            
                            for k_id, datos in kits_agrupados.items():
                                kit_obj = datos['kit_obj']
                                cantidad_a_descontar = datos['cantidad']
                                lista_fallas = ", ".join(datos['fallas'])
                                
                                kit_en_faena = KitsMaquinariaFaena.objects.filter(kitMaquinaria=kit_obj, faena=faena_solicitud).first()
                                 
                                if kit_en_faena:
                                    ultimo_movimiento = HistorialStockKitsMaquinariaFaena.objects.filter(kitMaquinaria=kit_en_faena).order_by('-fechacreacion').first()
                                    stock_actual = ultimo_movimiento.stockActual if ultimo_movimiento else 0
                                    
                                    if stock_actual > 0:
                                        nuevo_stock = stock_actual - cantidad_a_descontar
                                        
                                        HistorialStockKitsMaquinariaFaena.objects.create(
                                            kitMaquinaria=kit_en_faena,
                                            faena=faena_solicitud,
                                            stockMovimiento=-cantidad_a_descontar,
                                            stockActual=nuevo_stock,
                                            descripcion=f"Usado en Mantenimiento #{solicitud.id} por: {lista_fallas}",
                                            creador=f"{request.user.first_name} {request.user.last_name}",
                                            status=True
                                        )
                                         
                                        kit_en_faena.fechacreacion = datetime.datetime.now()
                                        kit_en_faena.save(update_fields=['fechacreacion'])
                                        
                                        kits_procesados_nombres.append(f"{kit_obj.nombreKit} (x{cantidad_a_descontar})")

                                        # Alerta de Stock Mínimo
                                        if nuevo_stock <= kit_obj.stockMinimo:
                                            notificacion_jefe_mantencion_stock_minimo_kit_email_sms(
                                                request,
                                                kit_en_faena,
                                                nuevo_stock
                                            )
                                            
                            if kits_procesados_nombres: 
                                messages.success(request, f"Stock descontado: {', '.join(kits_procesados_nombres)}", extra_tags='')

                    # Lógica de restitución de stock al revertir el estado de 'Terminado'.
                    elif progreso_antiguo_id == '4' and progreso_nuevo_id != '4':
                        if faena_solicitud:
                            kits_devueltos_nombres = []
                            
                            for k_id, datos in kits_agrupados.items():
                                kit_obj = datos['kit_obj']
                                cantidad_a_devolver = datos['cantidad']
                                lista_fallas = ", ".join(datos['fallas']) # Opcional: listar fallas involucradas
                                
                                kit_en_faena = KitsMaquinariaFaena.objects.filter(kitMaquinaria=kit_obj, faena=faena_solicitud).first()
                                 
                                if kit_en_faena:
                                    ultimo_movimiento = HistorialStockKitsMaquinariaFaena.objects.filter(kitMaquinaria=kit_en_faena).order_by('-fechacreacion').first()
                                    stock_actual = ultimo_movimiento.stockActual if ultimo_movimiento else 0
                            
                                    HistorialStockKitsMaquinariaFaena.objects.create(
                                        kitMaquinaria=kit_en_faena,
                                        faena=faena_solicitud,
                                        stockMovimiento=cantidad_a_devolver,
                                        stockActual=stock_actual + cantidad_a_devolver,
                                        descripcion=f"Devolución Mantenimiento #{solicitud.id} (Reabierto a {nombre_progreso_nuevo})",
                                        creador=f"{request.user.first_name} {request.user.last_name}",
                                        status=True
                                    )
                                    
                                    kit_en_faena.fechacreacion = datetime.datetime.now()
                                    kit_en_faena.save(update_fields=['fechacreacion'])
                                    
                                    kits_devueltos_nombres.append(f"{kit_obj.nombreKit} (x{cantidad_a_devolver})")
                            
                            if kits_devueltos_nombres:
                                messages.info(request, f"Stock devuelto al inventario: {', '.join(kits_devueltos_nombres)}", extra_tags='')

            for nombre_campo, valor in request.POST.items():
                if nombre_campo.startswith('valorServicio'):
                    numero = nombre_campo.split('valorServicio')[1]
                    if valor=="": valor="0"
                    try:
                        valorInt =int(valor.replace(".", ""))
                        SolicitudMantenimientoProblemasMaquinaria.objects.filter(id=numero).update(valorServicio=valorInt)
                    except: pass

                if nombre_campo.startswith('descripcion'):
                    numero = nombre_campo.split('descripcion')[1]
                    SolicitudMantenimientoProblemasMaquinaria.objects.filter(id=numero).update(descripcion=valor)

            estado_progreso = Mantenimiento.get_nombre_progreso(request.POST['progreso'])
            notificacion_update_mantenimiento_maquinaria_email_sms(request, solicitud, problemasList, estado_progreso, "actualizado")
            messages.success(request, 'Solicitud Actualizada con Exito', extra_tags='')
            return redirect('manage_maintenance_machine_request') 

        except Exception as e:
            print(f"ERROR CRITICO: {e}")
            messages.error(request, 'Error interno al guardar. Intente nuevamente.', extra_tags='')
            return redirect('edit_maintenance_machine_request')

    else:
        messages.error(request, 'Solicitud no Procesada', extra_tags='')
        return redirect('edit_maintenance_machine_request')
    
@login_required
@vehicular_avanzado_required
def maintenance_pdf_view(request):
    if request.method == 'POST':
        solicitud = NuevaSolicitudMantenimiento.objects.get(id=request.POST['solicitud_id'])
        historial = list(HistorialSolicitudMantenimiento.objects.filter(solicitud=solicitud).order_by('-fechacreacion'))
        problemas_solicitud = list(SolicitudMantenimientoProblemas.objects.filter(solicitudMantenimiento=solicitud))
        fotografiaUno = check_and_convert_pdf(solicitud.fotografiaUno.path)
        fotografiaDos = check_and_convert_pdf(solicitud.fotografiaDos.path)
        fotografiaTres = check_and_convert_pdf(solicitud.fotografiaTres.path)
        current_datetime = datetime.datetime.now()
        context = {
            'solicitud': solicitud,
            'historiales': historial,
            'problemas': problemas_solicitud,
            'fotografiaUno': fotografiaUno,
            'fotografiaDos': fotografiaDos,
            'fotografiaTres': fotografiaTres,
            'current_datetime': current_datetime,
        }
        
        template_path = 'pages/pdfs/maintenance_pdf_template.html'
        template = get_template(template_path)
        html = template.render(context)
        filename = f'{solicitud.vehiculo.placaPatente}-{solicitud.fechacreacion.strftime("%Y%m%d_%H%M%S")}-{current_datetime.strftime("%Y%m%d_%H%M%S")}.pdf'
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs_temp', filename)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        with open(pdf_path, 'wb') as pdf_file:
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
            if pisa_status.err:
                return JsonResponse({'error': 'Error al generar el PDF'})

        pdf_url = os.path.join(settings.MEDIA_URL, 'pdfs_temp', filename)
        return JsonResponse({'pdf_url': pdf_url, 'message': 'Documento creado con éxito'})
    else:
        return redirect('manage_maintenance_request')
    
@login_required
@vehicular_avanzado_required
def maintenance_machine_pdf_view(request):
    if request.method == 'POST':
        solicitud = NuevaSolicitudMantenimientoMaquinaria.objects.get(id=request.POST['solicitud_id'])
        historial = list(HistorialSolicitudMantenimientoMaquinaria.objects.filter(solicitud=solicitud).order_by('-fechacreacion'))
        problemas_solicitud = list(SolicitudMantenimientoProblemasMaquinaria.objects.filter(solicitudMantenimiento=solicitud))
        fotografiaUno = check_and_convert_pdf(solicitud.fotografiaUno.path)
        fotografiaDos = check_and_convert_pdf(solicitud.fotografiaDos.path)
        current_datetime = datetime.datetime.now()
        context = {
            'solicitud': solicitud,
            'historiales': historial,
            'problemas': problemas_solicitud,
            'fotografiaUno': fotografiaUno,
            'fotografiaDos': fotografiaDos,
            'current_datetime': current_datetime,
        }
        
        template_path = 'pages/pdfs/maintenance_machine_pdf_template.html'
        template = get_template(template_path)
        html = template.render(context)
        filename = f'{solicitud.maquinaria.maquinaria}-{solicitud.fechacreacion.strftime("%Y%m%d_%H%M%S")}-{current_datetime.strftime("%Y%m%d_%H%M%S")}.pdf'
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs_temp', filename)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        with open(pdf_path, 'wb') as pdf_file:
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
            if pisa_status.err:
                return JsonResponse({'error': 'Error al generar el PDF'})

        pdf_url = os.path.join(settings.MEDIA_URL, 'pdfs_temp', filename)
        return JsonResponse({'pdf_url': pdf_url, 'message': 'Documento creado con éxito'})
    else:
        return redirect('manage_maintenance_machine_request')