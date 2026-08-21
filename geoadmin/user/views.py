from datetime import datetime
from collections import defaultdict
import unicodedata
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from rut_chile import rut_chile
from .forms import (FormRegistro, FormRegistroExtra, FormRegistroSeccion, FormRegistroLicenciasUsuarioFecha, FormRegistroLicenciasUsuarioNoProfesionales, 
                    FormRegistroLicenciasUsuarioProfesionales, FormRegistroLicenciasUsuarioProfesionalesAntiguas, FormDocumentacionUsuario,
                    FormRegistroInformacionLaboral)
from .models import Usuario, UsuarioProfile, LicenciasUsuario, DocumentacionUsuario, User, UserInformacionLaboral
from core.models import Ciudad, Nacionalidad, Genero, Faena, TipoDocumentoFaenaGeneral
from core.utils import procesar_fotografia
from prevencion.models import VigilanciaArea, VigilanciaGes, VigilanciaCargo, VigilanciaTipoContrato, VigilanciaContrato
from drilling.models import ReportesOperacionales, ControlesHorarios
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import BadHeaderError
from django.db.models import Q
from django.http import JsonResponse
from messenger.views import notificacion_mi_usuario_email
from messenger.utils import notify_group, get_changes_message
from core.decorators import admin_or_base_datos_required
import json
import requests
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.db import transaction


def _normalizar_texto_persona(valor):
    texto = " ".join((valor or "").split()).strip()
    if not texto:
        return ""
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(ch for ch in texto if not unicodedata.combining(ch))
    return texto.casefold()


def _obtener_nombre_usuario(usuario):
    nombre = " ".join(
        parte.strip()
        for parte in [usuario.first_name or '', usuario.last_name or '']
        if parte and parte.strip()
    ).strip()
    return nombre if nombre else (usuario.username or '')


def _parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_seconds(time_value):
    if not time_value:
        return 0
    return (time_value.hour * 3600) + (time_value.minute * 60) + time_value.second


def _format_hh_mm(total_seconds):
    total_seconds = int(total_seconds or 0)
    horas = total_seconds // 3600
    minutos = (total_seconds % 3600) // 60
    return f"{horas:02d}:{minutos:02d}"


def _format_horas_perforacion(total_seconds):
    if int(total_seconds or 0) > 0:
        return _format_hh_mm(total_seconds)
    return "-"


def _contiene_perforacion(texto):
    if not texto:
        return False
    normalizado = unicodedata.normalize('NFKD', str(texto))
    normalizado = ''.join(ch for ch in normalizado if not unicodedata.combining(ch))
    return 'perfor' in normalizado.casefold()


def _build_sondaje_data(reporte):
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


