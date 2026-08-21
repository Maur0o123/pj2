import os
from collections import defaultdict
import unicodedata
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import (Genero, Ciudad, Nacionalidad, Ano, Marca, Modelo, Color, Tipo, Faena, TipoDocumentoFaena, EmpresaServicios, 
                    EmpresaTipoServicios, TipoFallaVehiculo, OcultarOpcionesVehiculo, CategoriaFallaVehiculo, TipoDocumentoFaenaGeneral,
                    TipoMaquinaria, MarcaMaquinaria, KitsMaquinaria, FallaMaquinaria, FechasImportantes, ReporteError, AyudaManuales,
                    Sondas, Sondajes, Diametros, TipoTerreno, Orientacion, DetalleControlHorario, Corona, Escareador, CantidadAgua,
                    Aditivos, Casing, Zapata, LargoBarra, Recomendacion, Perforistas, MaterialesSonda, MaterialesCaseta, Campana, Programa,
                    RecomendacionAjuste, RecomendacionFinal, ProblemaVehiculo)
from .forms import (FormGenero, FormCiudad, FormNacionalidad, FormAno, FormMarca, FormModelo, FormColor,FormTipo, FormNuevaFaena, 
                    FormTipoDocumentoFaena, FormNuevaEmpresaServicios, FormEmpresaTipoServicios, FormTipoFallaVehiculo, 
                    FormOcultarOpcionesVehiculoAdicional, FormOcultarOpcionesVehiculoTecnica, FormOcultarOpcionesVehiculoDocumentacion, 
                    FormNuevaFechasImportantes, FormOcultarOpcionesVehiculoInterior, FormOcultarOpcionesVehiculoExterior, FormCategoriaFallaVehiculo, 
                    FormTipoDocumentoFaenaGeneral, FormTipoMaquinaria, FormMarcaMaquinaria, FormKitReparacion, FormFallaMaquinaria, 
                    FormMarcaMaquinariaSelect, FormReporteError, FormAyudaManuales, FormSeleccionSeccion, FormCampana, FormPrograma,
                    FormSondas, FormSondajes, FormDiametros, FormTipoTerreno, FormOrientacion, FormDetalleControlHorario, FormCorona, FormEscareador,
                    FormCantidadAgua, FormAditivos, FormCasing, FormZapata, FormLargoBarra, FormRecomendaciones, FormPerforista, 
                    FormMaterialesSonda, FormMaterialesCaseta, FormRecomendacionesAjuste, FormRecomendacionesFinal, FormProblemaVehiculo)
from user.models import UsuarioProfile, LicenciasUsuario, User
from vehicle.models import Vehiculo, NuevoKilometraje
from machine.models import Maquinaria, NuevoHorometro, KitsMaquinariaFaena
from maintenance.models import NuevaSolicitudMantenimiento
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, OuterRef, Subquery, Q, F, IntegerField, ExpressionWrapper, Sum
from mining.models import VehiculoAsignado
import json
from django.shortcuts import get_object_or_404
from core.utils import procesar_fotografia_dos, ordenar_por_mes_inicial
from messenger.utils import notify_group, get_changes_message
from datetime import datetime
from messenger.views import notificacion_mantenedor_email, notificacion_admin_jefe_mantencion_email
from .decorators import admin_or_base_datos_required, mantenedor_sistema_required
from core.utils import formatear_fecha
from django.utils.timezone import make_aware
from equipment.models import NuevoEquipamiento
from django.db import DataError, IntegrityError

@login_required
def select(request):
    user_profile, _ = UsuarioProfile.objects.get_or_create(user=request.user)
    def tiene_acceso(valor_seccion):
        return valor_seccion not in [None, '', 'No', 'SIN ASIGNAR']
    def es_rol_dashboard(valor_seccion):
        return valor_seccion in ['ADMINISTRADOR', 'BASE DATOS']

    acceso_vehicular = tiene_acceso(user_profile.seccionVehicular)
    acceso_sondaje = tiene_acceso(user_profile.seccionSondaje)
    acceso_prevencion = tiene_acceso(user_profile.seccionPrevencion)
    acceso_inventario = tiene_acceso(user_profile.seccionInventario)
    acceso_administracion = tiene_acceso(user_profile.seccionAdministracion)
    
    if acceso_vehicular and not acceso_sondaje and not acceso_prevencion and not acceso_inventario and not acceso_administracion: 
        request.session['seccion'] = 'vehicular'
        if es_rol_dashboard(user_profile.seccionVehicular):
            return redirect('dashboard')
        return redirect('edit_my_profile')
        
    if acceso_sondaje and not acceso_vehicular and not acceso_prevencion and not acceso_inventario and not acceso_administracion:
        request.session['seccion'] = 'sondaje'
        if es_rol_dashboard(user_profile.seccionSondaje):
            return redirect('dashboardSondaje')
        return redirect('edit_my_profile')
        
    if acceso_prevencion and not acceso_vehicular and not acceso_sondaje and not acceso_inventario and not acceso_administracion:
        request.session['seccion'] = 'prevencion'
        if es_rol_dashboard(user_profile.seccionPrevencion):
            return redirect('dashboardPrevencion')
        return redirect('edit_my_profile')
    
    if acceso_inventario and not acceso_vehicular and not acceso_sondaje and not acceso_prevencion and not acceso_administracion:
        request.session['seccion'] = 'inventario'
        if es_rol_dashboard(user_profile.seccionInventario):
            return redirect('dashboardInventario')
        return redirect('edit_my_profile')
        
    if acceso_administracion and not acceso_vehicular and not acceso_sondaje and not acceso_prevencion and not acceso_inventario:
        request.session['seccion'] = 'administracion'
        if es_rol_dashboard(user_profile.seccionAdministracion):
            return redirect('dashboardAdministracion')
        return redirect('edit_my_profile')

    if not (acceso_vehicular or acceso_sondaje or acceso_prevencion or acceso_inventario or acceso_administracion):
        context = {
            'mensajeuno': "Sin secciones asignadas",
            'mensajedos': "Contacte al Administrador",
            'valor': False,
        }
        return render(request, 'main/select.html', context)

    context = {
        'valor': True,
        'usuario': user_profile,
        'formseleccionar': FormSeleccionSeccion(usuario_profile=user_profile),
    }
    return render(request, 'main/select.html', context)


@login_required
def selectOption(request):
    if request.method == 'POST':
        user_profile, _ = UsuarioProfile.objects.get_or_create(user=request.user)
        
        def es_rol_dashboard(valor_seccion):
            return valor_seccion in ['ADMINISTRADOR', 'BASE DATOS']
            
        seccion_seleccionada = request.POST.get('seccion_select')
        
        if seccion_seleccionada == 'administracion':
            request.session['seccion'] = 'administracion'
            if es_rol_dashboard(user_profile.seccionAdministracion):
                return redirect('dashboardAdministracion')
            return redirect('edit_my_profile')
            
        if seccion_seleccionada == 'vehicular':
            request.session['seccion'] = 'vehicular'
            if es_rol_dashboard(user_profile.seccionVehicular):
                return redirect('dashboard')
            return redirect('edit_my_profile')
            
        if seccion_seleccionada == 'sondaje':
            request.session['seccion'] = 'sondaje'
            if es_rol_dashboard(user_profile.seccionSondaje):
                return redirect('dashboardSondaje')
            return redirect('edit_my_profile')
            
        if seccion_seleccionada == 'prevencion':
            request.session['seccion'] = 'prevencion'
            if es_rol_dashboard(user_profile.seccionPrevencion):
                return redirect('dashboardPrevencion')
            return redirect('edit_my_profile')
            
        if seccion_seleccionada == 'inventario':
            request.session['seccion'] = 'inventario'
            if es_rol_dashboard(user_profile.seccionInventario):
                return redirect('dashboardInventario')
            return redirect('edit_my_profile')
            
        return redirect('select')
    else:
        return redirect('select')
    
@login_required
@admin_or_base_datos_required
def dashboard(request): 
    detalle_tipo_vehiculo = VehiculoAsignado.objects.filter(status=True, vehiculo__status=True).values('faena__faena', 'vehiculo__tipo__tipo').annotate(cantidad=Count('vehiculo__tipo__tipo'))
    detalle_por_faena = {}
    for item in detalle_tipo_vehiculo:
        nombre_faena = item['faena__faena']
        tipo_vehiculo = item['vehiculo__tipo__tipo']
        cantidad_vehiculos = item['cantidad']
        
        if nombre_faena not in detalle_por_faena:
            detalle_por_faena[nombre_faena] = {
                'cantidad_total_vehiculos': 0,
                'detalle_por_tipo': {}
            }
        
        detalle_por_faena[nombre_faena]['cantidad_total_vehiculos'] += cantidad_vehiculos
        
        if tipo_vehiculo not in detalle_por_faena[nombre_faena]['detalle_por_tipo']:
            detalle_por_faena[nombre_faena]['detalle_por_tipo'][tipo_vehiculo] = 0
        
        detalle_por_faena[nombre_faena]['detalle_por_tipo'][tipo_vehiculo] += cantidad_vehiculos
        
    if 'SIN ASIGNAR' in detalle_por_faena:
        sin_asignar = detalle_por_faena.pop('SIN ASIGNAR')
        detalle_por_faena = {'SIN ASIGNAR': sin_asignar, **detalle_por_faena}

    detalle_por_faena_json = json.dumps(detalle_por_faena, indent=4)
    detalle_por_faena_dict = json.loads(detalle_por_faena_json)
    
    vehiculos = Vehiculo.objects.all()
    data_vehiculos = []
    for vehiculo in vehiculos:
        diferencias = vehiculo.calculate_days_difference()        
        for fecha_tipo, detalles in diferencias.items():
            if detalles['dias_diferencia'] < 120:
                data_vehiculos.append({
                    'placaPatente': vehiculo.placaPatente,
                    'tipo_fecha': fecha_tipo,
                    'dias_diferencia': detalles['dias_diferencia'],
                    'fecha_vencimiento': detalles['fecha_vencimiento'],
                    'tipo_vehiculo': vehiculo.tipo.tipo
                })
    data_vehiculos.sort(key=lambda x: x['dias_diferencia'])

    today = timezone.now().date()
    data_arriendo = []
    for vehiculo in vehiculos:
        vehiculo_faena = VehiculoAsignado.objects.filter(status=True, vehiculo=vehiculo).first()
        nombre_faena = vehiculo_faena.faena if vehiculo_faena else "SIN ASIGNAR"
        
        if vehiculo.fechaArriendoFinal:
            dias_diferencia = (vehiculo.fechaArriendoFinal.date() - today).days
            if dias_diferencia < 120:
                data_arriendo.append({
                    'placaPatente': vehiculo.placaPatente,
                    'dias_diferencia': dias_diferencia,
                    'fecha_arriendo_inicial': vehiculo.fechaArriendoInicial,
                    'fecha_arriendo_final': vehiculo.fechaArriendoFinal,
                    'tipo_vehiculo': vehiculo.tipo.tipo,
                    'faena': nombre_faena,
                })

    data_arriendo.sort(key=lambda x: x['dias_diferencia'])    
    
    usuarios_profiles = UsuarioProfile.objects.select_related('user').all().exclude(user_id=2)
    licencias_usuarios = LicenciasUsuario.objects.select_related('user').all().exclude(user_id=2)
    data_usuarios = []
    # Recopilar datos y calcular diferencias de días
    for profile in usuarios_profiles:
        fechas = {
            'Cédula Identidad (Vencimiento)': profile.fechaCedulaVencimiento,
        }
        for fecha_tipo, fecha_vencimiento in fechas.items():
            if fecha_vencimiento:
                dias_diferencia = (fecha_vencimiento.date() - today).days
                if dias_diferencia < 120:
                    data_usuarios.append({
                        'username': profile.user.username,
                        'first_name': profile.user.first_name,
                        'last_name': profile.user.last_name,
                        'faena': profile.faena.faena if profile.faena else 'SIN ASIGNAR',
                        'tipo_fecha': fecha_tipo,
                        'dias_diferencia': dias_diferencia,
                        'fecha_vencimiento': fecha_vencimiento,
                    })
    
    for licencia in licencias_usuarios:
        usuario_profile = UsuarioProfile.objects.select_related('faena').filter(user=licencia.user).first()
        fechas = {
            'Licencia Conducir (Vencimiento)': licencia.fechaLicenciaVencimiento,
            'Licencia Interna (Vencimiento)': licencia.fechaLicenciaInternaVencimiento,
        }
        for fecha_tipo, fecha_vencimiento in fechas.items():
            if fecha_vencimiento:
                dias_diferencia = (fecha_vencimiento.date() - today).days
                if dias_diferencia < 120:
                    data_usuarios.append({
                        'username': licencia.user.username,
                        'first_name': licencia.user.first_name,
                        'last_name': licencia.user.last_name,
                        'faena': usuario_profile.faena.faena if usuario_profile and usuario_profile.faena else 'SIN ASIGNAR',
                        'tipo_fecha': fecha_tipo,
                        'dias_diferencia': dias_diferencia,
                        'fecha_vencimiento': fecha_vencimiento,
                    })
    # Ordenar los datos por 'dias_diferencia' en orden ascendente
    data_usuarios.sort(key=lambda x: x['dias_diferencia'])
    
    last_users = User.objects.all().exclude(username__in=['cconelli', '15.053.475-5']).order_by('-last_login')[:5]

    # Subconsulta para obtener el último registro de cada vehículo
    latest_kilometraje = NuevoKilometraje.objects.filter(
        vehiculo=OuterRef('vehiculo')
    ).order_by('-fechacreacion')

    # Consulta principal usando select_related para optimizar la relación ForeignKey
    ultimo_kilometraje_por_vehiculo = NuevoKilometraje.objects.filter(
        id=Subquery(latest_kilometraje.values('id')[:1])
    ).select_related('vehiculo')

    # Anotar los campos adicionales de InformacionTecnicaVehiculo
    ultimo_kilometraje_por_vehiculo = ultimo_kilometraje_por_vehiculo.annotate(
        frecuenciaMantenimiento=F('vehiculo__informaciontecnicavehiculo__frecuenciaMantenimiento'),
        proximoMantenimiento=F('vehiculo__informaciontecnicavehiculo__proximoMantenimiento'),
        proximoMantenimientoGrua=F('vehiculo__informaciontecnicavehiculo__proximoMantenimientoGrua'),
        kilometrosRestantes=F('vehiculo__informaciontecnicavehiculo__proximoMantenimiento') - F('kilometraje')
    ).order_by('kilometrosRestantes')
    
    # Subconsulta para obtener el último registro de cada maquinaria
    latest_horometro = NuevoHorometro.objects.filter(
        maquinaria=OuterRef('maquinaria')
    ).order_by('-fechacreacion')

    # Subconsulta para obtener el horometro cuando origen es "Mantención mayor"
    mantencion_mayor_horometro = NuevoHorometro.objects.filter(
        maquinaria=OuterRef('maquinaria'),
        origen='Mantención mayor'
    ).order_by('-fechacreacion').values('horometro')[:1]

    # Consulta principal usando select_related para optimizar la relación ForeignKey
    ultimo_horometro_por_maquinaria = NuevoHorometro.objects.filter(
        id=Subquery(latest_horometro.values('id')[:1])
    ).select_related('maquinaria')

    # Anotar el campo adicional de mantencionMayor y proximoMantenimientoMayor
    ultimo_horometro_por_maquinaria = ultimo_horometro_por_maquinaria.annotate(
        mantencionMayor=Subquery(mantencion_mayor_horometro),
        proximoMantenimientoMayor=ExpressionWrapper(F('maquinaria__frecuenciaMantenimiento') + Subquery(mantencion_mayor_horometro), output_field=IntegerField()),
        horasRestantes= ExpressionWrapper(F('proximoMantenimientoMayor') - F('horometro'), output_field=IntegerField()),
    )
    #ordenar fechas importantes
    mes_inicial = datetime.now().month
    fechas_importantes_ordenadas = ordenar_por_mes_inicial(mes_inicial)
    
    # Realiza la consulta con los filtros y ordenamiento
    data_solicitudes = NuevaSolicitudMantenimiento.objects.filter(status=True).exclude(Q(progreso='4') | Q(progreso='5')).order_by('-fechacreacion')

    request.session['seccion'] = 'vehicular'
    context = {
        'detalle_por_faena_json': detalle_por_faena_dict,
        'sidebar': 'dashboard',
        'fechavencimientodocumentacionvehiculos': data_vehiculos,
        'fechavencimientoarriendovehiculos': data_arriendo,
        'fechavencimientodocumentacionusuarios': data_usuarios,
        'last_users': last_users,
        'ultimo_kilometraje_por_vehiculo': ultimo_kilometraje_por_vehiculo,
        'ultimo_horometro_por_maquinaria': ultimo_horometro_por_maquinaria,
        'fechas_importantes': fechas_importantes_ordenadas,
        'mantenimientos_vehiculos': data_solicitudes,
    }
    return render(request,'main/homevehicular.html', context)

@login_required
@admin_or_base_datos_required
def dashboardSondaje(request):
    request.session['seccion'] = 'sondaje'
    context = {
        'seccion': 'sondaje',
        'sidebar': 'dashboardSondaje',
    }
    return render(request, 'main/homesondaje.html', context)

@login_required
@admin_or_base_datos_required
def dashboardPrevencion(request):
    request.session['seccion'] = 'prevencion'
    context = {
        'seccion': 'prevencion',
        'sidebar': 'dashboardPrevencion',
    }
    return render(request, 'main/homeprevencion.html', context)

@login_required
@admin_or_base_datos_required
def dashboardInventario(request):
    request.session['seccion'] = 'inventario'
    context = {
        'seccion': 'inventario',
        'sidebar': 'dashboardInventario',
    }
    return render(request, 'main/homeinventario.html', context)


# ---- A PARTIR DE AQUÍ COMIENZAN LAS VISTAS DEL MANTENEDOR DE SISTEMA ----


@login_required
@mantenedor_sistema_required
def manage_genders(request): 
    storage = messages.get_messages(request)
    storage.used = True
    generos = list(Genero.objects.all().order_by('id'))   
    context = {
        'generos': generos,
        'sidebarsubmenu': 'manage_genders',
        'sidebarmenu': 'manage_users',
        'sidebarmain': 'manage_system',
    }
    return render(request,'pages/maintainer/manage_genders.html', context)

@login_required
@mantenedor_sistema_required
def new_gender(request):     
    context = {
        'formgenero': FormGenero, 
        'sidebarsubmenu': 'manage_genders',
        'sidebarmenu': 'manage_users',
        'sidebarmain': 'manage_system',        
    }
    return render(request,'pages/maintainer/new_gender.html', context)

