import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.http import JsonResponse
from django.core import serializers
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
from threading import Thread
from rut_chile import rut_chile
import datetime
# pyrefly: ignore [missing-import]
from .forms import (FormNuevoVehiculo, FormInformacionTecnica, FormInfraccionesVehiculo, FormNuevoKilometraje, FormNuevaFuelCards, FormMarcaSomnolencia,
                    FormModeloSomnolencia, FormAyudaTecnicaVehiculo)
# pyrefly: ignore [missing-import]
from .models import (Vehiculo, DocumentacionesVehiculo, InformacionTecnicaVehiculo, InfraccionesVehiculo, NuevoKilometraje, NuevaTarjetaCombustible,
                    MarcaSomnolencia, ModeloSomnolencia, AyudaTecnicaVehiculo, HistorialDocumentacionVehiculo)
from mining.models import VehiculoAsignado
from maintenance.models import NuevaSolicitudMantenimiento
from core.choices import progreso, tipocombustible, tipodocumento
from core.utils import procesar_fotografia, validar_campo_vacio, formatear_fecha, extension_archivo, check_and_convert_pdf
from core.models import Tipo, Ano, Marca, Modelo, Color, Faena, OcultarOpcionesVehiculo, ProblemaVehiculo, CategoriaFallaVehiculo, TipoFallaVehiculo
from user.models import Usuario, UsuarioProfile
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from messenger.views import notificacion_vehiculos_email, notificacion_mantenedor_email
from core.decorators import (
    mantenedor_sistema_required,
    vehicular_basico_required,
    vehicular_avanzado_required,
    vehicular_admin_db_required,
)
from django.utils import timezone
from datetime import datetime
from django.db.models import Q, F, Prefetch
from django.middleware.csrf import get_token
from django.urls import reverse
from django.db import transaction, IntegrityError
from django.http import HttpResponse


def _apply_vehicle_dashboard_filters(queryset, faena_nombre=None, tipo_nombre=None, usuario_profile=None):
    if faena_nombre:
        queryset = queryset.filter(faena__faena=faena_nombre)

    if tipo_nombre:
        queryset = queryset.filter(vehiculo__tipo__tipo=tipo_nombre)

    if usuario_profile and usuario_profile.faena.faena != "SIN ASIGNAR":
        queryset = queryset.filter(faena=usuario_profile.faena)

    return queryset


@login_required
@vehicular_admin_db_required
def new_vehicle(request): 
    context = {
        'formnuevovehiculo': FormNuevoVehiculo(
            ocultar_fechaAdquisicion=False,
            ocultar_fechaArriendoInicial=False,
            ocultar_fechaArriendoFinal=False,
            ocultar_tieneTag=False,
            ocultar_tarjetaCombustible=False,        
            ocultar_fechaVencimientoPermisoCirculacion=True,
            ocultar_fechaVencimientoRevisionTecnica=True,
            ocultar_fechaVencimientoSeguroObligatorio=True,
        ),   
        'sidebar': 'manage_vehicles',
        'sidebarmain': 'system_vehicles',
    }
    return render(request,'pages/vehicle/new_vehicle.html', context)

@login_required
@vehicular_avanzado_required
def manage_vehicles(request):
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    filtro_faena = request.GET.get('faena', '').strip()
    filtro_tipo = request.GET.get('tipo', '').strip()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        
        estado_param = request.GET.get('estado')
        es_habilitado = True if estado_param == 'true' else False
        
        order_column_index = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'desc')

        # 1. Base Queryset enfocada directamente en el modelo Vehiculo
        base_queryset = Vehiculo.objects.filter(status=es_habilitado).select_related(
            'tipo', 'marca', 'modelo'
        ).prefetch_related(
            Prefetch('vehiculoasignado_set', 
                     queryset=VehiculoAsignado.objects.filter(status=True).select_related('faena'), 
                     to_attr='asignaciones_activas')
        )

        # 2. Filtros integrados para soportar la nueva estructura
        if filtro_faena:
            base_queryset = base_queryset.filter(
                vehiculoasignado__faena__faena=filtro_faena,
                vehiculoasignado__status=True
            )

        if filtro_tipo:
            base_queryset = base_queryset.filter(tipo__tipo=filtro_tipo)

        if usuario.faena.faena != "SIN ASIGNAR":
            base_queryset = base_queryset.filter(
                vehiculoasignado__faena=usuario.faena,
                vehiculoasignado__status=True
            )

        # 3. Lógica del buscador general
        if search_value:
            base_queryset = base_queryset.filter(
                Q(placaPatente__icontains=search_value) |
                Q(tipo__tipo__icontains=search_value) |
                Q(marca__marca__icontains=search_value) |
                Q(modelo__modelo__icontains=search_value) |
                Q(vehiculoasignado__faena__faena__icontains=search_value, vehiculoasignado__status=True)
            ).distinct() # Evita duplicados por los joins

        # 4. Mapeo de columnas para el ordenamiento del Datatable
        if es_habilitado:
            column_mapping = {
                1: 'completado',
                2: 'placaPatente',
                3: 'tipo__tipo',
                4: 'marca__marca',
                5: 'modelo__modelo',
                6: 'vehiculoasignado__faena__faena',
                7: 'status'
            }
        else:
            column_mapping = {
                1: 'completado',
                2: 'placaPatente',
                3: 'tipo__tipo',
                4: 'marca__marca',
                5: 'modelo__modelo',
                6: 'status'
            }

        col_name = column_mapping.get(order_column_index)
        if col_name:
            if order_direction == 'desc':
                base_queryset = base_queryset.order_by(f'-{col_name}')
            else:
                base_queryset = base_queryset.order_by(col_name)
        else:
            base_queryset = base_queryset.order_by('-fechacreacion')

        # 5. Paginación y segmentación de datos
        total_records = base_queryset.count()
        records_filtered = total_records 
        page_items = base_queryset[start:start+length]

        data = []
        csrf_token = get_token(request)
        
        url_edit = reverse('edit_vehicle_profile')
        url_status = reverse('status_vehicle')
       
        try: 
            url_assign = reverse('edit_vehicle_mining')
        except: 
            url_assign = "#"

        # 6. Armado de la lista final para JSON
        for vehiculo in page_items:
            pct = vehiculo.completado or 0
            badge_cls = 'success' if pct > 80 else 'danger' if pct < 50 else 'warning'
            badge_html = f'<div class="btn btn-{badge_cls}" style="cursor:default; width:75px; height:28px; padding:0; display:inline-flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:bold; border-radius:4px;">{pct}%</div>'

            btns = '<div class="form-inline-btn" style="display:flex; gap:3px;">'
            btns += f'''<form action="{url_edit}" method="POST"><input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}"><input type="hidden" name="placaPatente" value="{vehiculo.placaPatente}"><button type="submit" class="btn btn-info btn-size-edit">Editar</button></form>'''
            
            if es_habilitado:
                btns += f'''<form action="{url_assign}" method="POST"><input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}"><input type="hidden" name="placaPatente" value="{vehiculo.placaPatente}"><button type="submit" class="btn btn-success btn-size-edit">Asignar</button></form>'''
            
            btns += f'''<form class="vehicle-form" id="form-{vehiculo.placaPatente}" method="POST"><input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}"><input type="hidden" name="placaPatente" value="{vehiculo.placaPatente}"><button type="submit" class="btn btn-warning btn-size-edit">Pdf</button></form>'''
            
            perfil = getattr(request.user, 'usuarioprofile', None)

            roles_gestion = ["ADMINISTRADOR", "BASE DATOS", "JEFE MANTENCION", "SUPERVISOR"]

            if (perfil and perfil.seccionVehicular in roles_gestion) or request.user.is_superuser:
                st_cls = 'danger' if vehiculo.status else 'primary'
                st_txt = 'Deshabilitar' if vehiculo.status else 'Habilitar'
                btns += f'''<form class="status-form" action="{url_status}" method="POST"><input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}"><input type="hidden" name="id" value="{vehiculo.id}"><button type="submit" class="btn btn-{st_cls} btn-size-adm">{st_txt}</button></form>'''
            
            btns += '</div>'

            row = {
                "porcentaje": badge_html,
                "patente": vehiculo.placaPatente,
                "tipo": vehiculo.tipo.tipo if vehiculo.tipo else "",
                "marca": vehiculo.marca.marca if vehiculo.marca else "",
                "modelo": vehiculo.modelo.modelo if vehiculo.modelo else "",
                "estado": "Habilitado" if vehiculo.status else "Deshabilitado",
                "acciones": btns
            }
            
            # Asignación de Faena utilizando los datos pre-cargados (Prefetch)
            if es_habilitado:
                if vehiculo.asignaciones_activas:
                    row["faena"] = vehiculo.asignaciones_activas[0].faena.faena
                else:
                    row["faena"] = "SIN ASIGNAR"

            data.append(row)

        return JsonResponse({
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": records_filtered,
            "data": data
        })

    context = {
        'sidebar': 'manage_vehicles',
        'sidebarmain': 'system_vehicles',
        'api_url': reverse('manage_vehicles'),
        'filtro_faena': filtro_faena,
        'filtro_tipo': filtro_tipo,
        'problemas': ProblemaVehiculo.objects.all(),
    }
    return render(request,'pages/vehicle/manage_vehicles.html', context)

