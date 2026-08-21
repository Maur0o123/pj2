from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FormMaquinaria, FormNuevoHorometro, FormNuevoKitReparacionFaena, FormEditKitsMaquinariaFaena, FormEditKitsMaquinariaFaenaAdd
from .models import Maquinaria, MaquinariaFaena, NuevoHorometro, HistorialStockKitsMaquinariaFaena, KitsMaquinariaFaena
from django.utils.datastructures import MultiValueDictKeyError
from core.models import TipoMaquinaria, MarcaMaquinaria, Faena, FallaMaquinaria
from core.utils import procesar_fotografia, validar_campo_vacio, formatear_fecha
from django.http import JsonResponse
from user.models import User, Usuario, UsuarioProfile
from maintenance.models import NuevaSolicitudMantenimientoMaquinaria
from core.choices import progreso
import datetime
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db import IntegrityError
from django.db.models import Max, Subquery, OuterRef
from messenger.views import notificacion_maquinarias_email, notificacion_admin_jefe_mantencion_email, notificacion_nuevo_horometro_email
from core.decorators import vehicular_basico_required, vehicular_avanzado_required, vehicular_admin_db_required

@login_required
@vehicular_avanzado_required
def new_machine(request): 
    context = {
        'formnuevamaquinaria': FormMaquinaria,   
        'sidebar': 'manage_machines',
        'sidebarmain': 'system_machines',
    }
    return render(request,'pages/machine/new_machine.html', context)

@login_required
@vehicular_avanzado_required
def manage_machines(request):
    #request.session.pop('edit_username',None)
    #request.session.save()
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    if usuario.faena.faena == "SIN ASIGNAR":
        maquinarias = list(Maquinaria.objects.all().order_by('-fechacreacion'))
    else:
        maquinarias = list(Maquinaria.objects.filter(faena=usuario.faena).order_by('-fechacreacion'))

    context = {
        'faenausuario': usuario.faena,
        'maquinarias': maquinarias,
        'sidebar': 'manage_machines',
        'sidebarmain': 'system_machines',  
    }
    return render(request,'pages/machine/manage_machines.html', context)

@login_required
@vehicular_avanzado_required
def save_new_machine(request): 
    if request.method == 'POST':    
        nombre_maquinaria = request.POST.get('maquinaria')
        if Maquinaria.objects.filter(maquinaria=nombre_maquinaria).exists():
            return JsonResponse({'error': f'El nombre "{nombre_maquinaria}" ya se encuentra registrado.'}, status=400)
        
        tipo_instancia = TipoMaquinaria.objects.get(pk=request.POST['tipo'])    
        marca_instancia = MarcaMaquinaria.objects.get(pk=request.POST['marca'])  
        faena_instancia = Faena.objects.get(pk=request.POST['faena'])
        formulario = FormMaquinaria(data=request.POST)
        fechaAdquisicion = validar_campo_vacio('fechaAdquisicion',request)
        frecuenciaMantenimiento = validar_campo_vacio('frecuenciaMantenimiento',request)
        
        if formulario.is_valid():               
            maquinaria = Maquinaria(
                maquinaria = request.POST['maquinaria'],
                descripcion = request.POST['descripcion'],
                fechaAdquisicion = fechaAdquisicion,
                tipo = tipo_instancia,
                marca = marca_instancia,
                faena = faena_instancia,
                frecuenciaMantenimiento = frecuenciaMantenimiento,
                status = True,
            )    
            maquinaria.save()
            
            maquinaria = Maquinaria.objects.get(maquinaria=request.POST['maquinaria'])
            faena = MaquinariaFaena(
                maquinaria = maquinaria,
                faena = faena_instancia,
                status = True,
                creador = request.user.get_full_name() or request.user.username,                
            )
            faena.save()

            # Crear registro de horómetro actual
            NuevoHorometro.objects.create(
                maquinaria=maquinaria,
                horometro=request.POST['horometro_actual'],
                creador=request.user.get_full_name() or request.user.username,
                origen='Formulario'
            )

            # Obtener/crear falla "Mantención General"
            falla_nombre = 'Mantención General'
            falla = FallaMaquinaria.objects.filter(falla__iexact=falla_nombre).first()
            if not falla:
                falla = FallaMaquinaria.objects.filter(falla__iexact='Mantencion General').first()
            if not falla:
                falla = FallaMaquinaria.objects.create(
                    falla=falla_nombre,
                    kitMaquinaria=None,
                    creador=request.user.get_full_name() or request.user.username,
                    status=True
                )
            elif falla.falla != falla_nombre:
                falla.falla = falla_nombre
                falla.save()

            # Crear solicitud de mantenimiento general
            mantenimiento = NuevaSolicitudMantenimientoMaquinaria(
                solicitante=Usuario.objects.get(id=request.user.id),
                maquinaria=maquinaria,
                faena=faena_instancia,
                horometro=request.POST['horometro_ultima_mantencion'],
                progreso='4',
                comentario='Mantención general al crear maquinaria',
                avisoJefatura='Si',
                status=True,
            )
            mantenimiento.save()
            mantenimiento.problemas.set([falla])

            return JsonResponse({'success': True})          
        else:                
            return JsonResponse({'error': 'Error en los datos ingresados, verifique el formulario.'}, status=400)
    else:
        return redirect('new_machine')

