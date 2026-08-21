from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ChecklistMaterialesSonda, ChecklistMaterialesCaseta, EstadoEtapasReporteDigital
from .forms import ChecklistMaterialesSondaEntradaForm, ChecklistMaterialesSondaSalidaForm, ChecklistMaterialesCasetaFormTop, ChecklistMaterialesCasetaFormBottom
from core.forms import FormMaterialesCaseta, FormMaterialesSonda
from core.models import MaterialesCaseta, MaterialesSonda, Sondajes, Sondas
from core.choices import jornada, turno
from django.db.models import Max
from django.http import Http404
from django.utils.dateparse import parse_datetime
import os
from django.db import transaction
from messenger.utils import notify_group
from django.db.models import OuterRef, Subquery
from django import forms
from drilling.models import ReportesOperacionales
from .models import CasetaSondajeAsociado, ChecklistMaterialesCaseta, HistorialMovimientoCaseta
from core.models import Sondajes
from django.urls import reverse
from core.decorators import sondaje_avanzado_required
from drilling.models import ReportesOperacionales

#from core.decorators import sondaje_admin_or_controlador_or_base_datos_or_supervisor_required
#from core.decorators import (
    #sondaje_admin_or_base_datos_or_supervisor_required,
   # sondaje_admin_or_controlador_or_base_datos_or_supervisor_required,
  #  admin_required
#)



@login_required
@sondaje_avanzado_required
def manage_checklist_materiales_sonda(request): 
    lista = ChecklistMaterialesSonda.objects.values('id_checklist', 'fecha_checklist', 'turno', 'jornada', 'creador').distinct().order_by('-fecha_checklist')
    context = {
        'documentos': lista,
        'sidebar': 'manage_checklist_materiales_sonda',
        'sidebarmain': 'system_checklist', 
    }
    return render(request,'pages/checklist/manage_materiales_sonda.html', context)
@login_required
@sondaje_avanzado_required
def save_checklist_materiales_sonda_entrada(request):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Método no permitido.'
        }, status=405)

    form = ChecklistMaterialesSondaEntradaForm(request.POST)

    if not form.is_valid():
        if 'sonda_entrada' in form.errors:
            mensaje = 'Debe ingresar una sonda.'
        elif 'sondaje_entrada' in form.errors:
            mensaje = 'Debe ingresar un sondaje.'
        elif 'serie_entrada' in form.errors:
            mensaje = 'Debe ingresar un número de sondaje.'
        elif 'turno_entrada' in form.errors:
            mensaje = 'Debe seleccionar un turno.'
        elif 'fecha_checklist_entrada' in form.errors:
            mensaje = 'Debe ingresar la fecha del checklist.'
        else:
            mensaje = 'Debe completar todos los campos obligatorios.'

        return JsonResponse({
            'success': False,
            'message': mensaje,
            'titleText': 'Error al guardar'
        }, status=400)

    try:
        with transaction.atomic():
            jornada = '1'
            etapa = 'Entrada'
            progreso = 'Por Revisar'

            turno = form.cleaned_data['turno_entrada']
            fecha_checklist = form.cleaned_data['fecha_checklist_entrada']

            sonda_entrada = Sondas.objects.get(
                sonda=form.cleaned_data['sonda_entrada']
            )

            sondaje_nombre = str(
                form.cleaned_data['sondaje_entrada']
            ).strip()

            sondaje_entrada, created = Sondajes.objects.get_or_create(
                sondaje=sondaje_nombre,
                defaults={
                    'status': True
                }
            )

            serie_entrada = form.cleaned_data['serie_entrada']
            estado_entrada = form.cleaned_data['estado_entrada']

            nombre_sondaje = str(sondaje_entrada.sondaje).strip()
            numero_sondaje = str(serie_entrada).strip()

            caseta_temporal_id = request.POST.get('caseta_temporal_id')

            caseta_asociada = CasetaSondajeAsociado.objects.filter(
                sondaje__iexact=nombre_sondaje,
                numero_sondaje__iexact=numero_sondaje,
                status=True
            ).first()

            if not caseta_asociada and caseta_temporal_id:
                caseta = ChecklistMaterialesCaseta.objects.filter(
                    id_checklist=caseta_temporal_id,
                    status=True
                ).first()

                if caseta:
                    caseta_asociada = CasetaSondajeAsociado.objects.create(
                        id_checklist=str(caseta_temporal_id),
                        nombre_caseta=caseta.nombre_caseta or '',
                        sondaje=nombre_sondaje,
                        numero_sondaje=numero_sondaje,
                        status=True
                    )

            if not caseta_asociada:
                return JsonResponse({
                    'success': False,
                    'message': 'Este sondaje no tiene caseta asignada.'
                }, status=400)

            ultimo_id_checklist = ChecklistMaterialesSonda.objects.aggregate(
                Max('id_checklist')
            )['id_checklist__max'] or 0

            nuevo_id_checklist = int(ultimo_id_checklist) + 1

            materiales_ids = []

            for key in request.POST.keys():
                if key.startswith('agregar_'):
                    material_id = key.replace('agregar_', '')
                    if material_id.isdigit():
                        materiales_ids.append(material_id)

            if not materiales_ids:
                return JsonResponse({
                    'success': False,
                    'message': 'No hay materiales cargados para guardar.'
                }, status=400)

            materialesSonda = MaterialesSonda.objects.filter(
                id__in=materiales_ids
            )

            for material in materialesSonda:
                cantidad = int(request.POST.get(f'cantidad_{material.id}', '') or 0)
                stock = int(request.POST.get(f'stock_{material.id}', 0) or 0)
                agregar = int(request.POST.get(f'agregar_{material.id}', 0) or 0)
                total = int(request.POST.get(f'total_{material.id}', 0) or 0)

                if agregar > 0:
                    material_caseta = ChecklistMaterialesCaseta.objects.select_for_update().filter(
                        id_checklist=caseta_asociada.id_checklist,
                        item__material__iexact=material.material,
                        status=True
                    ).first()

                    if not material_caseta:
                        return JsonResponse({
                            'success': False,
                            'message': f'El material {material.material} no existe en la caseta asociada.'
                        }, status=400)

                    buenos_actuales = material_caseta.b or 0

                    if agregar > buenos_actuales:
                        return JsonResponse({
                            'success': False,
                            'message': f'No hay suficientes materiales en caseta para {material.material}. Disponibles: {buenos_actuales}.'
                        }, status=400)

                ChecklistMaterialesSonda.objects.update_or_create(
                    item=material,
                    id_checklist=nuevo_id_checklist,
                    etapa=etapa,
                    defaults={
                        'stock': stock,
                        'agregar': agregar,
                        'total': total,
                        'cantidad': cantidad,
                        'creador': request.user.first_name + " " + request.user.last_name,
                        'jornada': jornada,
                        'turno': turno,
                        'sonda': sonda_entrada,
                        'sondajeCodigo': sondaje_entrada,
                        'sondajeSerie': serie_entrada,
                        'sondajeEstado': estado_entrada,
                        'progreso': progreso,
                        'status': True,
                        'fecha_checklist': fecha_checklist,
                    }
                )

            estado, created = EstadoEtapasReporteDigital.objects.get_or_create(
                id_checklist=nuevo_id_checklist
            )

            estado.checklistEntrada = True
            estado.reporteDigital = False
            estado.checklistSalida = False
            estado.save()

            subject = f"Nuevo Checklist de Sonda (Entrada): {sonda_entrada}"
            message = f"Creación de Checklist por: {request.user.get_full_name() or request.user.username}\n\n"
            message += "Detalle de cambios:\n"
            message += f"- Identificador: {sonda_entrada}\n"
            message += f"- Fecha: {fecha_checklist.strftime('%d/%m/%Y') if fecha_checklist else 'No especificada'}\n"
            message += f"- Etapa: Entrada"
            notify_group('sondaje_general', subject, message)

        return JsonResponse({
            'success': True,
            'id_checklist': nuevo_id_checklist
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error real al guardar Checklist Entrada: {str(e)}'
        }, status=400)