@login_required
@vehicular_admin_db_required
def save_new_vehicle(request): 
    if request.method == 'POST':    
        try:
            tipo_id = request.POST.get('tipo')
            ano_id = request.POST.get('ano')
            marca_id = request.POST.get('marca')
            modelo_id = request.POST.get('modelo')
            color_id = request.POST.get('color')

            if not all([tipo_id, ano_id, marca_id, modelo_id, color_id]):
                return JsonResponse({
                    'success': False,
                    'error': 'Error: Por favor, seleccione todos los campos obligatorios (Tipo, Año, Marca, Modelo, Color).'
                }, status=400)

            tipo_instancia = Tipo.objects.get(pk=tipo_id)    
            ano_instancia = Ano.objects.get(pk=ano_id)  
            marca_instancia = Marca.objects.get(pk=marca_id)  
            modelo_instancia = Modelo.objects.get(pk=modelo_id)  
            color_instancia = Color.objects.get(pk=color_id)  
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error de selección: {str(e)}'
            }, status=400)
            
        
        formulario = FormNuevoVehiculo(
            data=request.POST,
            ocultar_fechaAdquisicion=False,
            ocultar_fechaArriendoInicial=False,
            ocultar_fechaArriendoFinal=False,
            ocultar_tieneTag=False,
            ocultar_tarjetaCombustible=False
        )
        
        placaPatente = request.POST.get('placaPatente', '').upper()
        fechaAdquisicion = validar_campo_vacio('fechaAdquisicion',request)
        
        fechaArriendoInicial = validar_campo_vacio('fechaArriendoInicial', request)
        fechaArriendoFinal = validar_campo_vacio('fechaArriendoFinal', request)
        
        tieneTag = validar_campo_vacio('tieneTag', request)
        tarjetaCombustible = validar_campo_vacio('tarjetaCombustible', request)

        
        if rut_chile.is_valid_rut(request.POST['rutPropietario']):
            if formulario.is_valid():               
                try:
                    with transaction.atomic():
                        vehiculo = Vehiculo(
                            placaPatente = placaPatente,
                            fechaAdquisicion = fechaAdquisicion,
                            fechaArriendoInicial = fechaArriendoInicial,
                            fechaArriendoFinal = fechaArriendoFinal,
                            tenencia = request.POST['tenencia'],
                            nombrePropietario = request.POST['nombrePropietario'],
                            rutPropietario = request.POST['rutPropietario'],
                            domicilio = request.POST['domicilio'],
                            tipo = tipo_instancia,
                            ano = ano_instancia,
                            marca = marca_instancia,
                            modelo = modelo_instancia,
                            numeroMotor = request.POST['numeroMotor'],
                            numeroChasis = request.POST['numeroChasis'],
                            numeroVin = request.POST['numeroVin'],
                            color = color_instancia,
                            tieneTag = tieneTag,
                            tarjetaCombustible = tarjetaCombustible,
                            fechaVencimientoPermisoCirculacion = validar_campo_vacio('fechaVencimientoPermisoCirculacion',request),
                            fechaVencimientoRevisionTecnica = validar_campo_vacio('fechaVencimientoRevisionTecnica',request),
                            fechaVencimientoSeguroObligatorio = validar_campo_vacio('fechaVencimientoSeguroObligatorio',request),
                            status = True,
                        )    
                        vehiculo.save()
                        
                        fecha_hoy = timezone.now().date().strftime('%Y-%m-%d')
                        vehiculo_faena = Vehiculo.objects.get(placaPatente=placaPatente)
                        usuario_creador = UsuarioProfile.objects.get(user=request.user.id)
                        
                        faena_usuario = usuario_creador.faena                        
                        faena = Faena.objects.get(faena='SIN ASIGNAR')
                        
                        vehiculo_actual = VehiculoAsignado(
                            vehiculo = vehiculo_faena,
                            faena = faena_usuario,#POSIBLE PROBLEMA ES FAENA O FAENA_USUARIO
                            faenaAnterior = "SIN ASIGNAR",
                            creador = request.user.get_full_name() or request.user.username,
                            fechaInicial = fecha_hoy,
                            status = True,
                        )
                        vehiculo_actual.save()

                        # Crear registro de kilometraje actual
                        NuevoKilometraje.objects.create(
                            vehiculo=vehiculo_faena,
                            kilometraje=request.POST['kilometraje_actual'],
                            creador=request.user.get_full_name() or request.user.username,
                            origen='Formulario'
                        )

                        # Obtener/crear categoría y falla "Mantención General"
                        categoria_nombre = 'Mantención'
                        categoria = CategoriaFallaVehiculo.objects.filter(categoria__iexact=categoria_nombre).first()
                        if not categoria:
                            categoria = CategoriaFallaVehiculo.objects.filter(categoria__iexact='Mantencion').first()
                        if not categoria:
                            categoria = CategoriaFallaVehiculo.objects.create(
                                categoria=categoria_nombre,
                                creador=request.user.get_full_name() or request.user.username,
                                status=True
                            )
                        elif categoria.categoria != categoria_nombre:
                            categoria.categoria = categoria_nombre
                            categoria.save()
                        falla_nombre = 'Mantención General'
                        falla = TipoFallaVehiculo.objects.filter(falla__iexact=falla_nombre).first()
                        if not falla:
                            falla = TipoFallaVehiculo.objects.filter(falla__iexact='Mantencion General').first()
                        if not falla:
                            falla = TipoFallaVehiculo.objects.create(
                                falla=falla_nombre,
                                categoria=categoria,
                                creador=request.user.get_full_name() or request.user.username,
                                status=True
                            )
                        elif falla.falla != falla_nombre:
                            falla.falla = falla_nombre
                            falla.save()

                        # Crear registro de mantenimiento general
                        mantenimiento = NuevaSolicitudMantenimiento(
                            solicitante=Usuario.objects.get(id=request.user.id),
                            vehiculo=vehiculo_faena,
                            faena=faena_usuario,
                            patente=vehiculo_faena.placaPatente,
                            kilometraje=request.POST['kilometraje_ultima_mantencion'],
                            progreso='4',
                            comentario='Mantención general al crear vehículo',
                            avisoJefatura='Si',
                            status=True,
                        )
                        mantenimiento.save()
                        mantenimiento.problemas.set([falla])

                        # Actualizar frecuencia de mantenimiento en Información Técnica
                        info_tecnica = InformacionTecnicaVehiculo.objects.get(vehiculo=vehiculo_faena)
                        info_tecnica.frecuenciaMantenimiento = request.POST['frecuencia_mantenimiento']
                        info_tecnica.save()

                        # notificacion_vehiculos_email(request, vehiculo_faena, "creado")
                        return JsonResponse({
                            'success': True,
                            'message': 'Vehículo Creado Correctamente',
                            'redirect': '/manage_vehicles'
                        })
                except IntegrityError as e:
                    error_msg = str(e)
                    if 'placaPatente' in error_msg.lower():
                        error_text = f'La Placa Patente {placaPatente} ya está registrada para otro vehículo. Cambie la patente o edite el vehículo existente.'
                    elif 'numeroMotor' in error_msg.lower():
                        error_text = f'El Número de Motor {request.POST.get("numeroMotor", "")} ya está registrado para otro vehículo. Verifique el número.'
                    elif 'numeroChasis' in error_msg.lower():
                        error_text = f'El Número de Chasis {request.POST.get("numeroChasis", "")} ya está registrado para otro vehículo. Verifique el número.'
                    elif 'numeroVin' in error_msg.lower():
                        error_text = f'El Número VIN {request.POST.get("numeroVin", "")} ya está registrado para otro vehículo. Verifique el número.'
                    else:
                        error_text = 'Error de duplicado en la base de datos. Verifique que los datos no estén repetidos.'
                    return JsonResponse({
                        'success': False,
                        'error': error_text
                    }, status=400)
                except Exception as e:
                    error_msg = str(e)
                    return JsonResponse({
                        'success': False,
                        'error': f'Error: {error_msg}'
                    }, status=400)
            else:
                error_list = []
                for field, errors in formulario.errors.items():
                    field_names = {
                        'placaPatente': 'Placa Patente',
                        'numeroMotor': 'Número de Motor',
                        'numeroChasis': 'Número de Chasis',
                        'numeroVin': 'Número VIN',
                        'rutPropietario': 'RUT Propietario',
                        'tipo': 'Tipo',
                        'marca': 'Marca',
                        'modelo': 'Modelo',
                        'ano': 'Año',
                        'color': 'Color',
                    }
                    field_label = field_names.get(field, field.title())
                    for error in errors:
                        error_list.append(f'{field_label}: {error}')
                
                error_text = '\n'.join(error_list) if error_list else 'Verifique los campos del formulario'
                
                return JsonResponse({
                    'success': False,
                    'error': error_text
                }, status=400)
        else: 
            return JsonResponse({
                'success': False,
                'error': 'Rut incorrecto'
            }, status=400)             
    else:
        return redirect('new_vehicle')