def _construir_contexto_uso_perforista(usuario, request):
    es_perforista = False
    if hasattr(usuario, 'usuarioprofile') and usuario.usuarioprofile:
        es_perforista = usuario.usuarioprofile.seccionSondaje == 'PERFORISTA'

    contexto = {
        'mostrar_tab_perforista': es_perforista,
        'estadisticas_uso_perforista': {
            'total_reportes': 0,
            'horas_perforacion': '-',
            'total_metros_perforados': '0.00',
            'promedio_metros_dia': '0.00',
            'ultimo_uso': None,
            'reportes_recientes': [],
        },
        'filtros_uso_perforista': {
            'anio': '',
            'mes': '',
            'sondaje': '',
            'turno': '',
        },
        'opciones_filtros_uso_perforista': {
            'anios': [],
            'meses': [],
            'sondajes': [],
            'turnos': [],
        },
        'payload_uso_perforista': {
            'total_reportes': 0,
            'horas_perforacion': '-',
            'total_metros_perforados': '0.00',
            'promedio_metros_dia': '0.00',
            'ultimo_uso': None,
            'reportes_recientes': [],
            'filtros_uso_perforista': {
                'anio': '',
                'mes': '',
                'sondaje': '',
                'turno': '',
            },
            'opciones_filtros_uso_perforista': {
                'anios': [],
                'meses': [],
                'sondajes': [],
                'turnos': [],
            },
        },
    }

    if not contexto['mostrar_tab_perforista']:
        return contexto

    nombre_usuario = _obtener_nombre_usuario(usuario)
    reportes_qs = (
        ReportesOperacionales.objects.filter(
            status=True,
            progreso='Aprobado',
        )
        .select_related('sondajeCodigo__faena', 'perforista')
        .order_by('-fechacreacion')
    )

    query_nombre = Q()
    if nombre_usuario:
        query_nombre |= Q(perforista__perforista__iexact=nombre_usuario)
    if usuario.username and usuario.username != nombre_usuario:
        query_nombre |= Q(perforista__perforista__iexact=usuario.username)

    reportes_base = list(reportes_qs.filter(query_nombre)) if query_nombre else []

    candidatos_nombre = {
        _normalizar_texto_persona(nombre_usuario),
        _normalizar_texto_persona(usuario.username),
    } - {''}

    reportes_aprobados_todos = reportes_base
    if not reportes_aprobados_todos and candidatos_nombre:
        reportes_aprobados_todos = [
            reporte for reporte in reportes_qs
            if _normalizar_texto_persona(getattr(reporte.perforista, 'perforista', '')) in candidatos_nombre
        ]

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

    if filtros_actuales['anio'] and _parse_int(filtros_actuales['anio']) is None:
        filtros_actuales['anio'] = ''

    if filtros_actuales['mes']:
        mes_int = _parse_int(filtros_actuales['mes'])
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

        sondaje_nombre, sondaje_key = _build_sondaje_data(reporte)
        turno_value = str(reporte.turno or '')
        turno_label = reporte.get_turno_display() if reporte.turno else 'Sin turno'

        reportes_enriquecidos.append({
            'reporte': reporte,
            'anio': str(fecha_reporte.year) if fecha_reporte else '',
            'mes': str(fecha_reporte.month) if fecha_reporte else '',
            'sondaje_key': sondaje_key,
            'sondaje_label': sondaje_nombre,
            'turno_value': turno_value,
            'turno_label': turno_label,
        })

    opciones_filtros_uso_perforista = {}
    for _ in range(4):
        opciones_filtros_uso_perforista = construir_opciones_filtros(reportes_enriquecidos, filtros_actuales)
        cambios = False
        for campo in ['anio', 'mes', 'sondaje', 'turno']:
            valor_actual = filtros_actuales.get(campo) or ''
            if valor_actual and not filtro_es_valido(campo, valor_actual, opciones_filtros_uso_perforista):
                filtros_actuales[campo] = ''
                cambios = True
        if not cambios:
            break
    else:
        opciones_filtros_uso_perforista = construir_opciones_filtros(reportes_enriquecidos, filtros_actuales)

    reportes_aprobados = [
        item['reporte']
        for item in reportes_enriquecidos
        if cumple_filtros_item(item, filtros_actuales)
    ]

    horas_perforacion_por_reporte = defaultdict(int)
    total_horas_perforacion_segundos = 0
    metros_por_dia_map = defaultdict(float)
    reportes_recientes = []

    reportes_ids = [reporte.id for reporte in reportes_aprobados]
    if reportes_ids:
        controles_horarios = ControlesHorarios.objects.filter(
            reporte_id__in=reportes_ids,
            status=True
        ).select_related('detalleControlHorario')
        for control in controles_horarios:
            detalle_nombre = control.detalleControlHorario.detalle if control.detalleControlHorario else ''
            if _contiene_perforacion(detalle_nombre):
                segundos = _to_seconds(control.total)
                total_horas_perforacion_segundos += segundos
                horas_perforacion_por_reporte[control.reporte_id] += segundos

    for reporte in reportes_aprobados:
        fecha_reporte = reporte.fechacreacion
        if fecha_reporte and timezone.is_aware(fecha_reporte):
            fecha_reporte = timezone.localtime(fecha_reporte)

        if fecha_reporte:
            metros_por_dia_map[fecha_reporte.date()] += float(reporte.totalPerforado or 0)

        faena_nombre = '-'
        if reporte.sondajeCodigo and reporte.sondajeCodigo.faena:
            faena_nombre = reporte.sondajeCodigo.faena.faena

        sondaje_nombre, _ = _build_sondaje_data(reporte)
        metros_reporte = float(reporte.totalPerforado or 0)

        reportes_recientes.append({
            'fecha': fecha_reporte,
            'faena': faena_nombre,
            'sondaje': sondaje_nombre,
            'turno': reporte.get_turno_display() if reporte.turno else 'Sin turno',
            'metros': f"{metros_reporte:.2f}",
            'horas_perforacion': _format_horas_perforacion(horas_perforacion_por_reporte.get(reporte.id)),
        })

    ultimo_uso = None
    if reportes_aprobados:
        ultimo = reportes_aprobados[0]
        fecha_ultimo = ultimo.fechacreacion
        if fecha_ultimo and timezone.is_aware(fecha_ultimo):
            fecha_ultimo = timezone.localtime(fecha_ultimo)

        ultimo_faena = '-'
        if ultimo.sondajeCodigo and ultimo.sondajeCodigo.faena:
            ultimo_faena = ultimo.sondajeCodigo.faena.faena

        ultimo_sondaje, _ = _build_sondaje_data(ultimo)

        ultimo_uso = {
            'fecha': fecha_ultimo,
            'faena': ultimo_faena,
            'turno': ultimo.get_turno_display() if ultimo.turno else 'Sin turno',
            'sondaje': ultimo_sondaje,
            'metros': f"{float(ultimo.totalPerforado or 0):.2f}",
        }

    promedio_metros_dia = 0
    if metros_por_dia_map:
        promedio_metros_dia = sum(metros_por_dia_map.values()) / len(metros_por_dia_map)

    total_metros_reportes = sum(float(reporte.totalPerforado or 0) for reporte in reportes_aprobados)

    estadisticas_uso_perforista = {
        'total_reportes': len(reportes_aprobados),
        'horas_perforacion': _format_horas_perforacion(total_horas_perforacion_segundos),
        'total_metros_perforados': f"{total_metros_reportes:.2f}",
        'promedio_metros_dia': f"{promedio_metros_dia:.2f}",
        'ultimo_uso': ultimo_uso,
        'reportes_recientes': reportes_recientes,
    }

    ultimo_uso_payload = None
    if ultimo_uso:
        ultimo_uso_payload = {
            'fecha': ultimo_uso['fecha'].strftime('%d/%m/%Y %H:%M') if ultimo_uso['fecha'] else '-',
            'faena': ultimo_uso.get('faena') or '-',
            'turno': ultimo_uso.get('turno') or '-',
            'sondaje': ultimo_uso.get('sondaje') or '-',
            'metros': ultimo_uso.get('metros') or '-',
        }

    reportes_payload = []
    for reporte in reportes_recientes:
        reportes_payload.append({
            'fecha': reporte['fecha'].strftime('%d/%m/%Y %H:%M') if reporte['fecha'] else '-',
            'faena': reporte.get('faena') or '-',
            'sondaje': reporte.get('sondaje') or '-',
            'turno': reporte.get('turno') or '-',
            'metros': reporte.get('metros') or '0.00',
            'horas_perforacion': reporte.get('horas_perforacion') or '-',
        })

    contexto.update({
        'estadisticas_uso_perforista': estadisticas_uso_perforista,
        'filtros_uso_perforista': filtros_actuales,
        'opciones_filtros_uso_perforista': opciones_filtros_uso_perforista,
        'payload_uso_perforista': {
            'total_reportes': estadisticas_uso_perforista['total_reportes'],
            'horas_perforacion': estadisticas_uso_perforista['horas_perforacion'],
            'total_metros_perforados': estadisticas_uso_perforista['total_metros_perforados'],
            'promedio_metros_dia': estadisticas_uso_perforista['promedio_metros_dia'],
            'ultimo_uso': ultimo_uso_payload,
            'reportes_recientes': reportes_payload,
            'filtros_uso_perforista': filtros_actuales,
            'opciones_filtros_uso_perforista': opciones_filtros_uso_perforista,
        },
    })

    return contexto


def validar_recaptcha(request):
    if not getattr(settings, "RECAPTCHA_ENABLED", True):
        return True, None

    secret_key = settings.RECAPTCHA_SECRET_KEY
    token = request.POST.get("g-recaptcha-response", "").strip()

    if not secret_key:
        return False, "Error de configuración de reCAPTCHA."
    if not token:
        return False, "Debes completar el reCAPTCHA."
    data = {
        "secret": secret_key,
        "response": token,
    }
    remote_ip = request.META.get("REMOTE_ADDR")
    if remote_ip:
        data["remoteip"] = remote_ip

    try:
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data=data,
            timeout=10
        )
        result = response.json()
    except requests.RequestException:
        return False, "No se pudo validar reCAPTCHA. Inténtalo nuevamente."
    if not result.get("success"):
        return False, "Validación reCAPTCHA fallida. Inténtalo nuevamente."
    return True, None

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm
    
    def post(self, request, *args, **kwargs):
        recaptcha_ok, recaptcha_error = validar_recaptcha(request)
        if not recaptcha_ok:
            messages.error(request, recaptcha_error)
            return self.form_invalid(self.get_form())
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY if getattr(settings, "RECAPTCHA_ENABLED", True) else ""
        return context
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('logincustom')

def register(request): 
    context = {
        'formregistro': FormRegistro,
        'sidebar': 'dashboard',
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY if getattr(settings, "RECAPTCHA_ENABLED", True) else "",
    }
    return render(request,'registration/register.html', context)

@login_required
@admin_or_base_datos_required
def new_user(request): 
    context = {
        'formregistro': FormRegistro,   
        'sidebar': 'manage_users',
        'sidebarmain': 'system_users',
    }
    return render(request,'pages/users/new_user.html', context)