@login_required
@sondaje_avanzado_required
def save_checklist_materiales_sonda_salida(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

    try:
        nuevo_id_checklist = request.POST.get('id')

        if not nuevo_id_checklist:
            return JsonResponse({
                'success': False,
                'message': 'No se recibió el ID del checklist.'
            }, status=400)

        entrada_base = ChecklistMaterialesSonda.objects.filter(
            id_checklist=nuevo_id_checklist,
            etapa='Entrada',
            status=True
        ).first()

        if not entrada_base:
            return JsonResponse({
                'success': False,
                'message': 'No existe Checklist Entrada para este reporte.'
            }, status=400)

        form = ChecklistMaterialesSondaSalidaForm(request.POST)

        # Si el form es válido usamos sus datos.
        # Si no, usamos los datos del checklist entrada porque los campos disabled no llegan por POST.
        if form.is_valid():
            turno = form.cleaned_data['turno_salida']
            fecha_checklist = form.cleaned_data['fecha_checklist_salida']

            sonda_salida = form.cleaned_data['sonda_salida']
            sonda_salida = Sondas.objects.get(sonda=sonda_salida)

            sondaje_salida = form.cleaned_data['sondaje_salida']
            sondaje_salida = Sondajes.objects.get(sondaje=sondaje_salida)

            serie_salida = form.cleaned_data['serie_salida']
            estado_salida = form.cleaned_data['estado_salida']
        else:
            print("ERRORES FORM SALIDA:", form.errors)

            turno = entrada_base.turno
            fecha_checklist = timezone.now()
            sonda_salida = entrada_base.sonda
            sondaje_salida = entrada_base.sondajeCodigo
            serie_salida = entrada_base.sondajeSerie
            estado_salida = entrada_base.sondajeEstado

        jornada = '2'
        etapa = 'Salida'
        progreso = 'Por Revisar'

        materialesSonda = MaterialesSonda.objects.filter(
            id__in=ChecklistMaterialesSonda.objects.filter(
                id_checklist=nuevo_id_checklist,
                etapa='Entrada',
                status=True
            ).values_list('item_id', flat=True)
        )

        with transaction.atomic():
            for material in materialesSonda:
                sobrante = int(request.POST.get(f'stock_{material.id}', 0) or 0)

                entrada = ChecklistMaterialesSonda.objects.filter(
                    item=material,
                    id_checklist=nuevo_id_checklist,
                    etapa='Entrada',
                    status=True
                ).order_by('-id').first()

                total_disponible = 0

                if entrada:
                    total_disponible = entrada.total if entrada.total is not None else 0

                    if total_disponible == 0:
                        total_disponible = (entrada.stock or 0) + (entrada.agregar or 0)

                if sobrante > total_disponible:
                    return JsonResponse({
                        'success': False,
                        'message': f'No se puede añadir más sobrante de los materiales disponibles para {material.material}. Máximo permitido: {total_disponible}.'
                    }, status=400)

                ChecklistMaterialesSonda.objects.update_or_create(
                    item=material,
                    id_checklist=nuevo_id_checklist,
                    etapa=etapa,
                    defaults={
                        'stock': sobrante,
                        'agregar': 0,
                        'total': sobrante,
                        'creador': request.user.first_name + " " + request.user.last_name,
                        'jornada': jornada,
                        'turno': turno,
                        'sonda': sonda_salida,
                        'sondajeCodigo': sondaje_salida,
                        'sondajeSerie': serie_salida,
                        'sondajeEstado': estado_salida,
                        'progreso': progreso,
                        'status': True,
                        'fecha_checklist': fecha_checklist,
                    }
                )

            estado, created = EstadoEtapasReporteDigital.objects.get_or_create(
                id_checklist=nuevo_id_checklist
            )
            estado.checklistSalida = True
            estado.save()

            subject = f"Nuevo Checklist de Sonda (Salida): {sonda_salida}"
            message = f"Creación de Checklist por: {request.user.get_full_name() or request.user.username}\n\n"
            message += "Detalle de cambios:\n"
            message += f"- Identificador: {sonda_salida}\n"
            message += f"- Fecha: {fecha_checklist.strftime('%d/%m/%Y') if fecha_checklist else 'No especificada'}\n"
            message += f"- Etapa: Salida"
            notify_group('sondaje_general', subject, message)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al guardar Checklist Salida: {str(e)}'
        }, status=400)