@login_required
@mantenedor_sistema_required
def save_new_gender(request):     
    if request.method == 'POST':
        formulario = FormGenero(data=request.POST)
        if formulario.is_valid():       
            genero = Genero(
                genero = request.POST['genero'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            genero.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nuevo género: {genero.genero}', f'Género: {genero.genero}\nCreado por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_gender')

@login_required
@mantenedor_sistema_required
def status_gender(request):
    if request.method == 'POST': 
        genero = Genero.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (genero.status): 
            Genero.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Género deshabilitado: {genero.genero}', f'Género: {genero.genero}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Genero Deshabilitado Correctamente')  
        else:
            Genero.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Género habilitado: {genero.genero}', f'Género: {genero.genero}\nHabilitado por: {user_name}')
            messages.success(request, 'Genero Habilitado Correctamente') 
        return redirect('manage_genders') 

@login_required
@mantenedor_sistema_required
def manage_cities(request): 
    storage = messages.get_messages(request)
    storage.used = True
    ciudades = list(Ciudad.objects.all().order_by('id'))   
    context = {
        'ciudades': ciudades,
        'sidebarsubmenu': 'manage_cities',
        'sidebarmenu': 'manage_users',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/manage_cities.html', context)

@login_required
@mantenedor_sistema_required
def new_city(request):     
    context = {
        'formciudad': FormCiudad, 
        'sidebarsubmenu': 'manage_cities',
        'sidebarmenu': 'manage_users',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_city.html', context)

@login_required
@mantenedor_sistema_required
def save_new_city(request):     
    if request.method == 'POST':
        formulario = FormCiudad(data=request.POST)
        if formulario.is_valid():       
            ciudad = Ciudad(
                ciudad = request.POST['ciudad'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            ciudad.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva ciudad: {ciudad.ciudad}', f'Ciudad: {ciudad.ciudad}\nCreada por: {user_name}')         
            return JsonResponse({'success': True})
    else:
        return redirect('new_city')

@login_required 
@mantenedor_sistema_required
def status_city(request):
    if request.method == 'POST': 
        ciudad = Ciudad.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (ciudad.status): 
            Ciudad.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Ciudad deshabilitada: {ciudad.ciudad}', f'Ciudad: {ciudad.ciudad}\nDeshabilitada por: {user_name}')
            messages.success(request, 'Ciudad Deshabilitado Correctamente')  
        else:
            Ciudad.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Ciudad habilitada: {ciudad.ciudad}', f'Ciudad: {ciudad.ciudad}\nHabilitada por: {user_name}')
            messages.success(request, 'Ciudad Habilitado Correctamente') 
        return redirect('manage_cities') 

@login_required
@mantenedor_sistema_required
def manage_nationalities(request): 
    storage = messages.get_messages(request)
    storage.used = True
    nacionalidades = list(Nacionalidad.objects.all().order_by('id'))   
    context = {
        'nacionalidades': nacionalidades,
        'sidebarsubmenu': 'manage_nationalities',
        'sidebarmenu': 'manage_users',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_nationalities.html', context)

@login_required
@mantenedor_sistema_required
def new_nationality(request):     
    context = {
        'formnacionalidad': FormNacionalidad, 
        'sidebarsubmenu': 'manage_nationalities',
        'sidebarmenu': 'manage_users',
        'sidebarmain': 'manage_system',         
    }
    return render(request,'pages/maintainer/new_nationality.html', context)

@login_required
@mantenedor_sistema_required
def save_new_nationality(request):     
    if request.method == 'POST':
        formulario = FormNacionalidad(data=request.POST)
        if formulario.is_valid():       
            nacionalidad = Nacionalidad(
                nacionalidad = request.POST['nacionalidad'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            nacionalidad.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva nacionalidad: {nacionalidad.nacionalidad}', f'Nacionalidad: {nacionalidad.nacionalidad}\nCreada por: {user_name}')             
            return JsonResponse({'success': True})
    else:
        return redirect('new_nationality')

@login_required
@mantenedor_sistema_required
def status_nationality(request):
    if request.method == 'POST': 
        nacionalidad = Nacionalidad.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (nacionalidad.status): 
            Nacionalidad.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Nacionalidad deshabilitada: {nacionalidad.nacionalidad}', f'Nacionalidad: {nacionalidad.nacionalidad}\nDeshabilitada por: {user_name}')
            messages.success(request, 'Nacionalidad Deshabilitado Correctamente')  
        else:
            Nacionalidad.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Nacionalidad habilitada: {nacionalidad.nacionalidad}', f'Nacionalidad: {nacionalidad.nacionalidad}\nHabilitada por: {user_name}')
            messages.success(request, 'Nacionalidad Habilitado Correctamente') 
        return redirect('manage_nationalities') 

@login_required
@mantenedor_sistema_required
def manage_years(request): 
    storage = messages.get_messages(request)
    storage.used = True
    anos = list(Ano.objects.all().order_by('id'))   
    context = {
        'anos': anos,
        'sidebarsubmenu': 'manage_years',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_years.html', context)

@login_required
@mantenedor_sistema_required
def new_year(request):     
    context = {
        'formano': FormAno,
        'sidebarsubmenu': 'manage_years',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/new_year.html', context)

@login_required
@mantenedor_sistema_required
def save_new_year(request):     
    if request.method == 'POST':
        formulario = FormAno(data=request.POST)
        if formulario.is_valid():       
            ano = Ano(
                ano = request.POST['ano'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            ano.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nuevo año: {ano.ano}', f'Año: {ano.ano}\nCreado por: {user_name}')

            return JsonResponse({'success': True})
    else:
        return redirect('new_year')

@login_required
@mantenedor_sistema_required
def status_year(request):
    if request.method == 'POST': 
        ano = Ano.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (ano.status): 
            Ano.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Año deshabilitado: {ano.ano}', f'Año: {ano.ano}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Año Deshabilitado Correctamente')  
        else:
            Ano.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Año habilitado: {ano.ano}', f'Año: {ano.ano}\nHabilitado por: {user_name}')
            messages.success(request, 'Año Habilitado Correctamente') 
        return redirect('manage_years') 

@login_required
@mantenedor_sistema_required
def manage_brands(request): 
    storage = messages.get_messages(request)
    storage.used = True
    marcas = list(Marca.objects.all().order_by('id'))   
    context = {
        'marcas': marcas,
        'sidebarsubmenu': 'manage_brands',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_brands.html', context)

@login_required
@mantenedor_sistema_required
def new_brand(request):     
    context = {
        'formmarca': FormMarca, 
        'sidebarsubmenu': 'manage_brands',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_brand.html', context)

@login_required
@mantenedor_sistema_required
def save_new_brand(request):    
    if request.method == 'POST':
         formulario = FormMarca(data=request.POST)
         if formulario.is_valid():       
            marca = Marca(
                marca = request.POST['marca'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            marca.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva marca: {marca.marca}', f'Marca de vehículo: {marca.marca}\nCreada por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_brand')

@login_required
@mantenedor_sistema_required
def status_brand(request):
    if request.method == 'POST': 
        marca = Marca.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (marca.status): 
            Marca.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Marca deshabilitada: {marca.marca}', f'Marca de vehículo: {marca.marca}\nDeshabilitada por: {user_name}')
            messages.success(request, 'Marca Deshabilitada Correctamente')  
        else:
            Marca.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Marca habilitada: {marca.marca}', f'Marca de vehículo: {marca.marca}\nHabilitada por: {user_name}')
            messages.success(request, 'Marca Habilitada Correctamente') 
        return redirect('manage_brands') 

@login_required
@mantenedor_sistema_required
def manage_models(request): 
    storage = messages.get_messages(request)
    storage.used = True
    modelos = list(Modelo.objects.all().order_by('id'))   
    context = {
        'modelos': modelos,
        'sidebarsubmenu': 'manage_models',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_models.html', context)

@login_required
@mantenedor_sistema_required
def new_model(request):     
    context = {
        'formmodelo': FormModelo, 
        'sidebarsubmenu': 'manage_models',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_model.html', context)

@login_required
@mantenedor_sistema_required
def save_new_model(request):     
    if request.method == 'POST':
        formulario = FormModelo(data=request.POST)
        if formulario.is_valid():       
            modelo = Modelo(
                modelo = request.POST['modelo'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            modelo.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nuevo modelo: {modelo.modelo}', f'Modelo de vehículo: {modelo.modelo}\nCreado por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_model')

@login_required
@mantenedor_sistema_required
def status_model(request):
    if request.method == 'POST': 
        modelo = Modelo.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (modelo.status): 
            Modelo.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Modelo deshabilitado: {modelo.modelo}', f'Modelo de vehículo: {modelo.modelo}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Modelo Deshabilitado Correctamente')  
        else:
            Modelo.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Modelo habilitado: {modelo.modelo}', f'Modelo de vehículo: {modelo.modelo}\nHabilitado por: {user_name}')
            messages.success(request, 'Modelo Habilitado Correctamente') 
        return redirect('manage_models') 

@login_required
@mantenedor_sistema_required
def manage_colours(request): 
    storage = messages.get_messages(request)
    storage.used = True
    colores = list(Color.objects.all().order_by('id'))   
    context = {
        'colores': colores,
        'sidebarsubmenu': 'manage_colours',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_colours.html', context)

@login_required
@mantenedor_sistema_required
def new_colour(request):     
    context = {
        'formcolor': FormColor, 
        'sidebarsubmenu': 'manage_colours',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_colour.html', context)

@login_required
@mantenedor_sistema_required
def save_new_colour(request):     
    if request.method == 'POST':
        formulario = FormColor(data=request.POST)
        if formulario.is_valid():    
            color = Color(
                color = request.POST['color'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            color.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nuevo color: {color.color}', f'Color de vehículo: {color.color}\nCreado por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_colour')

@login_required
@mantenedor_sistema_required
def status_colour(request):
    if request.method == 'POST': 
        color = Color.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (color.status): 
            Color.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Color deshabilitado: {color.color}', f'Color de vehículo: {color.color}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Color Deshabilitado Correctamente')  
        else:
            Color.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Color habilitado: {color.color}', f'Color de vehículo: {color.color}\nHabilitado por: {user_name}')
            messages.success(request, 'Color Habilitado Correctamente') 
        return redirect('manage_colours') 
    
@login_required
@mantenedor_sistema_required
def manage_types(request): 
    storage = messages.get_messages(request)
    storage.used = True
    tipos = list(Tipo.objects.all().order_by('id'))   
    context = {
        'tipos': tipos,
        'sidebarsubmenu': 'manage_types',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_types.html', context)

@login_required
@mantenedor_sistema_required
def new_type(request):     
    context = {
        'formtipo': FormTipo, 
        'sidebarsubmenu': 'manage_types',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_type.html', context)

@login_required
@mantenedor_sistema_required
def save_new_type(request):     
    if request.method == 'POST':
        formulario = FormTipo(data=request.POST)
        if formulario.is_valid():       
            tipo = Tipo(
                tipo = request.POST['tipo'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            tipo.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nuevo tipo: {tipo.tipo}', f'Tipo de vehículo: {tipo.tipo}\nCreado por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_type')

@login_required
@mantenedor_sistema_required
def status_type(request):
    if request.method == 'POST': 
        tipo = Tipo.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (tipo.status): 
            Tipo.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Tipo deshabilitado: {tipo.tipo}', f'Tipo de vehículo: {tipo.tipo}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Tipo de vehículo Deshabilitado Correctamente')  
        else:
            Tipo.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Tipo habilitado: {tipo.tipo}', f'Tipo de vehículo: {tipo.tipo}\nHabilitado por: {user_name}')
            messages.success(request, 'Tipo de vehículo Habilitado Correctamente') 
        return redirect('manage_types')

@login_required
@mantenedor_sistema_required
def edit_type(request):  
    try:
        request.session['edit_tipo_id'] = request.POST['tipo_id']            
    except MultiValueDictKeyError:
        request.session['edit_tipo_id'] = request.session['edit_tipo_id']
    tipo = Tipo.objects.get(id=request.session['edit_tipo_id'])
    opciones = OcultarOpcionesVehiculo.objects.get(tipo_vehiculo=tipo.tipo)
    formocultaropcionesadicional = FormOcultarOpcionesVehiculoAdicional(instance=opciones)
    formocultaropcionestecnica = FormOcultarOpcionesVehiculoTecnica(instance=opciones)
    formocultaropcionesdocumentacion = FormOcultarOpcionesVehiculoDocumentacion(instance=opciones)
    formocultaropcionesinterior = FormOcultarOpcionesVehiculoInterior(instance=opciones)
    formocultaropcionesexterior = FormOcultarOpcionesVehiculoExterior(instance=opciones)
    context = {
        'formocultaropcionesadicional': formocultaropcionesadicional,
        'formocultaropcionestecnica': formocultaropcionestecnica,
        'formocultaropcionesdocumentacion': formocultaropcionesdocumentacion,
        'formocultaropcionesinterior': formocultaropcionesinterior,
        'formocultaropcionesexterior': formocultaropcionesexterior,
        'opciones': opciones,  
        'sidebarsubmenu': 'manage_types',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/edit_type.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_type(request):
    if request.method == 'POST':
        instance = get_object_or_404(OcultarOpcionesVehiculo, tipo_vehiculo=request.POST['tipo_vehiculo'])
        
        formadicional = FormOcultarOpcionesVehiculoAdicional(request.POST, instance=instance)
        formtecnica = FormOcultarOpcionesVehiculoTecnica(request.POST, instance=instance)
        formdocumentacion = FormOcultarOpcionesVehiculoDocumentacion(request.POST, instance=instance)
        forminterior = FormOcultarOpcionesVehiculoInterior(request.POST, instance=instance)
        formexterior = FormOcultarOpcionesVehiculoExterior(request.POST, instance=instance)
        
        if all([
            formadicional.is_valid(),
            formtecnica.is_valid(),
            formdocumentacion.is_valid(),
            forminterior.is_valid(),
            formexterior.is_valid()
        ]):
            formadicional.save()
            formtecnica.save()
            formdocumentacion.save()
            forminterior.save()
            formexterior.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Opción de vehículo actualizada: {request.POST["tipo_vehiculo"]}', f'Ocultar opciones: {request.POST["tipo_vehiculo"]}\nActualizada por: {user_name}')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': True})
    else:
        return redirect('edit_type')
  
@login_required
@mantenedor_sistema_required
def manage_mining(request): 
    storage = messages.get_messages(request)
    storage.used = True
    faenas = list(Faena.objects.all().order_by('id'))   
    context = {
        'faenas': faenas,
        'sidebarsubmenu': 'manage_managemining',
        'sidebarmenu': 'manage_mining',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_mining.html', context)

@login_required
@mantenedor_sistema_required
def new_mining(request):     
    context = {
        'formnuevafaena': FormNuevaFaena, 
        'sidebarsubmenu': 'manage_managemining',
        'sidebarmenu': 'manage_mining',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_mining.html', context)

@login_required
@mantenedor_sistema_required
def save_new_mining(request):     
    if request.method == 'POST':
        formulario = FormNuevaFaena(data=request.POST)
        if formulario.is_valid():       
            faena = Faena(
                faena = request.POST['faena'],
                descripcion = request.POST['descripcion'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            faena.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva faena: {faena.faena}', f'Faena: {faena.faena}\nCreada por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_mining')

@login_required
@mantenedor_sistema_required
def status_mining(request):
    if request.method == 'POST': 
        try:
            faena = Faena.objects.get(id=request.POST['id'])
            user_name = request.user.get_full_name() or request.user.username
            
            # --- VALIDACIÓN DE SEGURIDAD ---
            if (faena.status): 
                # Contamos activos asociados
                vehiculos = VehiculoAsignado.objects.filter(faena=faena, status=True).count()
                maquinarias = Maquinaria.objects.filter(faena=faena, status=True).count()
                equipos = NuevoEquipamiento.objects.filter(faena=faena, status=True).count()

                if vehiculos > 0 or maquinarias > 0 or equipos > 0:
                    detalles = []
                    if vehiculos > 0: detalles.append(f"{vehiculos} Vehículo(s)")
                    if maquinarias > 0: detalles.append(f"{maquinarias} Maquinaria(s)")
                    if equipos > 0: detalles.append(f"{equipos} Equipo(s)")
                    
                    msj = f"No se puede deshabilitar. Tiene asociado: {', '.join(detalles)}."
                    
                    # Retornamos JSON con error lógico (success=False)
                    return JsonResponse({'success': False, 'message': msj})

                # Si pasa, deshabilitamos
                Faena.objects.filter(id=request.POST['id']).update(status=False)
                notify_group('mantenimiento_sistema', f'Faena deshabilitada: {faena.faena}', f'Faena: {faena.faena}\nDeshabilitada por: {user_name}')
                return JsonResponse({'success': True, 'message': 'Faena Deshabilitada Correctamente'})
            else:
                # Habilitamos
                Faena.objects.filter(id=request.POST['id']).update(status=True)
                notify_group('mantenimiento_sistema', f'Faena habilitada: {faena.faena}', f'Faena: {faena.faena}\nHabilitada por: {user_name}')
                return JsonResponse({'success': True, 'message': 'Faena Habilitada Correctamente'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error interno del servidor.'})
            
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@mantenedor_sistema_required
def edit_mining(request):  
    try:
        request.session['edit_faena_id'] = request.POST['faena_id']            
    except MultiValueDictKeyError:
        request.session['edit_faena_id'] = request.session['edit_faena_id']
    faena = Faena.objects.get(id=request.session['edit_faena_id'])
    context = {
        'formeditarfaena':  FormNuevaFaena(initial={
            'faena': faena.faena,
            'descripcion': faena.descripcion,              
            },
            faena_disabled = True,
        ),
        'faena_id': faena.id,  
        'sidebarsubmenu': 'manage_managemining',
        'sidebarmenu': 'manage_mining',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/edit_mining.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_mining(request):     
    if request.method == 'POST':
        faena = Faena.objects.get(id=request.POST['faena_id'])
        Faena.objects.filter(id=request.POST['faena_id']).update(descripcion=request.POST['descripcion'])
        user_name = request.user.get_full_name() or request.user.username
        notify_group('mantenimiento_sistema', f'Faena actualizada: {faena.faena}', f'Faena: {faena.faena}\nActualizada por: {user_name}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_mining')

@login_required
@mantenedor_sistema_required
def manage_mining_documents(request): 
    storage = messages.get_messages(request)
    storage.used = True
    tipo_documentos = list(TipoDocumentoFaena.objects.all().order_by('fechacreacion'))  
    context = {
        'tipo_documentos': tipo_documentos,
        'sidebarsubmenu': 'manage_documentsmining',
        'sidebarmenu': 'manage_mining',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_mining_documents.html', context)

@login_required
@mantenedor_sistema_required
def new_mining_document(request):     
    context = {
        'formnuevodocumento': FormTipoDocumentoFaena, 
        'sidebarsubmenu': 'manage_documentsmining',
        'sidebarmenu': 'manage_mining',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_mining_document.html', context)

@login_required
@mantenedor_sistema_required
def save_new_mining_document(request):
    if request.method == 'POST':
        try: 
            tipo_documento_faena = TipoDocumentoFaena.objects.get(documento=request.POST['documento'],faena=request.POST['faena'])
            return tipo_documento_faena
        except ObjectDoesNotExist:            
            faena = Faena.objects.get(pk=request.POST['faena'])
            formulario = FormTipoDocumentoFaena(data=request.POST)
            if formulario.is_valid():       
                tipo_documento = TipoDocumentoFaena(
                    faena = faena,
                    documento = request.POST['documento'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                tipo_documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo documento faena: {tipo_documento.documento}', f'Documento de faena: {tipo_documento.documento}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        return redirect('manage_mining_documents')

@login_required
@mantenedor_sistema_required
def status_mining_document(request):
    if request.method == 'POST': 
        tipo_documento = TipoDocumentoFaena.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (tipo_documento.status): 
            TipoDocumentoFaena.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Documento faena deshabilitado: {tipo_documento.documento}', f'Documento de faena: {tipo_documento.documento}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Documento Deshabilitado Correctamente')  
        else:
            TipoDocumentoFaena.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Documento faena habilitado: {tipo_documento.documento}', f'Documento de faena: {tipo_documento.documento}\nHabilitado por: {user_name}')
            messages.success(request, 'Documento Habilitado Correctamente') 
        return redirect('manage_mining_documents') 

@login_required
@mantenedor_sistema_required
def manage_maintenance_companies(request): 
    storage = messages.get_messages(request)
    storage.used = True
    empresas = list(EmpresaServicios.objects.all().order_by('id'))   
    context = {
        'empresas': empresas,
        'sidebarsubmenu': 'manage_newcompanie',
        'sidebarmenu': 'manage_maintenance',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_maintenance_companies.html', context)

@login_required
@mantenedor_sistema_required
def new_maintenance_companie(request):     
    context = {
        'formnuevaempresa': FormNuevaEmpresaServicios, 
        'sidebarsubmenu': 'manage_newcompanie',
        'sidebarmenu': 'manage_maintenance',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_maintenance_companie.html', context)

@login_required
@mantenedor_sistema_required
def save_new_maintenance_companie(request):     
    if request.method == 'POST':
        formulario = FormNuevaEmpresaServicios(data=request.POST)
        if formulario.is_valid():       
            empresa = EmpresaServicios(
                empresa = request.POST['empresa'],
                rut = request.POST['rut'],
                direccion = request.POST['direccion'],
                telefono = request.POST['telefono'],
                descripcion = request.POST['descripcion'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            empresa.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva empresa: {empresa.empresa}', f'Empresa de mantenimiento: {empresa.empresa}\nCreada por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_maintenance_companie')

@login_required
@mantenedor_sistema_required
def status_maintenance_companie(request):
    if request.method == 'POST': 
        empresa = EmpresaServicios.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (empresa.status): 
            EmpresaServicios.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Empresa deshabilitada: {empresa.empresa}', f'Empresa de mantenimiento: {empresa.empresa}\nDeshabilitada por: {user_name}')
            messages.success(request, 'Empresa Deshabilitada Correctamente')  
        else:
            EmpresaServicios.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Empresa habilitada: {empresa.empresa}', f'Empresa de mantenimiento: {empresa.empresa}\nHabilitada por: {user_name}')
            messages.success(request, 'Empresa Habilitada Correctamente') 
        return redirect('manage_maintenance_companies') 

@login_required
@mantenedor_sistema_required
def edit_maintenance_companie(request):  
    try:
        request.session['edit_empresa_id'] = request.POST['empresa_id']            
    except MultiValueDictKeyError:
        request.session['edit_empresa_id'] = request.session['edit_empresa_id']
    empresa = EmpresaServicios.objects.get(id=request.session['edit_empresa_id'])
    context = {
        'formeditarempresa':  FormNuevaEmpresaServicios(initial={
            'empresa': empresa.empresa,
            'rut': empresa.rut,
            'telefono': empresa.telefono,
            'direccion': empresa.direccion,
            'descripcion': empresa.descripcion,           
            },
            empresa_disabled = True,
            rut_disabled = True,
        ),
        'empresa_id': empresa.id,  
        'sidebarsubmenu': 'manage_newcompanie',
        'sidebarmenu': 'manage_maintenance',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/edit_maintenance_companie.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_maintenance_companie(request):    
    if request.method == 'POST':
        empresa = EmpresaServicios.objects.get(id=request.POST['empresa_id'])
        EmpresaServicios.objects.filter(id=request.POST['empresa_id']).update(telefono=request.POST['telefono'])
        EmpresaServicios.objects.filter(id=request.POST['empresa_id']).update(direccion=request.POST['direccion'])
        EmpresaServicios.objects.filter(id=request.POST['empresa_id']).update(descripcion=request.POST['descripcion'])
        user_name = request.user.get_full_name() or request.user.username
        notify_group('mantenimiento_sistema', f'Empresa actualizada: {empresa.empresa}', f'Empresa de mantenimiento: {empresa.empresa}\nActualizada por: {user_name}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_maintenance_companie')

@login_required
@mantenedor_sistema_required
def manage_maintenance_services(request): 
    storage = messages.get_messages(request)
    storage.used = True
    servicios = list(EmpresaTipoServicios.objects.all().order_by('fechacreacion'))  
    context = {
        'servicios': servicios,
        'sidebarsubmenu': 'manage_maintenanceservices',
        'sidebarmenu': 'manage_maintenance',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_maintenance_services.html', context)

@login_required
@mantenedor_sistema_required
def new_maintenance_service(request):     
    context = {
        'formnuevoservicio': FormEmpresaTipoServicios, 
        'sidebarsubmenu': 'manage_maintenanceservices',
        'sidebarmenu': 'manage_maintenance',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_maintenance_service.html', context)

@login_required
@mantenedor_sistema_required
def save_new_maintenance_service(request):
    if request.method == 'POST':
        try: 
            tipo_servicio = EmpresaTipoServicios.objects.get(servicio=request.POST['servicio'],empresa=request.POST['empresa'])
            return tipo_servicio
        except ObjectDoesNotExist:            
            empresa = EmpresaServicios.objects.get(pk=request.POST['empresa'])
            formulario = FormEmpresaTipoServicios(data=request.POST)
            if formulario.is_valid():       
                servicio_nuevo = EmpresaTipoServicios(
                    empresa = empresa,
                    servicio = request.POST['servicio'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                servicio_nuevo.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo servicio: {servicio_nuevo.servicio}', f'Servicio de mantenimiento: {servicio_nuevo.servicio}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        return redirect('manage_maintenance_services')

@login_required
@mantenedor_sistema_required
def status_maintenance_service(request):
    if request.method == 'POST': 
        servicio = EmpresaTipoServicios.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (servicio.status): 
            EmpresaTipoServicios.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Servicio deshabilitado: {servicio.servicio}', f'Servicio de mantenimiento: {servicio.servicio}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Servicio Deshabilitado Correctamente')  
        else:
            EmpresaTipoServicios.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Servicio habilitado: {servicio.servicio}', f'Servicio de mantenimiento: {servicio.servicio}\nHabilitado por: {user_name}')
            messages.success(request, 'Servicio Habilitado Correctamente') 
        return redirect('manage_maintenance_services') 

@login_required
@mantenedor_sistema_required
def manage_failures(request): 
    storage = messages.get_messages(request)
    storage.used = True
    fallas = list(TipoFallaVehiculo.objects.all().order_by('id'))   
    context = {
        'fallas': fallas,
        'sidebarsubsubmenu': 'manage_failures',
        'sidebarsubmenu': 'manage_failures',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_failures.html', context)

@login_required
@mantenedor_sistema_required
def new_failure(request):     
    context = {
        'formfalla': FormTipoFallaVehiculo,
        'sidebarsubsubmenu': 'manage_failures',
        'sidebarsubmenu': 'manage_failures',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_failure.html', context)

@login_required
@mantenedor_sistema_required
def save_new_failure(request):     
    if request.method == 'POST':
        formulario = FormTipoFallaVehiculo(data=request.POST)
        categoria = CategoriaFallaVehiculo(pk=request.POST['categoria'])
        if formulario.is_valid():       
            falla = TipoFallaVehiculo(
                categoria = categoria,
                falla = formulario.cleaned_data['falla'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            falla.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva falla: {falla.falla}', f'Falla de vehículo: {falla.falla}\nCreada por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_failure')

@login_required
@mantenedor_sistema_required
def status_failure(request):
    if request.method == 'POST': 
        falla = TipoFallaVehiculo.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (falla.status): 
            TipoFallaVehiculo.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Falla deshabilitada: {falla.falla}', f'Falla de vehículo: {falla.falla}\nDeshabilitada por: {user_name}')
            messages.success(request, 'Falla de Vehículo Deshabilitado Correctamente')  
        else:
            TipoFallaVehiculo.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Falla habilitada: {falla.falla}', f'Falla de vehículo: {falla.falla}\nHabilitada por: {user_name}')
            messages.success(request, 'Falla de Vehículo Habilitado Correctamente') 
        return redirect('manage_failures') 

@login_required
@mantenedor_sistema_required
def manage_categories_failures(request): 
    storage = messages.get_messages(request)
    storage.used = True
    categorias = list(CategoriaFallaVehiculo.objects.all().order_by('id'))   
    context = {
        'categorias': categorias,
        'sidebarsubsubmenu': 'manage_categories_failures',
        'sidebarsubmenu': 'manage_failures',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_categories_failures.html', context)

@login_required
@mantenedor_sistema_required
def new_categories_failure(request):     
    context = {
        'formcategoria': FormCategoriaFallaVehiculo,
        'sidebarsubsubmenu': 'manage_categories_failures',
        'sidebarsubmenu': 'manage_failures',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_categorie_failure.html', context)

@login_required
@mantenedor_sistema_required
def save_new_categories_failure(request):     
    if request.method == 'POST':
        formulario = FormCategoriaFallaVehiculo(data=request.POST)
        if formulario.is_valid():       
            categoria = CategoriaFallaVehiculo(
                categoria = formulario.cleaned_data['categoria'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            categoria.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva categoría: {categoria.categoria}', f'Categoría de vehículo: {categoria.categoria}\nCreada por: {user_name}')
            return JsonResponse({'success': True})
        else:
            errors = formulario.errors.as_json()
            return JsonResponse({'error': errors}, status=400)
    else:
        return redirect('new_categories_failure')

@login_required
@mantenedor_sistema_required
def status_categories_failure(request):
    if request.method == 'POST': 
        categoria = CategoriaFallaVehiculo.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (categoria.status): 
            CategoriaFallaVehiculo.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Categoría deshabilitada: {categoria.categoria}', f'Categoría de vehículo: {categoria.categoria}\nDeshabilitada por: {user_name}')
            messages.success(request, 'Categoría de Vehículo Deshabilitada Correctamente')  
        else:
            CategoriaFallaVehiculo.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Categoría habilitada: {categoria.categoria}', f'Categoría de vehículo: {categoria.categoria}\nHabilitada por: {user_name}')
            messages.success(request, 'Categoría de Vehículo Habilitada Correctamente') 
        return redirect('manage_categories_failures') 

@login_required
@mantenedor_sistema_required
def manage_mining_documents_general(request): 
    storage = messages.get_messages(request)
    storage.used = True
    tipo_documentos = list(TipoDocumentoFaenaGeneral.objects.all().order_by('fechacreacion'))  
    context = {
        'tipo_documentos': tipo_documentos,
        'sidebarsubmenu': 'manage_documentsmining_general',
        'sidebarmenu': 'manage_mining',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_mining_documents_general.html', context)

@login_required
@mantenedor_sistema_required
def new_mining_document_general(request):     
    context = {
        'formnuevodocumentogeneral': FormTipoDocumentoFaenaGeneral,
        'sidebarsubmenu': 'manage_documentsmining_general',
        'sidebarmenu': 'manage_mining',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_mining_document_general.html', context)

@login_required
@mantenedor_sistema_required
def save_new_mining_document_general(request):
    if request.method == 'POST':
        toggle_archivoDocumento = request.POST.get('toggle-archivoDocumento', 'no')
        archivo = procesar_fotografia_dos(toggle_archivoDocumento, 'archivoDocumento', 'base/no-imagen.png', request)
        try: 
            tipo_documento_faena_general = TipoDocumentoFaenaGeneral.objects.get(nombredocumento=request.POST['nombredocumento'],faena=request.POST['faena'])
            return tipo_documento_faena_general
        except ObjectDoesNotExist:            
            faena = Faena.objects.get(pk=request.POST['faena'])
            formulario = FormTipoDocumentoFaenaGeneral(data=request.POST)
            if formulario.is_valid():       
                
                fecha_caducidad = request.POST.get('fechacaducidad')
                if not fecha_caducidad:
                    fecha_caducidad = None

                tipo_documento_general = TipoDocumentoFaenaGeneral(
                    faena = faena,
                    nombredocumento = request.POST['nombredocumento'],
                    fechacaducidad = fecha_caducidad,
                    archivodocumento = archivo,
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                tipo_documento_general.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo documento general: {tipo_documento_general.nombredocumento}', f'Documento general: {tipo_documento_general.nombredocumento}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_mining_documents_general')

@login_required
@mantenedor_sistema_required
def status_mining_document_general(request):
    if request.method == 'POST': 
        tipo_documento = TipoDocumentoFaenaGeneral.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (tipo_documento.status): 
            TipoDocumentoFaenaGeneral.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Documento general deshabilitado: {tipo_documento.nombredocumento}', f'Documento general: {tipo_documento.nombredocumento}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Documento Deshabilitado Correctamente')  
        else:
            TipoDocumentoFaenaGeneral.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Documento general habilitado: {tipo_documento.nombredocumento}', f'Documento general: {tipo_documento.nombredocumento}\nHabilitado por: {user_name}')
            messages.success(request, 'Documento Habilitado Correctamente') 
        return redirect('manage_mining_documents_general')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_mining_documents_general') 

@login_required
@mantenedor_sistema_required
def edit_mining_document_general(request):  
    try:
        request.session['edit_document_general_id'] = request.POST['documento_id']            
    except MultiValueDictKeyError:
        request.session['edit_document_general_id'] = request.session['edit_document_general_id']
    
    documento = TipoDocumentoFaenaGeneral.objects.get(id=request.session['edit_document_general_id'])
    urlDocumento = documento.archivodocumento
    
    if urlDocumento.url.lower().endswith((".jpg", ".jpeg", ".png")):
        extensionDocumento = "imagen"
    elif urlDocumento.url.lower().endswith((".pdf")):
        extensionDocumento = "pdf"
    else:
        extensionDocumento = "otro"

    fecha_vencimiento = ""
    if documento.fechacaducidad:
        fecha_vencimiento = documento.fechacaducidad.strftime('%Y-%m-%d')

    context = {
        'formeditardocumento': FormTipoDocumentoFaenaGeneral(initial={
            'faena': documento.faena,
            'nombredocumento': documento.nombredocumento,
            'fechacaducidad': fecha_vencimiento,
        },
        faena_disabled = True,
        ),
        'documento_id': documento.id,
        'archivodocumento': documento.archivodocumento,
        'extensionDocumento': extensionDocumento,
        'sidebarsubmenu': 'manage_documentsmining_general',
        'sidebarmenu': 'manage_mining',
        'sidebarmain': 'manage_system',  
    }
    return render(request, 'pages/maintainer/edit_mining_document_general.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_mining_document_general(request):  
    if request.method == 'POST':
        documento = TipoDocumentoFaenaGeneral.objects.get(id=request.POST['documento_id'])
        old_documento = TipoDocumentoFaenaGeneral.objects.get(pk=documento.pk)
        
        toggle_Documento = request.POST.get('toggle-archivoDocumento', 'no')
        archivo = procesar_fotografia_dos(toggle_Documento, 'archivoDocumento', 'base/no-imagen.png', request)
        documento.archivodocumento = archivo
        
        if 'nombredocumento' in request.POST:
            documento.nombredocumento = request.POST['nombredocumento']
        
        nueva_fecha = request.POST.get('fechacaducidad')
        if nueva_fecha:
            documento.fechacaducidad = nueva_fecha
        else:
            documento.fechacaducidad = None
            
        documento.save()
        
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_documento, documento)
        if changes:
            notify_group('mantenimiento_sistema', f'Documento general actualizado: {documento.nombredocumento}', f'Documento general: {documento.nombredocumento}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_mining_document_general')

@login_required
@mantenedor_sistema_required
def manage_types_machines(request): 
    storage = messages.get_messages(request)
    storage.used = True
    tipos = list(TipoMaquinaria.objects.all().order_by('id'))   
    context = {
        'tiposmaquinas': tipos,
        'sidebarsubmenu': 'manage_managetypemachine',
        'sidebarmenu': 'manage_machine',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_types_machine.html', context)

@login_required
@mantenedor_sistema_required
def new_type_machine(request): 
    context = {
        'formnuevotipomaquinaria': FormTipoMaquinaria, 
        'sidebarsubmenu': 'manage_managetypemachine',
        'sidebarmenu': 'manage_machine',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_type_machine.html', context)

@login_required
@mantenedor_sistema_required
def save_new_type_machine(request):     
    if request.method == 'POST':
        formulario = FormTipoMaquinaria(data=request.POST)
        if formulario.is_valid():       
            tipo = TipoMaquinaria(
                tipo = request.POST['tipo'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            tipo.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nuevo tipo máquina: {tipo.tipo}', f'Tipo de maquinaria: {tipo.tipo}\nCreado por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_type_machine')

@login_required
@mantenedor_sistema_required
def status_type_machine(request):
    if request.method == 'POST': 
        tipo = TipoMaquinaria.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (tipo.status): 
            TipoMaquinaria.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Tipo máquina deshabilitado: {tipo.tipo}', f'Tipo de maquinaria: {tipo.tipo}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Tipo Maquinaria Deshabilitada Correctamente')  
        else:
            TipoMaquinaria.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Tipo máquina habilitado: {tipo.tipo}', f'Tipo de maquinaria: {tipo.tipo}\nHabilitado por: {user_name}')
            messages.success(request, 'Tipo Maquinaria Habilitado Correctamente') 
        return redirect('manage_types_machines')
    else:
        messages.error(request, 'Error al Deshabilitar') 
        return redirect('manage_types_machines')

@login_required
@mantenedor_sistema_required
def manage_brands_machines(request): 
    storage = messages.get_messages(request)
    storage.used = True
    marcas = list(MarcaMaquinaria.objects.all().order_by('id'))   
    context = {
        'marcasmaquinas': marcas,
        'sidebarsubmenu': 'manage_managebrandmachine',
        'sidebarmenu': 'manage_machine',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_brands_machine.html', context)

@login_required
@mantenedor_sistema_required
def new_brand_machine(request):     
    context = {
        'formmarcamaquinaria': FormMarcaMaquinaria, 
        'sidebarsubmenu': 'manage_managebrandmachine',
        'sidebarmenu': 'manage_machine',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_brand_machine.html', context)

@login_required
@mantenedor_sistema_required
def save_new_brand_machine(request):     
    if request.method == 'POST':
        tipo = TipoMaquinaria.objects.get(id=request.POST['tipo'])
        formulario = FormMarcaMaquinaria(data=request.POST)
        if formulario.is_valid():       
            marca = MarcaMaquinaria(
                tipo = tipo,
                marca = request.POST['marca'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            marca.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva marca máquina: {marca.marca}', f'Marca de maquinaria: {marca.marca}\nCreada por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_brand_machine')

@login_required
@mantenedor_sistema_required
def status_brand_machine(request):
    if request.method == 'POST': 
        marca = MarcaMaquinaria.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (marca.status): 
            MarcaMaquinaria.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Marca máquina deshabilitada: {marca.marca}', f'Marca de maquinaria: {marca.marca}\nDeshabilitada por: {user_name}')
            messages.success(request, 'Marca Maquinaria Deshabilitada Correctamente')  
        else:
            MarcaMaquinaria.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Marca máquina habilitada: {marca.marca}', f'Marca de maquinaria: {marca.marca}\nHabilitada por: {user_name}')
            messages.success(request, 'Marca Maquinaria Habilitado Correctamente') 
        return redirect('manage_brands_machines')
    else:
        messages.error(request, 'Error al Deshabilitar') 
        return redirect('manage_brands_machines')

@login_required
@mantenedor_sistema_required
def manage_kits_repairs(request): 
    storage = messages.get_messages(request)
    storage.used = True
    kits = list(KitsMaquinaria.objects.all().order_by('id'))   
    context = {
        'kitsreparacion': kits,
        'sidebarsubmenu': 'manage_managekitmachine',
        'sidebarmenu': 'manage_machine',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_kits_repair.html', context)

@login_required
@mantenedor_sistema_required
def new_kit_repair(request):     
    context = {
        'formkitreparacion': FormKitReparacion, 
        'sidebarsubmenu': 'manage_managekitmachine',
        'sidebarmenu': 'manage_machine',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_kit_repair.html', context)

@login_required
@mantenedor_sistema_required
def save_new_kit_repair(request):     
    if request.method == 'POST':
        marca = MarcaMaquinaria.objects.get(id=request.POST['marcaMaquina'])
        formulario = FormKitReparacion(data=request.POST)
        if formulario.is_valid():       
            kits = KitsMaquinaria(
                marcaMaquina = marca,
                nombreKit = request.POST['nombreKit'],
                stockMinimo = request.POST['stockMinimo'],
                stockMaximo = request.POST['stockMaximo'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            kits.save()
            # notificacion_mantenedor_email(request,kits,'Kit de reparación','creado')
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nuevo kit: {kits.nombreKit}', f'Kit de reparación: {kits.nombreKit}\nCreado por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_kit_repair')

@login_required
@mantenedor_sistema_required
def status_kit_repair(request):
    if request.method == 'POST': 
        try:
            # Se incorpora manejo de excepciones para prevenir errores de servidor (500) y gestionar fallos controlados.
            kit = KitsMaquinaria.objects.get(id=request.POST['id'])
            user_name = request.user.get_full_name() or request.user.username
            
            if kit.status: 
                kit.status = False
                kit.save()
                # notificacion_mantenedor_email(request, kit, 'Kit de reparación', 'deshabilitado')
                notify_group('mantenimiento_sistema', f'Kit deshabilitado: {kit.nombreKit}', f'Kit de reparación: {kit.nombreKit}\nDeshabilitado por: {user_name}')
                messages.success(request, 'Kit de Reparación Deshabilitado Correctamente')  
            else:
                kit.status = True
                kit.save()
                # notificacion_mantenedor_email(request, kit, 'Kit de reparación', 'habilitado')
                notify_group('mantenimiento_sistema', f'Kit habilitado: {kit.nombreKit}', f'Kit de reparación: {kit.nombreKit}\nHabilitado por: {user_name}')
                messages.success(request, 'Kit de Reparación Habilitado Correctamente') 
            
            return redirect('manage_kits_repairs')
            
        except Exception as e:
            print(e)
            messages.error(request, 'Error al cambiar estado') 
            return redirect('manage_kits_repairs')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_kits_repairs')
 
@login_required
@mantenedor_sistema_required
def edit_kit_repair(request):  
    try:
        request.session['edit_kit_repair_id'] = request.POST['kit_id']            
    except MultiValueDictKeyError:
        request.session['edit_kit_repair_id'] = request.session['edit_kit_repair_id']
    kit = KitsMaquinaria.objects.get(id=request.session['edit_kit_repair_id'])

    context = {
        'formkitreparacion':  FormKitReparacion(initial={
            'marcaMaquina': kit.marcaMaquina,
            'nombreKit': kit.nombreKit,
            'stockMinimo': kit.stockMinimo,
            'stockMaximo': kit.stockMaximo,
            },
            marcaMaquina_disabled = True,
            nombreKit_disabled = True,
        ),
        'kit_id': kit.id,
    }
    return render(request,'pages/maintainer/edit_kit_repair.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_kit_repair(request):     
    if request.method == 'POST':
        kit = KitsMaquinaria.objects.filter(id=request.POST['kit_id'])
        minimo = int(request.POST['stockMinimo'])
        maximo = int(request.POST['stockMaximo'])
        if minimo < 1 or maximo < 1:
            return JsonResponse({'error': 'Los valores no deben ser menor a 1'})
        else:
            if minimo < maximo:
                kit_obj = KitsMaquinaria.objects.get(id=request.POST['kit_id'])
                kit_obj.stockMinimo = minimo
                kit_obj.stockMaximo = maximo
                kit_obj.save()
                # notificacion_mantenedor_email(request,kit,'Kit de reparación','actualizado')
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Kit actualizado: {kit_obj.nombreKit}', f'Kit de reparación: {kit_obj.nombreKit}\nActualizado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'El valor minimo no puede ser mayor que el valor máximo o iguales'})
            
    else:
        return redirect('edit_kit_repair')

@login_required
@mantenedor_sistema_required
def manage_failures_machines(request): 
    storage = messages.get_messages(request)
    storage.used = True
    fallas = list(FallaMaquinaria.objects.all().order_by('id'))   
    context = {
        'fallasmaquinas': fallas,
        'sidebarsubmenu': 'manage_managefailuremachine',
        'sidebarmenu': 'manage_machine',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_failures_machine.html', context)

@login_required
@mantenedor_sistema_required
def new_failure_machine(request):
    context = {
        'formmarcasmaquinaria': FormMarcaMaquinariaSelect,
        'formfallamaquinaria': FormFallaMaquinaria, 
        'sidebarsubmenu': 'manage_managefailuremachine',
        'sidebarmenu': 'manage_machine',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_failure_machine.html', context)

@login_required
@mantenedor_sistema_required
def save_new_failure_machine(request):     
    if request.method == 'POST':
        kit = KitsMaquinaria.objects.get(id=request.POST['kitMaquinaria'])
        formulario = FormFallaMaquinaria(data=request.POST)
        if formulario.is_valid():       
            falla = FallaMaquinaria(
                kitMaquinaria = kit,
                falla = request.POST['falla'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            falla.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva falla máquina: {falla.falla}', f'Falla de maquinaria: {falla.falla}\nCreada por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_failure_machine')

@login_required
@mantenedor_sistema_required
def status_failure_machine(request):
    if request.method == 'POST': 
        falla = FallaMaquinaria.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (falla.status): 
            FallaMaquinaria.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Falla máquina deshabilitada: {falla.falla}', f'Falla de maquinaria: {falla.falla}\nDeshabilitada por: {user_name}')
            messages.success(request, 'Falla Maquinaria Deshabilitada Correctamente')  
        else:
            FallaMaquinaria.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Falla máquina habilitada: {falla.falla}', f'Falla de maquinaria: {falla.falla}\nHabilitada por: {user_name}')
            messages.success(request, 'Falla Maquinaria Habilitado Correctamente') 
        return redirect('manage_failures_machines')
    else:
        messages.error(request, 'Error al Deshabilitar') 
        return redirect('manage_failures_machines')
    
def cargar_kits_por_marca(request):
    marca_id = request.GET.get('marca_id')
    if marca_id:
        kits = KitsMaquinaria.objects.filter(marcaMaquina_id=marca_id,status=True)
        data = [{'id': kit.id, 'nombre': kit.nombreKit} for kit in kits]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({}, status=400)
    
@login_required
@mantenedor_sistema_required
def new_important_dates(request):
    context = {
        'formnuevafecha': FormNuevaFechasImportantes,
        'sidebarsubmenu': 'manage_important_dates',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_important_dates.html', context)

@login_required
@mantenedor_sistema_required
def save_new_important_dates(request):
    if request.method == 'POST':
        formulario = FormNuevaFechasImportantes(data=request.POST)
        if formulario.is_valid():       
            registro = FechasImportantes(
                descripcion = request.POST['descripcion'],
                fechaVencimiento = request.POST['fechaVencimiento'],
                creador = request.user.first_name+" "+request.user.last_name,
                status = True,
            )
            registro.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nueva fecha importante: {registro.descripcion}', f'Fecha importante: {registro.descripcion}\nCreada por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_important_dates')
    
@login_required
@mantenedor_sistema_required
def manage_important_dates(request): 
    storage = messages.get_messages(request)
    storage.used = True
    dates = list(FechasImportantes.objects.all().order_by('id'))   
    context = {
        'fechasimportantes': dates,
        'sidebarsubmenu': 'manage_important_dates',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/manage_important_dates.html', context)

@login_required
@mantenedor_sistema_required
def status_important_dates(request):
    if request.method == 'POST': 
        fecha = FechasImportantes.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (fecha.status): 
            FechasImportantes.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Fecha deshabilitada: {fecha.descripcion}', f'Fecha importante: {fecha.descripcion}\nDeshabilitada por: {user_name}')
            messages.success(request, 'Fecha Deshabilitada Correctamente')  
        else:
            FechasImportantes.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Fecha habilitada: {fecha.descripcion}', f'Fecha importante: {fecha.descripcion}\nHabilitada por: {user_name}')
            messages.success(request, 'Fecha Habilitado Correctamente') 
        return redirect('manage_important_dates') 

@login_required
@mantenedor_sistema_required
def edit_important_dates(request):  
    try:
        request.session['edit_fecha_id'] = request.POST['fecha_id']            
    except MultiValueDictKeyError:
        request.session['edit_fecha_id'] = request.session['edit_fecha_id']
    fecha = FechasImportantes.objects.get(id=request.session['edit_fecha_id'])
    formFecha = FormNuevaFechasImportantes(instance=fecha)
    context = {
        'id_fecha': fecha.id,
        'formnuevafecha': formFecha,
        'sidebarsubmenu': 'manage_important_dates',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/edit_important_dates.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_important_dates(request):
    if request.method == 'POST':
        instance = get_object_or_404(FechasImportantes, id=request.POST['id_fecha'])
        old_instance = FechasImportantes.objects.get(pk=instance.pk)
        formFecha = FormNuevaFechasImportantes(request.POST, instance=instance)
        if all([
            formFecha.is_valid()
        ]):
            formFecha.save()
            user_name = request.user.get_full_name() or request.user.username
            changes = get_changes_message(old_instance, instance)
            if changes:
                notify_group('mantenimiento_sistema', f'Fecha importante actualizada: {instance.descripcion}', f'Fecha importante: {instance.descripcion}\nActualizada por: {user_name}{changes}')
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': True})
    else:
        return redirect('edit_important_dates')
    
# ---- APLICACIÓN DEL DECORADOR DE ROLES UNIVERSAL PARA REPORTE DE ERRORES ----

@login_required
@admin_or_base_datos_required
def manage_report_error(request):
    storage = messages.get_messages(request)
    storage.used = True
    report_errors = list(ReporteError.objects.all().order_by('fechacreacion'))   
    context = {
        'errores':report_errors,
        'sidebarmain': 'system_report_error',  
    }
    return render(request,'pages/users/manage_report_errors.html', context)

@login_required    
def new_report_error(request):
    context = {
        'formnuevoreporte': FormReporteError,   
        'sidebar': 'dashboard',
    }
    return render(request,'pages/users/new_report_error.html', context)

@login_required
def save_new_report_error(request):
    if request.method == 'POST':
        registro = ReporteError(
            descripcion = request.POST['descripcion'],
            detalle = request.POST['detalle'],
            creador = request.user.first_name+" "+request.user.last_name,
            status = True,
        )
        registro.save()             
        user_name = request.user.get_full_name() or request.user.username
        notify_group('mantenimiento_sistema', f'Nuevo reporte error: {registro.descripcion}', f'Reporte de error: {registro.descripcion}\nCreado por: {user_name}')

        return JsonResponse({'success': True})
    else:
        return redirect('new_report_error')

@login_required
@admin_or_base_datos_required
def mostrar_reporte_error(request, id):
    registro = ReporteError.objects.get(id=id)
    context = {
        'registro': registro,
        'sidebarmain': 'system_report_error',
    }
    return render(request,'pages/users/mostrarregistro.html', context)

@login_required
@mantenedor_sistema_required
def manage_help_manuals(request): 
    storage = messages.get_messages(request)
    storage.used = True
    documentos = list(AyudaManuales.objects.all().order_by('-fechacreacion'))  
    context = {
        'documentos': documentos,
        'sidebarmenu': 'manage_ayuda_manuales',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/manage_help_manuals.html', context)

@login_required
@mantenedor_sistema_required
def new_help_manuals(request):     
    context = {
        'formnuevo': FormAyudaManuales,
        'sidebarmenu': 'manage_ayuda_manuales',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/new_help_manuals.html', context)

@login_required
@mantenedor_sistema_required
def save_new_help_manuals(request):
    if request.method == 'POST':
        toggle_archivoDocumento = request.POST.get('toggle-archivoDocumento', 'no')
        archivo = procesar_fotografia_dos(toggle_archivoDocumento, 'archivoDocumento', 'base/no-imagen.png', request)
        try: 
            documento_ayuda = AyudaManuales.objects.get(nombredocumento=request.POST['nombredocumento'],seccion=request.POST['seccion'])
            return documento_ayuda
        except ObjectDoesNotExist:            
            formulario = FormAyudaManuales(data=request.POST)
            if formulario.is_valid():       
                documento = AyudaManuales(
                    seccion = request.POST['seccion'],
                    nombredocumento = request.POST['nombredocumento'],
                    archivodocumento = archivo,
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_help_manuals')

@login_required
@mantenedor_sistema_required
def status_help_manuals(request):
    if request.method == 'POST': 
        tipo_documento = AyudaManuales.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (tipo_documento.status): 
            AyudaManuales.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Documento ayuda deshabilitado: {tipo_documento.nombredocumento}', f'Documento de ayuda: {tipo_documento.nombredocumento}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Documento Deshabilitado Correctamente')  
        else:
            AyudaManuales.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Documento ayuda habilitado: {tipo_documento.nombredocumento}', f'Documento de ayuda: {tipo_documento.nombredocumento}\nHabilitado por: {user_name}')
            messages.success(request, 'Documento Habilitado Correctamente') 
        return redirect('manage_help_manuals')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_help_manuals') 

@login_required
@mantenedor_sistema_required
def edit_help_manuals(request):  
    try:
        request.session['edit_document_general_id'] = request.POST['documento_id']             
    except MultiValueDictKeyError:
        request.session['edit_document_general_id'] = request.session['edit_document_general_id']
    documento = AyudaManuales.objects.get(id=request.session['edit_document_general_id'])
    urlDocumento = documento.archivodocumento
    if urlDocumento.url.lower().endswith((".jpg", ".jpeg", ".png")):
        extensionDocumento = "imagen"
    elif urlDocumento.url.lower().endswith((".pdf")):
        extensionDocumento = "pdf"
    else:
        extensionDocumento = "otro"
    context = {
        'formeditardocumento':  FormAyudaManuales(initial={
            'seccion': documento.seccion,
            'nombredocumento': documento.nombredocumento,
            },
        ),
        'documento_id': documento.id,
        'archivodocumento': documento.archivodocumento,
        'extensionDocumento': extensionDocumento,
        'sidebarmenu': 'manage_ayuda_manuales',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/edit_help_manuals.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_help_manuals(request):    
    if request.method == 'POST':
        old_documento = AyudaManuales.objects.get(id=request.POST['documento_id'])
        AyudaManuales.objects.filter(id=request.POST['documento_id']).update(seccion=request.POST['seccion'],nombredocumento=request.POST['nombredocumento'])
        documento = AyudaManuales.objects.get(id=request.POST['documento_id'])
        toggle_Documento = request.POST.get('toggle-archivoDocumento', 'no')
        archivo = procesar_fotografia_dos(toggle_Documento, 'archivoDocumento','base/no-imagen.png', request)
        documento.archivodocumento = archivo
        documento.save()
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_documento, documento)
        if changes:
            notify_group('mantenimiento_sistema', f'Documento ayuda actualizado: {documento.nombredocumento}', f'Documento de ayuda: {documento.nombredocumento}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_help_manuals')

@login_required
def view_help_manuals(request): 
    storage = messages.get_messages(request)
    storage.used = True
    documentos = list(AyudaManuales.objects.all().order_by('-fechacreacion'))  
    context = {
        'documentos': documentos,
        'sidebar': 'dashboard', 
    }
    return render(request,'pages/users/manage_help_manuals.html', context)

@login_required
@mantenedor_sistema_required
def manage_probe(request): 
    lista = list(Sondas.objects.all().order_by('sonda'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_sonda',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_probe.html', context)

@login_required
@mantenedor_sistema_required
def new_probe(request):     
    context = {
        'formnuevo': FormSondas,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_sonda',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_probe.html', context)

@login_required
@mantenedor_sistema_required
def save_new_probe(request):
    if request.method == 'POST':
        try: 
            sonda = Sondas.objects.get(sonda=request.POST['sonda'])
            return sonda
        except ObjectDoesNotExist:   
            formulario = FormSondas(data=request.POST)
            if formulario.is_valid():       
                documento = Sondas(
                    sonda = request.POST['sonda'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Sonda: {documento.sonda}', f'Sonda: {documento.sonda}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_probe')

@login_required
@mantenedor_sistema_required
def status_probe(request):
    if request.method == 'POST': 
        sonda = Sondas.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (sonda.status): 
            Sondas.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Sonda deshabilitada: {sonda.sonda}', f'Sonda: {sonda.sonda}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Sonda Deshabilitada Correctamente')  
        else:
            Sondas.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Sonda habilitada: {sonda.sonda}', f'Sonda: {sonda.sonda}\nHabilitado por: {user_name}')
            messages.success(request, 'Sonda Habilitada Correctamente') 
        return redirect('manage_probe')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_probe') 

@login_required
@mantenedor_sistema_required
def edit_probe(request):  
    from drilling.models import ReportesOperacionales, ControlesHorarios

    def to_seconds(time_value):
        if not time_value:
            return 0
        return (time_value.hour * 3600) + (time_value.minute * 60) + time_value.second

    def format_hh_mm(total_seconds):
        total_seconds = int(total_seconds or 0)
        horas = total_seconds // 3600
        minutos = (total_seconds % 3600) // 60
        return f"{horas:02d}:{minutos:02d}"

    def format_horas_perforacion(total_seconds, metros_perforados):
        segundos = int(total_seconds or 0)
        if segundos > 0:
            return format_hh_mm(segundos)
        return "-"

    def contiene_perforacion(texto):
        if not texto:
            return False
        normalizado = unicodedata.normalize('NFKD', str(texto))
        normalizado = ''.join(ch for ch in normalizado if not unicodedata.combining(ch))
        return 'perfor' in normalizado.casefold()

    def parse_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def build_sondaje_data(reporte):
        sondaje_nombre = "-"
        sondaje_key = ""
        if reporte.sondajeCodigo:
            base_sondaje = f"{reporte.sondajeCodigo.sondaje}-{reporte.sondajeSerie}"
            if reporte.sondajeEstado:
                base_sondaje = f"{base_sondaje} {reporte.get_sondajeEstado_display()}"
            sondaje_nombre = base_sondaje
            estado = reporte.sondajeEstado or ""
            serie = reporte.sondajeSerie if reporte.sondajeSerie is not None else ""
            sondaje_key = f"{reporte.sondajeCodigo_id}|{serie}|{estado}"
        return sondaje_nombre, sondaje_key

    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Sondas.objects.get(id=request.session['edit_id'])

    reportes_aprobados_todos = list(
        ReportesOperacionales.objects.filter(
            sonda=documento,
            status=True,
            progreso='Aprobado',
        )
        .select_related('sondajeCodigo__faena', 'controlador')
        .order_by('-fechacreacion')
    )

    filtro_anio = (request.GET.get('anio') or '').strip()
    filtro_mes = (request.GET.get('mes') or '').strip()
    filtro_sondaje = (request.GET.get('sondaje') or '').strip()
    filtro_turno = (request.GET.get('turno') or '').strip()
    filtros_actuales = {
        'anio': filtro_anio,
        'mes': filtro_mes,
        'sondaje': filtro_sondaje,
        'turno': filtro_turno,
    }

    if filtros_actuales['anio'] and parse_int(filtros_actuales['anio']) is None:
        filtros_actuales['anio'] = ''
    if filtros_actuales['mes']:
        mes_int = parse_int(filtros_actuales['mes'])
        if mes_int is None or mes_int < 1 or mes_int > 12:
            filtros_actuales['mes'] = ''

    nombres_meses = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }

    def get_filter_item_value(item, campo):
        if campo == 'anio':
            return item['anio']
        if campo == 'mes':
            return item['mes']
        if campo == 'sondaje':
            return item['sondaje_key']
        if campo == 'turno':
            return item['turno_value']
        return ''

    def cumple_filtros_item(item, filtros, campo_excluido=None):
        for campo in ['anio', 'mes', 'sondaje', 'turno']:
            if campo_excluido == campo:
                continue
            valor_filtro = filtros.get(campo) or ''
            if valor_filtro and get_filter_item_value(item, campo) != valor_filtro:
                return False
        return True

    def construir_opciones_filtros(items, filtros):
        anios_disponibles = sorted(
            {
                item['anio']
                for item in items
                if item['anio'] and cumple_filtros_item(item, filtros, campo_excluido='anio')
            },
            key=lambda x: int(x),
            reverse=True
        )

        meses_disponibles_numericos = sorted(
            {
                int(item['mes'])
                for item in items
                if item['mes'].isdigit() and cumple_filtros_item(item, filtros, campo_excluido='mes')
            }
        )
        meses_disponibles = [
            {'value': str(mes), 'label': nombres_meses[mes]}
            for mes in meses_disponibles_numericos
            if mes in nombres_meses
        ]

        sondajes_disponibles_map = {}
        for item in items:
            if not cumple_filtros_item(item, filtros, campo_excluido='sondaje'):
                continue
            if item['sondaje_key'] and item['sondaje_key'] not in sondajes_disponibles_map:
                sondajes_disponibles_map[item['sondaje_key']] = item['sondaje_label']
        sondajes_disponibles = [
            {'value': key, 'label': value}
            for key, value in sorted(sondajes_disponibles_map.items(), key=lambda option: option[1])
        ]

        turnos_disponibles_map = {}
        for item in items:
            if not cumple_filtros_item(item, filtros, campo_excluido='turno'):
                continue
            if item['turno_value'] and item['turno_value'] not in turnos_disponibles_map:
                turnos_disponibles_map[item['turno_value']] = item['turno_label']
        turnos_disponibles = [
            {'value': key, 'label': value}
            for key, value in sorted(turnos_disponibles_map.items(), key=lambda option: option[1])
        ]

        return {
            'anios': anios_disponibles,
            'meses': meses_disponibles,
            'sondajes': sondajes_disponibles,
            'turnos': turnos_disponibles,
        }

    def filtro_es_valido(campo, valor, opciones):
        if not valor:
            return True
        if campo == 'anio':
            return valor in opciones['anios']
        if campo == 'mes':
            return valor in [opcion['value'] for opcion in opciones['meses']]
        if campo == 'sondaje':
            return valor in [opcion['value'] for opcion in opciones['sondajes']]
        if campo == 'turno':
            return valor in [opcion['value'] for opcion in opciones['turnos']]
        return True

    reportes_enriquecidos = []
    for reporte in reportes_aprobados_todos:
        fecha_reporte = reporte.fechacreacion
        if fecha_reporte and timezone.is_aware(fecha_reporte):
            fecha_reporte = timezone.localtime(fecha_reporte)

        sondaje_nombre, sondaje_key = build_sondaje_data(reporte)
        turno_value = str(reporte.turno or "")
        turno_label = reporte.get_turno_display() if reporte.turno else "Sin turno"

        reportes_enriquecidos.append({
            'reporte': reporte,
            'anio': str(fecha_reporte.year) if fecha_reporte else '',
            'mes': str(fecha_reporte.month) if fecha_reporte else '',
            'sondaje_key': sondaje_key,
            'sondaje_label': sondaje_nombre,
            'turno_value': turno_value,
            'turno_label': turno_label,
        })

    opciones_filtros_uso_sonda = {}
    for _ in range(4):
        opciones_filtros_uso_sonda = construir_opciones_filtros(reportes_enriquecidos, filtros_actuales)
        cambios = False
        for campo in ['anio', 'mes', 'sondaje', 'turno']:
            valor_actual = filtros_actuales.get(campo) or ''
            if valor_actual and not filtro_es_valido(campo, valor_actual, opciones_filtros_uso_sonda):
                filtros_actuales[campo] = ''
                cambios = True
        if not cambios:
            break
    else:
        opciones_filtros_uso_sonda = construir_opciones_filtros(reportes_enriquecidos, filtros_actuales)

    reportes_aprobados = [
        item['reporte']
        for item in reportes_enriquecidos
        if cumple_filtros_item(item, filtros_actuales)
    ]

    horas_por_reporte = defaultdict(int)
    horas_perforacion_por_reporte = defaultdict(int)
    total_horas_segundos = 0
    total_horas_perforacion_segundos = 0

    reportes_ids = [reporte.id for reporte in reportes_aprobados]
    if reportes_ids:
        # Fuente de horas: controles horarios del reporte aprobado.
        controles_horarios = ControlesHorarios.objects.filter(
            reporte_id__in=reportes_ids,
            status=True
        ).select_related('detalleControlHorario')
        for control in controles_horarios:
            segundos = to_seconds(control.total)
            total_horas_segundos += segundos
            horas_por_reporte[control.reporte_id] += segundos

            detalle_nombre = ""
            if control.detalleControlHorario:
                detalle_nombre = control.detalleControlHorario.detalle or ""
            if contiene_perforacion(detalle_nombre):
                total_horas_perforacion_segundos += segundos
                horas_perforacion_por_reporte[control.reporte_id] += segundos

    turnos_usados = defaultdict(int)
    metros_por_dia_map = defaultdict(float)
    reportes_recientes = []

    for reporte in reportes_aprobados:
        turno = reporte.get_turno_display() if reporte.turno else "Sin turno"
        turnos_usados[turno] += 1

        if reporte.fechacreacion:
            fecha_reporte = reporte.fechacreacion
            if timezone.is_aware(fecha_reporte):
                fecha_reporte = timezone.localtime(fecha_reporte)
            metros_por_dia_map[fecha_reporte.date()] += float(reporte.totalPerforado or 0)

        faena_nombre = "-"
        if reporte.sondajeCodigo and reporte.sondajeCodigo.faena:
            faena_nombre = reporte.sondajeCodigo.faena.faena

        sondaje_nombre, _ = build_sondaje_data(reporte)

        metros_reporte = float(reporte.totalPerforado or 0)
        reportes_recientes.append({
            'fecha': reporte.fechacreacion,
            'faena': faena_nombre,
            'sondaje': sondaje_nombre,
            'turno': turno,
            'metros': f"{metros_reporte:.2f}",
            'horas_total': format_hh_mm(horas_por_reporte.get(reporte.id)),
            'horas_perforacion': format_horas_perforacion(
                horas_perforacion_por_reporte.get(reporte.id),
                metros_reporte
            ),
        })

    metros_por_dia = []
    for fecha in sorted(metros_por_dia_map.keys(), reverse=True):
        metros_por_dia.append({
            'fecha': fecha,
            'metros': f"{metros_por_dia_map[fecha]:.2f}",
        })

    ultimo_uso = None
    if reportes_aprobados:
        ultimo = reportes_aprobados[0]
        ultimo_faena = "-"
        if ultimo.sondajeCodigo and ultimo.sondajeCodigo.faena:
            ultimo_faena = ultimo.sondajeCodigo.faena.faena

        ultimo_sondaje, _ = build_sondaje_data(ultimo)

        metros_ultimo = float(ultimo.totalPerforado or 0)
        ultimo_uso = {
            'fecha': ultimo.fechacreacion,
            'faena': ultimo_faena,
            'sondaje': ultimo_sondaje,
            'turno': ultimo.get_turno_display() if ultimo.turno else "Sin turno",
            'metros': f"{metros_ultimo:.2f}",
            'horas_total': format_hh_mm(horas_por_reporte.get(ultimo.id)),
            'horas_perforacion': format_horas_perforacion(
                horas_perforacion_por_reporte.get(ultimo.id),
                metros_ultimo
            ),
        }

    promedio_metros_dia = 0
    if metros_por_dia_map:
        promedio_metros_dia = sum(metros_por_dia_map.values()) / len(metros_por_dia_map)

    total_metros_reportes = sum(float(reporte.totalPerforado or 0) for reporte in reportes_aprobados)
    estadisticas_uso_sonda = {
        'total_reportes': len(reportes_aprobados),
        'ultimo_uso': ultimo_uso,
        'horas_total': format_hh_mm(total_horas_segundos),
        'horas_perforacion': format_horas_perforacion(total_horas_perforacion_segundos, total_metros_reportes),
        'total_metros_perforados': f"{total_metros_reportes:.2f}",
        'promedio_metros_dia': f"{promedio_metros_dia:.2f}",
        'turnos': [{'nombre': nombre, 'cantidad': cantidad} for nombre, cantidad in sorted(turnos_usados.items())],
        'metros_por_dia': metros_por_dia,
        'reportes_recientes': reportes_recientes,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        ultimo_uso_payload = None
        if ultimo_uso:
            fecha_ultimo = ultimo_uso.get('fecha')
            if fecha_ultimo and timezone.is_aware(fecha_ultimo):
                fecha_ultimo = timezone.localtime(fecha_ultimo)
            ultimo_uso_payload = {
                'fecha': fecha_ultimo.strftime('%d/%m/%Y %H:%M') if fecha_ultimo else '-',
                'faena': ultimo_uso.get('faena') or '-',
                'turno': ultimo_uso.get('turno') or '-',
                'sondaje': ultimo_uso.get('sondaje') or '-',
                'metros': ultimo_uso.get('metros') or '-',
            }

        reportes_payload = []
        for reporte in reportes_recientes:
            fecha_reporte = reporte.get('fecha')
            if fecha_reporte and timezone.is_aware(fecha_reporte):
                fecha_reporte = timezone.localtime(fecha_reporte)
            reportes_payload.append({
                'fecha': fecha_reporte.strftime('%d/%m/%Y %H:%M') if fecha_reporte else '-',
                'faena': reporte.get('faena') or '-',
                'sondaje': reporte.get('sondaje') or '-',
                'turno': reporte.get('turno') or '-',
                'metros': reporte.get('metros') or '0.00',
                'horas_perforacion': reporte.get('horas_perforacion') or '-',
            })

        return JsonResponse({
            'total_reportes': estadisticas_uso_sonda['total_reportes'],
            'horas_perforacion': estadisticas_uso_sonda['horas_perforacion'],
            'total_metros_perforados': estadisticas_uso_sonda['total_metros_perforados'],
            'promedio_metros_dia': estadisticas_uso_sonda['promedio_metros_dia'],
            'ultimo_uso': ultimo_uso_payload,
            'reportes_recientes': reportes_payload,
            'filtros_uso_sonda': filtros_actuales,
            'opciones_filtros_uso_sonda': opciones_filtros_uso_sonda,
        })

    context = {
        'formeditar':  FormSondas(initial={
            'sonda': documento.sonda,
        },
        ),
        'estadisticas_uso_sonda': estadisticas_uso_sonda,
        'filtros_uso_sonda': {
            'anio': filtros_actuales['anio'],
            'mes': filtros_actuales['mes'],
            'sondaje': filtros_actuales['sondaje'],
            'turno': filtros_actuales['turno'],
        },
        'opciones_filtros_uso_sonda': opciones_filtros_uso_sonda,
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_sonda',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_probe.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_probe(request):     
    if request.method == 'POST':
        old_obj = Sondas.objects.get(pk=request.POST['id'])
        Sondas.objects.filter(id=request.POST['id']).update(sonda=request.POST['sonda'])
        obj = Sondas.objects.get(pk=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Sonda actualizada: {obj.sonda}', f'Sonda: {obj.sonda}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_probe')

@login_required
@mantenedor_sistema_required
def manage_aditivos(request): 
    lista = list(Aditivos.objects.all().order_by('aditivo'))   
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_aditivo',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_aditivos.html', context)

@login_required
@mantenedor_sistema_required
def new_aditivos(request):     
    context = {
        'formnuevo': FormAditivos,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_aditivo',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_aditivos.html', context)

@login_required
@mantenedor_sistema_required
def save_new_aditivos(request):
    if request.method == 'POST':
        try: 
            aditivo = Aditivos.objects.get(aditivo=request.POST['aditivo'])
            return aditivo
        except ObjectDoesNotExist:            
            formulario = FormAditivos(data=request.POST)
            if formulario.is_valid():       
                documento = Aditivos(
                    aditivo = request.POST['aditivo'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Aditivo: {documento.aditivo}', f'Aditivo: {documento.aditivo}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_aditivos')

@login_required
@mantenedor_sistema_required
def status_aditivos(request):
    if request.method == 'POST': 
        aditivo = Aditivos.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (aditivo.status): 
            Aditivos.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Aditivo deshabilitado: {aditivo.aditivo}', f'Aditivo: {aditivo.aditivo}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Aditivo Deshabilitado Correctamente')  
        else:
            Aditivos.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Aditivo habilitado: {aditivo.aditivo}', f'Aditivo: {aditivo.aditivo}\nHabilitado por: {user_name}')
            messages.success(request, 'Aditivo Habilitado Correctamente') 
        return redirect('manage_aditivos')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_aditivos') 

@login_required
@mantenedor_sistema_required
def edit_aditivos(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Aditivos.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormAditivos(initial={
            'aditivo': documento.aditivo,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_aditivo',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_aditivos.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_aditivos(request):     
    if request.method == 'POST':
        old_obj = Aditivos.objects.get(pk=request.POST['id'])
        Aditivos.objects.filter(id=request.POST['id']).update(aditivo=request.POST['aditivo'])
        obj = Aditivos.objects.get(pk=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Aditivo actualizado: {obj.aditivo}', f'Aditivo: {obj.aditivo}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_aditivos')
    
@login_required
@mantenedor_sistema_required
def manage_cantidadAgua(request): 
    lista = list(CantidadAgua.objects.all().order_by('cantidadAgua'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_cantidadAgua',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_cantidadAgua.html', context)

@login_required
@mantenedor_sistema_required
def new_cantidadAgua(request):     
    context = {
        'formnuevo': FormCantidadAgua,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_cantidadAgua',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_cantidadAgua.html', context)

@login_required
@mantenedor_sistema_required
def save_new_cantidadAgua(request):
    if request.method == 'POST':
        try: 
            cantidadAgua = CantidadAgua.objects.get(cantidadAgua=request.POST['cantidadAgua'])
            return cantidadAgua
        except ObjectDoesNotExist:            
            formulario = FormCantidadAgua(data=request.POST)
            if formulario.is_valid():       
                documento = CantidadAgua(
                    cantidadAgua = request.POST['cantidadAgua'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nueva Cantidad de agua: {documento.cantidadAgua}', f'Cantidad de agua: {documento.cantidadAgua}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_cantidadAgua')

@login_required
@mantenedor_sistema_required
def status_cantidadAgua(request):
    if request.method == 'POST': 
        cantidadAgua = CantidadAgua.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (cantidadAgua.status): 
            CantidadAgua.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Cantidad de agua deshabilitada: {cantidadAgua.cantidadAgua}', f'Cantidad de agua: {cantidadAgua.cantidadAgua}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Cantidad Agua Deshabilitada Correctamente')  
        else:
            CantidadAgua.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Cantidad de agua habilitada: {cantidadAgua.cantidadAgua}', f'Cantidad de agua: {cantidadAgua.cantidadAgua}\nHabilitado por: {user_name}')
            messages.success(request, 'Cantidad Agua Habilitada Correctamente') 
        return redirect('manage_cantidadAgua')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_cantidadAgua') 

@login_required
@mantenedor_sistema_required
def edit_cantidadAgua(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = CantidadAgua.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormCantidadAgua(initial={
            'cantidadAgua': documento.cantidadAgua,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_cantidadAgua',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_cantidadAgua.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_cantidadAgua(request):     
    if request.method == 'POST':
        old_obj = CantidadAgua.objects.get(pk=request.POST['id'])
        CantidadAgua.objects.filter(id=request.POST['id']).update(cantidadAgua=request.POST['cantidadAgua'])
        obj = CantidadAgua.objects.get(pk=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Cantidad de agua actualizada: {obj.cantidadAgua}', f'Cantidad de agua: {obj.cantidadAgua}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_cantidadAgua')

@login_required
@mantenedor_sistema_required
def manage_casing(request): 
    lista = list(Casing.objects.all().order_by('casing'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_casing',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_casing.html', context)

@login_required
@mantenedor_sistema_required
def new_casing(request):     
    context = {
        'formnuevo': FormCasing,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_casing',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_casing.html', context)

@login_required
@mantenedor_sistema_required
def save_new_casing(request):
    if request.method == 'POST':
        try: 
            casing = Casing.objects.get(casing=request.POST['casing'])
            return casing
        except ObjectDoesNotExist:            
            formulario = FormCasing(data=request.POST)
            if formulario.is_valid():       
                documento = Casing(
                    casing = request.POST['casing'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Casing: {documento.casing}', f'Casing: {documento.casing}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_casing')

@login_required
@mantenedor_sistema_required
def status_casing(request):
    if request.method == 'POST': 
        casing = Casing.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (casing.status): 
            Casing.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Casing deshabilitado: {casing.casing}', f'Casing: {casing.casing}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Casing Deshabilitado Correctamente')  
        else:
            Casing.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Casing habilitado: {casing.casing}', f'Casing: {casing.casing}\nHabilitado por: {user_name}')
            messages.success(request, 'Casing Habilitado Correctamente') 
        return redirect('manage_casing')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_casing') 

@login_required
@mantenedor_sistema_required
def edit_casing(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Casing.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormCasing(initial={
            'casing': documento.casing,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_casing',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_casing.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_casing(request):     
    if request.method == 'POST':
        old_obj = Casing.objects.get(pk=request.POST['id'])
        Casing.objects.filter(id=request.POST['id']).update(casing=request.POST['casing'])
        obj = Casing.objects.get(pk=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Casing actualizado: {obj.casing}', f'Casing: {obj.casing}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_casing')
    
@login_required
@mantenedor_sistema_required
def manage_corona(request): 
    lista = list(Corona.objects.all().order_by('corona'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_corona',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_corona.html', context)

@login_required
@mantenedor_sistema_required
def new_corona(request):     
    context = {
        'formnuevo': FormCorona,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_corona',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_corona.html', context)

@login_required
@mantenedor_sistema_required
def save_new_corona(request):
    if request.method == 'POST':
        try: 
            corona = Corona.objects.get(corona=request.POST['corona'])
            return corona
        except ObjectDoesNotExist:      
            formulario = FormCorona(data=request.POST)
            if formulario.is_valid():       
                documento = Corona(
                    corona = request.POST['corona'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nueva Corona: {documento.corona}', f'Corona: {documento.corona}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                 return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_corona')

@login_required
@mantenedor_sistema_required
def status_corona(request):
    if request.method == 'POST': 
        corona = Corona.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (corona.status): 
            Corona.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Corona deshabilitada: {corona.corona}', f'Corona: {corona.corona}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Corona Deshabilitada Correctamente')  
        else:
            Corona.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Corona habilitada: {corona.corona}', f'Corona: {corona.corona}\nHabilitado por: {user_name}')
            messages.success(request, 'Corona Habilitada Correctamente') 
        return redirect('manage_corona')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_corona') 

@login_required
@mantenedor_sistema_required
def edit_corona(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Corona.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormCorona(initial={
            'corona': documento.corona,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_corona',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_corona.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_corona(request):     
    if request.method == 'POST':
        old_obj = Corona.objects.get(pk=request.POST['id'])
        Corona.objects.filter(id=request.POST['id']).update(corona=request.POST['corona'])
        obj = Corona.objects.get(pk=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Corona actualizada: {obj.corona}', f'Corona: {obj.corona}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_corona')
    
@login_required
@mantenedor_sistema_required
def manage_details(request): 
    lista = list(DetalleControlHorario.objects.all().order_by('detalle'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_detalle',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_details.html', context)

@login_required
@mantenedor_sistema_required
def new_details(request):     
    context = {
        'formnuevo': FormDetalleControlHorario,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_detalle',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_details.html', context)

@login_required
@mantenedor_sistema_required
def save_new_details(request):
    if request.method == 'POST':
        try: 
            detalle = DetalleControlHorario.objects.get(detalle=request.POST['detalle'])
            return detalle
        except ObjectDoesNotExist:            
            formulario = FormDetalleControlHorario(data=request.POST)
            if formulario.is_valid():       
                documento = DetalleControlHorario(
                    detalle = request.POST['detalle'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Detalle: {documento.detalle}', f'Detalle: {documento.detalle}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_details')

@login_required
@mantenedor_sistema_required
def status_details(request):
    if request.method == 'POST': 
        detalle = DetalleControlHorario.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (detalle.status): 
            DetalleControlHorario.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Detalle deshabilitado: {detalle.detalle}', f'Detalle: {detalle.detalle}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Detalle Deshabilitada Correctamente')  
        else:
            DetalleControlHorario.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Detalle habilitado: {detalle.detalle}', f'Detalle: {detalle.detalle}\nHabilitado por: {user_name}')
            messages.success(request, 'Detalle Habilitada Correctamente') 
        return redirect('manage_details')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_details') 

@login_required
@mantenedor_sistema_required
def edit_details(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = DetalleControlHorario.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormDetalleControlHorario(initial={
            'detalle': documento.detalle,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_detalle',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_details.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_details(request):     
    if request.method == 'POST':
        old_obj = DetalleControlHorario.objects.get(pk=request.POST['id'])
        DetalleControlHorario.objects.filter(id=request.POST['id']).update(detalle=request.POST['detalle'])
        obj = DetalleControlHorario.objects.get(pk=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Detalle actualizado: {obj.detalle}', f'Detalle: {obj.detalle}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_details')

@login_required
@mantenedor_sistema_required
def manage_diameter(request): 
    lista = list(Diametros.objects.all().order_by('diametro'))  

    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_diametro',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_diameter.html', context)

@login_required
@mantenedor_sistema_required
def new_diameter(request):     
    context = {
        'formnuevo': FormDiametros,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_diametro',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_diameter.html', context)

@login_required
@mantenedor_sistema_required
def save_new_diameter(request):
    if request.method == 'POST':
        try: 
            diametro = Diametros.objects.get(diametro=request.POST['diametro'])
            return diametro
        except ObjectDoesNotExist:            
            formulario = FormDiametros(data=request.POST)
            if formulario.is_valid():       
                documento = Diametros(
                    diametro = request.POST['diametro'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Diámetro: {documento.diametro}', f'Diámetro: {documento.diametro}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_diameter')

@login_required
@mantenedor_sistema_required
def status_diameter(request):
    if request.method == 'POST': 
        diametro = Diametros.objects.get(id=request.POST['id'])
        if (diametro.status): 
            Diametros.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Diametro Deshabilitada Correctamente')
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Diámetro deshabilitado: {diametro.diametro}', f'Diámetro: {diametro.diametro}\nDeshabilitado por: {user_name}')
        else:
            Diametros.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Diametro Habilitada Correctamente')
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Diámetro habilitado: {diametro.diametro}', f'Diámetro: {diametro.diametro}\nHabilitado por: {user_name}')
        return redirect('manage_diameter')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_diameter') 

@login_required
@mantenedor_sistema_required
def edit_diameter(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Diametros.objects.get(id=request.session['edit_id'])
    
    context = {
        'formeditar':  FormDiametros(initial={
            'diametro': documento.diametro,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_diametro',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_diameter.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_diameter(request):     
    if request.method == 'POST':
        obj = Diametros.objects.get(pk=request.POST['id'])
        old_obj = Diametros.objects.get(pk=obj.pk)
        obj.diametro = request.POST['diametro']
        obj.save()
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Diámetro actualizado: {obj.diametro}', f'Diámetro: {obj.diametro}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_diameter')
    
@login_required
@mantenedor_sistema_required
def manage_drilling(request): 
    lista = list(Sondajes.objects.all().order_by('sondaje'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_sondaje',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_drilling.html', context)

@login_required
@mantenedor_sistema_required
def new_drilling(request):     
    context = {
        'formnuevo': FormSondajes,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_sondaje',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_drilling.html', context)

@login_required
@mantenedor_sistema_required
def save_new_drilling(request):
    if request.method == 'POST':
        faena = Faena.objects.get(id=request.POST['faena'])
        try: 
            sondaje = Sondajes.objects.get(sondaje=request.POST['sondaje'])
            return sondaje
        except ObjectDoesNotExist:
            formulario = FormSondajes(data=request.POST)
            if formulario.is_valid():       
                documento = Sondajes(
                    faena = faena,
                    sondaje = request.POST['sondaje'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Perforación (Sondaje): {documento.sondaje}', f'Perforación (Sondaje): {documento.sondaje}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_drilling')

@login_required
@mantenedor_sistema_required
def status_drilling(request):
    if request.method == 'POST': 
        sondaje = Sondajes.objects.get(id=request.POST['id'])
        if (sondaje.status): 
            Sondajes.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Sondaje Deshabilitado Correctamente')
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Perforación (Sondaje) deshabilitado: {sondaje.sondaje}', f'Perforación (Sondaje): {sondaje.sondaje}\nDeshabilitado por: {user_name}')
        else:
            Sondajes.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Sondaje Habilitado Correctamente')
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Perforación (Sondaje) habilitado: {sondaje.sondaje}', f'Perforación (Sondaje): {sondaje.sondaje}\nHabilitado por: {user_name}')
        return redirect('manage_drilling')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_drilling') 

@login_required
@mantenedor_sistema_required
def edit_drilling(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Sondajes.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormSondajes(initial={
            'faena': documento.faena,
            'sondaje': documento.sondaje,
        },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_sondaje',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_drilling.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_drilling(request):     
    if request.method == 'POST':
        obj = Sondajes.objects.get(pk=request.POST['id'])
        old_obj = Sondajes.objects.get(pk=obj.pk)
        obj.faena_id = request.POST['faena']
        obj.sondaje = request.POST['sondaje']
        obj.save()
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Perforación (Sondaje) actualizado: {obj.sondaje}', f'Perforación (Sondaje): {obj.sondaje}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_drilling')
    
@login_required
@mantenedor_sistema_required
def manage_escareador(request): 
    lista = list(Escareador.objects.all().order_by('escareador'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_escareador',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_escareador.html', context)

@login_required
@mantenedor_sistema_required
def new_escareador(request):     
    context = {
        'formnuevo': FormEscareador,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_escareador',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_escareador.html', context)

@login_required
@mantenedor_sistema_required
def save_new_escareador(request):
    if request.method == 'POST':
        try: 
            escareador = Escareador.objects.get(escareador=request.POST['escareador'])
            return escareador
        except ObjectDoesNotExist:  
            formulario = FormEscareador(data=request.POST)
            if formulario.is_valid():       
                documento = Escareador(
                    escareador = request.POST['escareador'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Escareador: {documento.escareador}', f'Escareador: {documento.escareador}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_escareador')

@login_required
@mantenedor_sistema_required
def status_escareador(request):
    if request.method == 'POST': 
        escareador = Escareador.objects.get(id=request.POST['id'])
        if (escareador.status): 
            Escareador.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Escareador Deshabilitado Correctamente')
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Escareador deshabilitado: {escareador.escareador}', f'Escareador: {escareador.escareador}\nDeshabilitado por: {user_name}')
        else:
            Escareador.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Escareador Habilitado Correctamente')
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Escareador habilitado: {escareador.escareador}', f'Escareador: {escareador.escareador}\nHabilitado por: {user_name}')
        return redirect('manage_escareador')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_escareador') 

@login_required
@mantenedor_sistema_required
def edit_escareador(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Escareador.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormEscareador(initial={
            'escareador': documento.escareador,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_escareador',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_escareador.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_escareador(request):    
    if request.method == 'POST':
        obj = Escareador.objects.get(pk=request.POST['id'])
        old_obj = Escareador.objects.get(pk=obj.pk)
        obj.escareador = request.POST['escareador']
        obj.save()
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Escareador actualizado: {obj.escareador}', f'Escareador: {obj.escareador}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_escareador')
    
@login_required
@mantenedor_sistema_required
def manage_largoBarra(request): 
    lista = list(LargoBarra.objects.all().order_by('largoBarra'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_largoBarra',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_largoBarra.html', context)

@login_required
@mantenedor_sistema_required
def new_largoBarra(request):     
    context = {
        'formnuevo': FormLargoBarra,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_largoBarra',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_largoBarra.html', context)

@login_required
@mantenedor_sistema_required
def save_new_largoBarra(request):
    if request.method == 'POST':
        try: 
            largoBarra = LargoBarra.objects.get(largoBarra=request.POST['largoBarra'])
            return largoBarra
        except ObjectDoesNotExist:            
            formulario = FormLargoBarra(data=request.POST)
            if formulario.is_valid():       
                documento = LargoBarra(
                    largoBarra = request.POST['largoBarra'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Largo de barra: {documento.largoBarra}', f'Largo de barra: {documento.largoBarra}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_largoBarra')

@login_required
@mantenedor_sistema_required
def status_largoBarra(request):
    if request.method == 'POST': 
        largoBarra = LargoBarra.objects.get(id=request.POST['id'])
        if (largoBarra.status): 
            LargoBarra.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Largo Barra Deshabilitada Correctamente')
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Largo de barra deshabilitado: {largoBarra.largoBarra}', f'Largo de barra: {largoBarra.largoBarra}\nDeshabilitado por: {user_name}')
        else:
            LargoBarra.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Largo Barra Habilitada Correctamente')
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Largo de barra habilitado: {largoBarra.largoBarra}', f'Largo de barra: {largoBarra.largoBarra}\nHabilitado por: {user_name}')
        return redirect('manage_largoBarra')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_largoBarra') 

@login_required
@mantenedor_sistema_required
def edit_largoBarra(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = LargoBarra.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormLargoBarra(initial={
            'largoBarra': documento.largoBarra,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_largoBarra',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_largoBarra.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_largoBarra(request):     
    if request.method == 'POST':
        obj = LargoBarra.objects.get(pk=request.POST['id'])
        old_obj = LargoBarra.objects.get(pk=obj.pk)
        obj.largoBarra = request.POST['largoBarra']
        obj.save()
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Largo de barra actualizado: {obj.largoBarra}', f'Largo de barra: {obj.largoBarra}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_largoBarra')
    
@login_required
@mantenedor_sistema_required
def manage_orientation(request): 
    lista = list(Orientacion.objects.all().order_by('orientacion'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_orientacion',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_orientation.html', context)

@login_required
@mantenedor_sistema_required
def new_orientation(request):     
    context = {
        'formnuevo': FormOrientacion,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_orientacion',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_orientation.html', context)

@login_required
@mantenedor_sistema_required
def save_new_orientation(request):
    if request.method == 'POST':
        try: 
            orientacion = Orientacion.objects.get(orientacion=request.POST['orientacion'])
            return orientacion
        except ObjectDoesNotExist:            
            formulario = FormOrientacion(data=request.POST)
            if formulario.is_valid():       
                documento = Orientacion(
                    orientacion = request.POST['orientacion'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Orientación: {documento.orientacion}', f'Orientación: {documento.orientacion}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_orientation')

@login_required
@mantenedor_sistema_required
def status_orientation(request):
    if request.method == 'POST': 
        orientacion = Orientacion.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (orientacion.status): 
            Orientacion.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Orientación Deshabilitada Correctamente')  
            notify_group('mantenimiento_sistema', f'Orientación deshabilitado: {orientacion.orientacion}', f'Orientación: {orientacion.orientacion}\nDeshabilitado por: {user_name}')
        else:
            Orientacion.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Orientación Habilitada Correctamente') 
            notify_group('mantenimiento_sistema', f'Orientación habilitado: {orientacion.orientacion}', f'Orientación: {orientacion.orientacion}\nHabilitado por: {user_name}')
        return redirect('manage_orientation')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_orientation') 

@login_required
@mantenedor_sistema_required
def edit_orientation(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Orientacion.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormOrientacion(initial={
            'orientacion': documento.orientacion,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_orientacion',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_orientation.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_orientation(request):     
    if request.method == 'POST':
        obj = Orientacion.objects.get(pk=request.POST['id'])
        old_obj = Orientacion.objects.get(pk=obj.pk)
        obj.orientacion = request.POST['orientacion']
        obj.save()
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Orientación actualizado: {obj.orientacion}', f'Orientación: {obj.orientacion}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_orientation')
    
@login_required
@mantenedor_sistema_required
def manage_tipoTerreno(request): 
    lista = list(TipoTerreno.objects.all().order_by('tipoTerreno'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_tipoTerreno',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_tipoTerreno.html', context)

@login_required
@mantenedor_sistema_required
def new_tipoTerreno(request):     
    context = {
        'formnuevo': FormTipoTerreno,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_tipoTerreno',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_tipoTerreno.html', context)

@login_required
@mantenedor_sistema_required
def save_new_tipoTerreno(request):
    if request.method == 'POST':
        try: 
            tipoTerreno = TipoTerreno.objects.get(tipoTerreno=request.POST['tipoTerreno'])
            return tipoTerreno
        except ObjectDoesNotExist:            
            formulario = FormTipoTerreno(data=request.POST)
            if formulario.is_valid():       
                documento = TipoTerreno(
                    tipoTerreno = request.POST['tipoTerreno'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Nuevo Tipo de terreno: {documento.tipoTerreno}', f'Tipo de terreno: {documento.tipoTerreno}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_tipoTerreno')

@login_required
@mantenedor_sistema_required
def status_tipoTerreno(request):
    if request.method == 'POST': 
        tipoTerreno = TipoTerreno.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (tipoTerreno.status): 
            TipoTerreno.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Tipo Terreno Deshabilitada Correctamente')  
            notify_group('mantenimiento_sistema', f'Tipo de terreno deshabilitado: {tipoTerreno.tipoTerreno}', f'Tipo de terreno: {tipoTerreno.tipoTerreno}\nDeshabilitado por: {user_name}')
        else:
            TipoTerreno.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Tipo Terreno Habilitada Correctamente') 
            notify_group('mantenimiento_sistema', f'Tipo de terreno habilitado: {tipoTerreno.tipoTerreno}', f'Tipo de terreno: {tipoTerreno.tipoTerreno}\nHabilitado por: {user_name}')
        return redirect('manage_tipoTerreno')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_tipoTerreno') 

@login_required
@mantenedor_sistema_required
def edit_tipoTerreno(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = TipoTerreno.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormTipoTerreno(initial={
            'tipoTerreno': documento.tipoTerreno,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_tipoTerreno',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_tipoTerreno.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_tipoTerreno(request):     
    if request.method == 'POST':
        obj = TipoTerreno.objects.get(pk=request.POST['id'])
        old_obj = TipoTerreno.objects.get(pk=obj.pk)
        obj.tipoTerreno = request.POST['tipoTerreno']
        obj.save()
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Tipo de terreno actualizado: {obj.tipoTerreno}', f'Tipo de terreno: {obj.tipoTerreno}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_tipoTerreno')

@login_required
@mantenedor_sistema_required
def manage_zapata(request): 
    lista = list(Zapata.objects.all().order_by('zapata')) 
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_zapata',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_zapata.html', context)

@login_required
@mantenedor_sistema_required
def new_zapata(request):     
    context = {
        'formnuevo': FormZapata,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_zapata',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_zapata.html', context)

@login_required
@mantenedor_sistema_required
def save_new_zapata(request):
    if request.method == 'POST':
        try: 
            zapata = Zapata.objects.get(zapata=request.POST['zapata'])
            return zapata
        except ObjectDoesNotExist:            
            formulario = FormZapata(data=request.POST)
            if formulario.is_valid():       
                documento = Zapata(
                    zapata = request.POST['zapata'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.first_name + " " + request.user.last_name
                notify_group('mantenimiento_sistema', request, f'Se ha creado una nueva Zapata: {documento.zapata}', user_name, 'Zapata', documento.id)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_zapata')

@login_required
@mantenedor_sistema_required
def status_zapata(request):
    if request.method == 'POST': 
        user_name = request.user.first_name + " " + request.user.last_name
        zapata = Zapata.objects.get(id=request.POST['id'])
        if (zapata.status): 
            Zapata.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Zapata Deshabilitada Correctamente')
            notify_group('mantenimiento_sistema', request, f'Se ha deshabilitado la Zapata: {zapata.zapata}', user_name, 'Zapata', zapata.id)
        else:
            Zapata.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Zapata Habilitada Correctamente')
            notify_group('mantenimiento_sistema', request, f'Se ha habilitado la Zapata: {zapata.zapata}', user_name, 'Zapata', zapata.id)
        return redirect('manage_zapata')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_zapata') 

@login_required
@mantenedor_sistema_required
def edit_zapata(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Zapata.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormZapata(initial={
            'zapata': documento.zapata,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_zapata',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_zapata.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_zapata(request):     
    if request.method == 'POST':
        old_obj = Zapata.objects.get(pk=request.POST['id'])
        Zapata.objects.filter(id=request.POST['id']).update(zapata=request.POST['zapata'])
        obj = Zapata.objects.get(pk=request.POST['id'])
        user_name = request.user.first_name + " " + request.user.last_name
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', request, f'Se ha editado la Zapata: {obj.zapata}\n{changes}', user_name, 'Zapata', obj.id)
        return JsonResponse({'success': True})
    else:
        return redirect('edit_zapata')
    
@login_required
@mantenedor_sistema_required
def manage_perforista(request): 
    lista = list(Perforistas.objects.all().order_by('perforista'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_perforista',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_perforista.html', context)

@login_required
@mantenedor_sistema_required
def new_perforista(request):   
    context = {
        'formnuevo': FormPerforista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_perforista',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_perforista.html', context)

@login_required
@mantenedor_sistema_required
def save_new_perforista(request):
    if request.method == 'POST':
        try: 
            perforista = Perforistas.objects.get(perforista=request.POST['perforista'])
            return perforista
        except ObjectDoesNotExist:            
            formulario = FormPerforista(data=request.POST)
            if formulario.is_valid():       
                documento = Perforistas(
                    perforista = request.POST['perforista'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.first_name + " " + request.user.last_name
                notify_group('mantenimiento_sistema', request, f'Se ha creado un nuevo Perforista: {documento.perforista}', user_name, 'Perforista', documento.id)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_perforista')

@login_required
@mantenedor_sistema_required
def status_perforista(request):
    if request.method == 'POST': 
        user_name = request.user.first_name + " " + request.user.last_name
        perforista = Perforistas.objects.get(id=request.POST['id'])
        if (perforista.status): 
            Perforistas.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Perforista Deshabilitado Correctamente')
            notify_group('mantenimiento_sistema', request, f'Se ha deshabilitado el Perforista: {perforista.perforista}', user_name, 'Perforista', perforista.id)
        else:
            Perforistas.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Perforista Habilitado Correctamente')
            notify_group('mantenimiento_sistema', request, f'Se ha habilitado el Perforista: {perforista.perforista}', user_name, 'Perforista', perforista.id)
        return redirect('manage_perforista')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_perforista') 

@login_required
@mantenedor_sistema_required
def edit_perforista(request):  
    try:
        request.session['edit_id'] = request.POST['id']   
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Perforistas.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormPerforista(initial={
            'perforista': documento.perforista,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_perforista',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_perforista.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_perforista(request):     
    if request.method == 'POST':
        old_obj = Perforistas.objects.get(pk=request.POST['id'])
        Perforistas.objects.filter(id=request.POST['id']).update(perforista=request.POST['perforista'])
        obj = Perforistas.objects.get(pk=request.POST['id'])
        user_name = request.user.first_name + " " + request.user.last_name
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', request, f'Se ha editado el Perforista: {obj.perforista}\n{changes}', user_name, 'Perforista', obj.id)
        return JsonResponse({'success': True})
    else:
        return redirect('edit_perforista')
    
@login_required
@mantenedor_sistema_required
def manage_recomendaciones(request):
    lista = Recomendacion.objects.all().order_by('-fecha_inicio')
    
    for recomendacion in lista:
        recomendacion.este = str(recomendacion.este).rstrip('0').rstrip('.') if recomendacion.este else None
        recomendacion.norte = str(recomendacion.norte).rstrip('0').rstrip('.') if recomendacion.norte else None
        recomendacion.cota = str(recomendacion.cota).rstrip('0').rstrip('.') if recomendacion.cota else None
        recomendacion.largo_real = int(recomendacion.largo_real) if recomendacion.largo_real == 0 else recomendacion.largo_real
    
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_recomendacion',
        'sidebarmain': 'manage_system', 
    }
    return render(request, 'pages/maintainer/drilling/manage_recomendacion.html', context)

@login_required
@mantenedor_sistema_required
def new_recomendacion(request):     
    context = {
        'formnuevo': FormRecomendaciones,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_recomendacion',
        'sidebarmain': 'manage_system',
    }
    return render(request,'pages/maintainer/drilling/new_recomendacion.html', context)

from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Sum
from django.db import DataError, IntegrityError
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
import re

@login_required
@mantenedor_sistema_required
def save_new_recomendacion(request):
    """
    Crea recomendación (AJAX).
    - Valida formulario
    - Valida azimut 0..360
    - Valida metros disponibles del programa
    - Regla SONDA: si estado 2/3 y sonda ocupada -> crea ABORTADO (1) y devuelve error
    - Traduce errores de Form y BD (MySQL 1264 Out of range) a español
    - Devuelve errors={campo:[...]} para que el frontend los muestre
    """
    if request.method != 'POST':
        messages.error(request, 'Error en la Acción')
        return redirect('manage_recomendacion')

    # ---- Traducción simple de mensajes típicos de Django forms (EN -> ES) ----
    def traducir_error_form(msg: str) -> str:
        s = str(msg)

        # "Ensure that there are no more than 10 digits in total."
        m = re.search(r"Ensure that there are no more than (\d+) digits", s)
        if m:
            return f"Este valor es demasiado grande. Máximo {m.group(1)} dígitos."

        # "Ensure that there are no more than 3 decimal places."
        m = re.search(r"Ensure that there are no more than (\d+) decimal places", s)
        if m:
            return f"Demasiados decimales. Máximo {m.group(1)} decimales."

        if "Enter a number" in s:
            return "Ingresa un número válido."

        if "This field is required" in s:
            return "Este campo es obligatorio."

        if "Select a valid choice" in s:
            return "Selecciona una opción válida."

        if "Enter a whole number" in s:
            return "Ingresa un número entero válido."

        if "Enter a valid date" in s:
            return "Ingresa una fecha válida."

        # fallback: devolvemos el mensaje tal cual si no calza
        return s

    def json_form_errors(form):
        out = {}
        for field, errs in form.errors.items():
            out[field] = [traducir_error_form(e) for e in errs]
        return out

    def parse_mysql_out_of_range_field(msg: str):
        """
        Extrae el nombre de columna desde:
        "Out of range value for column 'este' at row 1"
        """
        campo = None
        if "Out of range value for column" in msg:
            try:
                campo = msg.split("Out of range value for column")[1].split("'")[1]
            except Exception:
                campo = None
        return campo

    try:
        # 1) Formulario
        formulario = FormRecomendaciones(data=request.POST)
        if not formulario.is_valid():
            errs = json_form_errors(formulario)

            # mensaje principal más útil (primer error encontrado)
            primer_campo = next(iter(errs.keys()), None)
            primer_error = errs.get(primer_campo, ["Corrige el formulario."])[0] if primer_campo else "Corrige el formulario."

            return JsonResponse({
                'success': False,
                'message': primer_error,
                'errors': errs
            })

        # 2) Validación nombre duplicado
        nombre = (request.POST.get('recomendacion') or '').strip()
        if Recomendacion.objects.filter(recomendacion=nombre).exists():
            return JsonResponse({
                'success': False,
                'message': 'Ya existe una recomendación con ese nombre.',
                'errors': {'recomendacion': ['Ya existe una recomendación con ese nombre.']}
            })

        # 3) Obtener FK
        campana = Campana.objects.get(id=request.POST.get('campana'))
        programa = Programa.objects.get(id=request.POST.get('programa'))

        # 4) Fecha
        fecha_inicio_raw = (request.POST.get('fecha_inicio') or '').strip()
        fecha_inicio_aware = None
        if fecha_inicio_raw:
            try:
                fecha_inicio_aware = make_aware(datetime.strptime(fecha_inicio_raw, '%Y-%m-%d'))
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Formato de fecha inválido (usa YYYY-MM-DD).',
                    'errors': {'fecha_inicio': ['Formato inválido (usa YYYY-MM-DD).']}
                })

        # 5) Sonda
        sonda_id = request.POST.get('sonda')
        try:
            sonda = Sondas.objects.get(id=sonda_id)
        except Sondas.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'La sonda seleccionada no existe.',
                'errors': {'sonda': ['La sonda seleccionada no existe.']}
            })

        # 6) Azimut
        azimut_raw = (request.POST.get('azimut') or '').strip()
        azimut = int(azimut_raw) if azimut_raw != '' else None
        if azimut is not None and (azimut < 0 or azimut > 360):
            return JsonResponse({
                'success': False,
                'message': 'El azimut debe estar entre 0 y 360.',
                'errors': {'azimut': ['El azimut debe estar entre 0 y 360.']}
            })

        # 7) Conversión numéricos
        def ffloat(key, default=None):
            v = (request.POST.get(key) or '').strip()
            if v == '':
                return default
            return float(v.replace(',', '.'))

        inclinacion = ffloat('inclinacion', None)
        largo_programado_solicitado = ffloat('largo_programado', 0.0)
        este = ffloat('este', None)
        norte = ffloat('norte', None)
        cota = ffloat('cota', None)
        manteo = ffloat('manteo', None)

        # 8) Validación metros disponibles por programa
        metros_usados = Recomendacion.objects.filter(
            programa=programa,
            status=True
        ).aggregate(total=Sum('largo_programado'))['total'] or 0

        metros_disponibles = float(programa.metros) - float(metros_usados)

        if float(largo_programado_solicitado) > float(metros_disponibles):
            return JsonResponse({
                'success': False,
                'message': f'El largo programado excede el disponible del programa.\nDisponibles: {metros_disponibles:.2f} mts.',
                'errors': {'largo_programado': [f'Excede disponibles ({metros_disponibles:.2f} mts).']}
            })

        # 9) Regla SONDA ocupada
        estado_solicitado = str(request.POST.get('estado') or '').strip()
        ESTADOS_OCUPAN = ('2', '3')
        ESTADO_ABORTADO = '1'

        def crear_recomendacion(estado_final: str):
            obj = Recomendacion.objects.create(
                campana=campana,
                programa=programa,
                recomendacion=nombre,
                pozo=request.POST.get('pozo'),
                sonda=sonda,
                fecha_inicio=fecha_inicio_aware,
                sector=request.POST.get('sector'),
                azimut=azimut,
                inclinacion=inclinacion,
                largo_programado=largo_programado_solicitado,
                largo_real=0,
                este=este,
                norte=norte,
                cota=cota,
                manteo=manteo,
                estado=estado_final,
                status=True,
                creador=f"{request.user.first_name} {request.user.last_name}".strip(),
                fechaUpdateEstado=timezone.now(),
            )
            user_name = f"{request.user.first_name} {request.user.last_name}".strip()
            notify_group('mantenimiento_sistema', request, f'Se ha creado una nueva Recomendación: {obj.recomendacion}', user_name, 'Recomendación', obj.id)
            return obj

        if estado_solicitado in ESTADOS_OCUPAN:
            ocupada = Recomendacion.objects.filter(
                status=True,
                sonda_id=sonda.id,
                estado__in=ESTADOS_OCUPAN
            ).exists()

            if ocupada:
                crear_recomendacion(ESTADO_ABORTADO)
                return JsonResponse({
                    'success': False,
                    'message': 'La sonda ya se está ocupando (En Avance / En Espera). Se creó automáticamente como ABORTADO.',
                    'estado_aplicado': ESTADO_ABORTADO,
                    'errors': {'sonda': ['Sonda ocupada en otra recomendación (En Avance / En Espera).']}
                })

        # 10) Crear normal
        crear_recomendacion(estado_solicitado)
        return JsonResponse({'success': True, 'message': 'Recomendación creada con éxito.'})

    except Campana.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'La campaña seleccionada no existe.', 'errors': {'campana': ['No existe.']}})

    except Programa.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El programa seleccionado no existe.', 'errors': {'programa': ['No existe.']}})

    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'Ingresa valores numéricos válidos (Este, Norte, Cota, Largo, etc.).',
            'errors': {'__all__': ['Formato numérico inválido.']}
        })

    except IntegrityError:
        return JsonResponse({
            'success': False,
            'message': 'No se pudo guardar por un conflicto de datos (posible duplicado).',
            'errors': {'__all__': ['Conflicto de integridad.']}
        })

    # ✅ MySQL out of range
    except DataError as e:
        msg = str(e)

        if "Out of range value for column" in msg:
            campo = parse_mysql_out_of_range_field(msg)
            nombres = {
                "este": "Este",
                "norte": "Norte",
                "cota": "Cota",
                "azimut": "Azimut",
                "inclinacion": "Inclinación",
                "largo_programado": "Largo Programado",
                "largo_real": "Largo Real",
                "manteo": "Manteo",
            }
            campo_es = nombres.get(campo, campo or "un campo numérico")
            key_error = campo if campo else "__all__"

            return JsonResponse({
                'success': False,
                'message': f"El valor ingresado en '{campo_es}' es demasiado grande.\nReduce el número e inténtalo nuevamente.",
                'errors': {key_error: [f"El valor es demasiado grande para '{campo_es}'."]}
            })

        return JsonResponse({
            'success': False,
            'message': 'Error de datos en la base de datos. Revisa los valores ingresados.',
            'errors': {'__all__': ['Error de datos.']}
        })

    except Exception:
        return JsonResponse({
            'success': False,
            'message': 'Ocurrió un error inesperado al crear la recomendación.',
            'errors': {'__all__': ['Error inesperado.']}
        })


@login_required
@mantenedor_sistema_required
def status_recomendacion(request):
    if request.method == 'POST': 
        user_name = request.user.first_name + " " + request.user.last_name
        recomendacion = Recomendacion.objects.get(id=request.POST['id'])
        if (recomendacion.status): 
            Recomendacion.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Recomendación Terminada Correctamente')
            notify_group('mantenimiento_sistema', request, f'Se ha terminado la Recomendación: {recomendacion.recomendacion}', user_name, 'Recomendación', recomendacion.id)
        else:
            Recomendacion.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Recomendación Activa Correctamente')
            notify_group('mantenimiento_sistema', request, f'Se ha activado la Recomendación: {recomendacion.recomendacion}', user_name, 'Recomendación', recomendacion.id)
        return redirect('manage_recomendacion')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_recomendacion')

@login_required
@mantenedor_sistema_required
def edit_recomendacion(request):  
    # Obtener o mantener el ID de la recomendación a editar
    if request.method == "POST":
        try:
            request.session['edit_id'] = request.POST['id']
        except MultiValueDictKeyError:
            if 'edit_id' not in request.session:
                return render(request, 'pages/maintainer/drilling/edit_recomendacion.html', {'error': 'No se encontró un ID válido.'})

    documento = Recomendacion.objects.get(id=request.session['edit_id'])
    try:
        recomendacionAjuste = RecomendacionAjuste.objects.get(recomendacionAjuste=documento)
        azimut_ajuste = recomendacionAjuste.azimutAjuste
        este_ajuste = recomendacionAjuste.esteAjuste
        norte_ajuste = recomendacionAjuste.norteAjuste
        cota_ajuste = recomendacionAjuste.cotaAjuste
        manteo_ajuste = recomendacionAjuste.manteoAjuste
    except RecomendacionAjuste.DoesNotExist:
        recomendacionAjuste = None
        azimut_ajuste = None
        este_ajuste = None
        norte_ajuste = None
        cota_ajuste = None
        manteo_ajuste = None
    try:
        recomendacionFinal = RecomendacionFinal.objects.get(recomendacionFinal=documento)
        este_final = recomendacionFinal.esteFinal
        norte_final = recomendacionFinal.norteFinal
        cota_final = recomendacionFinal.cotaFinal
        fecha_final = formatear_fecha(recomendacionFinal.fechaFinal)
    except RecomendacionFinal.DoesNotExist:
        recomendacionFinal = None
        este_final = None
        norte_final = None
        cota_final = None
        fecha_final = None

    # Manejo de la fecha de inicio
    if documento.fecha_inicio:
        fecha_inicio_formateada = make_aware(documento.fecha_inicio) if documento.fecha_inicio.tzinfo is None else documento.fecha_inicio
        fecha_inicio_str = fecha_inicio_formateada.strftime('%Y-%m-%d')
    else:
        fecha_inicio_str = ""

    # Formateo de los valores opcionales (evita errores si están en `None`)
    este_formateado = str(documento.este).rstrip('0').rstrip('.') if documento.este is not None else ""
    norte_formateado = str(documento.norte).rstrip('0').rstrip('.') if documento.norte is not None else ""
    cota_formateada = str(documento.cota).rstrip('0').rstrip('.') if documento.cota is not None else ""

    # Contexto con los datos formateados
    context = {
        'formeditar': FormRecomendaciones(instance=documento,initial={
            'campana': documento.campana,
            'programa': documento.programa,
            'recomendacion': documento.recomendacion,
            'pozo': documento.pozo,
            'sonda': documento.sonda,
            'fecha_inicio': fecha_inicio_str,
            'sector': documento.sector,
            'azimut': documento.azimut if documento.azimut is not None else "",
            'inclinacion': documento.inclinacion,
            'largo_programado': documento.largo_programado if documento.largo_programado is not None else "",
            'largo_real': 0,  # Siempre se mantiene como 0
            'este': este_formateado,
            'norte': norte_formateado,
            'cota': cota_formateada,
            'manteo': documento.manteo,
            'estado': documento.estado,
            },
            campana_disabled = True,
            programa_disabled = True,
        ),
        'formeditarajuste': FormRecomendacionesAjuste(initial={
            'azimutAjuste': azimut_ajuste,
            'esteAjuste': este_ajuste,
            'norteAjuste': norte_ajuste,
            'cotaAjuste': cota_ajuste,
            'manteoAjuste': manteo_ajuste,
            },
        ),
        'formeditarfinal': FormRecomendacionesFinal(initial={
            'esteFinal': este_final,
            'norteFinal': norte_final,
            'cotaFinal': cota_final,
            'fechaFinal': fecha_final,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_recomendacion',
        'sidebarmain': 'manage_system',
    }
    return render(request, 'pages/maintainer/drilling/edit_recomendacion.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_recomendacion(request):
    """
    Edita recomendación (AJAX).
    - Valida fecha
    - Valida azimut 0..360
    - Valida sonda existe
    - Regla SONDA: si intentan estado 2/3 y sonda ocupada en otra recomendación -> fuerza ABORTADO (1) y devuelve error
    - Traduce errores de BD (ej: MySQL 1264 Out of range) a mensajes en español
    """
    if request.method != 'POST':
        return redirect('edit_recomendacion')

    try:
        recomendacion_id = request.POST.get('id')
        if not recomendacion_id:
            return JsonResponse({'success': False, 'message': 'ID no recibido.'})

        recomendacion = Recomendacion.objects.get(id=recomendacion_id)
        old_obj = Recomendacion.objects.get(id=recomendacion_id)

        # =========================
        # Fecha
        # =========================
        fecha_inicio_raw = (request.POST.get('fecha_inicio') or '').strip()
        fecha_inicio_aware = None
        if fecha_inicio_raw:
            try:
                fecha_inicio_aware = make_aware(datetime.strptime(fecha_inicio_raw, '%Y-%m-%d'))
            except ValueError:
                return JsonResponse({
                    'success': False,
                    'message': 'Formato de fecha inválido.',
                    'errors': {'fecha_inicio': ['Formato inválido (usa YYYY-MM-DD).']}
                })

        # =========================
        # Numéricos
        # =========================
        azimut_raw = (request.POST.get('azimut') or '').strip()
        azimut = int(azimut_raw) if azimut_raw != '' else None
        if azimut is not None and (azimut < 0 or azimut > 360):
            return JsonResponse({
                'success': False,
                'message': 'El azimut debe estar entre 0 y 360.',
                'errors': {'azimut': ['El azimut debe estar entre 0 y 360.']}
            })

        def ffloat(key, default=None):
            v = (request.POST.get(key) or '').strip()
            if v == '':
                return default
            # soporta coma decimal
            return float(v.replace(',', '.'))

        inclinacion = ffloat('inclinacion', None)
        largo_programado = ffloat('largo_programado', None)
        largo_real = ffloat('largo_real', 0)
        este = ffloat('este', None)
        norte = ffloat('norte', None)
        cota = ffloat('cota', None)
        manteo = ffloat('manteo', None)

        # =========================
        # Sonda
        # =========================
        sonda_id = request.POST.get('sonda')
        try:
            sonda = Sondas.objects.get(id=sonda_id)
        except Sondas.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'La sonda seleccionada no existe.',
                'errors': {'sonda': ['La sonda seleccionada no existe.']}
            })

        # =========================
        # Regla sonda ocupada
        # =========================
        estado_solicitado = str(request.POST.get('estado') or '').strip()
        ESTADOS_OCUPAN = ('2', '3')   # En Avance / En Espera
        ESTADO_ABORTADO = '1'

        def actualizar_recomendacion(estado_final: str):
            Recomendacion.objects.filter(id=recomendacion.id).update(
                recomendacion=request.POST.get('recomendacion'),
                pozo=request.POST.get('pozo'),
                sonda=sonda,
                fecha_inicio=fecha_inicio_aware,
                sector=request.POST.get('sector'),
                azimut=azimut,
                inclinacion=inclinacion,
                largo_programado=largo_programado,
                largo_real=largo_real,
                este=este,
                norte=norte,
                cota=cota,
                manteo=manteo,
                estado=estado_final,
                fechaUpdateEstado=timezone.now(),
            )
            obj = Recomendacion.objects.get(id=recomendacion.id)
            user_name = f"{request.user.first_name} {request.user.last_name}".strip()
            changes = get_changes_message(old_obj, obj)
            if changes:
                notify_group('mantenimiento_sistema', request, f'Se ha editado la Recomendación: {obj.recomendacion}\n{changes}', user_name, 'Recomendación', obj.id)

        if estado_solicitado in ESTADOS_OCUPAN:
            ocupada = Recomendacion.objects.filter(
                status=True,
                sonda_id=sonda.id,
                estado__in=ESTADOS_OCUPAN
            ).exclude(id=recomendacion.id).exists()

            if ocupada:
                actualizar_recomendacion(ESTADO_ABORTADO)
                return JsonResponse({
                    'success': False,
                    'message': 'La sonda ya se está ocupando (En Avance / En Espera).\nSe cambió automáticamente a ABORTADO.',
                    'estado_aplicado': ESTADO_ABORTADO,
                    'errors': {'sonda': ['Sonda ocupada en otra recomendación (En Avance / En Espera).']}
                })

        # =========================
        # Update normal
        # =========================
        actualizar_recomendacion(estado_solicitado)

        return JsonResponse({'success': True, 'message': 'Recomendación actualizada con éxito.'})

    except Recomendacion.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'La recomendación no existe.'})

    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'Error en la conversión de datos numéricos. Revisa los campos (Este, Norte, Cota, Largo, etc.).'
        })

    # ✅ Traducción de error MySQL tipo "Out of range value for column 'este' at row 1"
    except DataError as e:
        msg = str(e)

        if "1264" in msg and "Out of range value for column" in msg:
            campo = None
            try:
                # extrae lo que viene entre comillas simples
                campo = msg.split("Out of range value for column")[1].split("'")[1]
            except Exception:
                campo = None

            nombres = {
                "este": "Este",
                "norte": "Norte",
                "cota": "Cota",
                "azimut": "Azimut",
                "inclinacion": "Inclinación",
                "largo_programado": "Largo Programado",
                "largo_real": "Largo Real",
                "manteo": "Manteo",
            }

            campo_es = nombres.get(campo, campo or "un campo numérico")

            return JsonResponse({
                'success': False,
                'message': f"El valor ingresado en '{campo_es}' es demasiado grande para el formato permitido. Reduce el número e inténtalo nuevamente.",
                'errors': {campo or 'valor': [f"El valor es demasiado grande para '{campo_es}'."]}
            })

        # Otros DataError
        return JsonResponse({
            'success': False,
            'message': 'Error de datos: revisa los campos numéricos (valores demasiado grandes o formato inválido).'
        })

    except Exception as e:
        # fallback: no mostrar inglés crudo si no quieres
        return JsonResponse({
            'success': False,
            'message': 'Ocurrió un error inesperado al guardar. Revisa los datos ingresados e inténtalo nuevamente.'
        })

    
@login_required
@mantenedor_sistema_required
def save_edit_recomendacion_ajuste(request):
    if request.method == 'POST':
        recomendacion_id = request.POST.get('id')
        recomendacion = Recomendacion.objects.get(id=recomendacion_id)
        RecomendacionAjuste.objects.update_or_create(
            recomendacionAjuste=recomendacion,
            defaults={
                'azimutAjuste': request.POST.get('azimutAjuste'),
                'esteAjuste': request.POST.get('esteAjuste'),
                'norteAjuste': request.POST.get('norteAjuste'),
                'cotaAjuste': request.POST.get('cotaAjuste'),
                'manteoAjuste': request.POST.get('manteoAjuste'),
                'statusAjuste': True,
            }
        )
        user_name = request.user.first_name + " " + request.user.last_name
        notify_group('mantenimiento_sistema', request, f'Se ha actualizado el ajuste de la Recomendación: {recomendacion.recomendacion}', user_name, 'Recomendación', recomendacion.id)
        return JsonResponse({'success': True, 'message': 'Recomendación actualizada con éxito.'})
    else:
        return redirect('edit_recomendacion')

@login_required
@mantenedor_sistema_required
def save_edit_recomendacion_final(request):
    if request.method == 'POST':
        recomendacion_id = request.POST.get('id')
        recomendacion = Recomendacion.objects.get(id=recomendacion_id)
        RecomendacionFinal.objects.update_or_create(
            recomendacionFinal=recomendacion,
            defaults={
                'esteFinal': request.POST.get('esteFinal'),
                'norteFinal': request.POST.get('norteFinal'),
                'cotaFinal': request.POST.get('cotaFinal'),
                'fechaFinal': request.POST.get('fechaFinal'),
                'statusFinal': True,
            }
        )
        user_name = request.user.first_name + " " + request.user.last_name
        notify_group('mantenimiento_sistema', request, f'Se ha actualizado el dato final de la Recomendación: {recomendacion.recomendacion}', user_name, 'Recomendación', recomendacion.id)
        return JsonResponse({'success': True, 'message': 'Recomendación actualizada con éxito.'})
    else:
        return redirect('edit_recomendacion')
    
@login_required
@mantenedor_sistema_required
def update_estado_recomendacion(request):
    """
    Cambia el estado desde la tabla (dropdown).
    Regla: una misma SONDA no puede tener 2 recomendaciones activas (status=True)
    en estado En Avance (2) o En Espera (3).
    Si intentan poner 2/3 y está ocupada: se fuerza a Abortado (1) y se devuelve error.
    """
    try:
        recomendacion_id = request.POST.get('id')
        nuevo_estado = str(request.POST.get('estado') or '').strip()

        if not recomendacion_id or not nuevo_estado:
            return JsonResponse({'success': False, 'message': 'Datos incompletos.'})

        recomendacion = Recomendacion.objects.get(id=recomendacion_id)

        ESTADOS_OCUPAN = ('2', '3')  # En Avance / En Espera
        ESTADO_ABORTADO = '1'

        # Si quieren ocupar (2/3) validamos ocupación por SONDA
        if nuevo_estado in ESTADOS_OCUPAN and recomendacion.sonda_id:
            ocupada = Recomendacion.objects.filter(
                status=True,
                sonda_id=recomendacion.sonda_id,
                estado__in=ESTADOS_OCUPAN
            ).exclude(id=recomendacion.id).exists()

            if ocupada:
                recomendacion.estado = ESTADO_ABORTADO
                recomendacion.fechaUpdateEstado = datetime.now()
                recomendacion.save(update_fields=['estado', 'fechaUpdateEstado'])
                user_name = request.user.first_name + " " + request.user.last_name
                notify_group('mantenimiento_sistema', request, f'Se ha forzado el estado ABORTADO de la Recomendación: {recomendacion.recomendacion}', user_name, 'Recomendación', recomendacion.id)
                return JsonResponse({
                    'success': False,
                    'message': 'La sonda ya se está ocupando en otra recomendación (En Avance / En Espera).\nSe cambió automáticamente a ABORTADO.',
                    'estado_aplicado': ESTADO_ABORTADO
                })

        # Aplicar cambio normal
        recomendacion.estado = nuevo_estado
        recomendacion.fechaUpdateEstado = datetime.now()
        recomendacion.save(update_fields=['estado', 'fechaUpdateEstado'])
        user_name = request.user.first_name + " " + request.user.last_name
        notify_group('mantenimiento_sistema', request, f'Se ha actualizado el estado de la Recomendación: {recomendacion.recomendacion}', user_name, 'Recomendación', recomendacion.id)
        return JsonResponse({'success': True, 'message': 'Estado actualizado correctamente.'})

    except Recomendacion.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Recomendación no encontrada.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error inesperado: {str(e)}'})

    
@login_required
@mantenedor_sistema_required
def manage_materiales_sonda(request): 
    lista = list(MaterialesSonda.objects.all().order_by('material'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_materiales',
        'sidebarsubmenu': 'manage_materiales_sonda',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/checklist/manage_materiales_sonda.html', context)

@login_required
@mantenedor_sistema_required
def new_materiales_sonda(request):     
    context = {
        'formnuevo': FormMaterialesSonda,
        'sidebarmenu': 'manage_materiales',
        'sidebarsubmenu': 'manage_materiales_sonda',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/checklist/new_materiales_sonda.html', context)

@login_required
@mantenedor_sistema_required
def save_new_materiales_sonda(request):
    if request.method != 'POST':
        messages.error(request, 'Error en la Acción')
        return redirect('manage_materiales_sonda')

    nombre_material = request.POST.get('material', '').strip()

    if not nombre_material:
        return JsonResponse({
            'success': False,
            'message': 'Debe ingresar un material.'
        }, status=400)

    if MaterialesSonda.objects.filter(material__iexact=nombre_material).exists():
        return JsonResponse({
            'success': False,
            'message': 'Este material ya existe en Materiales Sonda.'
        }, status=400)

    formulario = FormMaterialesSonda(data=request.POST)

    if not formulario.is_valid():
        return JsonResponse({
            'success': False,
            'message': 'El formulario no es válido.'
        }, status=400)

    creador = request.user.first_name + " " + request.user.last_name

    MaterialesSonda.objects.create(
        material=nombre_material,
        status=True,
        creador=creador,
    )

    MaterialesCaseta.objects.get_or_create(
        material=nombre_material,
        defaults={
            'status': True,
            'creador': creador,
        }
    )

    user_name = request.user.get_full_name() or request.user.username
    notify_group('mantenimiento_sistema', f'Material de sonda creado: {nombre_material}', f'Material de sonda: {nombre_material}\nCreado por: {user_name}')

    return JsonResponse({'success': True})

@login_required
@mantenedor_sistema_required
def status_materiales_sonda(request):
    if request.method != 'POST':
        messages.error(request, 'Error en la Acción')
        return redirect('manage_materiales_sonda')

    materiales = MaterialesSonda.objects.get(id=request.POST['id'])
    user_name = request.user.get_full_name() or request.user.username

    nuevo_estado = not materiales.status

    MaterialesSonda.objects.filter(id=materiales.id).update(
        status=nuevo_estado
    )

    MaterialesCaseta.objects.filter(
        material__iexact=str(materiales.material).strip()
    ).update(
        status=nuevo_estado
    )

    if nuevo_estado:
        messages.success(request, 'Material Habilitado Correctamente')
        notify_group('mantenimiento_sistema', f'Material de sonda habilitado: {materiales.material}', f'Material de sonda: {materiales.material}\nHabilitado por: {user_name}')
    else:
        messages.success(request, 'Material Deshabilitado Correctamente')
        notify_group('mantenimiento_sistema', f'Material de sonda deshabilitado: {materiales.material}', f'Material de sonda: {materiales.material}\nDeshabilitado por: {user_name}')

    return redirect('manage_materiales_sonda')

@login_required
@mantenedor_sistema_required
def edit_materiales_sonda(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = MaterialesSonda.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormMaterialesSonda(initial={
            'material': documento.material,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_materiales',
        'sidebarsubmenu': 'manage_materiales_sonda',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/checklist/edit_materiales_sonda.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_materiales_sonda(request):     
    if request.method == 'POST':
        old_obj = MaterialesSonda.objects.get(pk=request.POST['id'])
        MaterialesSonda.objects.filter(id=request.POST['id']).update(material=request.POST['material'])
        obj = MaterialesSonda.objects.get(pk=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Material de sonda actualizado: {obj.material}', f'Material de sonda: {obj.material}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_materiales_sonda')
    
@login_required
@mantenedor_sistema_required
def manage_materiales_caseta(request): 
    lista = list(MaterialesCaseta.objects.all().order_by('material'))  
    context = {
        'documentos': lista,
        'sidebarmenu': 'manage_materiales',
        'sidebarsubmenu': 'manage_materiales_caseta',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/checklist/manage_materiales_caseta.html', context)

@login_required
@mantenedor_sistema_required
def new_materiales_caseta(request):     
    context = {
        'formnuevo': FormMaterialesCaseta,
        'sidebarmenu': 'manage_materiales',
        'sidebarsubmenu': 'manage_materiales_caseta',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/checklist/new_materiales_caseta.html', context)

@login_required
@mantenedor_sistema_required
def save_new_materiales_caseta(request):
    if request.method != 'POST':
        messages.error(request, 'Error en la Acción')
        return redirect('manage_materiales_caseta')

    nombre_material = request.POST.get('material', '').strip()

    if not nombre_material:
        return JsonResponse({
            'success': False,
            'message': 'Debe ingresar un material.'
        }, status=400)

    if MaterialesCaseta.objects.filter(material__iexact=nombre_material).exists():
        return JsonResponse({
            'success': False,
            'message': 'Este material ya existe en Materiales Caseta.'
        }, status=400)

    formulario = FormMaterialesCaseta(data=request.POST)

    if not formulario.is_valid():
        return JsonResponse({
            'success': False,
            'message': 'El formulario no es válido.'
        }, status=400)

    creador = request.user.first_name + " " + request.user.last_name

    MaterialesCaseta.objects.create(
        material=nombre_material,
        status=True,
        creador=creador,
    )

    MaterialesSonda.objects.get_or_create(
        material=nombre_material,
        defaults={
            'status': True,
            'creador': creador,
        }
    )

    user_name = request.user.get_full_name() or request.user.username
    notify_group('mantenimiento_sistema', f'Material de caseta creado: {nombre_material}', f'Material de caseta: {nombre_material}\nCreado por: {user_name}')

    return JsonResponse({'success': True})

@login_required
@mantenedor_sistema_required
def status_materiales_caseta(request):
    if request.method != 'POST':
        messages.error(request, 'Error en la Acción')
        return redirect('manage_materiales_caseta')

    materiales = MaterialesCaseta.objects.get(id=request.POST['id'])
    user_name = request.user.get_full_name() or request.user.username

    nuevo_estado = not materiales.status

    MaterialesCaseta.objects.filter(id=materiales.id).update(
        status=nuevo_estado
    )

    MaterialesSonda.objects.filter(
        material__iexact=str(materiales.material).strip()
    ).update(
        status=nuevo_estado
    )

    if nuevo_estado:
        messages.success(request, 'Material Habilitado Correctamente')
        notify_group('mantenimiento_sistema', f'Material de caseta habilitado: {materiales.material}', f'Material de caseta: {materiales.material}\nHabilitado por: {user_name}')
    else:
        messages.success(request, 'Material Deshabilitado Correctamente')
        notify_group('mantenimiento_sistema', f'Material de caseta deshabilitado: {materiales.material}', f'Material de caseta: {materiales.material}\nDeshabilitado por: {user_name}')

    return redirect('manage_materiales_caseta')

@login_required
@mantenedor_sistema_required
def edit_materiales_caseta(request):
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = MaterialesCaseta.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormMaterialesCaseta(initial={
            'material': documento.material,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_materiales',
        'sidebarsubmenu': 'manage_materiales_caseta',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/checklist/edit_materiales_caseta.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_materiales_caseta(request):     
    if request.method == 'POST':
        old_obj = MaterialesCaseta.objects.get(pk=request.POST['id'])
        MaterialesCaseta.objects.filter(id=request.POST['id']).update(material=request.POST['material'])
        obj = MaterialesCaseta.objects.get(pk=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Material de caseta actualizado: {obj.material}', f'Material de caseta: {obj.material}\nActualizado por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_materiales_caseta')

@login_required
@mantenedor_sistema_required
def manage_campanas(request): 
    lista = list(Campana.objects.all().order_by('campana'))  
    context = {
        'campanas': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_campanas',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_campanas.html', context)

@login_required
@mantenedor_sistema_required
def new_campana(request):     
    context = {
        'formnuevo': FormCampana,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_campanas',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_campana.html', context)

@login_required
@mantenedor_sistema_required
def save_new_campana(request):
    if request.method == 'POST':
        faena = Faena.objects.get(id=request.POST['faena'])
        try: 
            campana = Campana.objects.get(campana=request.POST['campana'])
            return campana
        except ObjectDoesNotExist:            
            formulario = FormCampana(data=request.POST)
            if formulario.is_valid():       
                documento = Campana(
                    campana = request.POST['campana'],
                    faena = faena,
                    metros = request.POST['metros'],
                    anoInicial = request.POST['anoInicial'],
                    anoFinal = request.POST['anoFinal'],
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Campa\u00f1a creada: {documento.campana}', f'Campa\u00f1a: {documento.campana}\nCreada por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_campanas')

@login_required
@mantenedor_sistema_required
def status_campana(request):
    if request.method == 'POST': 
        campana = Campana.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (campana.status): 
            Campana.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Campaña Deshabilitada Correctamente')
            notify_group('mantenimiento_sistema', f'Campa\u00f1a deshabilitada: {campana.campana}', f'Campa\u00f1a: {campana.campana}\nDeshabilitada por: {user_name}')
        else:
            Campana.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Campaña Habilitada Correctamente')
            notify_group('mantenimiento_sistema', f'Campa\u00f1a habilitada: {campana.campana}', f'Campa\u00f1a: {campana.campana}\nHabilitada por: {user_name}')
        return redirect('manage_campanas')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_campanas') 

@login_required
@mantenedor_sistema_required
def edit_campana(request):
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Campana.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormCampana(initial={
            'campana': documento.campana,
            'faena': documento.faena,
            'anoInicial': documento.anoInicial,
            'anoFinal': documento.anoFinal,
            'metros': documento.metros,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_campanas',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_campana.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_campana(request):     
    if request.method == 'POST':
        old_obj = Campana.objects.get(pk=request.POST['id'])
        Campana.objects.filter(id=request.POST['id']).update(campana=request.POST['campana'])
        Campana.objects.filter(id=request.POST['id']).update(faena=request.POST['faena'])
        Campana.objects.filter(id=request.POST['id']).update(metros=request.POST['metros'])
        Campana.objects.filter(id=request.POST['id']).update(anoInicial=request.POST['anoInicial'])
        Campana.objects.filter(id=request.POST['id']).update(anoFinal=request.POST['anoFinal'])
        obj = Campana.objects.get(pk=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Campa\u00f1a actualizada: {obj.campana}', f'Campa\u00f1a: {obj.campana}\nActualizada por: {user_name}{changes}')
        return JsonResponse({'success': True})
    else:
        return redirect('edit_campana')
    
@login_required
@mantenedor_sistema_required
def manage_programas(request): 
    lista = list(Programa.objects.all().order_by('programa'))  
    context = {
        'programas': lista,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_programas',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/manage_programas.html', context)

@login_required
@mantenedor_sistema_required
def new_programa(request):     
    context = {
        'formnuevo': FormPrograma,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_programas',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/maintainer/drilling/new_programa.html', context)

@login_required
@mantenedor_sistema_required
def save_new_programa(request):
    if request.method == 'POST':
        try: 
            programa = Programa.objects.get(
                programa=request.POST['programa'], 
                campana_id=request.POST['campana']
            )
            
            return JsonResponse({'success': False, 'message': 'El nombre del programa ya existe en esta campaña.'})
        except ObjectDoesNotExist:      
            formulario = FormPrograma(data=request.POST)
            if formulario.is_valid():
                # 1. Obtener datos
                campana = Campana.objects.get(id=request.POST['campana'])
                metros_nuevos = int(request.POST['metros'])

                # 2. Calcular metros ya utilizados en esta campaña por otros programas activos
                metros_usados = Programa.objects.filter(
                    campana=campana, 
                    status=True
                ).aggregate(total=Sum('metros'))['total'] or 0

                # 3. Validar (AHORA CON 30% DE MARGEN EXTRA)
                
                # Calculamos el límite real (Los metros oficiales + 30%)
                limite_con_bono = campana.metros * 1.30  
                
                # Calculamos cuánto tendríamos en total si sumamos este nuevo programa
                total_proyectado = metros_usados + metros_nuevos

                # Si nos pasamos incluso del bono del 30%, lanzamos error
                if total_proyectado > limite_con_bono:
                    # Calculamos cuánto queda realmente para mostrarlo en el mensaje
                    disponible_real = limite_con_bono - metros_usados
                    
                    return JsonResponse({
                        'success': False, 
                        'message': f'Excede el límite (incluyendo el 30% extra).\nDisponibles: {int(disponible_real)} mts.'
                    })

                # 4. Guardar si pasa la validación
                documento = Programa(
                    campana = campana,
                    programa = request.POST['programa'],
                    metros = metros_nuevos,
                    status = True,
                    creador = request.user.first_name+" "+request.user.last_name,
                )
                documento.save()
                user_name = request.user.get_full_name() or request.user.username
                notify_group('mantenimiento_sistema', f'Programa creado: {documento.programa}', f'Programa: {documento.programa}\nCreado por: {user_name}')
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_programas')

@login_required
@mantenedor_sistema_required
def status_programa(request):
    if request.method == 'POST': 
        programa = Programa.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (programa.status): 
            Programa.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Programa Deshabilitado Correctamente')
            notify_group('mantenimiento_sistema', f'Programa deshabilitado: {programa.programa}', f'Programa: {programa.programa}\nDeshabilitado por: {user_name}')
        else:
            Programa.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Programa Habilitado Correctamente')
            notify_group('mantenimiento_sistema', f'Programa habilitado: {programa.programa}', f'Programa: {programa.programa}\nHabilitado por: {user_name}')
        return redirect('manage_programas')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_programas') 

@login_required
@mantenedor_sistema_required
def edit_programa(request):
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = Programa.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormPrograma(initial={
            'campana': documento.campana,
            'programa': documento.programa,
            'metros': documento.metros,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_drilling',
        'sidebarsubmenu': 'manage_programas',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/maintainer/drilling/edit_programa.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_programa(request):
    if request.method == 'POST':
        # 1) Obtener datos
        programa_id = request.POST.get('id')
        campana_id = request.POST.get('campana')
        nombre_programa = request.POST.get('programa', '').strip()

        # ✅ Ojo: metros puede venir vacío o con espacios
        try:
            metros_nuevos = int(str(request.POST.get('metros', '0')).strip())
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Error: El valor de "metros" no es válido.'
            })

        # 2) Campaña actual seleccionada en el edit
        campana = Campana.objects.get(id=campana_id)

        # 3) Calcular metros usados por OTROS programas activos de esta campaña (excluyendo el actual)
        metros_usados = (
            Programa.objects
            .filter(campana=campana, status=True)
            .exclude(id=programa_id)
            .aggregate(total=Sum('metros'))
            .get('total') or 0
        )

        # ✅ MISMA REGLA QUE CREAR: campaña permite 30% extra
        max_metros_permitidos = int(campana.metros * 1.3)

        # Disponibles considerando el 30% extra
        metros_disponibles = max_metros_permitidos - metros_usados

        # 4) Validación
        if metros_nuevos > metros_disponibles:
            return JsonResponse({
                'success': False,
                'message': (
                    f'Excede el límite (incluyendo el 30% extra).\n'
                    f'Disponibles: {metros_disponibles} mts.'
                )
            })

        # 5) Actualizar
        old_obj = Programa.objects.get(pk=programa_id)
        Programa.objects.filter(id=programa_id).update(
            campana=campana,
            programa=nombre_programa,
            metros=metros_nuevos
        )

        obj = Programa.objects.get(pk=programa_id)
        user_name = request.user.get_full_name() or request.user.username
        changes = get_changes_message(old_obj, obj)
        if changes:
            notify_group('mantenimiento_sistema', f'Programa actualizado: {obj.programa}', f'Programa: {obj.programa}\nActualizado por: {user_name}{changes}')

        return JsonResponse({'success': True})

    return redirect('edit_programa')

   

def error_400(request, exception):
    template = 'errors/400_logged_in.html' if request.user.is_authenticated else 'errors/400.html'
    return render(request, template, status=400)

def error_403(request, exception):
    template = 'errors/403_logged_in.html' if request.user.is_authenticated else 'errors/403.html'
    return render(request, template, status=403)

def error_404(request, exception):
    template = 'errors/404_logged_in.html' if request.user.is_authenticated else 'errors/404.html'
    return render(request, template, status=404)

def error_413(request, exception):
    template = 'errors/413_logged_in.html' if request.user.is_authenticated else 'errors/413.html'
    return render(request, template, status=413)

def error_500(request):
    template = 'errors/500_logged_in.html' if request.user.is_authenticated else 'errors/500.html'
    return render(request, template, status=500)

def cargar_programas_por_campana(request):
    campana_id = request.GET.get('campana_id')
    if campana_id:
        programas = Programa.objects.filter(campana_id=campana_id, status=True)
        data = [{'id': p.id, 'programa': p.programa} for p in programas]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def landing_page(request):
    return render(request, 'landing/home.html')

@login_required
@mantenedor_sistema_required
def manage_problems(request): 
    storage = messages.get_messages(request)
    storage.used = True
    problemas = list(ProblemaVehiculo.objects.all().order_by('id'))   
    context = {
        'problemas': problemas,
        'sidebarsubmenu': 'manage_problems',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request, 'pages/maintainer/manage_problems.html', context)

@login_required
@mantenedor_sistema_required
def new_problem(request):     
    context = {
        'formproblema': FormProblemaVehiculo(), 
        'sidebarsubmenu': 'manage_problems',
        'sidebarmenu': 'manage_vehicles',
        'sidebarmain': 'manage_system', 
    }
    return render(request, 'pages/maintainer/new_problem.html', context)

@login_required
@mantenedor_sistema_required
def save_new_problem(request):     
    if request.method == 'POST':
        formulario = FormProblemaVehiculo(data=request.POST)
        if formulario.is_valid():       
            problema = ProblemaVehiculo(
                problema = request.POST['problema'],
                status = True,
                creador = request.user.first_name+" "+request.user.last_name,
            )
            problema.save()
            user_name = request.user.get_full_name() or request.user.username
            notify_group('mantenimiento_sistema', f'Nuevo problema: {problema.problema}', f'Problema de vehículo: {problema.problema}\nCreado por: {user_name}')
            return JsonResponse({'success': True})
    else:
        return redirect('new_problem')

@login_required
@mantenedor_sistema_required
def status_problem(request):
    if request.method == 'POST': 
        problema = ProblemaVehiculo.objects.get(id=request.POST['id'])
        user_name = request.user.get_full_name() or request.user.username
        if (problema.status): 
            ProblemaVehiculo.objects.filter(id=request.POST['id']).update(status=False)
            notify_group('mantenimiento_sistema', f'Problema deshabilitado: {problema.problema}', f'Problema de vehículo: {problema.problema}\nDeshabilitado por: {user_name}')
            messages.success(request, 'Problema Deshabilitado Correctamente')  
        else:
            ProblemaVehiculo.objects.filter(id=request.POST['id']).update(status=True)
            notify_group('mantenimiento_sistema', f'Problema habilitado: {problema.problema}', f'Problema de vehículo: {problema.problema}\nHabilitado por: {user_name}')
            messages.success(request, 'Problema Habilitado Correctamente') 
        return redirect('manage_problems')

@login_required
@admin_or_base_datos_required
def dashboardAdministracion(request):
    request.session['seccion'] = 'administracion'
    context = {
        'seccion': 'administracion',
        'sidebar': 'dashboardAdministracion',
    }
    return render(request, 'main/homeadmin.html', context)