def save_new_user(request): 
    origen = request.POST.get('ubicacion', None)
    
    if request.method == 'POST':        
        formulario = FormRegistro(data=request.POST)

        if origen != 'inside':
            recaptcha_ok, recaptcha_error = validar_recaptcha(request)
            if not recaptcha_ok:
                messages.error(request, recaptcha_error, extra_tags='Vuelva a intentarlo')
                context = {
                    'formregistro': formulario,
                    'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY if getattr(settings, "RECAPTCHA_ENABLED", True) else "",
                }
                return render(request, 'registration/register.html', context)
        
        if not formulario.is_valid():
            return error_campos_origen(request, origen, formulario)
            
        if not rut_chile.is_valid_rut(request.POST['username']):
            return error_rut_origen(request, origen, formulario)

        try:
            with transaction.atomic():
                Usuario.objects.create_user(
                    username = request.POST['username'],
                    first_name = request.POST['first_name'],
                    last_name = request.POST['last_name'],
                    password = request.POST['password1'],
                    phone = request.POST['phone'],
                    email = request.POST['email'],
                    role = "SIN ASIGNAR",
                    is_active = False,
                )
        
                usuario = Usuario.objects.get(username=request.POST['username'])

            try:
                if origen == 'inside':
                    notificacion_usuarios_email(request, usuario, "creado")
                else:
                    notificacion_usuarios_email(request, usuario, "creado")
                    notificacion_mi_usuario_email(request, usuario, "Usuario", "creado")
            except Exception as e_email:
                print(f"Alerta: Usuario creado pero falló envío de correo: {e_email}")

            if origen == 'inside':
                messages.success(request, 'Usuario Creado Correctamente', extra_tags='Recuerda habilitar el perfil creado')
                return redirect('manage_users')   
            else:
                messages.success(request, 'Usuario Creado Correctamente', extra_tags='Tu perfil será habilitado en las próximas horas')
                return redirect('logincustom')  

        except Exception as e:
            msg_error = f"Error del sistema: {str(e)}"

            if "UNIQUE constraint failed" in str(e) or "Duplicate entry" in str(e):
                if "email" in str(e):
                    msg_error = "Este correo electrónico ya está registrado."
                elif "phone" in str(e):
                    msg_error = "Este número de teléfono ya está registrado."
                elif "username" in str(e):
                    msg_error = "Este RUT ya se encuentra registrado."
            print(f"Error crítico al guardar usuario: {e}")
            messages.error(request, msg_error)
            formulario.add_error(None, msg_error)
            return error_campos_origen(request, origen, formulario)
            
    else:
        perfil_req = getattr(request.user, 'usuarioprofile', None)
        es_admin = perfil_req and perfil_req.seccionAdministracion in ['ADMINISTRADOR', 'BASE DATOS']
        if origen == 'inside' or (request.user.is_authenticated and es_admin):
            return redirect('new_user')
        else:
            return redirect('register')

def error_rut_origen(request,origen,formulario):
    if origen == 'inside':
        messages.error(request, "Rut incorrecto", extra_tags='Vuelva a intentarlo')
        context = {
            'formregistro': formulario,   
            'sidebar': 'manage_users',
            'sidebarmain': 'system_users',         
        }         
        return render(request,'pages/users/new_user.html',context)
    else:
        messages.error(request, "Rut incorrecto", extra_tags='Vuelva a intentarlo')
        context = {
            'formregistro': formulario,
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY if getattr(settings, "RECAPTCHA_ENABLED", True) else "",
        }         
        return render(request,'registration/register.html',context)

def error_campos_origen(request,origen,formulario):
    if origen == 'inside': 
        messages.error(request, "Corrija los datos incorrectos", extra_tags='Vuelva a intentarlo')
        context = {
            'formregistro': formulario,   
            'sidebar': 'manage_users',
            'sidebarmain': 'system_users',         
        }         
        return render(request,'pages/users/new_user.html',context)
    else:
        messages.error(request, "Corrija los datos incorrectos", extra_tags='Vuelva a intentarlo')
        context = {
            'formregistro': formulario,
            'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY if getattr(settings, "RECAPTCHA_ENABLED", True) else "",
        }         
        return render(request,'registration/register.html',context)

@login_required
@admin_or_base_datos_required
def manage_users(request):
    request.session.pop('edit_username',None)
    request.session.save()
    usuarios = list(Usuario.objects.all().order_by('-date_joined'))
    usuariosProfile = list(UsuarioProfile.objects.all())
    context = {
        'usuarios': usuarios,
        'usuariosProfile': usuariosProfile,
        'sidebar': 'manage_users',
        'sidebarmain': 'system_users',  
    }
    return render(request,'pages/users/manage_users.html', context)

@login_required
@admin_or_base_datos_required
def status_user(request):
    if request.method == 'POST': 
        usuario = Usuario.objects.get(username=request.POST['username'])
        user_name = request.user.get_full_name() or request.user.username
        if (usuario.is_active): 
            Usuario.objects.filter(username=request.POST['username']).update(is_active=False)
            subject = f'Usuario {usuario} deshabilitado'
            mensaje = f'Usuario: {usuario} \nDeshabilitado por: {user_name}'
            notify_group('usuarios', subject, mensaje)
            messages.success(request, 'Usuario Deshabilitado Correctamente')             
        else:         
            Usuario.objects.filter(username=request.POST['username']).update(is_active=True)
            subject = f'Usuario {usuario} habilitado'
            mensaje = f'Usuario: {usuario} \nHabilitado por: {user_name}'
            notify_group('usuarios', subject, mensaje)
            messages.success(request, 'Usuario Habilitado correctamente')  
        return redirect('manage_users') 