@login_required
@sondaje_avanzado_required
def edit_checklist_materiales_sonda(request):
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    checklist_id = request.session['edit_id']
    
    # Obtener los datos de ChecklistMaterialesSonda correspondientes al id_checklist
    checklists = ChecklistMaterialesSonda.objects.filter(id_checklist=checklist_id)

    # Obtener los primeros datos para los valores iniciales del formulario
    first_checklist = checklists.first()  # Usamos first() para obtener el primer resultado

    # Inicializar el formulario con los valores actuales del checklist
    form = ChecklistMaterialesSondaEntradaForm(initial={
        'fecha_checklist_entrada': first_checklist.fecha_checklist,
        'turno_entrada': first_checklist.turno,
        'jornada_entrada': first_checklist.jornada,
        'sonda_entrada': first_checklist.sonda.sonda if first_checklist.sonda else '',
        'sondaje_entrada': first_checklist.sondajeCodigo.sondaje if first_checklist.sondajeCodigo else '',
        'serie_entrada': first_checklist.sondajeSerie,
        'estado_entrada': first_checklist.sondajeEstado,
    })
    
    # Pasar los datos al contexto para el template
    context = {
        'documento_id': first_checklist.id_checklist,
        'form': form,
        'checklist': checklists,
        'sidebar': 'manage_checklist_materiales_sonda',
        'sidebarmain': 'system_checklist',
    }
    return render(request, 'pages/checklist/edit_materiales_sonda.html', context)

@login_required
@sondaje_avanzado_required
def save_edit_checklist_materiales_sonda_entrada(request):
    # Si la solicitud es POST, se actualizan los datos
    if request.method == 'POST':
        # Obtener los valores de turno, jornada
        #turno = request.POST.get('turno')
        #jornada = request.POST.get('jornada')            

        for key, value in request.POST.items():
            if key.startswith('cantidad_'):
                material_id = int(key.split('_')[1])
                checklist = ChecklistMaterialesSonda.objects.get(id=material_id)
                checklist.cantidad = value  # Nueva cantidad
                #checklist.turno = turno  # Actualizar turno
                #checklist.jornada = jornada  # Actualizar jornada
                checklist.save()  # Guardar el registro actualizado
        user_name = request.user.get_full_name() or request.user.username
        notify_group('sondaje_general', 'Checklist entrada editado', f'Checklist entrada editado por: {user_name}')
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    
@login_required
@sondaje_avanzado_required
def save_edit_checklist_materiales_sonda_salida(request):
    # Si la solicitud es POST, se actualizan los datos
    if request.method == 'POST':
        # Obtener los valores de turno, jornada
        #turno = request.POST.get('turno')
        #jornada = request.POST.get('jornada')            

        for key, value in request.POST.items():
            if key.startswith('cantidad_'):
                material_id = int(key.split('_')[1])
                checklist = ChecklistMaterialesSonda.objects.get(id=material_id)
                checklist.cantidad = value  # Nueva cantidad
                #checklist.turno = turno  # Actualizar turno
                #checklist.jornada = jornada  # Actualizar jornada
                checklist.save()  # Guardar el registro actualizado
        user_name = request.user.get_full_name() or request.user.username
        notify_group('sondaje_general', 'Checklist salida editado', f'Checklist salida editado por: {user_name}')
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    
@login_required
@sondaje_avanzado_required
def manage_checklist_materiales_caseta(request):

    lista = ChecklistMaterialesCaseta.objects.values(
        'id_checklist',
        'fecha_checklist',
        'creador',
        'creador_cargo',
        'turno',
        'supervisor',
        'nombre_caseta'
    ).distinct().order_by('-fecha_checklist')

    nombres_casetas = ChecklistMaterialesCaseta.objects.values_list(
        'nombre_caseta',
        flat=True
    ).distinct()

    context = {
        'documentos': lista,
        'nombres_casetas': nombres_casetas,
        'sidebar': 'manage_checklist_materiales_caseta',
        'sidebarmain': 'system_checklist',
    }

    return render(
        request,
        'pages/checklist/manage_materiales_caseta.html',
        context
    )