@login_required
@vehicular_avanzado_required
def status_machine(request):
    if request.method == 'POST': 
        maquinaria = Maquinaria.objects.get(id=request.POST['maquinaria_id'])
        if (maquinaria.status):
            maquinaria.status = False
            maquinaria.save()
            messages.success(request, 'Maquinaria Deshabilitada Correctamente')
            return redirect('manage_machines') 
        else:          
            maquinaria.status = True
            maquinaria.save()
            messages.success(request, 'Maquinaria Habilitada Correctamente')  
        return redirect('manage_machines') 
    else:
        return redirect('manage_machines') 

@login_required
@vehicular_avanzado_required
def edit_machine_profile(request):
    try:
        request.session['edit_machine_id'] = request.POST['maquinaria_id']        
    except MultiValueDictKeyError:
        request.session['edit_machine_id'] = request.session['edit_machine_id']
    maquinaria = Maquinaria.objects.get(id=request.session['edit_machine_id'])
    solicitudesMantenimiento = NuevaSolicitudMantenimientoMaquinaria.objects.filter(maquinaria=maquinaria).order_by('-fechacreacion')
    tipo_actual = TipoMaquinaria.objects.filter(tipo=maquinaria.tipo)
    marca_actual = MarcaMaquinaria.objects.filter(marca=maquinaria.marca)
    faena_actual = Faena.objects.filter(faena=maquinaria.faena)
    fecha_adquisicion = formatear_fecha(maquinaria.fechaAdquisicion)
    historialfaenas = list(MaquinariaFaena.objects.filter(maquinaria=maquinaria).order_by('-fechacreacion'))
    horometros = NuevoHorometro.objects.filter(maquinaria=maquinaria).order_by('-fechacreacion')
    perfil = getattr(request.user, 'usuarioprofile', None)
    if perfil and perfil.seccionVehicular == "SUPERVISOR":
        faena_disabled = True
    else:
        faena_disabled = False 
    context = {
        'sidebar': 'manage_machines',
        'sidebarmain': 'system_machines',
        'maquinaria': maquinaria,
        'faena':maquinaria.faena.id,
        'historialfaenas': historialfaenas,
        'solicitudesMantenimiento': solicitudesMantenimiento,
        'choicesprogreso': progreso,
        'horometros': horometros,
        'formnuevamaquinaria': FormMaquinaria(initial={
            'maquinaria': maquinaria.maquinaria,
            'descripcion': maquinaria.descripcion,
            'fechaAdquisicion': fecha_adquisicion,
            'tipo': maquinaria.tipo,
            'marca': maquinaria.marca,
            'faena': maquinaria.faena,
            'frecuenciaMantenimiento': maquinaria.frecuenciaMantenimiento,
            },
            tipo_actual=tipo_actual,
            marca_actual=marca_actual,
            faena_actual=faena_actual,
            faena_disabled=faena_disabled,
            es_creacion=False,
        ),          
    }
    return render(request,'pages/machine/edit_machine_profile.html', context)

@login_required
@vehicular_avanzado_required
def save_edit_machine_profile(request):  
    if request.method == 'POST': 
        try:
            fechaAdquisicion = validar_campo_vacio('fechaAdquisicion',request)
            frecuenciaMantenimiento = validar_campo_vacio('frecuenciaMantenimiento',request)
            tipo = validar_campo_vacio('tipo',request)
            marca = validar_campo_vacio('marca',request)
            faena_id = request.POST['faena']
            
            maquinaria = Maquinaria.objects.get(id=request.POST['maquinaria_id'])
            if str(maquinaria.faena.id) != str(faena_id):
                MaquinariaFaena.objects.filter(maquinaria=maquinaria,status=True).update(status=False)
                nueva_faena = Faena.objects.get(id=faena_id)
                faena_obj = MaquinariaFaena(
                    maquinaria = maquinaria,
                    faena = nueva_faena,
                    status = True,
                    creador = request.user.get_full_name() or request.user.username,                
                )
                faena_obj.save()
            
            maquinaria.maquinaria = request.POST['maquinaria']
            maquinaria.descripcion = request.POST['descripcion']
            maquinaria.fechaAdquisicion = fechaAdquisicion
            if tipo:
                maquinaria.tipo = TipoMaquinaria.objects.get(id=tipo)
            if marca:
                maquinaria.marca = MarcaMaquinaria.objects.get(id=marca)
            maquinaria.faena = Faena.objects.get(id=faena_id)
            maquinaria.frecuenciaMantenimiento = frecuenciaMantenimiento
            maquinaria.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else: 
        return redirect('manage_machines') 