@login_required
@admin_or_base_datos_required
def edit_user_profile(request):
        try:
            request.session['edit_username'] = request.POST['username']          
        except MultiValueDictKeyError:
            request.session['edit_username'] = request.session['edit_username']
        usuario = Usuario.objects.get(username=request.session['edit_username'])
        contexto_uso_perforista = _construir_contexto_uso_perforista(usuario, request)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and contexto_uso_perforista['mostrar_tab_perforista']:
            return JsonResponse(contexto_uso_perforista['payload_uso_perforista'])
        usuarioProfile = UsuarioProfile.objects.get(user_id=usuario.id) 
        info_laboral, _ = UserInformacionLaboral.objects.get_or_create(user=usuario)
        usuarioLicencias = LicenciasUsuario.objects.get(user_id=usuario.id)  
        usuarioDocumentacion = DocumentacionUsuario.objects.get(user_id=usuario.id)  
        ciudad_actual = Ciudad.objects.filter(ciudad=usuarioProfile.ciudad)
        nacionalidad_actual = Nacionalidad.objects.filter(nacionalidad=usuarioProfile.nacionalidad)
        genero_actual = Genero.objects.filter(genero=usuarioProfile.genero)
        faena_actual = Faena.objects.filter(faena=usuarioProfile.faena)
        area_actual = VigilanciaArea.objects.filter(pk=info_laboral.area_id)
        ges_actual = VigilanciaGes.objects.filter(pk=info_laboral.ges_id)
        cargo_actual = VigilanciaCargo.objects.filter(pk=info_laboral.cargo_id)
        tipo_contrato_actual = (
            VigilanciaTipoContrato.objects.filter(pk=info_laboral.tipo_contrato_id)
        )
        contrato_actual = VigilanciaContrato.objects.filter(pk=info_laboral.contrato_id)
        
        urlUsuario = usuarioDocumentacion.fotografiaUsuario
        urlCedula = usuarioDocumentacion.fotografiaCedula
        urlLicencia = usuarioDocumentacion.fotografiaLicencia
        urlLicenciaInterna = usuarioDocumentacion.fotografiaLicenciaInterna
        if urlUsuario.url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg")):
            extensionUsuario = "imagen"
        elif urlUsuario.url.lower().endswith((".pdf")):
            extensionUsuario = "pdf"
        else:
            extensionUsuario = "otro"
        if urlCedula.url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg")):
            extensionCedula = "imagen"
        elif urlCedula.url.lower().endswith((".pdf")):
            extensionCedula = "pdf"
        else:
            extensionCedula = "otro"
        if urlLicencia.url.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg")):
            extensionLicencia = "imagen"
        elif urlLicencia.url.lower().endswith((".pdf")):
            extensionLicencia = "pdf"
        else:
            extensionLicencia = "otro"
        if urlLicenciaInterna.url.lower().endswith((".jpg", ".jpeg", ".png")):
            extensionLicenciaInterna = "imagen"
        elif urlLicenciaInterna.url.lower().endswith((".pdf")):
            extensionLicenciaInterna = "pdf"
        else:
            extensionLicenciaInterna = "otro"
        
        if not usuarioProfile.fechaNacimiento:
            fecha_nacimiento =""
        else:
            fecha_nacimiento_original = str(datetime.strftime(usuarioProfile.fechaNacimiento, "%Y-%m-%d"))
            fecha_nacimiento_formateada = datetime.strptime(fecha_nacimiento_original, "%Y-%m-%d")
            fecha_nacimiento = fecha_nacimiento_formateada.strftime('%Y-%m-%d')
        if not usuarioProfile.fechaCedulaVencimiento:
            fecha_cedula_vencimiento =""
        else:
            fecha_cedula_vencimiento_original = str(datetime.strftime(usuarioProfile.fechaCedulaVencimiento, "%Y-%m-%d"))
            fecha_cedula_vencimiento_formateada = datetime.strptime(fecha_cedula_vencimiento_original, "%Y-%m-%d")
            fecha_cedula_vencimiento = fecha_cedula_vencimiento_formateada.strftime('%Y-%m-%d')
        if not usuarioLicencias.fechaLicenciaVencimiento:
            fecha_licencia_vencimiento =""
        else:
            fecha_licencia_vencimiento_original = str(datetime.strftime(usuarioLicencias.fechaLicenciaVencimiento, "%Y-%m-%d"))
            fecha_licencia_vencimiento_formateada = datetime.strptime(fecha_licencia_vencimiento_original, "%Y-%m-%d")
            fecha_licencia_vencimiento = fecha_licencia_vencimiento_formateada.strftime('%Y-%m-%d')
        if not usuarioLicencias.fechaLicenciaInternaVencimiento:
            fecha_licencia_interna_vencimiento =""
        else:
            fecha_licencia_interna_vencimiento_original = str(datetime.strftime(usuarioLicencias.fechaLicenciaInternaVencimiento, "%Y-%m-%d"))
            fecha_licencia_interna_vencimiento_formateada = datetime.strptime(fecha_licencia_interna_vencimiento_original, "%Y-%m-%d")
            fecha_licencia_interna_vencimiento = fecha_licencia_interna_vencimiento_formateada.strftime('%Y-%m-%d')

        perfil_actual = getattr(request.user, 'usuarioprofile', None)
        seccion_activa = request.session.get('seccion', '')
        
        condicion = True
        
        if perfil_actual:
            roles_admin = ["ADMINISTRADOR", "BASE DATOS"]
            if seccion_activa == 'vehicular' and perfil_actual.seccionVehicular in roles_admin:
                condicion = False
            elif seccion_activa == 'sondaje' and perfil_actual.seccionSondaje in roles_admin:
                condicion = False
            elif seccion_activa == 'prevencion' and perfil_actual.seccionPrevencion in roles_admin:
                condicion = False
            elif seccion_activa == 'inventario' and perfil_actual.seccionInventario in roles_admin:
                condicion = False
            elif seccion_activa == 'administracion' and perfil_actual.seccionAdministracion in roles_admin:
                condicion = False
            elif request.user.is_superuser:
                condicion = False
                
        mostrar_secciones_admin = usuarioProfile.seccionAdministracion in ["ADMINISTRADOR", "BASE DATOS"]
        seccion_administracion = usuarioProfile.seccionAdministracion
        context = {
            'rut_username': usuario.username,
            'sidebar': 'manage_users',
            'sidebarmain': 'system_users',
            'usuario': usuario,
            'formregistro': FormRegistro(initial={
                'username': usuario.username,
                'first_name':usuario.first_name,
                'last_name': usuario.last_name,
                'email': usuario.email,
                'phone': usuario.phone,
                'role': usuario.usuarioprofile.seccionAdministracion,
                },
                ocultar_password=True,
                ocultar_role=True,
                username_disabled=True,
                first_name_disabled=condicion,
                last_name_disabled=condicion,
                phone_disabled=condicion,
                email_disabled=condicion,
                role_disabled=condicion,
            ),   
            'formregistroextra': FormRegistroExtra(initial={
                'ciudad': usuarioProfile.ciudad,
                'nacionalidad': usuarioProfile.nacionalidad,
                'genero': usuarioProfile.genero,
                'fechaNacimiento': fecha_nacimiento,
                'fechaCedulaVencimiento': fecha_cedula_vencimiento,
                'faena': usuarioProfile.faena,
                },
                ciudad_disabled=condicion,
                nacionalidad_disabled=condicion,
                genero_disabled=condicion,
                fechanacimiento_disabled=condicion,
                fechacedulavencimiento_disabled=condicion,
                faena_disabled=condicion,
                ciudad_actual=ciudad_actual,
                nacionalidad_actual=nacionalidad_actual,
                genero_actual=genero_actual,
                faena_actual=faena_actual,
            ),
            'formregistroseccion': FormRegistroSeccion(initial={
                'seccionVehicular': usuarioProfile.seccionVehicular,
                'seccionSondaje': usuarioProfile.seccionSondaje,
                'seccionPrevencion': usuarioProfile.seccionPrevencion,
                'seccionInventario': usuarioProfile.seccionInventario,
                'seccionAdministracion': seccion_administracion,
                },
                seccionVehicular_disabled=condicion,
                seccionSondaje_disabled=condicion,
                seccionPrevencion_disabled=condicion,
                seccionInventario_disabled=condicion,
                seccionAdministracion_disabled=condicion,
            ),
            'formregistroinformacionlaboral': FormRegistroInformacionLaboral(initial={
                'area': info_laboral.area,
                'ges': info_laboral.ges,
                'cargo': info_laboral.cargo,
                'tipo_contrato': info_laboral.tipo_contrato,
                'contrato': info_laboral.contrato,
                'fechaIngreso': info_laboral.fechaIngreso.strftime('%Y-%m-%d') if info_laboral.fechaIngreso else '',
                'fechaDesvinculacion': (
                    info_laboral.fechaDesvinculacion.strftime('%Y-%m-%d')
                    if info_laboral.fechaDesvinculacion else ''
                ),
                },
                area_disabled=condicion,
                ges_disabled=condicion,
                cargo_disabled=condicion,
                tipo_contrato_disabled=condicion,
                contrato_disabled=condicion,
                fecha_ingreso_disabled=condicion,
                fecha_desvinculacion_disabled=condicion,
                area_actual=area_actual,
                ges_actual=ges_actual,
                cargo_actual=cargo_actual,
                tipo_contrato_actual=tipo_contrato_actual,
                contrato_actual=contrato_actual,
            ),
            'formregistrolicenciasusuariofecha': FormRegistroLicenciasUsuarioFecha(initial={
                'fechaLicenciaVencimiento': fecha_licencia_vencimiento,
                'fechaLicenciaInternaVencimiento': fecha_licencia_interna_vencimiento,
                },
                fechalicenciavencimiento_disabled=condicion,
                fechalicenciainternavencimiento_disabled=condicion,
            ),
            'formregistrolicenciasusuarionoprofesionales': FormRegistroLicenciasUsuarioNoProfesionales(initial={
                'licenciaClaseB': usuarioLicencias.licenciaClaseB,                   
                'licenciaClaseC': usuarioLicencias.licenciaClaseC,
                'licenciaClaseD': usuarioLicencias.licenciaClaseD,
                'licenciaClaseE': usuarioLicencias.licenciaClaseE,
                'licenciaClaseF': usuarioLicencias.licenciaClaseF,
                },
                licenciaclaseb_disabled=condicion,
                licenciaclasec_disabled=condicion,
                licenciaclased_disabled=condicion,
                licenciaclasee_disabled=condicion,
                licenciaclasef_disabled=condicion,
            ),
            'formregistrolicenciasusuarioprofesionales': FormRegistroLicenciasUsuarioProfesionales(initial={
                'licenciaClaseA1': usuarioLicencias.licenciaClaseA1,                   
                'licenciaClaseA2': usuarioLicencias.licenciaClaseA2,
                'licenciaClaseA3': usuarioLicencias.licenciaClaseA3,
                'licenciaClaseA4': usuarioLicencias.licenciaClaseA4,
                'licenciaClaseA5': usuarioLicencias.licenciaClaseA5,
                },
                licenciaclasea1_disabled=condicion,
                licenciaclasea2_disabled=condicion,
                licenciaclasea3_disabled=condicion,
                licenciaclasea4_disabled=condicion,
                licenciaclasea5_disabled=condicion,
            ),
            'formregistrolicenciasusuarioprofesionalesantiguas': FormRegistroLicenciasUsuarioProfesionalesAntiguas(initial={
                'licenciaClaseA1Antigua': usuarioLicencias.licenciaClaseA1Antigua,          
                'licenciaClaseA2Antigua': usuarioLicencias.licenciaClaseA2Antigua,
                },
                licenciaclasea1antigua_disabled=condicion,
                licenciaclasea2antigua_disabled=condicion,
            ),    
            'formdocumentacionusuario': FormDocumentacionUsuario(initial={
                'fotografiaUsuario': usuarioDocumentacion.fotografiaUsuario,
                'fotografiaCedula': usuarioDocumentacion.fotografiaCedula,
                'fotografiaLicencia': usuarioDocumentacion.fotografiaLicencia,            
                },
            ),    
            'fotografiaUsuario': usuarioDocumentacion.fotografiaUsuario,            
            'fotografiaCedula': usuarioDocumentacion.fotografiaCedula,            
            'fotografiaLicencia': usuarioDocumentacion.fotografiaLicencia,   
            'fotografiaLicenciaInterna': usuarioDocumentacion.fotografiaLicenciaInterna, 
            'extensionUsuario': extensionUsuario,
            'extensionCedula': extensionCedula,
            'extensionLicencia': extensionLicencia,
            'extensionLicenciaInterna': extensionLicenciaInterna,
            'mostrar_secciones_admin': mostrar_secciones_admin,
            'mostrar_tab_perforista': contexto_uso_perforista['mostrar_tab_perforista'],
            'estadisticas_uso_perforista': contexto_uso_perforista['estadisticas_uso_perforista'],
            'filtros_uso_perforista': contexto_uso_perforista['filtros_uso_perforista'],
            'opciones_filtros_uso_perforista': contexto_uso_perforista['opciones_filtros_uso_perforista'],
        }
        return render(request,'pages/users/edit_user_profile.html', context)