@login_required
@sondaje_avanzado_required
def new_checklist_materiales_caseta(request):
    materiales = MaterialesCaseta.objects.filter(status=True)

    if request.method == 'POST':

        if not materiales.exists():
            return JsonResponse({
                'success': False,
                'message': 'No hay materiales creados o habilitados para crear una caseta.'
            }, status=400)

        formTop = ChecklistMaterialesCasetaFormTop(request.POST)
        formBottom = ChecklistMaterialesCasetaFormBottom(request.POST, request.FILES)

        if formTop.is_valid():
            creador = formTop.cleaned_data['responsable']
            turno = formTop.cleaned_data['turno']
            fecha_checklist = formTop.cleaned_data['fecha_checklist']
            cargo = formTop.cleaned_data['cargo']

            ultimo_id_checklist = ChecklistMaterialesCaseta.objects.aggregate(
                Max('id_checklist')
            )['id_checklist__max'] or 0

            nuevo_id_checklist = int(ultimo_id_checklist) + 1

            nombre_caseta = request.POST.get('nombre_caseta', '').strip()

            if not nombre_caseta:
                return JsonResponse({
                    'success': False,
                    'message': 'Debe ingresar un nombre de caseta.'
                }, status=400)

            caseta_existente = ChecklistMaterialesCaseta.objects.filter(
                nombre_caseta__iexact=nombre_caseta,
                status=True
            ).exists()

            if caseta_existente:
                return JsonResponse({
                    'success': False,
                    'message': 'Ese nombre de caseta ya está ocupado.'
                }, status=400)

            for material in materiales:
                b = int(request.POST.get(f'b_{material.id}', '') or 0)
                m = int(request.POST.get(f'm_{material.id}', '') or 0)
                observacion = request.POST.get(f'observacion_{material.id}', "")
                fecha_str = request.POST.get(f'fecha_{material.id}', "")
                fotografia = request.FILES.get(f'fotografia_{material.id}', None)

                ChecklistMaterialesCaseta.objects.create(
                    item=material,
                    b=b,
                    m=m,
                    observacion=observacion,
                    fotografiaMaterial=fotografia,
                    creador=creador,
                    creador_cargo=cargo,
                    status=True,
                    turno=turno,
                    id_checklist=nuevo_id_checklist,
                    fecha_checklist=fecha_checklist,
                    fecha_control=parse_datetime(fecha_str) if fecha_str else None,
                    fecha_revision=None,
                    observaciones_revision=None,
                    supervisor=None,
                    nombre_caseta=nombre_caseta,
                )
            
            # Notificar creación (una sola vez por checklist)
            subject = f"Nuevo Checklist de Caseta: {nombre_caseta}"
            message = f"Creación de Checklist por: {creador}\n\n"
            message += "Detalle de cambios:\n"
            message += f"- Identificador: {nombre_caseta}\n"
            message += f"- Fecha: {fecha_checklist.strftime('%d/%m/%Y') if fecha_checklist else 'No especificada'}"
            notify_group('sondaje_general', subject, message)


            return JsonResponse({'success': True})

        return JsonResponse({
            'success': False,
            'message': 'El formulario no es válido.'
        }, status=400)

    responsable = f"{request.user.first_name} {request.user.last_name}"
    role = request.user.role.capitalize()

    formTop = ChecklistMaterialesCasetaFormTop(initial={
        'responsable': responsable,
        'cargo': role,
    })

    formBottom = ChecklistMaterialesCasetaFormBottom()

    context = {
        'formTop': formTop,
        'formBottom': formBottom,
        'materiales': materiales,
        'sidebar': 'new_checklist_materiales_caseta',
        'sidebarmain': 'system_checklist',
    }

    return render(request, 'pages/checklist/new_materiales_caseta.html', context)