@login_required
@vehicular_avanzado_required
def status_vehicle(request):
    if request.method == 'POST': 
        try:
            vehiculo_id = request.POST.get('id')
            problema_id = request.POST.get('problema_id')
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            
            if (vehiculo.status):
                asignacion_activa = VehiculoAsignado.objects.filter(vehiculo=vehiculo, status=True).last()
                
                if asignacion_activa and asignacion_activa.faena.faena != "SIN ASIGNAR":
                    return JsonResponse({
                        'success': False, 
                        'message': f'Acción Denegada. No se puede deshabilitar el vehículo porque está asignado a la faena {asignacion_activa.faena.faena}. Debe desasignarlo primero.'
                    })

                vehiculo.status = False
                vehiculo.problema_id = problema_id
                vehiculo.save()
                return JsonResponse({'success': True, 'message': 'Vehículo Deshabilitado Correctamente'})
            
            else:   
                vehiculo.status = True
                vehiculo.problema = None
                vehiculo.save()
                return JsonResponse({'success': True, 'message': 'Vehículo Habilitado Correctamente'})
                
        except Vehiculo.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'El vehículo no existe.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error interno: {str(e)}'})
            
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@vehicular_avanzado_required
def edit_vehicle_profile(request):
    try:
        request.session['edit_placaPatente'] = request.POST.get('placaPatente', request.session.get('edit_placaPatente'))
    except (MultiValueDictKeyError, KeyError):
        pass
    
    vehiculo = Vehiculo.objects.get(placaPatente=request.session['edit_placaPatente'])
    vehiculoDocumentacion = DocumentacionesVehiculo.objects.get(vehiculo_id=vehiculo.id)
    vehiculoInformacion = InformacionTecnicaVehiculo.objects.get(vehiculo_id=vehiculo.id)
    
    infracciones = InfraccionesVehiculo.objects.filter(vehiculo=vehiculo).order_by('-fechaInfraccion')
    solicitudesMantenimiento = NuevaSolicitudMantenimiento.objects.filter(vehiculo=vehiculo).order_by('-fechacreacion')
    historial_docs = HistorialDocumentacionVehiculo.objects.filter(vehiculo=vehiculo).order_by('-fechacreacion')
    kilometrajes = NuevoKilometraje.objects.filter(vehiculo=vehiculo).order_by('-fechacreacion')
    
    tipo_actual = Tipo.objects.filter(tipo=vehiculo.tipo)
    marca_actual = Marca.objects.filter(marca=vehiculo.marca)
    modelo_actual = Modelo.objects.filter(modelo=vehiculo.modelo)
    ano_actual = Ano.objects.filter(ano=vehiculo.ano)
    color_actual = Color.objects.filter(color=vehiculo.color)

    extensionFotografiaPadron = extension_archivo(vehiculoDocumentacion.fotografiaPadron)
    extensionFotografiaPermisoCirculacion = extension_archivo(vehiculoDocumentacion.fotografiaPermisoCirculacion)
    extensionFotografiaRevisionTecnica = extension_archivo(vehiculoDocumentacion.fotografiaRevisionTecnica)
    extensionFotografiaRevisionTecnicaGases = extension_archivo(vehiculoDocumentacion.fotografiaRevisionTecnicaGases)
    extensionFotografiaSeguroObligatorio = extension_archivo(vehiculoDocumentacion.fotografiaSeguroObligatorio)
    extensionFotografiaCertificadoGps = extension_archivo(vehiculoDocumentacion.fotografiaCertificadoGps)
    extensionFotografiaCertificadoMantencion = extension_archivo(vehiculoDocumentacion.fotografiaCertificadoMantencion)
    extensionFotografiaCertificadoOperatividad = extension_archivo(vehiculoDocumentacion.fotografiaCertificadoOperatividad)
    extensionFotografiaCertificadoGrua = extension_archivo(vehiculoDocumentacion.fotografiaCertificadoGrua)
    extensionFotografiaFacturaCompra = extension_archivo(vehiculoDocumentacion.fotografiaFacturaCompra)
    extensionFotografiaSeguroAutomotriz = extension_archivo(vehiculoDocumentacion.fotografiaSeguroAutomotriz)
    extensionFotografiaCertificadoLamina = extension_archivo(vehiculoDocumentacion.fotografiaCertificadoLamina)
    extensionFotografiaCertificadoBarraAntiVuelco = extension_archivo(vehiculoDocumentacion.fotografiaCertificadoBarraAntiVuelco)
    extensionFotografiaDocumentacionMiniBus = extension_archivo(vehiculoDocumentacion.fotografiaDocumentacionMiniBus)
    extensionFotografiaExteriorFrontis = extension_archivo(vehiculoDocumentacion.fotografiaExteriorFrontis)
    extensionFotografiaExteriorAtras = extension_archivo(vehiculoDocumentacion.fotografiaExteriorAtras)
    extensionFotografiaExteriorPiloto = extension_archivo(vehiculoDocumentacion.fotografiaExteriorPiloto)
    extensionFotografiaExteriorCopiloto = extension_archivo(vehiculoDocumentacion.fotografiaExteriorCopiloto)
    extensionFotografiaInteriorTablero = extension_archivo(vehiculoDocumentacion.fotografiaInteriorTablero)
    extensionFotografiaInteriorCopiloto = extension_archivo(vehiculoDocumentacion.fotografiaInteriorCopiloto)
    extensionFotografiaInteriorAtrasPiloto = extension_archivo(vehiculoDocumentacion.fotografiaInteriorAtrasPiloto)
    extensionFotografiaInteriorAtrasCopiloto = extension_archivo(vehiculoDocumentacion.fotografiaInteriorAtrasCopiloto)
    extensionFotografiaTraspasoVenta = extension_archivo(vehiculoDocumentacion.fotografiaTraspasoVenta)

    try:
        tarjeta_combustible = NuevaTarjetaCombustible.objects.get(vehiculo=vehiculo, actual=True)
        tarjeta = tarjeta_combustible.numeroTarjeta
    except NuevaTarjetaCombustible.DoesNotExist:
        tarjeta = "Sin Tarjeta"

    try:
        modeloDispositivo = AyudaTecnicaVehiculo.objects.get(vehiculo=vehiculo)
        dispositivo = modeloDispositivo.dispositivo
        proveedor = modeloDispositivo.proveedor
    except AyudaTecnicaVehiculo.DoesNotExist:
        dispositivo = None
        proveedor = None
    
    context = {
        'numero_placaPatente': vehiculo.placaPatente,
        'sidebar': 'manage_vehicles',
        'sidebarmain': 'system_vehicles',
        'vehiculo': vehiculo,
        'infracciones': infracciones,
        'kilometrajes': kilometrajes,
        'historial_docs': historial_docs,
        'forminfracciones': FormInfraccionesVehiculo,
        'solicitudesMantenimiento': solicitudesMantenimiento,
        'choicesprogreso': progreso,
        'formnuevovehiculo': FormNuevoVehiculo(es_creacion=False, initial={
            'placaPatente': vehiculo.placaPatente,
            'tenencia': vehiculo.tenencia,
            'fechaAdquisicion': formatear_fecha(vehiculo.fechaAdquisicion),
            'fechaArriendoInicial': formatear_fecha(vehiculo.fechaArriendoInicial),
            'fechaArriendoFinal': formatear_fecha(vehiculo.fechaArriendoFinal),
            'nombrePropietario': vehiculo.nombrePropietario,
            'rutPropietario': vehiculo.rutPropietario,
            'domicilio': vehiculo.domicilio,
            'tipo': vehiculo.tipo,
            'ano': vehiculo.ano,
            'marca': vehiculo.marca,
            'modelo': vehiculo.modelo,
            'numeroMotor': vehiculo.numeroMotor,
            'numeroChasis': vehiculo.numeroChasis,
            'numeroVin': vehiculo.numeroVin,
            'color': vehiculo.color,
            'fechaVencimientoPermisoCirculacion': formatear_fecha(vehiculo.fechaVencimientoPermisoCirculacion),
            'fechaVencimientoRevisionTecnica': formatear_fecha(vehiculo.fechaVencimientoRevisionTecnica),
            'fechaVencimientoSeguroObligatorio': formatear_fecha(vehiculo.fechaVencimientoSeguroObligatorio),
            'fechaInstalacionGps': formatear_fecha(vehiculo.fechaInstalacionGps),
            'fechaVencimientoLamina': formatear_fecha(vehiculo.fechaVencimientoLamina),
            'fechaVencimientoTransportePrivado': formatear_fecha(vehiculo.fechaVencimientoTransportePrivado),
            'fechaInstalacionBarraAntiVuelco': formatear_fecha(vehiculo.fechaInstalacionBarraAntiVuelco),
            'fechaCertificadoOperatividad': formatear_fecha(vehiculo.fechaCertificadoOperatividad),
            'fechaCertificadoMantencion': formatear_fecha(vehiculo.fechaCertificadoMantencion),
            'fechaCertificadoGrua': formatear_fecha(vehiculo.fechaCertificadoGrua),
            'tieneTag': vehiculo.tieneTag,
            'tarjetaCombustible': tarjeta,
            },
            placaPatente_disabled=True,
            tipo_actual=tipo_actual,
            marca_actual=marca_actual,
            modelo_actual=modelo_actual,
            ano_actual=ano_actual,
            color_actual=color_actual,
            ocultar_fechaAdquisicion=False,
            ocultar_fechaArriendoInicial=False,
            ocultar_fechaArriendoFinal=False,
            ocultar_tieneTag=False,
            ocultar_tarjetaCombustible=False,
        ),    
        'forminformaciontecnicavehiculo': FormInformacionTecnica(initial={
            'tipoTraccion': vehiculoInformacion.tipoTraccion,
            'pesoBrutoVehicular': vehiculoInformacion.pesoBrutoVehicular,
            'capacidadCarga': vehiculoInformacion.capacidadCarga,
            'tipoNeumatico': vehiculoInformacion.tipoNeumatico,
            'tipoAceiteMotor': vehiculoInformacion.tipoAceiteMotor,
            'tipoRefrigeranteMotor': vehiculoInformacion.tipoRefrigeranteMotor,
            'tipoFiltroAireMotor': vehiculoInformacion.tipoFiltroAireMotor,
            'tipoFiltroCombustible': vehiculoInformacion.tipoFiltroCombustible,
            'frecuenciaMantenimiento': vehiculoInformacion.frecuenciaMantenimiento,
            'proximoMantenimiento': vehiculoInformacion.proximoMantenimiento,
            'proximoMantenimientoGrua': vehiculoInformacion.proximoMantenimientoGrua,
            }
        ),
        'formayudatecnicavehiculo': FormAyudaTecnicaVehiculo(initial={'dispositivo': dispositivo, 'proveedor': proveedor}),
        'fotografiaPadron': vehiculoDocumentacion.fotografiaPadron,
        'fotografiaPermisoCirculacion': vehiculoDocumentacion.fotografiaPermisoCirculacion,
        'fotografiaRevisionTecnica': vehiculoDocumentacion.fotografiaRevisionTecnica,
        'fotografiaRevisionTecnicaGases': vehiculoDocumentacion.fotografiaRevisionTecnicaGases,
        'fotografiaSeguroObligatorio': vehiculoDocumentacion.fotografiaSeguroObligatorio,
        'fotografiaCertificadoGps': vehiculoDocumentacion.fotografiaCertificadoGps,
        'fotografiaCertificadoMantencion': vehiculoDocumentacion.fotografiaCertificadoMantencion,
        'fotografiaCertificadoOperatividad': vehiculoDocumentacion.fotografiaCertificadoOperatividad,
        'fotografiaCertificadoGrua': vehiculoDocumentacion.fotografiaCertificadoGrua,
        'fotografiaFacturaCompra': vehiculoDocumentacion.fotografiaFacturaCompra,
        'fotografiaSeguroAutomotriz': vehiculoDocumentacion.fotografiaSeguroAutomotriz,
        'fotografiaCertificadoLamina': vehiculoDocumentacion.fotografiaCertificadoLamina,
        'fotografiaCertificadoBarraAntiVuelco': vehiculoDocumentacion.fotografiaCertificadoBarraAntiVuelco,
        'fotografiaDocumentacionMiniBus': vehiculoDocumentacion.fotografiaDocumentacionMiniBus,  
        'fotografiaExteriorFrontis': vehiculoDocumentacion.fotografiaExteriorFrontis,
        'fotografiaExteriorAtras': vehiculoDocumentacion.fotografiaExteriorAtras,
        'fotografiaExteriorPiloto': vehiculoDocumentacion.fotografiaExteriorPiloto,
        'fotografiaExteriorCopiloto': vehiculoDocumentacion.fotografiaExteriorCopiloto,
        'fotografiaInteriorTablero': vehiculoDocumentacion.fotografiaInteriorTablero,
        'fotografiaInteriorCopiloto': vehiculoDocumentacion.fotografiaInteriorCopiloto,
        'fotografiaInteriorAtrasPiloto': vehiculoDocumentacion.fotografiaInteriorAtrasPiloto,
        'fotografiaInteriorAtrasCopiloto': vehiculoDocumentacion.fotografiaInteriorAtrasCopiloto,
        'fotografiaTraspasoVenta': vehiculoDocumentacion.fotografiaTraspasoVenta,
        'extensionFotografiaPadron': extensionFotografiaPadron,
        'extensionFotografiaPermisoCirculacion': extensionFotografiaPermisoCirculacion,
        'extensionFotografiaRevisionTecnica': extensionFotografiaRevisionTecnica,
        'extensionFotografiaRevisionTecnicaGases': extensionFotografiaRevisionTecnicaGases,
        'extensionFotografiaSeguroObligatorio': extensionFotografiaSeguroObligatorio,
        'extensionFotografiaCertificadoGps': extensionFotografiaCertificadoGps,
        'extensionFotografiaCertificadoMantencion': extensionFotografiaCertificadoMantencion,
        'extensionFotografiaCertificadoOperatividad': extensionFotografiaCertificadoOperatividad,
        'extensionFotografiaCertificadoGrua': extensionFotografiaCertificadoGrua,
        'extensionFotografiaFacturaCompra': extensionFotografiaFacturaCompra,
        'extensionFotografiaSeguroAutomotriz': extensionFotografiaSeguroAutomotriz,
        'extensionFotografiaCertificadoLamina': extensionFotografiaCertificadoLamina,
        'extensionFotografiaCertificadoBarraAntiVuelco': extensionFotografiaCertificadoBarraAntiVuelco,
        'extensionFotografiaDocumentacionMiniBus': extensionFotografiaDocumentacionMiniBus,
        'extensionFotografiaExteriorFrontis': extensionFotografiaExteriorFrontis,
        'extensionFotografiaExteriorAtras': extensionFotografiaExteriorAtras,
        'extensionFotografiaExteriorPiloto': extensionFotografiaExteriorPiloto,
        'extensionFotografiaExteriorCopiloto': extensionFotografiaExteriorCopiloto,
        'extensionFotografiaInteriorTablero': extensionFotografiaInteriorTablero,
        'extensionFotografiaInteriorCopiloto': extensionFotografiaInteriorCopiloto,
        'extensionFotografiaInteriorAtrasPiloto': extensionFotografiaInteriorAtrasPiloto,
        'extensionFotografiaInteriorAtrasCopiloto': extensionFotografiaInteriorAtrasCopiloto,
        'extensionFotografiaTraspasoVenta': extensionFotografiaTraspasoVenta,
    }
    return render(request, 'pages/vehicle/edit_vehicle_profile.html', context)