@login_required
@vehicular_avanzado_required
def cargar_marca_por_tipo(request):
    tipo_id = request.GET.get('tipo_id')
    if tipo_id:
        marcas = MarcaMaquinaria.objects.filter(tipo=tipo_id,status=True)
        data = [{'id': marca.id, 'nombre': marca.marca} for marca in marcas]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({}, status=400)

@login_required    
@vehicular_avanzado_required
def new_horometro_register(request):
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    if usuario.faena.faena == "SIN ASIGNAR":
        maquinarias = Maquinaria.objects.filter(status=True).order_by('-maquinaria')
    else:
        maquinarias = Maquinaria.objects.filter(faena=usuario.faena, status=True).order_by('-maquinaria')

    context = {
        'formnuevohorometro': FormNuevoHorometro(maquinarias=maquinarias),   
        'sidebar': 'new_horometro_register',
        'sidebarmain': 'system_machines',
    }
    return render(request,'pages/machine/new_horometro.html', context)

@login_required
@vehicular_avanzado_required
def save_new_horometro_register(request):
    if request.method == 'POST':
        #formulario = FormNuevoHorometro(data=request.POST)
        maquinaria = Maquinaria.objects.get(id= request.POST['maquinaria'])
        registro = NuevoHorometro(
            maquinaria = maquinaria,
            horometro = request.POST['horometro'],
            creador = request.user.get_full_name() or request.user.username,
            origen = "Formulario"
        )
        registro.save()             
        return JsonResponse({'success': True})
    else:
        return redirect('new_kilometraje_register')

@login_required
@vehicular_avanzado_required
def machine_pdf_view(request):
    if request.method == 'POST':
        maquinaria = get_object_or_404(Maquinaria, id=request.POST['maquinaria_id'])
        current_datetime = datetime.datetime.now()

        perfil = getattr(request.user, 'usuarioprofile', None)
        context = {
            'maquinaria': maquinaria,
            'user_role': perfil.seccionVehicular if perfil else 'SIN ASIGNAR',
            'current_datetime': current_datetime,
        }

        template_path = 'pages/pdfs/machine_pdf_template.html'
        template = get_template(template_path)
        html = template.render(context)
        filename = f'{maquinaria.maquinaria}-{current_datetime.strftime("%Y%m%d_%H%M%S")}.pdf'
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs_temp', filename)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        with open(pdf_path, 'wb') as pdf_file:
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
            if pisa_status.err:
                return JsonResponse({'error': 'Error al generar el PDF'})

        pdf_url = os.path.join(settings.MEDIA_URL, 'pdfs_temp', filename)
        return JsonResponse({'pdf_url': pdf_url, 'message': 'Documento creado con éxito'})
    else:
        return redirect('manage_machines')

@login_required
@vehicular_avanzado_required
def manage_machines_kits_repair(request):
    # Se reestructura la consulta para listar asignaciones de Kits (KitsMaquinariaFaena) en lugar de registros históricos brutos.
    # Se implementa una lógica de cálculo de stock en tiempo real, obteniendo el saldo del último movimiento registrado 
    # para cada asignación, lo que permite visualizar la disponibilidad actual y consolidada del inventario por Faena.
    asignaciones = KitsMaquinariaFaena.objects.all().order_by('-status', '-fechacreacion')
    
    kits_para_mostrar = []

    for asignacion in asignaciones:
        ultimo_historial = HistorialStockKitsMaquinariaFaena.objects.filter(
            kitMaquinaria=asignacion
        ).order_by('-fechacreacion').first()
        
        stock_real = ultimo_historial.stockActual if ultimo_historial else 0
        asignacion.stock_calculado = stock_real 
        kits_para_mostrar.append(asignacion)

    context = {
        'kits_faena': kits_para_mostrar,
        'sidebar': 'manage_machines_kits_repair',
        'sidebarmain': 'system_machines', 
    }
    
    return render(request, 'pages/machine/manage_machines_kits_repair.html', context)

@login_required
@vehicular_avanzado_required
def new_machines_kits_repair(request):
    context = {
        'formnuevokitsfaena': FormNuevoKitReparacionFaena,
        'sidebar': 'manage_machines_kits_repair',
        'sidebarmain': 'system_machines',
    }
    return render(request,'pages/machine/new_machines_kits_repair.html', context)