@login_required
@sondaje_avanzado_required
def edit_checklist_materiales_caseta(request):

    try:
        request.session['edit_id'] = request.POST['id']
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']

    checklist_id = request.session['edit_id']

    sondajes_asociados = CasetaSondajeAsociado.objects.filter(
        id_checklist=checklist_id,
        status=True
    ).order_by('-fecha')

    historial_movimientos = HistorialMovimientoCaseta.objects.filter(
        id_checklist=checklist_id,
        status=True
    ).order_by('-fecha')

    ultima_observacion = HistorialMovimientoCaseta.objects.filter(
        id_checklist=checklist_id,
        item=OuterRef('item'),
        observacion__isnull=False
    ).exclude(
        observacion=''
    ).order_by('-fecha').values('observacion')[:1]

    checklists = ChecklistMaterialesCaseta.objects.filter(
        id_checklist=checklist_id,
        status=True
    ).annotate(
        ultima_observacion_historial=Subquery(ultima_observacion)
    )

    for item in checklists:
        item.ultima_observacion = (
            item.ultima_observacion_historial
            if item.ultima_observacion_historial
            else item.observacion
        )

    first_checklist = checklists.first()

    formTop = ChecklistMaterialesCasetaFormTop(initial={
        'fecha_checklist': first_checklist.fecha_checklist,
        'turno': first_checklist.turno,
        'responsable': first_checklist.creador,
        'cargo': first_checklist.creador_cargo
    })

    supervisor = f"{request.user.first_name} {request.user.last_name}"

    formBottom = ChecklistMaterialesCasetaFormBottom(initial={
        'supervisor': supervisor,
        'observaciones': first_checklist.observaciones_revision
    })

    # =====================================================
    # COMBINACIONES YA ASOCIADAS A CUALQUIER CASETA
    # =====================================================
    sondajes_ocupados = set(
        CasetaSondajeAsociado.objects.filter(
            status=True
        ).values_list(
            'sondaje',
            'numero_sondaje'
        )
    )

    sondajes_ocupados = {
        (str(sondaje).strip(), str(numero).strip())
        for sondaje, numero in sondajes_ocupados
    }

    # =====================================================
    # TODAS LAS COMBINACIONES CREADAS EN REPORTES
    # =====================================================
    combinaciones_reportes = list(
        ReportesOperacionales.objects.filter(
            status=True
        ).exclude(
            sondajeCodigo__isnull=True
        ).exclude(
            sondajeSerie__isnull=True
        ).values(
            'sondajeCodigo__sondaje',
            'sondajeSerie'
        ).distinct()
    )

    combinaciones_checklist = list(
        ChecklistMaterialesSonda.objects.filter(
            status=True,
            etapa='Entrada'
        ).exclude(
            sondajeCodigo__isnull=True
        ).exclude(
            sondajeSerie__isnull=True
        ).values(
            'sondajeCodigo__sondaje',
            'sondajeSerie'
        ).distinct()
    )

    todas_combinaciones_dict = {}

    for item in combinaciones_reportes + combinaciones_checklist:
        clave = (
            str(item['sondajeCodigo__sondaje']).strip(),
            str(item['sondajeSerie']).strip()
        )
        todas_combinaciones_dict[clave] = item

    todas_combinaciones = sorted(
        todas_combinaciones_dict.values(),
        key=lambda x: (
            str(x['sondajeCodigo__sondaje']).strip(),
            str(x['sondajeSerie']).strip()
        )
    )

    # =====================================================
    # SOLO MOSTRAR LAS QUE NO ESTÉN ASOCIADAS
    # =====================================================
    combinaciones_sondajes = [
        item for item in todas_combinaciones
        if (
            str(item['sondajeCodigo__sondaje']).strip(),
            str(item['sondajeSerie']).strip()
        ) not in sondajes_ocupados
    ]
    materiales_caseta_actual_ids = checklists.values_list('item_id', flat=True)

    materiales_caseta_actual_ids = checklists.values_list('item_id', flat=True)

    materiales_habilitados = MaterialesCaseta.objects.filter(
        status=True
    ).exclude(
        id__in=materiales_caseta_actual_ids
    ).order_by('material')
    

    sondajes_caseta = CasetaSondajeAsociado.objects.filter(
    id_checklist=checklist_id,
    status=True
)

    hay_reporte_en_proceso = False

    for asociado in sondajes_caseta:
        sondaje = str(asociado.sondaje).strip()
        numero = str(asociado.numero_sondaje).strip()

        existe_checklist_en_proceso = ChecklistMaterialesSonda.objects.filter(
            sondajeCodigo__sondaje__iexact=sondaje,
            sondajeSerie=numero,
            status=True,
            progreso__in=[
                'Creado',
                'Por Revisar',
                'Por Corregir',
                'Corregido'
            ]
        ).exists()

        existe_reporte_en_proceso = ReportesOperacionales.objects.filter(
            sondajeCodigo__sondaje__iexact=sondaje,
            sondajeSerie=numero,
            status=True,
            progreso__in=[
                'Creado',
                'Por Revisar',
                'Por Corregir',
                'Corregido'
            ]
        ).exists()

        if existe_checklist_en_proceso or existe_reporte_en_proceso:
            hay_reporte_en_proceso = True
            break

    context = {
        'sondajes_asociados': sondajes_asociados,
        'combinaciones_sondajes': combinaciones_sondajes,
        'documento_id': first_checklist.id_checklist,
        'formTop': formTop,
        'formBottom': formBottom,
        'checklist': checklists,
        'sidebar': 'manage_checklist_materiales_caseta',
        'sidebarmain': 'system_checklist',
        'historial_movimientos': historial_movimientos,
        'materiales_habilitados': materiales_habilitados,
        'materiales_caseta_actual_ids': list(materiales_caseta_actual_ids),
        'hay_reporte_en_proceso': hay_reporte_en_proceso,
    }

    return render(request, 'pages/checklist/edit_materiales_caseta.html', context)