@login_required
@vehicular_avanzado_required
def save_edit_vehicle_profile(request):  
    if request.method == 'POST':
        
        def obtener_fecha_aware(nombre_campo):
            valor = validar_campo_vacio(nombre_campo, request)
            if valor and isinstance(valor, str):
                dt = datetime.strptime(valor, '%Y-%m-%d')
                return timezone.make_aware(dt)
            return valor

        fechaAdquisicion = obtener_fecha_aware('fechaAdquisicion')
        fechaArriendoInicial = obtener_fecha_aware('fechaArriendoInicial')
        fechaArriendoFinal = obtener_fecha_aware('fechaArriendoFinal')        
        tieneTag = validar_campo_vacio('tieneTag', request)
        tarjetaCombustible = validar_campo_vacio('tarjetaCombustible', request)
        pesoBrutoVehicular = validar_campo_vacio('pesoBrutoVehicular', request)
        capacidadCarga = validar_campo_vacio('capacidadCarga', request)
        tipoNeumatico = validar_campo_vacio('tipoNeumatico', request)
        tipoAceiteMotor = validar_campo_vacio('tipoAceiteMotor', request)
        tipoRefrigeranteMotor = validar_campo_vacio('tipoRefrigeranteMotor', request)
        tipoFiltroAireMotor = validar_campo_vacio('tipoFiltroAireMotor', request)
        tipoFiltroCombustible = validar_campo_vacio('tipoFiltroCombustible', request)
        frecuenciaMantenimiento = validar_campo_vacio('frecuenciaMantenimiento', request)
        proximoMantenimiento = validar_campo_vacio('proximoMantenimiento', request)
        proximoMantenimientoGrua = validar_campo_vacio('proximoMantenimientoGrua', request)

        def preparar_vencimiento(nombre_campo):
            valor = request.POST.get(nombre_campo, '').strip()
            if valor:
                dt = datetime.strptime(f"{valor}-01", '%Y-%m-%d')
                return timezone.make_aware(dt)
            return None

        venc_factura = preparar_vencimiento('vencimiento_FacturaCompra')
        venc_permiso = preparar_vencimiento('vencimiento_PermisoCirculacion')
        venc_revision = preparar_vencimiento('vencimiento_RevisionTecnica')
        venc_gases = preparar_vencimiento('vencimiento_RevisionTecnicaGases')
        venc_seguro_obligatorio = preparar_vencimiento('vencimiento_SeguroObligatorio')
        venc_seguro_auto = preparar_vencimiento('vencimiento_SeguroAutomotriz')
        venc_gps = preparar_vencimiento('vencimiento_CertificadoGps')
        venc_mantencion = preparar_vencimiento('vencimiento_CertificadoMantencion')
        venc_operatividad = preparar_vencimiento('vencimiento_CertificadoOperatividad')
        venc_grua = preparar_vencimiento('vencimiento_CertificadoGrua')
        venc_lamina = preparar_vencimiento('vencimiento_CertificadoLamina')
        venc_barra = preparar_vencimiento('vencimiento_CertificadoBarraAntiVuelco')
        venc_minibus = preparar_vencimiento('vencimiento_DocumentacionMiniBus')
        venc_traspaso = preparar_vencimiento('vencimiento_TraspasoVenta')
            
        if rut_chile.is_valid_rut(request.POST['rutPropietario']):
            vehicle_update_fields = {
                'tenencia': request.POST['tenencia'],
                'fechaAdquisicion': fechaAdquisicion,
                'fechaArriendoInicial': fechaArriendoInicial,
                'fechaArriendoFinal': fechaArriendoFinal,
                'nombrePropietario': request.POST['nombrePropietario'],
                'rutPropietario': request.POST['rutPropietario'],
                'domicilio': request.POST['domicilio'],
                'tipo': request.POST['tipo'],
                'ano': request.POST['ano'],
                'marca': request.POST['marca'],
                'modelo': request.POST['modelo'],
                'numeroMotor': request.POST['numeroMotor'],
                'numeroChasis': request.POST['numeroChasis'],
                'numeroVin': request.POST['numeroVin'],
                'color': request.POST['color'],
                'tieneTag': tieneTag,
                'tarjetaCombustible': tarjetaCombustible
            }

            if venc_factura: vehicle_update_fields['fechaVencimientoFacturaCompra'] = venc_factura
            if venc_permiso: vehicle_update_fields['fechaVencimientoPermisoCirculacion'] = venc_permiso
            if venc_revision: vehicle_update_fields['fechaVencimientoRevisionTecnica'] = venc_revision
            if venc_gases: vehicle_update_fields['fechaVencimientoRevisionTecnicaGases'] = venc_gases
            if venc_seguro_obligatorio: vehicle_update_fields['fechaVencimientoSeguroObligatorio'] = venc_seguro_obligatorio
            if venc_seguro_auto: vehicle_update_fields['fechaVencimientoSeguroAutomotriz'] = venc_seguro_auto
            if venc_gps: vehicle_update_fields['fechaInstalacionGps'] = venc_gps
            if venc_mantencion: vehicle_update_fields['fechaVencimientoCertificadoMantencion'] = venc_mantencion
            if venc_operatividad: vehicle_update_fields['fechaVencimientoCertificadoOperatividad'] = venc_operatividad
            if venc_grua: vehicle_update_fields['fechaVencimientoCertificadoGrua'] = venc_grua
            if venc_lamina: vehicle_update_fields['fechaVencimientoLamina'] = venc_lamina
            if venc_barra: vehicle_update_fields['fechaInstalacionBarraAntiVuelco'] = venc_barra
            if venc_minibus: vehicle_update_fields['fechaVencimientoTransportePrivado'] = venc_minibus
            if venc_traspaso: vehicle_update_fields['fechaVencimientoTraspasoVenta'] = venc_traspaso

            vehiculo_antes = Vehiculo.objects.get(placaPatente=request.POST['numero_placaPatente'])
            
            vehiculo = Vehiculo.objects.get(placaPatente=request.POST['numero_placaPatente'])
        
            fk_fields = ['tipo', 'ano', 'marca', 'modelo', 'color']
            for attr, value in vehicle_update_fields.items():
                if attr in fk_fields:
                    # Usamos el sufijo _id para asignar el ID directamente en campos ForeignKey
                    setattr(vehiculo, f"{attr}_id", value)
                else:
                    setattr(vehiculo, attr, value)
            vehiculo.save()
            
            vehiculo = Vehiculo.objects.get(placaPatente=request.POST['numero_placaPatente'])
            
            InformacionTecnicaVehiculo.objects.filter(vehiculo=vehiculo).update(
                tipoTraccion=request.POST['tipoTraccion'],
                pesoBrutoVehicular=pesoBrutoVehicular,
                capacidadCarga=capacidadCarga,
                tipoNeumatico=tipoNeumatico,
                tipoAceiteMotor=tipoAceiteMotor,
                tipoRefrigeranteMotor=tipoRefrigeranteMotor,
                tipoFiltroAireMotor=tipoFiltroAireMotor,
                tipoFiltroCombustible=tipoFiltroCombustible,
                frecuenciaMantenimiento=frecuenciaMantenimiento,
                proximoMantenimiento=proximoMantenimiento,
                proximoMantenimientoGrua=proximoMantenimientoGrua,
            )
            
            try:
                proveedor_id = request.POST.get('proveedor')
                proveedor = MarcaSomnolencia.objects.filter(id=proveedor_id).first() if proveedor_id else None
                dispositivo = request.POST.get('dispositivo') == 'true'
                if not dispositivo: proveedor = None

                AyudaTecnicaVehiculo.objects.update_or_create(
                    vehiculo=vehiculo,
                    defaults={
                        "dispositivo": dispositivo,
                        "proveedor": proveedor,
                        "creador": request.user.get_full_name() or request.user.username,
                        "status": True
                    }
                )
            except Exception as e:
                print(f"Error en Ayuda Técnica: {e}")

            documentacionVehiculo = DocumentacionesVehiculo.objects.get(vehiculo_id=vehiculo.id)
            doc_antes = DocumentacionesVehiculo.objects.get(vehiculo_id=vehiculo.id)

            toggles = {
                'fotografiaPadron': 'toggle-Padron', 'fotografiaPermisoCirculacion': 'toggle-PermisoCirculacion',
                'fotografiaRevisionTecnica': 'toggle-RevisionTecnica', 'fotografiaRevisionTecnicaGases': 'toggle-RevisionTecnicaGases',
                'fotografiaSeguroObligatorio': 'toggle-SeguroObligatorio', 'fotografiaCertificadoGps': 'toggle-CertificadoGps',
                'fotografiaCertificadoMantencion': 'toggle-CertificadoMantencion', 'fotografiaCertificadoOperatividad': 'toggle-CertificadoOperatividad',
                'fotografiaCertificadoGrua': 'toggle-CertificadoGrua', 'fotografiaFacturaCompra': 'toggle-FacturaCompra',
                'fotografiaSeguroAutomotriz': 'toggle-SeguroAutomotriz', 'fotografiaCertificadoLamina': 'toggle-CertificadoLamina',
                'fotografiaCertificadoBarraAntiVuelco': 'toggle-CertificadoBarraAntiVuelco', 'fotografiaDocumentacionMiniBus': 'toggle-DocumentacionMiniBus',
                'fotografiaInteriorTablero': 'toggle-InteriorTablero', 'fotografiaInteriorCopiloto': 'toggle-InteriorCopiloto',
                'fotografiaInteriorAtrasPiloto': 'toggle-InteriorAtrasPiloto', 'fotografiaInteriorAtrasCopiloto': 'toggle-InteriorAtrasCopiloto',
                'fotografiaExteriorFrontis': 'toggle-ExteriorFrontis', 'fotografiaExteriorAtras': 'toggle-ExteriorAtras',
                'fotografiaExteriorPiloto': 'toggle-ExteriorPiloto', 'fotografiaExteriorCopiloto': 'toggle-ExteriorCopiloto',
                'fotografiaTraspasoVenta': 'toggle-TraspasoVenta',
            }

            for field, toggle in toggles.items():
                default_img = 'documentacion_vehiculo/no-imagen-vehiculo.png' if 'Exterior' in field or 'Interior' in field else 'documentacion_vehiculo/no-imagen.png'
                procesar_fotografia(documentacionVehiculo, request.POST.get(toggle, 'no'), field, default_img, request)

            documentacionVehiculo.save()

            documentos_labels = [
                ('fotografiaPadron', 'toggle-Padron', 'Padrón Vehicular'),
                ('fotografiaPermisoCirculacion', 'toggle-PermisoCirculacion', 'Permiso de Circulación'),
                ('fotografiaRevisionTecnica', 'toggle-RevisionTecnica', 'Revisión Técnica'),
                ('fotografiaRevisionTecnicaGases', 'toggle-RevisionTecnicaGases', 'Revisión Técnica de Gases'),
                ('fotografiaSeguroObligatorio', 'toggle-SeguroObligatorio', 'Seguro Obligatorio (SOAP)'),
                ('fotografiaSeguroAutomotriz', 'toggle-SeguroAutomotriz', 'Seguro Automotriz'),
                ('fotografiaCertificadoGps', 'toggle-CertificadoGps', 'Certificado GPS'),
                ('fotografiaCertificadoMantencion', 'toggle-CertificadoMantencion', 'Certificado Mantención'),
                ('fotografiaCertificadoOperatividad', 'toggle-CertificadoOperatividad', 'Certificado Operatividad'),
                ('fotografiaCertificadoGrua', 'toggle-CertificadoGrua', 'Certificado Grúa'),
                ('fotografiaCertificadoLamina', 'toggle-CertificadoLamina', 'Certificado de Lámina'),
                ('fotografiaCertificadoBarraAntiVuelco', 'toggle-CertificadoBarraAntiVuelco', 'Certificado Barra AntiVuelco'),
                ('fotografiaDocumentacionMiniBus', 'toggle-DocumentacionMiniBus', 'Documentación Transp. Privado'),
                ('fotografiaFacturaCompra', 'toggle-FacturaCompra', 'Factura de Compra'),
                ('fotografiaTraspasoVenta', 'toggle-TraspasoVenta', 'Traspaso/Venta'),
            ]

            fechas_vencimiento_docs = {
                'fotografiaFacturaCompra': venc_factura,
                'fotografiaPermisoCirculacion': venc_permiso,
                'fotografiaRevisionTecnica': venc_revision,
                'fotografiaRevisionTecnicaGases': venc_gases,
                'fotografiaSeguroObligatorio': venc_seguro_obligatorio,
                'fotografiaSeguroAutomotriz': venc_seguro_auto,
                'fotografiaCertificadoGps': venc_gps,
                'fotografiaCertificadoMantencion': venc_mantencion,
                'fotografiaCertificadoOperatividad': venc_operatividad,
                'fotografiaCertificadoGrua': venc_grua,
                'fotografiaCertificadoLamina': venc_lamina,
                'fotografiaCertificadoBarraAntiVuelco': venc_barra,
                'fotografiaDocumentacionMiniBus': venc_minibus,
                'fotografiaTraspasoVenta': venc_traspaso,
            }

            usuario_actual = request.user.get_full_name() or request.user.username

            mapeo_fechas_vehiculo = {
                'fotografiaFacturaCompra': 'fechaVencimientoFacturaCompra',
                'fotografiaPermisoCirculacion': 'fechaVencimientoPermisoCirculacion',
                'fotografiaRevisionTecnica': 'fechaVencimientoRevisionTecnica',
                'fotografiaRevisionTecnicaGases': 'fechaVencimientoRevisionTecnicaGases',
                'fotografiaSeguroObligatorio': 'fechaVencimientoSeguroObligatorio',
                'fotografiaSeguroAutomotriz': 'fechaVencimientoSeguroAutomotriz',
                'fotografiaCertificadoGps': 'fechaInstalacionGps',
                'fotografiaCertificadoMantencion': 'fechaVencimientoCertificadoMantencion',
                'fotografiaCertificadoOperatividad': 'fechaVencimientoCertificadoOperatividad',
                'fotografiaCertificadoGrua': 'fechaVencimientoCertificadoGrua',
                'fotografiaCertificadoLamina': 'fechaVencimientoLamina',
                'fotografiaCertificadoBarraAntiVuelco': 'fechaInstalacionBarraAntiVuelco',
                'fotografiaDocumentacionMiniBus': 'fechaVencimientoTransportePrivado',
                'fotografiaTraspasoVenta': 'fechaVencimientoTraspasoVenta',
            }

            for file_key, toggle_key, doc_name in documentos_labels:
                fecha_venc_historial = fechas_vencimiento_docs.get(file_key, None) 

                if file_key in request.FILES:
                    archivo_previo = getattr(doc_antes, file_key)
                    accion_final = 'Subido'
                    
                    if archivo_previo and 'no-imagen' not in str(archivo_previo):
                        nombre_campo_fecha = mapeo_fechas_vehiculo.get(file_key)
                        fecha_anterior = getattr(vehiculo_antes, nombre_campo_fecha) if nombre_campo_fecha else None

                        if fecha_anterior and fecha_venc_historial:
                            mes_ano_nuevo = fecha_venc_historial.strftime('%Y-%m') 
                            mes_ano_anterior = fecha_anterior.strftime('%Y-%m')
                            
                            if mes_ano_nuevo == mes_ano_anterior:
                                accion_final = 'Editado'

                    archivo_actual = getattr(documentacionVehiculo, file_key)
                    
                    HistorialDocumentacionVehiculo.objects.create(
                        vehiculo=vehiculo, documento_modificado=doc_name, accion=accion_final, 
                        archivo=archivo_actual.url if archivo_actual else None, 
                        creador=usuario_actual, fecha_vencimiento=fecha_venc_historial 
                    )
                
                elif str(request.POST.get(toggle_key)).lower() in ['si', 'on', 'true', '1']:
                    archivo_antes = getattr(doc_antes, file_key)
                    
                    nombre_campo_fecha = mapeo_fechas_vehiculo.get(file_key)
                    fecha_antigua = getattr(vehiculo, nombre_campo_fecha) if nombre_campo_fecha else None

                    HistorialDocumentacionVehiculo.objects.create(
                        vehiculo=vehiculo, documento_modificado=doc_name, accion='Eliminado', 
                        archivo=archivo_antes.url if archivo_antes and 'no-imagen' not in archivo_antes.url else None, 
                        creador=usuario_actual, 
                        fecha_vencimiento=fecha_antigua
                    )
      
            informacionTecnicaVehiculo = InformacionTecnicaVehiculo.objects.get(vehiculo_id=vehiculo.id)
            c1, t1 = vehiculo.calcular_completitud_vehiculo()
            c2, t2 = informacionTecnicaVehiculo.calcular_completitud_informacion_tecnica()
            c3, t3 = documentacionVehiculo.calcular_completitud_documentaciones()
            
            porcentaje = ((16 + c1 + c2 + c3) / (16 + t1 + t2 + t3)) * 100
            Vehiculo.objects.filter(placaPatente=request.POST['numero_placaPatente']).update(completado=porcentaje)
            
            # notificacion_vehiculos_email(request, vehiculo, "actualizado")
            return JsonResponse({'success': True})
        else: 
            return JsonResponse({'success': False, 'error': 'Rut incorrecto'}, status=400)