@login_required
@admin_or_base_datos_required
def save_edit_user_profile(request):  
    if request.method == 'POST':
        usuario = Usuario.objects.get(username=request.POST['rut_username'])
        old_usuario = Usuario.objects.get(pk=usuario.pk)
        old_profile = UsuarioProfile.objects.get(user_id=usuario.id)
        Usuario.objects.filter(username=request.POST['rut_username']).update(first_name=request.POST['first_name'])
        Usuario.objects.filter(username=request.POST['rut_username']).update(last_name=request.POST['last_name'])
        try:
            Usuario.objects.filter(username=request.POST['rut_username']).update(phone=request.POST['phone']) 
        except:
            return JsonResponse({'titleText': "N° de Teléfono ya existe",'text': "Intenta nuevamente"}, status=400)
        try:
            Usuario.objects.filter(username=request.POST['rut_username']).update(email=request.POST['email']) 
        except:
            return JsonResponse({'titleText': "Dirección de Correo ya existe",'text': "Intenta nuevamente"}, status=400)
        try:
            UsuarioProfile.objects.filter(user_id=usuario.id).update(ciudad=request.POST['ciudad']) 
        except:
            pass
        try:
            UsuarioProfile.objects.filter(user_id=usuario.id).update(nacionalidad=request.POST['nacionalidad']) 
        except:
            pass
        try:
            UsuarioProfile.objects.filter(user_id=usuario.id).update(genero=request.POST['genero']) 
        except:
            pass
        try:
            UsuarioProfile.objects.filter(user_id=usuario.id).update(fechaNacimiento=request.POST['fechaNacimiento']) 
        except:
            pass
        try:
            UsuarioProfile.objects.filter(user_id=usuario.id).update(fechaCedulaVencimiento=request.POST['fechaCedulaVencimiento']) 
        except:
            pass
        try:
            UsuarioProfile.objects.filter(user_id=usuario.id).update(faena=request.POST['faena']) 
        except:
            pass
        
        UserInformacionLaboral.objects.update_or_create(
            user=usuario,
            defaults={
                'area_id': request.POST.get('area') or None,
                'ges_id': request.POST.get('ges') or None,
                'cargo_id': request.POST.get('cargo') or None,
                'tipo_contrato_id': request.POST.get('tipo_contrato') or None,
                'contrato_id': request.POST.get('contrato') or None,
                'fechaIngreso': request.POST.get('fechaIngreso') or None,
                'fechaDesvinculacion': request.POST.get('fechaDesvinculacion') or None,
            }
        )
        seccion_inventario_valor = request.POST.get('seccionInventario', 'SIN ASIGNAR')
        seccion_administracion_valor = request.POST.get('seccionAdministracion', 'SIN ASIGNAR')
         
        try:
            UsuarioProfile.objects.filter(user_id=usuario.id).update(
                seccionVehicular=request.POST.get('seccionVehicular', 'SIN ASIGNAR'),
                seccionSondaje=request.POST.get('seccionSondaje', 'SIN ASIGNAR'),
                seccionPrevencion=request.POST.get('seccionPrevencion', 'SIN ASIGNAR'),
                seccionInventario=seccion_inventario_valor,
                seccionAdministracion=seccion_administracion_valor,
            )
        except:
            return JsonResponse({'titleText': "Error al actualizar el Perfil",'text': "Intenta nuevamente"}, status=400)


        try:
            LicenciasUsuario.objects.filter(user_id=usuario.id).update(fechaLicenciaVencimiento=request.POST['fechaLicenciaVencimiento']) 
        except:
            LicenciasUsuario.objects.filter(user_id=usuario.id).update(fechaLicenciaVencimiento=None) 
        try:
            LicenciasUsuario.objects.filter(user_id=usuario.id).update(fechaLicenciaInternaVencimiento=request.POST['fechaLicenciaInternaVencimiento']) 
        except:
            LicenciasUsuario.objects.filter(user_id=usuario.id).update(fechaLicenciaInternaVencimiento=None)
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseB=request.POST['licenciaClaseB']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseC=request.POST['licenciaClaseC']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseD=request.POST['licenciaClaseD']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseE=request.POST['licenciaClaseE']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseF=request.POST['licenciaClaseF']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseA1=request.POST['licenciaClaseA1']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseA2=request.POST['licenciaClaseA2']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseA3=request.POST['licenciaClaseA3']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseA4=request.POST['licenciaClaseA4']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseA5=request.POST['licenciaClaseA5']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseA1Antigua=request.POST['licenciaClaseA1Antigua']) 
        LicenciasUsuario.objects.filter(user_id=usuario.id).update(licenciaClaseA2Antigua=request.POST['licenciaClaseA2Antigua']) 
         
        documentacionUsuario = DocumentacionUsuario.objects.get(user_id=usuario.id) 
        
        toggle_Usuario = request.POST.get('toggle-Usuario', 'no')
        procesar_fotografia(documentacionUsuario, toggle_Usuario, 'fotografiaUsuario','documentacion_usuario/no-avatar.png', request)
            
        toggle_Cedula = request.POST.get('toggle-Cedula', 'no')
        procesar_fotografia(documentacionUsuario, toggle_Cedula, 'fotografiaCedula','documentacion_usuario/no-imagen.png', request)
                
        toggle_Licencia = request.POST.get('toggle-Licencia', 'no')
        procesar_fotografia(documentacionUsuario, toggle_Licencia, 'fotografiaLicencia','documentacion_usuario/no-imagen.png', request)
        
        toggle_LicenciaInterna = request.POST.get('toggle-LicenciaInterna', 'no')
        procesar_fotografia(documentacionUsuario, toggle_LicenciaInterna, 'fotografiaLicenciaInterna','documentacion_usuario/no-imagen.png', request)

        documentacionUsuario.save()
        
        notificacion_mi_usuario_email(request, usuario,"Usuario", "actualizado")
        
        user_name = request.user.get_full_name() or request.user.username
        new_usuario = Usuario.objects.get(pk=usuario.pk)
        new_profile = UsuarioProfile.objects.get(user_id=usuario.id)
        changes_user = get_changes_message(old_usuario, new_usuario)
        changes_profile = get_changes_message(old_profile, new_profile)
        subject = f'Usuario {usuario} actualizado'
        mensaje = f'Usuario: {usuario}\nActualizado por: {user_name}'
        if changes_user:
            mensaje += changes_user
        if changes_profile:
            mensaje += changes_profile
        notify_group('usuarios', subject, mensaje)
        
        messages.success(request, 'Datos Actualizados Correctamente') 
        request.session.pop('edit_username',None)
        request.session.save()
        return redirect('manage_users') 
    