@login_required
@sondaje_avanzado_required
def save_edit_checklist_materiales_caseta(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

    turno = request.POST.get('turno')
    fecha_revision_str = request.POST.get('fecha_revision')
    fecha_revision = parse_datetime(fecha_revision_str) if fecha_revision_str else None
    observaciones_revision = request.POST.get('observaciones')
    supervisor = request.user.first_name + " " + request.user.last_name

    documento_id = request.POST.get('id')
    sondajes_asociados = CasetaSondajeAsociado.objects.filter(
        id_checklist=documento_id,
        status=True
    ).values_list(
        'sondaje',
        'numero_sondaje'
    )

    hay_reporte_en_proceso = False

    for sondaje, numero_sondaje in sondajes_asociados:
        existe_reporte = ReportesOperacionales.objects.filter(
            sondajeCodigo__sondaje__iexact=str(sondaje).strip(),
            sondajeSerie=str(numero_sondaje).strip(),
            status=True,
            progreso__in=[
                'Creado',
                'Por Revisar',
                'Por Corregir',
                'Corregido'
            ]
        ).exists()

        if existe_reporte:
            hay_reporte_en_proceso = True
            break

    if hay_reporte_en_proceso:
        return JsonResponse({
            'success': False,
            'message': 'Hay un reporte en proceso con esta caseta, apruébelo o elimínelo antes de modificar.'
        }, status=400)

    

    accion = request.POST.get('accion_material')
    material_id = request.POST.get('material_movimiento')
    mov_buenos = int(request.POST.get('mov_buenos', 0) or 0)
    mov_malos = int(request.POST.get('mov_malos', 0) or 0)

    try:
        with transaction.atomic():

            datos_revision = {
                'turno': turno,
                'fecha_revision': fecha_revision,
                'observaciones_revision': observaciones_revision,
                'supervisor': supervisor,
            }

            if hasattr(ChecklistMaterialesCaseta, 'progreso'):
                datos_revision['progreso'] = 'Revisado'

            ChecklistMaterialesCaseta.objects.filter(
                id_checklist=documento_id,
                status=True
            ).update(**datos_revision)

            checklists_caseta = ChecklistMaterialesCaseta.objects.filter(
                id_checklist=documento_id,
                status=True
            )

            if not accion and not material_id:
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('manage_checklist_materiales_caseta')
                })

            if accion and not material_id:
                return JsonResponse({
                    'success': False,
                    'message': 'Debe seleccionar un material.'
                }, status=400)

            nueva_observacion = request.POST.get(
                'nueva_observacion_movimiento',
                ''
            ).strip()

            nueva_foto = request.FILES.get('nueva_imagen_movimiento', None)

            if mov_buenos == 0 and mov_malos == 0 and not nueva_observacion and not nueva_foto:
                return JsonResponse({
                    'success': False,
                    'message': 'Debe ingresar buenos, malos, una observación o una imagen.'
                }, status=400)

            caseta_base = ChecklistMaterialesCaseta.objects.filter(
                id_checklist=documento_id,
                status=True
            ).first()

            if not caseta_base:
                return JsonResponse({
                    'success': False,
                    'message': 'No se encontró la caseta.'
                }, status=404)

            # =====================================================
            # AÑADIR A TODOS LOS MATERIALES EXISTENTES EN LA CASETA
            # =====================================================
            if accion == 'editar' and material_id == 'todos':
                checklists = ChecklistMaterialesCaseta.objects.select_for_update().filter(
                    id_checklist=documento_id,
                    status=True
                )

                for checklist in checklists:
                    if not checklist.item.status:
                        
                        continue

                    checklist.b = (checklist.b or 0) + mov_buenos
                    checklist.m = (checklist.m or 0) + mov_malos
                    checklist.turno = turno
                    checklist.fecha_revision = fecha_revision
                    checklist.observaciones_revision = observaciones_revision
                    checklist.supervisor = supervisor

                    if hasattr(checklist, 'progreso'):
                        checklist.progreso = 'Revisado'

                    if nueva_foto:
                        checklist.fotografiaMaterial = nueva_foto

                    checklist.save()

                    HistorialMovimientoCaseta.objects.create(
                        id_checklist=checklist.id_checklist,
                        item=checklist.item,
                        movimiento='MODIFICACION',
                        cantidad=mov_buenos + mov_malos,
                        cantidad_buenos=mov_buenos,
                        cantidad_malos=mov_malos,
                        observacion=nueva_observacion,
                        imagen=nueva_foto if nueva_foto else None,
                        creado_por=supervisor,
                        status=True
                    )

                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('manage_checklist_materiales_caseta')
                })

            # =====================================================
            # AÑADIR MATERIAL NUEVO A ESTA CASETA
            # ejemplo material_id = nuevo_15
            # =====================================================
            if accion == 'anadir' and material_id.startswith('nuevo_'):
                material_base_id = material_id.replace('nuevo_', '')

                material_base = MaterialesCaseta.objects.get(
                    id=material_base_id,
                    status=True
                )

                existe_en_caseta = ChecklistMaterialesCaseta.objects.filter(
                    id_checklist=documento_id,
                    item=material_base,
                    status=True
                ).exists()

                if existe_en_caseta:
                    return JsonResponse({
                        'success': False,
                        'message': 'Este material ya existe en la caseta. Use Editar actuales.'
                    }, status=400)

                ChecklistMaterialesCaseta.objects.create(
                    id_checklist=documento_id,
                    item=material_base,
                    b=mov_buenos,
                    m=mov_malos,
                    observacion=nueva_observacion,
                    fotografiaMaterial=nueva_foto if nueva_foto else None,
                    creador=caseta_base.creador,
                    creador_cargo=caseta_base.creador_cargo,
                    status=True,
                    turno=turno,
                    fecha_checklist=caseta_base.fecha_checklist,
                    fecha_revision=fecha_revision,
                    observaciones_revision=observaciones_revision,
                    supervisor=supervisor,
                    nombre_caseta=caseta_base.nombre_caseta,
                )

                HistorialMovimientoCaseta.objects.create(
                    
                    id_checklist=documento_id,
                    item=material_base,
                    movimiento='INGRESO',
                    cantidad=mov_buenos + mov_malos,
                    cantidad_buenos=mov_buenos,
                    cantidad_malos=mov_malos,
                    observacion='Nuevo material añadido a caseta',
                    imagen=nueva_foto if nueva_foto else None,
                    creado_por=supervisor,
                    status=True
                )
                

                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('manage_checklist_materiales_caseta')
                })

            # =====================================================
            # EDITAR MATERIAL EXISTENTE / AÑADIR A UNO EXISTENTE
            # =====================================================
            checklist = ChecklistMaterialesCaseta.objects.select_for_update().get(
                id=material_id,
                id_checklist=documento_id,
                status=True
            )

            b_actual = checklist.b or 0
            m_actual = checklist.m or 0


            if accion == 'editar':
                checklist.b = b_actual + mov_buenos
                checklist.m = m_actual + mov_malos
                movimiento = 'MODIFICACION'

            elif accion == 'anadir':
                checklist.b = b_actual + mov_buenos
                checklist.m = m_actual + mov_malos
                movimiento = 'INGRESO'

            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Acción no válida.'
                }, status=400)

            checklist.turno = turno
            checklist.fecha_revision = fecha_revision
            checklist.observaciones_revision = observaciones_revision
            checklist.supervisor = supervisor

            if hasattr(checklist, 'progreso'):
                checklist.progreso = 'Revisado'

            if nueva_foto:
                checklist.fotografiaMaterial = nueva_foto

            checklist.save()

            HistorialMovimientoCaseta.objects.create(
                id_checklist=checklist.id_checklist,
                item=checklist.item,
                movimiento=movimiento,
                cantidad=mov_buenos + mov_malos,
                cantidad_buenos=mov_buenos,
                cantidad_malos=mov_malos,
                observacion=nueva_observacion,
                imagen=nueva_foto if nueva_foto else None,
                creado_por=supervisor,
                status=True
            )

        user_name = request.user.get_full_name() or request.user.username
        notify_group('sondaje_general', 'Checklist caseta editado', f'Checklist caseta {documento_id} editado por: {user_name}')
        return JsonResponse({
            'success': True,
            'redirect_url': reverse('manage_checklist_materiales_caseta')
        })

    except MaterialesCaseta.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'El material seleccionado no existe o está deshabilitado.'
        }, status=404)

    except ChecklistMaterialesCaseta.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'El material seleccionado no pertenece a esta caseta.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error al guardar: {str(e)}'
        }, status=500)