@login_required
@vehicular_avanzado_required
def hide_options_vehicle(request):
    if request.method == 'POST':
        tipo = request.POST['tipo_vehiculo']
        opciones = OcultarOpcionesVehiculo.objects.get(tipo_vehiculo=tipo)
        opciones_dict = serializers.serialize('python', [opciones])[0]['fields']      
        data = {
            'opciones': opciones_dict,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

@login_required
@vehicular_admin_db_required
def save_penalty(request):
    if request.method == 'POST':
        vehiculo = Vehiculo.objects.get(placaPatente=request.POST['patente'])
        infraccion = InfraccionesVehiculo(
            vehiculo = vehiculo,
            fechaInfraccion = request.POST['fecha'],
            ciudadInfraccion = request.POST['ciudad'], 
            infraccion = request.POST['infraccion'],
            estadoPagoInfraccion = request.POST['estado'],
            valorInfraccion = request.POST['valor'],            
        )
        infraccion.save()
        return JsonResponse({'success': 'Multa Creada'}, status=200)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

@login_required
@vehicular_basico_required
def new_kilometraje_register(request):
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    if usuario.faena.faena == "SIN ASIGNAR":
        vehiculos = Vehiculo.objects.filter(status=True).exclude(tipo=7).order_by('-placaPatente')
    else:
        asignados = VehiculoAsignado.objects.filter(faena=usuario.faena, status=True).exclude(vehiculo__tipo=7).order_by('-vehiculo')
        vehiculos = [asignado.vehiculo for asignado in asignados]
    context = {
        'formnuevokilometraje': FormNuevoKilometraje(vehiculos=vehiculos),   
        'sidebar': 'new_kilometraje_register',
        'sidebarmain': 'system_vehicles',
    }
    return render(request,'pages/vehicle/new_kilometraje.html', context)

@login_required
@vehicular_basico_required
def save_new_kilometraje_register(request):
    if request.method == 'POST':
        vehiculo = Vehiculo.objects.get(id= request.POST['vehiculo'])   
        registro = NuevoKilometraje(
            vehiculo = vehiculo,
            kilometraje = request.POST['kilometraje'],
            creador = request.user.get_full_name() or request.user.username,
            origen = "Formulario"
        )
        registro.save()  
            
        return JsonResponse({'success': True})
    else:
        return redirect('new_kilometraje_register')

@login_required
@vehicular_avanzado_required
def vehicle_pdf_view(request):
    if request.method == 'POST':
        vehiculo = get_object_or_404(Vehiculo, placaPatente=request.POST['placaPatente'])
        tipo_str = getattr(vehiculo.tipo, 'tipo', str(vehiculo.tipo)) if vehiculo.tipo else ""
        opciones = OcultarOpcionesVehiculo.objects.filter(
            Q(tipo_vehiculo=tipo_str) | Q(tipo_vehiculo=vehiculo.tipo)
        ).first()

        vehiculoDocumentacion = DocumentacionesVehiculo.objects.get(vehiculo_id=vehiculo.id)
        vehiculoInformacion = InformacionTecnicaVehiculo.objects.get(vehiculo_id=vehiculo.id)
        current_datetime = datetime.now()
        document_fields = [
            'fotografiaFacturaCompra', 'fotografiaPadron', 'fotografiaPermisoCirculacion', 'fotografiaRevisionTecnica', 
            'fotografiaRevisionTecnicaGases', 'fotografiaSeguroObligatorio', 'fotografiaSeguroAutomotriz', 'fotografiaCertificadoGps', 
            'fotografiaCertificadoMantencion', 'fotografiaCertificadoOperatividad', 'fotografiaCertificadoGrua', 
            'fotografiaCertificadoLamina', 'fotografiaDocumentacionMiniBus', 'fotografiaCertificadoBarraAntiVuelco', 
            'fotografiaInteriorTablero', 'fotografiaInteriorCopiloto', 'fotografiaInteriorAtrasPiloto', 
            'fotografiaInteriorAtrasCopiloto', 'fotografiaExteriorFrontis', 'fotografiaExteriorAtras', 
            'fotografiaExteriorPiloto', 'fotografiaExteriorCopiloto', 'fotografiaTraspasoVenta'
        ]

        mapeo_nombres_historial = {
            'fotografiaPadron': 'Padrón Vehicular',
            'fotografiaPermisoCirculacion': 'Permiso de Circulación',
            'fotografiaRevisionTecnica': 'Revisión Técnica',
            'fotografiaRevisionTecnicaGases': 'Revisión Técnica de Gases',
            'fotografiaSeguroObligatorio': 'Seguro Obligatorio (SOAP)',
            'fotografiaSeguroAutomotriz': 'Seguro Automotriz',
            'fotografiaCertificadoGps': 'Certificado GPS',
            'fotografiaCertificadoMantencion': 'Certificado Mantención',
            'fotografiaCertificadoOperatividad': 'Certificado Operatividad',
            'fotografiaCertificadoGrua': 'Certificado Grúa',
            'fotografiaCertificadoLamina': 'Certificado de Lámina',
            'fotografiaCertificadoBarraAntiVuelco': 'Certificado Barra AntiVuelco',
            'fotografiaDocumentacionMiniBus': 'Documentación Transp. Privado',
            'fotografiaFacturaCompra': 'Factura de Compra',
            'fotografiaTraspasoVenta': 'Traspaso/Venta',
        }

        mapeo_fechas_vehiculo = {
            'fotografiaFacturaCompra': 'fechaVencimientoFacturaCompra',
            'fotografiaPermisoCirculacion': 'fechaVencimientoPermisoCirculacion',
            'fotografiaRevisionTecnica': 'fechaVencimientoRevisionTecnica',
            'fotografiaRevisionTecnicaGases': 'fechaVencimientoRevisionTecnicaGases',
            'fotografiaSeguroObligatorio': 'fechaVencimientoSeguroObligatorio',
            'fotografiaSeguroAutomotriz': 'fechaVencimientoSeguroAutomotriz',
            'fotografiaCertificadoGps': 'fechaInstalacionGps',
            'fotografiaCertificadoMantencion': 'fechaVencimientoCertificadoMantencion',
            'fotografiaCertificadoOperatividad': 'fechaVencimientoCertificadoOperatividad',
            'fotografiaCertificadoGrua': 'fechaVencimientoCertificadoGrua',
            'fotografiaCertificadoLamina': 'fechaVencimientoLamina',
            'fotografiaCertificadoBarraAntiVuelco': 'fechaInstalacionBarraAntiVuelco',
            'fotografiaDocumentacionMiniBus': 'fechaVencimientoTransportePrivado',
            'fotografiaTraspasoVenta': 'fechaVencimientoTraspasoVenta',
        }

        documentos_list = []

        for field in document_fields:
            if getattr(opciones, field, "Si") == "Si":
                file_field = getattr(vehiculoDocumentacion, field, None)
                field_name = vehiculoDocumentacion._meta.get_field(field).verbose_name
                
                tiene_imagen = False
                archivo_url = ""
                if file_field and getattr(file_field, 'name', None) and 'no-imagen' not in str(file_field.name):
                    tiene_imagen = True
                    archivo_url = f"{request.scheme}://{request.get_host()}{file_field.url}"
                
                doc_name_historial = mapeo_nombres_historial.get(field, field_name)
                historial = HistorialDocumentacionVehiculo.objects.filter(
                    vehiculo=vehiculo
                ).filter(
                    Q(documento_modificado=doc_name_historial) | Q(documento_modificado=field_name)
                ).order_by('-fechacreacion')

                nombre_campo_fecha = mapeo_fechas_vehiculo.get(field)
                fecha_venc = getattr(vehiculo, nombre_campo_fecha, None) if nombre_campo_fecha else None

                documentos_list.append({
                    'nombre': field_name,
                    'estado': "Subido" if tiene_imagen else "Sin Imagen",
                    'vencimiento': fecha_venc,
                    'archivo_url': archivo_url,
                    'historial': historial,
                })

        perfil = getattr(request.user, 'usuarioprofile', None)
        context = {
            'vehiculo': vehiculo,
            'opciones': opciones,
            'informacion': vehiculoInformacion,
            'documentacion': vehiculoDocumentacion,
            'documentos': documentos_list,
            'user_role': perfil.seccionVehicular if perfil else 'SIN ASIGNAR',
            'current_datetime': current_datetime,
            'request': request,
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
                return JsonResponse({'error': 'Error al generar el PDF'}, status=500)

        pdf_url = os.path.join(settings.MEDIA_URL, 'pdfs_temp', filename)
        return JsonResponse({'pdf_url': pdf_url, 'message': 'Documento PDF creado con éxito'})
    else:
        return redirect('manage_vehicles')

@login_required
@vehicular_admin_db_required
def report_vehicles_kilometrajes(request): 
    context = {
        'sidebar': 'report_vehicles_kilometrajes',
        'sidebarmain': 'system_report_vehicles',
    }
    return render(request,'pages/vehicle/report/report_vehicles_kilometrajes.html', context)

@login_required
@vehicular_admin_db_required
def report_vehicles_general(request): 
    context = {
        'sidebar': 'report_vehicles_general',
        'sidebarmain': 'system_report_vehicles',
    }
    return render(request,'pages/vehicle/report/report_vehicles_general.html', context)

@login_required
@vehicular_admin_db_required
def report_vehicles_faenas(request): 
    context = {
        'sidebar': 'report_vehicles_faenas',
        'sidebarmain': 'system_report_vehicles',
    }
    return render(request,'pages/vehicle/report/report_vehicles_faenas.html', context)

@login_required
@vehicular_admin_db_required
def report_vehicles_camionetas_ano(request): 
    context = {
        'sidebar': 'report_vehicles_camionetas_ano',
        'sidebarmain': 'system_report_vehicles',
    }
    return render(request,'pages/vehicle/report/report_vehicles_camionetas_ano.html', context)

@login_required
@vehicular_admin_db_required
def report_vehicles_camionetas_faenas(request): 
    context = {
        'sidebar': 'report_vehicles_camionetas_faenas',
        'sidebarmain': 'system_report_vehicles',
    }
    return render(request,'pages/vehicle/report/report_vehicles_camionetas_faenas.html', context)


@login_required
@vehicular_avanzado_required
def manage_fuel_cards(request):
    usuario = UsuarioProfile.objects.get(user=request.user.id)
    
    if usuario.faena.faena == "SIN ASIGNAR":
        tarjeta = list(NuevaTarjetaCombustible.objects.filter(actual=True).order_by('-fechacreacion'))
    else:
        tarjeta = list(NuevaTarjetaCombustible.objects.filter(faena=usuario.faena, actual=True).order_by('-fechacreacion')) 

    completados = Vehiculo.objects.all()

    context = {
        'tarjetas': tarjeta,  
        'porcentajes': completados,
        'sidebar': 'manage_fuel_cards',
        'sidebarmain': 'system_vehicles',  
    }
    return render(request, 'pages/vehicle/manage_fuel_cards.html', context)

@login_required
@vehicular_avanzado_required
def new_fuel_cards(request):

    form = FormNuevaFuelCards(user=request.user)  
     
    context = {
        'formnuevafuelcards': form,
        'sidebar': 'manage_fuel_cards',
        'sidebarmain': 'system_vehicles',
    }
    return render(request,'pages/vehicle/new_fuel_cards.html', context)

@login_required
def cargar_informacion_vehiculo(request):
    vehiculo_id = request.GET.get('vehiculo_id')
    vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    faena = VehiculoAsignado.objects.get(vehiculo=vehiculo, status=True)
    data = {
        'faena': faena.faena.faena,
        'placaPatente': vehiculo.placaPatente,
        'tipoVehiculo': vehiculo.tipo.tipo,
        'nombrePropietario': vehiculo.nombrePropietario,
        'rutPropietario': vehiculo.rutPropietario,
    }
    return JsonResponse(data, safe=False)

@login_required
@vehicular_admin_db_required
def save_new_fuel_cards(request): 
    if request.method == 'POST':
        vehiculo = Vehiculo.objects.get(id=request.POST['vehiculo'])
        vehiculo_id = int(request.POST['vehiculo'])  
        vehiculo = get_object_or_404(Vehiculo, id=vehiculo_id)
        if NuevaTarjetaCombustible.objects.filter(vehiculo=vehiculo).exists():
            return JsonResponse({'success': False, 'error': 'Este vehículo ya tiene una tarjeta registrada.'}, status=400)
        form = FormNuevaFuelCards(request.POST)
        if form.is_valid():
            nueva_tarjeta = form.save(commit=False)
            nueva_tarjeta.patente = vehiculo.placaPatente
            nueva_tarjeta.actual = True
            nueva_tarjeta.status = True
            nueva_tarjeta.creador = request.user.get_full_name() or request.user.username
            nueva_tarjeta.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)   
      
    else:
        return redirect('new_fuel_cards')

@login_required 
@vehicular_admin_db_required
def status_fuel_cards(request):
    if request.method == 'POST': 
        tarjeta = NuevaTarjetaCombustible.objects.get(id=request.POST['id'])
        if (tarjeta.status): 
            NuevaTarjetaCombustible.objects.filter(id=request.POST['id']).update(status=False)
            notificacion_mantenedor_email(request,tarjeta,'secciones','deshabilitada')  
            messages.success(request, 'seccion Deshabilitado Correctamente')  
        else:
            NuevaTarjetaCombustible.objects.filter(id=request.POST['id']).update(status=True)
            notificacion_mantenedor_email(request,tarjeta,'secciones','habilitada')  
            messages.success(request, 'seccion Habilitado Correctamente') 
        return redirect('manage_fuel_cards')

@login_required
@vehicular_avanzado_required
def edit_fuel_card(request, card_id):
    try:
        tarjeta = NuevaTarjetaCombustible.objects.get(id=card_id)
    except NuevaTarjetaCombustible.DoesNotExist:
        return redirect('manage_fuel_cards')

    form = FormNuevaFuelCards(instance=tarjeta)

    historial_tarjetas = NuevaTarjetaCombustible.objects.filter(patente=tarjeta.patente).order_by('-fechacreacion')
    context = {
        'form': form,
        'tarjeta': tarjeta,
        'historial_tarjetas': historial_tarjetas, 
    }

    return render(request, 'pages/vehicle/edit_fuel_card.html', context)

@login_required
@vehicular_avanzado_required
def save_edit_fuel_card(request, card_id):
    try:
        tarjeta_actual = NuevaTarjetaCombustible.objects.get(id=card_id)
    except NuevaTarjetaCombustible.DoesNotExist:
        return JsonResponse({'success': False, 'error': "La tarjeta de combustible no existe."}, status=404)

    if request.method == 'POST':
        form = FormNuevaFuelCards(request.POST)
        if form.is_valid():
            tarjeta_actual.actual = False
            tarjeta_actual.save()

            vehiculo = Vehiculo.objects.get(id=request.POST['vehiculo'])
            nueva_tarjeta = form.save(commit=False)
            nueva_tarjeta.patente = vehiculo.placaPatente
            nueva_tarjeta.actual = True
            nueva_tarjeta.status = True
            nueva_tarjeta.creador = request.user.get_full_name() or request.user.username
            nueva_tarjeta.save()
            Vehiculo.objects.filter(id=request.POST['vehiculo']).update(tarjetaCombustible=request.POST['numeroTarjeta'])

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

    return redirect('edit_fuel_card', card_id=card_id)

@login_required
@vehicular_avanzado_required
def fuel_cards_pdf_view(request):
    if request.method == 'POST':
        tarjeta = get_object_or_404(NuevaTarjetaCombustible, id=request.POST['id']) 
        current_datetime = datetime.now() 
        
        perfil = getattr(request.user, 'usuarioprofile', None)
        context = {
            'tarjeta': tarjeta,
            'user_role': perfil.seccionVehicular if perfil else 'SIN ASIGNAR',
            'current_datetime': current_datetime,
        }
        
        template_path = 'pages/pdfs/card_pdf_template.html'
        template = get_template(template_path)
        html = template.render(context)
        
        filename = f'{tarjeta.patente}-{current_datetime.strftime("%Y%m%d_%H%M%S")}.pdf'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)

        return response
    else:
        return redirect('manage_fuel_cards')


