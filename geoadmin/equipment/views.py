from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from core.decorators import mantenedor_sistema_required, sondaje_avanzado_required
from .models import MarcaEquipo, TipoEquipo, NuevoEquipamiento
from .forms import FormMarcaEquipo, FormNuevoEquipamiento, FormTipoEquipo
from messenger.utils import notify_group, get_changes_message
from core.models import Faena
from core.utils import formatear_fecha

@login_required
@sondaje_avanzado_required
def manage_types_equipment(request): 
    storage = messages.get_messages(request)
    storage.used = True
    tipos = list(TipoEquipo.objects.all().order_by('id'))
    context = {
        'tipos': tipos,
        'sidebarsubmenu': 'manage_typeequipment',
        'sidebarmenu': 'manage_equipment',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/equipment/manage_types_equipment.html', context)

@login_required
@mantenedor_sistema_required
def new_type_equipment(request):     
    context = {
        'formnuevotipomaquinaria': FormTipoEquipo, 
        'sidebarsubmenu': 'manage_typeequipment',
        'sidebarmenu': 'manage_equipment',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/equipment/new_type_equipment.html', context)

@login_required
@mantenedor_sistema_required
def save_new_type_equipment(request):     
    if request.method == 'POST':
        formulario = FormTipoEquipo(data=request.POST)
        if formulario.is_valid():       
            tipo = TipoEquipo(
                tipo = request.POST['tipo'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            tipo.save()
            user_name = request.user.get_full_name() or request.user.username
            action = 'creada'.capitalize()
            mensaje = f'Mantenedor de Tipo equipo: {tipo} \n{action} por: {user_name}'
            subject = f'Mantenedor de Tipo equipo: {tipo} {action}'
            notify_group('mantenimiento_sistema', subject, mensaje)
            return JsonResponse({'success': True})
    else:
        return redirect('new_type_equipment')

@login_required
@mantenedor_sistema_required
def status_type_equipment(request):
    if request.method == 'POST': 
        tipo = TipoEquipo.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (tipo.status): 
            TipoEquipo.objects.filter(id=request.POST['id']).update(status=False)
            action = 'deshabilitada'.capitalize()
            mensaje = f'Mantenedor de Tipo equipo: {tipo} \n{action} por: {user_name}'
            subject = f'Mantenedor de Tipo equipo: {tipo} {action}'
            notify_group('mantenimiento_sistema', subject, mensaje)
            messages.success(request, 'Tipo Equipo Deshabilitada Correctamente')  
        else:
            TipoEquipo.objects.filter(id=request.POST['id']).update(status=True)
            action = 'habilitada'.capitalize()
            mensaje = f'Mantenedor de Tipo equipo: {tipo} \n{action} por: {user_name}'
            subject = f'Mantenedor de Tipo equipo: {tipo} {action}'
            notify_group('mantenimiento_sistema', subject, mensaje)
            messages.success(request, 'Tipo Equipo Habilitado Correctamente') 
        return redirect('manage_types_equipment')
    else:
        messages.error(request, 'Error al Deshabilitar') 
        return redirect('manage_types_equipment')

@login_required
@mantenedor_sistema_required
def manage_brands_equipment(request): 
    storage = messages.get_messages(request)
    storage.used = True
    marcas = list(MarcaEquipo.objects.all().order_by('id'))   
    context = {
        'marcas': marcas,
        'sidebarsubmenu': 'manage_brandequipment',
        'sidebarmenu': 'manage_equipment',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/equipment/manage_brands_equipment.html', context)

@login_required
@mantenedor_sistema_required
def new_brand_equipment(request):     
    context = {
        'formmarcamaquinaria': FormMarcaEquipo, 
        'sidebarsubmenu': 'manage_brandequipment',
        'sidebarmenu': 'manage_equipment',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/equipment/new_brand_equipment.html', context)

@login_required
@mantenedor_sistema_required
def save_new_brand_equipment(request):     
    if request.method == 'POST':
        tipo = TipoEquipo.objects.get(id=request.POST['tipo'])
        formulario = FormMarcaEquipo(data=request.POST)
        if formulario.is_valid():       
            marca = MarcaEquipo(
                tipo = tipo,
                marca = request.POST['marca'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            marca.save()
            user_name = request.user.get_full_name() or request.user.username
            action = 'creada'.capitalize()
            mensaje = f'Mantenedor de Marca equipo: {marca} \n{action} por: {user_name}'
            subject = f'Mantenedor de Marca equipo: {marca} {action}'
            notify_group('mantenimiento_sistema', subject, mensaje)
            return JsonResponse({'success': True})
    else:
        return redirect('new_brand_equipment')

@login_required
@mantenedor_sistema_required
def status_brand_equipment(request):
    if request.method == 'POST': 
        marca = MarcaEquipo.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (marca.status): 
            MarcaEquipo.objects.filter(id=request.POST['id']).update(status=False)
            action = 'deshabilitada'.capitalize()
            mensaje = f'Mantenedor de Marca equipo: {marca} \n{action} por: {user_name}'
            subject = f'Mantenedor de Marca equipo: {marca} {action}'
            notify_group('mantenimiento_sistema', subject, mensaje)
            messages.success(request, 'Marca Equipo Deshabilitada Correctamente')  
        else:
            MarcaEquipo.objects.filter(id=request.POST['id']).update(status=True)
            action = 'habilitada'.capitalize()
            mensaje = f'Mantenedor de Marca equipo: {marca} \n{action} por: {user_name}'
            subject = f'Mantenedor de Marca equipo: {marca} {action}'
            notify_group('mantenimiento_sistema', subject, mensaje)
            messages.success(request, 'Marca Equipo Habilitado Correctamente') 
        return redirect('manage_brands_equipment')
    else:
        messages.error(request, 'Error al Deshabilitar') 
        return redirect('manage_brands_equipment')

@login_required
@sondaje_avanzado_required
def manage_equipments(request):
    storage = messages.get_messages(request)
    storage.used = True
    equipos = list(NuevoEquipamiento.objects.all().order_by('id'))   
    context = {
        'equipos': equipos,
        'sidebar': 'manage_equipments',
        'sidebarmain': 'system_equipments', 
    }
    return render(request,'pages/equipment/manage_equipment.html', context)

@login_required
@sondaje_avanzado_required
def new_equipment(request):     
    context = {
        'formnuevoequipo': FormNuevoEquipamiento,   
        'sidebar': 'manage_equipments',
        'sidebarmain': 'system_equipments', 
    }
    return render(request,'pages/equipment/new_equipment.html', context)

@login_required
@sondaje_avanzado_required
def save_new_equipment(request): 
    if request.method == 'POST':    
        formulario = FormNuevoEquipamiento(data=request.POST)
        if formulario.is_valid():               
            equipo = formulario.save(commit=False)
            equipo.status = True
            equipo.creador = request.user.first_name + " " + request.user.last_name
            equipo.save()
            user_name = request.user.get_full_name() or request.user.username
            action = 'creado'.capitalize()
            mensaje = f'Registro de Equipo: {equipo} \n{action} por: {user_name}'
            subject = f'Equipo {equipo} {action}'
            notify_group('registro_equipos', subject, mensaje)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': formulario.errors}, status=400)
    else:
        return redirect('new_equipment')

@login_required
@sondaje_avanzado_required
def status_equipment(request):
    if request.method == 'POST': 
        equipo = NuevoEquipamiento.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (equipo.status): 
            NuevoEquipamiento.objects.filter(id=request.POST['id']).update(status=False) 
            action = 'deshabilitado'.capitalize()
            mensaje = f'Registro de Equipo: {equipo} \n{action} por: {user_name}'
            subject = f'Equipo {equipo} {action}'
            notify_group('registro_equipos', subject, mensaje)
            messages.success(request, 'Equipo Deshabilitado Correctamente')  
        else:
            NuevoEquipamiento.objects.filter(id=request.POST['id']).update(status=True)
            action = 'habilitado'.capitalize()
            mensaje = f'Registro de Equipo: {equipo} \n{action} por: {user_name}'
            subject = f'Equipo {equipo} {action}'
            notify_group('registro_equipos', subject, mensaje)
            messages.success(request, 'Equipo Habilitado Correctamente') 
        return redirect('manage_equipments')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_equipments')

@login_required
@sondaje_avanzado_required
def edit_equipment(request):  
    try:
        request.session['edit_id'] = request.POST['equipo_id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    equipo = NuevoEquipamiento.objects.get(id=request.session['edit_id'])
    
    formequipo = FormNuevoEquipamiento(
        instance=equipo,
        tipo_disabled=True,
        marca_disabled=True,
    )
    
    context = {
        'formequipo': formequipo,
        'equipo_id': equipo.id,  
        'sidebar': 'manage_equipments',
        'sidebarmain': 'system_equipments', 
    }
    return render(request,'pages/equipment/edit_equipment.html', context)

@login_required
@sondaje_avanzado_required
def save_edit_equipment(request):     
    if request.method == 'POST':
        equipo = NuevoEquipamiento.objects.get(id=request.POST['equipo_id'])
        old_equipo = NuevoEquipamiento.objects.get(pk=equipo.pk)
        formulario = FormNuevoEquipamiento(data=request.POST, instance=equipo)
        if formulario.is_valid():
            formulario.save()
            user_name = request.user.get_full_name() or request.user.username
            changes = get_changes_message(old_equipo, equipo)
            if changes:
                mensaje = f'Registro de Equipo: {equipo}\nActualizado por: {user_name}{changes}'
                subject = f'Equipo {equipo} Actualizado'
                notify_group('registro_equipos', subject, mensaje)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': formulario.errors}, status=400)
    else:
        return redirect('edit_equipment')

def cargar_marcas_por_tipo(request):
    tipo_id = request.GET.get('tipo_id')
    if tipo_id:
        marcas = MarcaEquipo.objects.filter(tipo=tipo_id,status=True)
        data = [{'id': marca.id, 'nombre': marca.marca} for marca in marcas]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({}, status=400)