@login_required
@sondaje_avanzado_required
def desasociar_sondaje_caseta(request):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Método no permitido.'
        }, status=405)

    asociado_id = request.POST.get('asociado_id')

    if not asociado_id:
        return JsonResponse({
            'success': False,
            'message': 'No se recibió el sondaje asociado.'
        }, status=400)

    asociado = CasetaSondajeAsociado.objects.filter(
        id=asociado_id,
        status=True
    ).first()

    if not asociado:
        return JsonResponse({
            'success': False,
            'message': 'El sondaje asociado no existe.'
        }, status=404)

    sondaje = str(asociado.sondaje).strip()
    numero_sondaje = str(asociado.numero_sondaje).strip()

    estados_en_proceso = [
        'Creado',
        'Por Revisar',
        'Por Corregir',
        'Corregido',
    ]

    checklist_en_proceso = ChecklistMaterialesSonda.objects.filter(
        sondajeCodigo__sondaje__iexact=sondaje,
        sondajeSerie=numero_sondaje,
        status=True,
        progreso__in=estados_en_proceso
    ).exists()

    reporte_en_proceso = ReportesOperacionales.objects.filter(
        sondajeCodigo__sondaje__iexact=sondaje,
        sondajeSerie=numero_sondaje,
        status=True,
        progreso__in=estados_en_proceso
    ).exists()

    if checklist_en_proceso or reporte_en_proceso:
        return JsonResponse({
            'success': False,
            'message': (
                f'No se puede desasociar {sondaje} - {numero_sondaje} porque tiene '
                'un reporte en proceso. Apruébelo o elimínelo antes de continuar.'
            )
        }, status=400)

    asociado.status = False
    asociado.save()

    user_name = request.user.get_full_name() or request.user.username
    notify_group('sondaje_general', 'Sondaje desasociado de caseta', f'Sondaje {asociado.sondaje} desasociado de caseta {asociado.nombre_caseta or asociado.id_checklist} por: {user_name}')

    return JsonResponse({
        'success': True,
        'message': 'Sondaje desasociado correctamente.',
        'sondaje': asociado.sondaje,
        'numero_sondaje': asociado.numero_sondaje,
    })
@login_required
@sondaje_avanzado_required
def asociar_sondaje_caseta(request):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Método no permitido.'
        }, status=405)

    id_checklist = request.POST.get('id_checklist')
    sondaje_seleccionado = request.POST.get('sondaje_asociado')

    if not id_checklist:
        return JsonResponse({
            'success': False,
            'message': 'No se recibió la caseta.'
        }, status=400)

    if not sondaje_seleccionado:
        return JsonResponse({
            'success': False,
            'message': 'Debe seleccionar un sondaje.'
        }, status=400)

    try:
        sondaje, numero_sondaje = sondaje_seleccionado.split('|')
    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'Formato de sondaje inválido.'
        }, status=400)

    sondaje = sondaje.strip()
    numero_sondaje = str(numero_sondaje).strip()

    caseta = ChecklistMaterialesCaseta.objects.filter(
        id_checklist=id_checklist,
        status=True
    ).first()

    if not caseta:
        return JsonResponse({
            'success': False,
            'message': 'No se encontró la caseta.'
        }, status=404)

    ya_ocupado = CasetaSondajeAsociado.objects.filter(
        sondaje__iexact=sondaje,
        numero_sondaje__iexact=numero_sondaje,
        status=True
    ).exists()

    if ya_ocupado:
        return JsonResponse({
            'success': False,
            'message': 'Ese sondaje ya está asociado a una caseta.'
        }, status=400)

    asociado = CasetaSondajeAsociado.objects.create(
        id_checklist=id_checklist,
        nombre_caseta=caseta.nombre_caseta or '',
        sondaje=sondaje,
        numero_sondaje=numero_sondaje,
        status=True
    )

    user_name = request.user.get_full_name() or request.user.username
    notify_group('sondaje_general', 'Sondaje asociado a caseta', f'Sondaje {sondaje} asociado a caseta {caseta.nombre_caseta or id_checklist} por: {user_name}')

    return JsonResponse({
        'success': True,
        'message': 'Sondaje asociado correctamente.',
        'id': asociado.id,
        'sondaje': asociado.sondaje,
        'numero_sondaje': asociado.numero_sondaje
    })