@login_required
@mantenedor_sistema_required
def manage_brand_sleepiness(request): 
    lista = list(MarcaSomnolencia.objects.all().order_by('marca'))  
    context = {
        'dispositivos': lista,
        'sidebarmenu': 'manage_vehicles',
        'sidebarsubmenu': 'manage_sleepiness',
        'sidebarsubsubmenu': 'manage_brand_sleepiness',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/vehicle/manage_brand_sleepiness.html', context)

@login_required
@mantenedor_sistema_required
def new_brand_sleepiness(request):      
    context = {
        'formnuevamarca': FormMarcaSomnolencia,
        'sidebarmenu': 'manage_vehicles',
        'sidebarsubmenu': 'manage_sleepiness',
        'sidebarsubsubmenu': 'manage_brand_sleepiness',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/vehicle/new_brand_sleepiness.html', context)

@login_required
@mantenedor_sistema_required
def save_new_brand_sleepiness(request):
    if request.method == 'POST':
        try: 
            marca = MarcaSomnolencia.objects.get(marca=request.POST['marca'])
            return marca
        except ObjectDoesNotExist:            
            formulario = FormMarcaSomnolencia(data=request.POST)
            if formulario.is_valid():        
                documento = MarcaSomnolencia(
                    marca = request.POST['marca'],
                    status = True,
                    creador = request.user.get_full_name() or request.user.username,
                )
                documento.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_brand_sleepiness')

@login_required
@mantenedor_sistema_required
def status_brand_sleepiness(request):
    if request.method == 'POST': 
        marca = MarcaSomnolencia.objects.get(id=request.POST['id'])
        if (marca.status): 
            MarcaSomnolencia.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Proveedor de Equipo Deshabilitado Correctamente')  
        else:
            MarcaSomnolencia.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Proveedor de Equipo Habilitado Correctamente') 
        return redirect('manage_brand_sleepiness')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_brand_sleepiness') 

@login_required
@mantenedor_sistema_required
def edit_brand_sleepiness(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = MarcaSomnolencia.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormMarcaSomnolencia(initial={
            'marca': documento.marca,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_vehicles',
        'sidebarsubmenu': 'manage_sleepiness',
        'sidebarsubsubmenu': 'manage_brand_sleepiness',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/vehicle/edit_brand_sleepiness.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_brand_sleepiness(request):     
    if request.method == 'POST':
        MarcaSomnolencia.objects.filter(id=request.POST['id']).update(marca=request.POST['marca'])
        return JsonResponse({'success': True})
    else:
        return redirect('edit_brand_sleepiness')

@login_required
@mantenedor_sistema_required
def manage_model_sleepiness(request): 
    lista = list(ModeloSomnolencia.objects.all().order_by('marca'))  
    context = {
        'dispositivos': lista,
        'sidebarmenu': 'manage_vehicles',
        'sidebarsubmenu': 'manage_sleepiness',
        'sidebarsubsubmenu': 'manage_model_sleepiness',
        'sidebarmain': 'manage_system', 
    }
    return render(request,'pages/vehicle/manage_model_sleepiness.html', context)

@login_required
@mantenedor_sistema_required
def new_model_sleepiness(request):      
    context = {
        'formnuevomodelo': FormModeloSomnolencia,
        'sidebarmenu': 'manage_vehicles',
        'sidebarsubmenu': 'manage_sleepiness',
        'sidebarsubsubmenu': 'manage_model_sleepiness',
        'sidebarmain': 'manage_system',
    }
    return render(request,'pages/vehicle/new_model_sleepiness.html', context)

@login_required
@mantenedor_sistema_required
def save_new_model_sleepiness(request):
    if request.method == 'POST':
        marca = MarcaSomnolencia.objects.get(id=request.POST['marca'])
        formulario = FormModeloSomnolencia(data=request.POST)
        if formulario.is_valid():        
            documento = ModeloSomnolencia(
                marca = marca,
                modelo = request.POST['modelo'],
                status = True,
                creador = request.user.get_full_name() or request.user.username,
            )
            documento.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'El formulario no es válido.'})
    else:
        messages.error(request, 'Error en la Acción')
        return redirect('manage_model_sleepiness')

@login_required
@mantenedor_sistema_required
def status_model_sleepiness(request):
    if request.method == 'POST': 
        modelo = ModeloSomnolencia.objects.get(id=request.POST['id'])
        if (modelo.status): 
            ModeloSomnolencia.objects.filter(id=request.POST['id']).update(status=False)
            messages.success(request, 'Modelo Somnolencia Deshabilitada Correctamente')  
        else:
            ModeloSomnolencia.objects.filter(id=request.POST['id']).update(status=True)
            messages.success(request, 'Modelo Somnolencia Habilitada Correctamente') 
        return redirect('manage_model_sleepiness')
    else:
        messages.error(request, 'Error en la Acción') 
        return redirect('manage_model_sleepiness') 

@login_required
@mantenedor_sistema_required
def edit_model_sleepiness(request):  
    try:
        request.session['edit_id'] = request.POST['id']            
    except MultiValueDictKeyError:
        request.session['edit_id'] = request.session['edit_id']
    documento = ModeloSomnolencia.objects.get(id=request.session['edit_id'])
    context = {
        'formeditar':  FormModeloSomnolencia(initial={
            'zapata': documento.zapata,
            },
        ),
        'documento_id': documento.id,
        'sidebarmenu': 'manage_vehicles',
        'sidebarsubmenu': 'manage_sleepiness',
        'sidebarsubsubmenu': 'manage_model_sleepiness',
        'sidebarmain': 'manage_system',  
    }
    return render(request,'pages/vehicle/edit_model_sleepiness.html', context)

@login_required
@mantenedor_sistema_required
def save_edit_model_sleepiness(request):     
    if request.method == 'POST':
        ModeloSomnolencia.objects.filter(id=request.POST['id']).update(modelo=request.POST['modelo'])
        return JsonResponse({'success': True})
    else:
        return redirect('edit_model_sleepiness')


@login_required
@vehicular_avanzado_required
def manage_vehicles_por_faena(request):
    faena = request.POST.get('faena', '').strip()
    if not faena:
        return redirect('manage_vehicles')

    return redirect(f"{reverse('manage_vehicles')}?faena={faena}")

@login_required
@vehicular_avanzado_required
def manage_vehicles_por_tipo(request):
    faena = request.POST.get('faena', '').strip()
    tipo = request.POST.get('tipo', '').strip()
    query = []

    if faena:
        query.append(f"faena={faena}")
    if tipo:
        query.append(f"tipo={tipo}")

    url = reverse('manage_vehicles')
    if query:
        url = f"{url}?{'&'.join(query)}"
    return redirect(url)

@login_required
@vehicular_admin_db_required
def update_penalty(request):
    if request.method == 'POST':
        try:
            infraccion_id = request.POST.get('id')
            nuevo_estado = request.POST.get('estado')
            nuevo_valor = request.POST.get('valor', '0')
            
            nuevo_valor_limpio = ''.join(filter(str.isdigit, str(nuevo_valor))) or '0'

            infraccion = InfraccionesVehiculo.objects.get(pk=infraccion_id)

            if infraccion.estadoPagoInfraccion in ['Pagada', 'Anulada']:
                return JsonResponse({
                    'success': False, 
                    'error': 'No es posible editar una infracción que ya está Pagada o Anulada.'
                }, status=403)
                
            infraccion.estadoPagoInfraccion = nuevo_estado
            infraccion.valorInfraccion = int(nuevo_valor_limpio)
            infraccion.save()
            
            return JsonResponse({'success': True})
        except InfraccionesVehiculo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Infracción no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido'}, status=405)