@login_required
def edit_my_profile(request):
    usuario = Usuario.objects.get(username=request.user.username)
    contexto_uso_perforista = _construir_contexto_uso_perforista(usuario, request)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and contexto_uso_perforista['mostrar_tab_perforista']:
        return JsonResponse(contexto_uso_perforista['payload_uso_perforista'])
    usuarioProfile = UsuarioProfile.objects.get(user_id=usuario.id)
    info_laboral, _ = UserInformacionLaboral.objects.get_or_create(user=usuario)
    usuarioLicencias, _ = LicenciasUsuario.objects.get_or_create(user_id=usuario.id)  
    usuarioDocumentacion, _ = DocumentacionUsuario.objects.get_or_create(user_id=usuario.id)  
    ciudad_actual = Ciudad.objects.filter(ciudad=usuarioProfile.ciudad)
    nacionalidad_actual = Nacionalidad.objects.filter(nacionalidad=usuarioProfile.nacionalidad)
    genero_actual = Genero.objects.filter(genero=usuarioProfile.genero)
    faena_actual = Faena.objects.filter(faena=usuarioProfile.faena)
    area_actual = VigilanciaArea.objects.filter(pk=info_laboral.area_id)
    ges_actual = VigilanciaGes.objects.filter(pk=info_laboral.ges_id)
    cargo_actual = VigilanciaCargo.objects.filter(pk=info_laboral.cargo_id)
    tipo_contrato_actual = VigilanciaTipoContrato.objects.filter(pk=info_laboral.tipo_contrato_id)
    contrato_actual = VigilanciaContrato.objects.filter(pk=info_laboral.contrato_id)
    tipoDocumentacionFaenaGeneral = TipoDocumentoFaenaGeneral.objects.filter(faena=usuarioProfile.faena)
    urlUsuario = usuarioDocumentacion.fotografiaUsuario
    urlCedula = usuarioDocumentacion.fotografiaCedula
    urlLicencia = usuarioDocumentacion.fotografiaLicencia
    urlLicenciaInterna = usuarioDocumentacion.fotografiaLicenciaInterna
    if urlUsuario.url.lower().endswith((".jpg", ".jpeg", ".png")):
        extensionUsuario = "imagen"
    elif urlUsuario.url.lower().endswith((".pdf")):
        extensionUsuario = "pdf"
    else:
        extensionUsuario = "otro"
    if urlCedula.url.lower().endswith((".jpg", ".jpeg", ".png")):
        extensionCedula = "imagen"
    elif urlCedula.url.lower().endswith((".pdf")):
        extensionCedula = "pdf"
    else:
        extensionCedula = "otro"
    if urlLicencia.url.lower().endswith((".jpg", ".jpeg", ".png")):
        extensionLicencia = "imagen"
    elif urlLicencia.url.lower().endswith((".pdf")):
        extensionLicencia = "pdf"
    else:
        extensionLicencia = "otro"        
    if urlLicenciaInterna.url.lower().endswith((".jpg", ".jpeg", ".png")):
        extensionLicenciaInterna = "imagen"
    elif urlLicenciaInterna.url.lower().endswith((".pdf")):
        extensionLicenciaInterna = "pdf"
    else:
        extensionLicenciaInterna = "otro"
   
    if not usuarioProfile.fechaNacimiento:
        fecha_nacimiento =""
    else:
        fecha_nacimiento_original = str(datetime.strftime(usuarioProfile.fechaNacimiento, "%Y-%m-%d"))
        fecha_nacimiento_formateada = datetime.strptime(fecha_nacimiento_original, "%Y-%m-%d")
        fecha_nacimiento = fecha_nacimiento_formateada.strftime('%Y-%m-%d')
    if not usuarioProfile.fechaCedulaVencimiento:
        fecha_cedula_vencimiento =""
    else:
        fecha_cedula_vencimiento_original = str(datetime.strftime(usuarioProfile.fechaCedulaVencimiento, "%Y-%m-%d"))
        fecha_cedula_vencimiento_formateada = datetime.strptime(fecha_cedula_vencimiento_original, "%Y-%m-%d")
        fecha_cedula_vencimiento = fecha_cedula_vencimiento_formateada.strftime('%Y-%m-%d')
    if not usuarioLicencias.fechaLicenciaVencimiento:
        fecha_licencia_vencimiento =""
    else:
        fecha_licencia_vencimiento_original = str(datetime.strftime(usuarioLicencias.fechaLicenciaVencimiento, "%Y-%m-%d"))
        fecha_licencia_vencimiento_formateada = datetime.strptime(fecha_licencia_vencimiento_original, "%Y-%m-%d")
        fecha_licencia_vencimiento = fecha_licencia_vencimiento_formateada.strftime('%Y-%m-%d')
    if not usuarioLicencias.fechaLicenciaInternaVencimiento:
        fecha_licencia_interna_vencimiento =""
    else:
        fecha_licencia_interna_vencimiento_original = str(datetime.strftime(usuarioLicencias.fechaLicenciaInternaVencimiento, "%Y-%m-%d"))
        fecha_licencia_interna_vencimiento_formateada = datetime.strptime(fecha_licencia_interna_vencimiento_original, "%Y-%m-%d")
        fecha_licencia_interna_vencimiento = fecha_licencia_interna_vencimiento_formateada.strftime('%Y-%m-%d')
      
    seccion_administracion = usuarioProfile.seccionAdministracion

    perfil = usuario.usuarioprofile
    mostrar_secciones_admin = perfil.seccionAdministracion in ["ADMINISTRADOR", "BASE DATOS"]
    context = {
        'rut_username': usuario.username,
        'faena': usuarioProfile.faena,
        'sidebar': 'dashboard',
        'formregistro': FormRegistro(initial={
            'username': usuario.username,
            'first_name':usuario.first_name,
            'last_name': usuario.last_name,
            'email': usuario.email,
            'phone': usuario.phone,
            'role': usuario.usuarioprofile.seccionAdministracion,
            },
            username_disabled=True,
            first_name_disabled=False,
            last_name_disabled=False,
            role_disabled=True,
            ocultar_password=True,
            ocultar_role=True,            
        ),   
        'formregistroextra': FormRegistroExtra(initial={
            'ciudad': usuarioProfile.ciudad,
            'nacionalidad': usuarioProfile.nacionalidad,
            'genero': usuarioProfile.genero,
            'fechaNacimiento': fecha_nacimiento,
            'fechaCedulaVencimiento': fecha_cedula_vencimiento,
            'faena': usuarioProfile.faena,
            },
            ciudad_disabled=False,
            nacionalidad_disabled=False,
            genero_disabled=False,
            faena_disabled=True,
            ciudad_actual=ciudad_actual,
            nacionalidad_actual=nacionalidad_actual,
            genero_actual=genero_actual,
            faena_actual=faena_actual,
        ),
        'formregistroinformacionlaboral': FormRegistroInformacionLaboral(
            initial={
                'area': info_laboral.area_id,
                'ges': info_laboral.ges_id,
                'cargo': info_laboral.cargo_id,
                'tipo_contrato': info_laboral.tipo_contrato_id,
                'contrato': info_laboral.contrato_id,
                'fechaIngreso': info_laboral.fechaIngreso.strftime('%Y-%m-%d') if info_laboral.fechaIngreso else '',
                'fechaDesvinculacion': (
                    info_laboral.fechaDesvinculacion.strftime('%Y-%m-%d')
                    if info_laboral.fechaDesvinculacion else ''
                ),
            },
            area_disabled=True,
            ges_disabled=True,
            cargo_disabled=True,
            tipo_contrato_disabled=True,
            contrato_disabled=True,
            fecha_ingreso_disabled=True,
            fecha_desvinculacion_disabled=True,
            area_actual=area_actual,
            ges_actual=ges_actual,
            cargo_actual=cargo_actual,
            tipo_contrato_actual=tipo_contrato_actual,
            contrato_actual=contrato_actual,
        ),
        'formregistroseccion': FormRegistroSeccion(initial={
            'seccionVehicular': usuarioProfile.seccionVehicular,
            'seccionSondaje': usuarioProfile.seccionSondaje,
            'seccionPrevencion': usuarioProfile.seccionPrevencion,
            'seccionInventario': usuarioProfile.seccionInventario,
            'seccionAdministracion': seccion_administracion,
            },
            seccionVehicular_disabled=True,
            seccionSondaje_disabled=True,
            seccionPrevencion_disabled=True,
            seccionInventario_disabled=True,
            seccionAdministracion_disabled=True,
        ),
        'formregistrolicenciasusuariofecha': FormRegistroLicenciasUsuarioFecha(initial={
            'fechaLicenciaVencimiento': fecha_licencia_vencimiento,
            'fechaLicenciaInternaVencimiento': fecha_licencia_interna_vencimiento,
            },
        ),
        'formregistrolicenciasusuarionoprofesionales': FormRegistroLicenciasUsuarioNoProfesionales(initial={
            'licenciaClaseB': usuarioLicencias.licenciaClaseB,                   
            'licenciaClaseC': usuarioLicencias.licenciaClaseC,
            'licenciaClaseD': usuarioLicencias.licenciaClaseD,
            'licenciaClaseE': usuarioLicencias.licenciaClaseE,
            'licenciaClaseF': usuarioLicencias.licenciaClaseF,
            },
        ),
        'formregistrolicenciasusuarioprofesionales': FormRegistroLicenciasUsuarioProfesionales(initial={
            'licenciaClaseA1': usuarioLicencias.licenciaClaseA1,         
            'licenciaClaseA2': usuarioLicencias.licenciaClaseA2,
            'licenciaClaseA3': usuarioLicencias.licenciaClaseA3,
            'licenciaClaseA4': usuarioLicencias.licenciaClaseA4,
            'licenciaClaseA5': usuarioLicencias.licenciaClaseA5,
            },
        ),
        'formregistrolicenciasusuarioprofesionalesantiguas': FormRegistroLicenciasUsuarioProfesionalesAntiguas(initial={
            'licenciaClaseA1Antigua': usuarioLicencias.licenciaClaseA1Antigua,  
            'licenciaClaseA2Antigua': usuarioLicencias.licenciaClaseA2Antigua,
            },
        ),  
        'fotografiaUsuario': usuarioDocumentacion.fotografiaUsuario,            
        'fotografiaCedula': usuarioDocumentacion.fotografiaCedula,            
        'fotografiaLicencia': usuarioDocumentacion.fotografiaLicencia,   
        'fotografiaLicenciaInterna': usuarioDocumentacion.fotografiaLicenciaInterna,
        'extensionUsuario': extensionUsuario,
        'extensionCedula': extensionCedula,
        'extensionLicencia': extensionLicencia,
        'extensionLicenciaInterna': extensionLicenciaInterna,
        'documentacionFaenaGeneral': tipoDocumentacionFaenaGeneral,
        'mostrar_secciones_admin': mostrar_secciones_admin,
        'mostrar_tab_perforista': contexto_uso_perforista['mostrar_tab_perforista'],
        'estadisticas_uso_perforista': contexto_uso_perforista['estadisticas_uso_perforista'],
        'filtros_uso_perforista': contexto_uso_perforista['filtros_uso_perforista'],
        'opciones_filtros_uso_perforista': contexto_uso_perforista['opciones_filtros_uso_perforista'],
    }
    return render(request,'pages/users/my_profile.html', context)