@login_required
@sondaje_avanzado_required
def obtener_casetas_disponibles(request):
    casetas = ChecklistMaterialesCaseta.objects.filter(
        status=True
    ).values(
        'id_checklist',
        'nombre_caseta'
    ).distinct().order_by('nombre_caseta')

    data = [
        {
            'id_checklist': c['id_checklist'],
            'nombre_caseta': c['nombre_caseta']
        }
        for c in casetas
        if c['nombre_caseta']
    ]

    return JsonResponse({
        'success': True,
        'casetas': data
    })

@login_required
@sondaje_avanzado_required
def asociar_sondaje_caseta_desde_reporte(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

    id_checklist = request.POST.get('id_checklist')
    sondaje_valor = request.POST.get('sondaje_id')
    numero_sondaje = request.POST.get('numero_sondaje')

    if not id_checklist or not sondaje_valor or not numero_sondaje:
        return JsonResponse({
            'success': False,
            'message': 'Faltan datos para asociar el sondaje.'
        }, status=400)

    caseta = ChecklistMaterialesCaseta.objects.filter(
        id_checklist=id_checklist,
        status=True
    ).first()

    if not caseta:
        return JsonResponse({
            'success': False,
            'message': 'No se encontró la caseta seleccionada.'
        }, status=404)

    sondaje_obj = None

    if str(sondaje_valor).isdigit():
        sondaje_obj = Sondajes.objects.filter(id=sondaje_valor).first()

    if not sondaje_obj:
        sondaje_obj = Sondajes.objects.filter(
            sondaje__iexact=str(sondaje_valor).strip()
        ).first()

    if not sondaje_obj:
        return JsonResponse({
            'success': False,
            'message': 'No se encontró el sondaje seleccionado.'
        }, status=404)

    nombre_sondaje = str(sondaje_obj.sondaje).strip()
    numero_sondaje = str(numero_sondaje).strip()

    ocupado = CasetaSondajeAsociado.objects.filter(
        sondaje__iexact=nombre_sondaje,
        numero_sondaje__iexact=numero_sondaje,
        status=True
    ).exists()

    if ocupado:
        return JsonResponse({
            'success': False,
            'message': 'Ese sondaje ya está asociado a una caseta.'
        }, status=400)

    asociado = CasetaSondajeAsociado.objects.create(
        id_checklist=id_checklist,
        nombre_caseta=caseta.nombre_caseta or '',
        sondaje=nombre_sondaje,
        numero_sondaje=numero_sondaje,
        status=True
    )

    user_name = request.user.get_full_name() or request.user.username
    notify_group('sondaje_general', f'Sondaje {nombre_sondaje} asociado a caseta', f'Sondaje {nombre_sondaje} asociado a caseta {caseta.nombre_caseta or id_checklist} por: {user_name}')

    return JsonResponse({
        'success': True,
        'message': 'Sondaje asociado correctamente.',
        'id': asociado.id,
        'id_checklist': asociado.id_checklist,
        'nombre_caseta': asociado.nombre_caseta,
        'sondaje': asociado.sondaje,
        'numero_sondaje': asociado.numero_sondaje,
    })


@login_required
@sondaje_avanzado_required
def obtener_materiales_caseta_por_id(request):
    id_checklist = request.GET.get('id_checklist')

    if not id_checklist:
        return JsonResponse({
            'success': False,
            'message': 'No se recibió la caseta.'
        }, status=400)

    caseta_base = ChecklistMaterialesCaseta.objects.filter(
        id_checklist=id_checklist,
        status=True
    ).first()

    if not caseta_base:
        return JsonResponse({
            'success': False,
            'message': 'No se encontró la caseta seleccionada.'
        }, status=404)

    materiales_caseta = ChecklistMaterialesCaseta.objects.filter(
            id_checklist=id_checklist,
            status=True,
            usar_en_reporte=True
        ).select_related('item')

    materiales = {}

    for mat in materiales_caseta:
        nombre_material = str(mat.item.material).strip()

        material_sonda, creado = MaterialesSonda.objects.get_or_create(
            material__iexact=nombre_material,
            defaults={
                'material': nombre_material,
                'status': mat.item.status,
                'creador': 'Sistema',
            }
        )

        materiales[str(material_sonda.id)] = {
            'id': material_sonda.id,
            'nombre': nombre_material,
            'buenos': mat.b or 0,
            'malos': mat.m or 0,
            'total': (mat.b or 0) + (mat.m or 0),
            'status': mat.item.status,
        }

    return JsonResponse({
        'success': True,
        'caseta': caseta_base.nombre_caseta,
        'materiales': materiales,
    })

@login_required
@sondaje_avanzado_required
def cambiar_usar_material_reporte(request):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Método no permitido.'
        }, status=405)

    try:
        material_id = request.POST.get('id')
        usar = request.POST.get('usar') == 'true'

        material = ChecklistMaterialesCaseta.objects.get(
            id=material_id,
            status=True
        )

        material.usar_en_reporte = usar
        material.save(update_fields=['usar_en_reporte'])

        user_name = request.user.get_full_name() or request.user.username
        notify_group('sondaje_general', f'Material {"usado" if usar else "no usado"} en reportes', f'Material {material.item} cambiado por: {user_name}')

        return JsonResponse({
            'success': True,
            'usar_en_reporte': material.usar_en_reporte
        })

    except ChecklistMaterialesCaseta.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Material no encontrado.'
        }, status=404)