@login_required
@vehicular_avanzado_required
def save_new_machines_kits_repair(request):
    if request.method == 'POST':
        form = FormNuevoKitReparacionFaena(request.POST)
        if form.is_valid():
            try:
                nueva_solicitud = form.save(commit=False)
                nueva_solicitud.status = True
                nueva_solicitud.creador = request.user.get_full_name() or request.user.username
                nueva_solicitud.save()
                stock_inicial = nueva_solicitud.kitMaquinaria.stockMaximo or 0
                nueva = HistorialStockKitsMaquinariaFaena(
                    kitMaquinaria = nueva_solicitud,
                    faena = nueva_solicitud.faena,
                    stockMovimiento = stock_inicial, 
                    stockActual = stock_inicial,   
                    descripcion = 'Creación del Kit (Stock Inicial Completo)',
                    creador = request.user.get_full_name() or request.user.username,
                    status = True,
                )
                nueva.save()
                return JsonResponse({'success': True})
            except IntegrityError:
                return JsonResponse({'error': 'Error al generar el Kit'})
    else:
        return redirect('new_machines_kits_repair')
        
@login_required
@vehicular_avanzado_required
def status_machines_kits_repair(request):
    if request.method == 'POST': 
        try:
            kit_faena_id = request.POST.get('kit_id')
            kit_faena = get_object_or_404(KitsMaquinariaFaena, id=kit_faena_id)
            
            if kit_faena.status: 
                kit_faena.status = False
                kit_faena.save()
                messages.success(request, 'Kit en Faena Deshabilitado')             
            else:            
                kit_faena.status = True
                kit_faena.save()
                messages.success(request, 'Kit en Faena Habilitado')  
            
            return redirect('manage_machines_kits_repair')
        except Exception as e:
            messages.error(request, 'Error al cambiar estado')
            return redirect('manage_machines_kits_repair')
    else:
        return redirect('manage_machines_kits_repair')
    
@login_required
@vehicular_avanzado_required
def edit_machines_kits_repair(request):
    try:
        if request.method == 'POST' and 'kit_faena_id' in request.POST:
            request.session['kit_faena_id'] = request.POST['kit_faena_id']
        
        kit_faena_id = request.session.get('kit_faena_id')
        
        if not kit_faena_id:
            return redirect('manage_machines_kits_repair')

    except MultiValueDictKeyError:
        return redirect('manage_machines_kits_repair')

    kit_asignado = get_object_or_404(KitsMaquinariaFaena, id=kit_faena_id)

    historial = HistorialStockKitsMaquinariaFaena.objects.filter(kitMaquinaria=kit_asignado ).order_by('-fechacreacion')
    ultimo_registro = historial.first()
    stock_actual = ultimo_registro.stockActual if ultimo_registro else 0

    context = {
        'sidebar': 'manage_machines_kits_repair',
        'sidebarmain': 'system_machines',

        'kit_asignado': kit_asignado, 
        'kit_faena_id': kit_asignado.id,
        'stock_actual': stock_actual,
        
        'formeditkit': FormEditKitsMaquinariaFaena(initial={
            'kitMaquinaria': kit_asignado.kitMaquinaria,
            'faena': kit_asignado.faena,
            'stockActual': stock_actual,
        }),
        
        'formeditkitadd': FormEditKitsMaquinariaFaenaAdd, 
        'historial': historial,
    }
    
    return render(request, 'pages/machine/edit_machines_kits_repair.html', context)
    
@login_required
@vehicular_avanzado_required
def save_edit_machines_kits_repair(request):
    if request.method == 'POST':
        try:
            kit_faena_id = request.POST.get('kit_faena_id')
            kit_asignado = get_object_or_404(KitsMaquinariaFaena, id=kit_faena_id)

            ultimo_historial = HistorialStockKitsMaquinariaFaena.objects.filter(
                kitMaquinaria=kit_asignado
            ).order_by('-fechacreacion').first()
         
            stock_actual_anterior = ultimo_historial.stockActual if ultimo_historial else 0
            
            movimiento = int(request.POST['stockMovimiento'])
            nuevo_stock = stock_actual_anterior + movimiento
            
            nueva_entrada = HistorialStockKitsMaquinariaFaena(
                kitMaquinaria = kit_asignado,
                faena = kit_asignado.faena,
                stockMovimiento = movimiento,
                stockActual = nuevo_stock,
                descripcion = request.POST['descripcion'],
                creador = request.user.get_full_name() or request.user.username,
                status = True,
            )
            nueva_entrada.save()
            kit_asignado.fechacreacion = datetime.datetime.now()
            kit_asignado.save(update_fields=['fechacreacion'])
            messages.success(request, 'Stock agregado Correctamente') 
            return redirect('manage_machines_kits_repair') 

        except Exception as e:
            print(e)
            messages.error(request, 'Error al Agregar Stock, intente Nuevamente') 
            return redirect('manage_machines_kits_repair') 

    else:
        return redirect('manage_machines_kits_repair')