@login_required
def save_edit_my_profile(request):  
    if request.method == 'POST':
        old_user = Usuario.objects.get(username=request.user.username)
        old_profile = UsuarioProfile.objects.get(user_id=request.user.id)
        Usuario.objects.filter(username=request.user.username).update(first_name=request.POST['first_name'])
        Usuario.objects.filter(username=request.user.username).update(last_name=request.POST['last_name'])
        try:
            Usuario.objects.filter(username=request.user.username).update(phone=request.POST['phone']) 
        except:
            return JsonResponse({'titleText': "N° de Teléfono ya existe",'text': "Intenta nuevamente"}, status=400)
        try:
            Usuario.objects.filter(username=request.user.username).update(email=request.POST['email']) 
        except:
            return JsonResponse({'titleText': "Dirección de Correo ya existe",'text': "Intenta nuevamente"}, status=400)
        try:
            UsuarioProfile.objects.filter(user_id=request.user.id).update(ciudad=request.POST['ciudad']) 
        except:
            pass
        try:
            UsuarioProfile.objects.filter(user_id=request.user.id).update(nacionalidad=request.POST['nacionalidad']) 
        except:
            pass
        try:
            UsuarioProfile.objects.filter(user_id=request.user.id).update(genero=request.POST['genero']) 
        except:
            pass
        try:
            UsuarioProfile.objects.filter(user_id=request.user.id).update(fechaNacimiento=request.POST['fechaNacimiento']) 
        except:
            pass
        try:
            UsuarioProfile.objects.filter(user_id=request.user.id).update(fechaCedulaVencimiento=request.POST['fechaCedulaVencimiento']) 
        except:
            pass
        try:
            LicenciasUsuario.objects.filter(user_id=request.user.id).update(fechaLicenciaVencimiento=request.POST['fechaLicenciaVencimiento']) 
        except:
            LicenciasUsuario.objects.filter(user_id=request.user.id).update(fechaLicenciaVencimiento=None) 
        try:
            LicenciasUsuario.objects.filter(user_id=request.user.id).update(fechaLicenciaInternaVencimiento=request.POST['fechaLicenciaInternaVencimiento']) 
        except:
            LicenciasUsuario.objects.filter(user_id=request.user.id).update(fechaLicenciaInternaVencimiento=None) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseB=request.POST['licenciaClaseB']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseC=request.POST['licenciaClaseC']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseD=request.POST['licenciaClaseD']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseE=request.POST['licenciaClaseE']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseF=request.POST['licenciaClaseF']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseA1=request.POST['licenciaClaseA1']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseA2=request.POST['licenciaClaseA2']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseA3=request.POST['licenciaClaseA3']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseA4=request.POST['licenciaClaseA4']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseA5=request.POST['licenciaClaseA5']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseA1Antigua=request.POST['licenciaClaseA1Antigua']) 
        LicenciasUsuario.objects.filter(user_id=request.user.id).update(licenciaClaseA2Antigua=request.POST['licenciaClaseA2Antigua']) 
        documentacionUsuario = DocumentacionUsuario.objects.get(user_id=request.user.id) 
        
        toggle_Usuario = request.POST.get('toggle-Usuario', 'no')
        procesar_fotografia(documentacionUsuario, toggle_Usuario, 'fotografiaUsuario','documentacion_usuario/no-avatar.png', request)
                    
        toggle_Cedula = request.POST.get('toggle-Cedula', 'no')
        procesar_fotografia(documentacionUsuario, toggle_Cedula, 'fotografiaCedula','documentacion_usuario/no-imagen.png', request)
        
        toggle_Licencia = request.POST.get('toggle-Licencia', 'no')
        procesar_fotografia(documentacionUsuario, toggle_Licencia, 'fotografiaLicencia','documentacion_usuario/no-imagen.png', request)
                
        toggle_LicenciaInterna = request.POST.get('toggle-LicenciaInterna', 'no')
        procesar_fotografia(documentacionUsuario, toggle_LicenciaInterna, 'fotografiaLicenciaInterna','documentacion_usuario/no-imagen.png', request)
        
        documentacionUsuario.save()
        usuario = Usuario.objects.get(username=request.user.username)
        user_name = request.user.get_full_name() or request.user.username
        new_profile = UsuarioProfile.objects.get(user_id=request.user.id)
        changes_user = get_changes_message(old_user, usuario)
        changes_profile = get_changes_message(old_profile, new_profile)
        subject = f'Usuario {usuario} actualizó su perfil'
        mensaje = f'Usuario: {usuario}\nActualizado por: {user_name}'
        if changes_user:
            mensaje += changes_user
        if changes_profile:
            mensaje += changes_profile
        notify_group('usuarios', subject, mensaje)
        notificacion_mi_usuario_email(request, usuario,"Usuario", "actualizado")
        messages.success(request, 'Datos Actualizados Correctamente') 
        return redirect('edit_my_profile') 
    
@login_required
def save_password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña Actualizada Correctamente') 
            return redirect('edit_my_profile')
        else:
            messages.error(request, 'Error en las Contraseñas', extra_tags='Intenta nuevamente')
            return redirect('password_change')
    else:
        messages.error(request, 'Error al Actualizar la Contraseña')
        return redirect('password_change')

def password_reset_send(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    try:
                        form.save(
                            request=request,
                            use_https=request.is_secure(),
                            email_template_name='registration/password_reset_email.html',
                        )
                        messages.success(request, 'Email enviado con éxito.', extra_tags='Siga las instrucciones en su correo electrónico')
                        return redirect('logincustom')
                    except BadHeaderError:
                        return HttpResponse('Solicitud Invalida.')
            else:
                messages.error(request, 'No hay usuarios registrados con ese email.', extra_tags='Intenta nuevamente')
                return redirect('password_reset')
        else:
            messages.error(request, 'Error en Email ingresado.', extra_tags='Intenta nuevamente')
            return redirect('password_reset')
            
    else:
        messages.error(request, 'Error en Email ingresado.', extra_tags='Intenta nuevamente')
        return redirect('password_reset')