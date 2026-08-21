from django.shortcuts import render
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail
from user.models import User
from core.models import Faena
from twilio.base.exceptions import TwilioRestException
from .models import NotificationGroup
from .utils import notify_group
import json
from django.contrib.auth.decorators import login_required
#from core.decorators import admin_required
from django.http import JsonResponse

# NOTA: Se eliminó CORREO_ADICIONAL para usar el sistema dinámico de grupos.

def send_sms_message(numero, mensaje):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            from_=settings.TWILIO_PHONE_NUMBER,
            body=mensaje,
            to='+56'+str(numero)
        )
        return message
    except TwilioRestException as e:
        return None

def send_email_message(to_email, subject, message):
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])
        return
    except Exception as e:
        return {"error": str(e)}

def get_group_emails(slug):
    """Auxiliar para obtener emails de un grupo."""
    try:
        group = NotificationGroup.objects.get(slug=slug)
        emails = list(group.users.values_list('email', flat=True))
        emails.extend(group.external_emails)
        return list(set([e for e in emails if e]))
    except NotificationGroup.DoesNotExist:
        return []

# --- FUNCIONES DE VEHICULOS ---

def notificacion_vehiculos_email(request, vehiculo, action):
    action = action.capitalize()
    user_name = request.user.get_full_name() or request.user.username
    mensaje_notificacion = f'Vehículo: {vehiculo.placaPatente} \n{action} por: {user_name} \n\nMás información en www.geoadmin.cl'
    subject = f'Vehículo {vehiculo.placaPatente} {action}'
    destinatarios = list(User.objects.filter(usuarioprofile__seccionVehicular='JEFE MANTENCION').values_list('email', flat=True))
    destinatarios.extend(get_group_emails('admin_vehiculos_maquinaria'))
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje_notificacion)

def notificacion_cambio_faena_vehiculo_email(request, datos, action):
    action = action.capitalize()
    faenaAnterior = Faena.objects.get(id=datos.faenaAnterior)
    user_name = request.user.get_full_name() or request.user.username
    mensaje_notificacion = (
        f"Se ha realizado una asignación de faena para el vehículo {datos.vehiculo.tipo} ({datos.vehiculo.placaPatente}).\n\n"
        f"Acción por: {user_name}\n\n"
        f"Detalle de cambios:\n"
        f"- Faena: {datos.faena}"
    )
    subject = f'Asignación de faena {datos.vehiculo.placaPatente}'
    destinatarios = list(User.objects.filter(usuarioprofile__seccionVehicular='JEFE MANTENCION').values_list('email', flat=True))
    destinatarios.extend(User.objects.filter(usuarioprofile__seccionVehicular='SUPERVISOR', usuarioprofile__faena=datos.faena).values_list('email', flat=True))
    destinatarios.extend(get_group_emails('admin_vehiculos_maquinaria'))
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje_notificacion)

# --- FUNCIONES DE MANTENIMIENTO (VEHICULOS) ---

def notificacion_nuevo_mantenimiento_vehiculos_email_sms(request, mantenimiento, problemas, progreso, action):
    action = action.capitalize()
    problemas_str = " - ".join([str(p) for p in problemas])
    user_name = request.user.get_full_name() or request.user.username
    mensaje = f'Nuevo mantenimiento\nVehículo: {mantenimiento.vehiculo.placaPatente}\n{action} por: {user_name}\nProblemas: {problemas_str}'
    subject = f'Nuevo mantenimiento {mantenimiento.vehiculo.placaPatente}'
    for to_email in set(User.objects.filter(usuarioprofile__seccionVehicular='JEFE MANTENCION').values_list('email', flat=True)):
        send_email_message(to_email, subject, mensaje)

def notificacion_update_mantenimiento_vehiculos_email_sms(request, mantenimiento, problemas, progreso, action):
    action = action.capitalize()
    problemas_str = " - ".join([str(p) for p in problemas])
    user_name = request.user.get_full_name() or request.user.username
    mensaje = f'Actualización mantenimiento\nVehículo: {mantenimiento.vehiculo.placaPatente}\n{action} por: {user_name}\nProgreso: {progreso}'
    subject = f'Actualización mantenimiento {mantenimiento.vehiculo.placaPatente}'
    notify_group('mantenimiento_km_horometros', subject, mensaje)
    for to_email in set(User.objects.filter(usuarioprofile__seccionVehicular='JEFE MANTENCION').values_list('email', flat=True)):
        send_email_message(to_email, subject, mensaje)

# --- FUNCIONES DE MAQUINARIA ---

def notificacion_maquinarias_email(request, maquinaria, action):
    action = action.capitalize()
    user_name = request.user.get_full_name() or request.user.username
    mensaje = f'Maquinaria: {maquinaria.maquinaria} \n{action} por: {user_name}'
    subject = f'Maquinaria {maquinaria.maquinaria} {action}'
    notify_group('admin_vehiculos_maquinaria', subject, mensaje)
    for to_email in set(User.objects.filter(usuarioprofile__seccionVehicular='JEFE MANTENCION').values_list('email', flat=True)):
        send_email_message(to_email, subject, mensaje)

def notificacion_nuevo_mantenimiento_maquinaria_email_sms(request, mantenimiento, problemas, progreso, action):
    action = action.capitalize()
    user_name = request.user.get_full_name() or request.user.username
    mensaje = f'Nuevo mantenimiento maquinaria\nMaquinaria: {mantenimiento.maquinaria}\n{action} por: {user_name}'
    subject = f'Nueva solicitud mantenimiento maquinaria {mantenimiento.maquinaria}'
    for to_email in set(User.objects.filter(usuarioprofile__seccionVehicular='JEFE MANTENCION').values_list('email', flat=True)):
        send_email_message(to_email, subject, mensaje)

def notificacion_update_mantenimiento_maquinaria_email_sms(request, mantenimiento, problemas, progreso, action):
    action = action.capitalize()
    mensaje = f'Actualización mantenimiento maquinaria\nMaquinaria: {mantenimiento.maquinaria}\nProgreso: {progreso}'
    subject = f'Actualización mantenimiento maquinaria {mantenimiento.maquinaria}'
    notify_group('mantenimiento_km_horometros', subject, mensaje)
    for to_email in set(User.objects.filter(usuarioprofile__seccionVehicular='JEFE MANTENCION').values_list('email', flat=True)):
        send_email_message(to_email, subject, mensaje)

# --- FUNCIONES DE STOCK / INVENTARIO ---

def notificacion_jefe_mantencion_stock_minimo_kit_email_sms(request, kit_en_faena, stock_actual):
    subject = f'ALERTA STOCK MÍNIMO: {kit_en_faena.kitMaquinaria.nombreKit}'
    mensaje = f'El kit {kit_en_faena.kitMaquinaria.nombreKit} en la faena {kit_en_faena.faena} ha alcanzado su stock mínimo.\nStock actual: {stock_actual}'
    destinatarios = list(User.objects.filter(usuarioprofile__seccionVehicular='JEFE MANTENCION').values_list('email', flat=True))
    destinatarios.extend(get_group_emails('registro_equipos'))
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje)

# --- OTRAS FUNCIONES ---

def notificacion_usuarios_email(request, usuario, action):
    action = action.capitalize()
    
    if hasattr(request.user, 'get_full_name') and getattr(request.user, 'is_authenticated', False):
        actor = request.user.get_full_name() or request.user.username
    else:
        actor = 'Registro web Geoadmin (Público)'
        
    user_display = usuario.get_full_name() or usuario.username
    mensaje = f'Usuario: {user_display} \n{action} por: {actor}'
    subject = f'Usuario {user_display} {action}'
    destinatarios = get_group_emails('usuarios')
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje)

def notificacion_mantenedor_email(request, seccion, nombre, action):
    action = action.capitalize()
    user_name = request.user.get_full_name() or request.user.username
    mensaje = f'Mantenedor de {nombre}: {seccion} \n{action} por: {user_name}'
    subject = f'Mantenedor de {nombre}: {seccion} {action}'
    destinatarios = get_group_emails('mantenimiento_sistema')
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje)

def notificacion_registro_equipos_email(request, equipo, action):
    action = action.capitalize()
    user_name = request.user.get_full_name() or request.user.username
    mensaje = f'Registro de Equipo: {equipo} \n{action} por: {user_name}'
    subject = f'Equipo {equipo} {action}'
    destinatarios = get_group_emails('registro_equipos')
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje)

def notificacion_nuevo_kilometraje_email(request, registro):
    vehiculo = registro.vehiculo
    valor = registro.kilometraje
    user_name = request.user.get_full_name() or request.user.username
    mensaje = f'Nuevo Kilometraje Registrado \nVehículo: {vehiculo} \nKilometraje: {valor} KM \nRegistrado por: {user_name}'
    subject = f'Nuevo Kilometraje: {vehiculo} ({valor} KM)'
    destinatarios = get_group_emails('mantenimiento_km_horometros')
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje)

def notificacion_nuevo_horometro_email(request, registro):
    maquinaria = registro.maquinaria
    valor = registro.horometro
    user_name = request.user.get_full_name() or request.user.username
    mensaje = f'Nuevo Horómetro Registrado \nMaquinaria: {maquinaria} \nHorómetro: {valor} Hrs \nRegistrado por: {user_name}'
    subject = f'Nuevo Horómetro: {maquinaria} ({valor} Hrs)'
    destinatarios = get_group_emails('mantenimiento_km_horometros')
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje)

def notificacion_mi_usuario_email(request, usuario, nombre, action):
    action = action.capitalize()
    mensaje = f'{nombre}: {usuario.username} \n{action}'
    subject = f'{nombre} {action}: {usuario.username}'
    destinatarios = [usuario.email]
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje)

def notificacion_admin_jefe_mantencion_email(request, documento, nombre, action):
    action = action.capitalize()
    mensaje = f'{nombre}: {documento.nombredocumento} \nFaena: {documento.faena}'
    subject = f'{nombre} {documento.nombredocumento} {action}'
    destinatarios = list(User.objects.filter(usuarioprofile__seccionVehicular='JEFE MANTENCION').values_list('email', flat=True))
    destinatarios.extend(get_group_emails('admin_vehiculos_maquinaria'))
    for to_email in set(destinatarios):
        send_email_message(to_email, subject, mensaje)        

def notificacion_celery_email():
    pass

@login_required
def manage_notifications(request):
    perfil = getattr(request.user, 'usuarioprofile', None)
    es_perforista = perfil and perfil.seccionSondaje == "PERFORISTA"
    
    if not request.session.get('seccion') and not es_perforista:
        request.session['seccion'] = 'administracion'

    default_groups = [
        # Vehicular
        {'slug': 'admin_vehiculos_maquinaria', 'name': 'Administración Vehículos y Maquinaria', 'category': NotificationGroup.Category.VEHICULAR},
        {'slug': 'mantenimiento_km_horometros', 'name': 'Mantenimiento, Kilometraje y Horómetros', 'category': NotificationGroup.Category.VEHICULAR},
        {'slug': 'registro_equipos', 'name': 'Registro de Equipos', 'category': NotificationGroup.Category.VEHICULAR},
        # Sondaje
        {'slug': 'sondaje_general', 'name': 'Notificaciones Generales Sondaje', 'category': NotificationGroup.Category.SONDAJE},
        # Prevención
        {'slug': 'prevencion_general', 'name': 'Notificaciones Generales Prevención', 'category': NotificationGroup.Category.PREVENCION},
        # Sistema
        {'slug': 'usuarios', 'name': 'Administración de Usuarios', 'category': NotificationGroup.Category.SISTEMA},
        {'slug': 'mantenimiento_sistema', 'name': 'Mantenimiento del Sistema', 'category': NotificationGroup.Category.SISTEMA},
    ]
    
    for dg in default_groups:
        NotificationGroup.objects.get_or_create(
            slug=dg['slug'],
            defaults={'name': dg['name'], 'category': dg['category']}
        )

    area_requested = request.GET.get('area')
    
    # Obtener todos los grupos con sus relaciones (users es M2M, external_emails no)
    groups_qs = NotificationGroup.objects.prefetch_related('users').all()
    
    # Estructura de categorías para el template
    categories = []
    for choice_val, choice_label in NotificationGroup.Category.choices:
        # Si se pidió un área específica, filtramos el menú lateral también
        if area_requested and area_requested != choice_val:
            continue
            
        categories.append({
            'key': choice_val,
            'name': choice_label,
            'groups': [g for g in groups_qs if g.category == choice_val]
        })

    context = {
        'categories': categories,
        'all_users': User.objects.all().order_by('first_name'),
        'sidebar': 'manage_notifications',
        'sidebarmain': 'manage_system',
        'area_requested': area_requested,
    }
    return render(request, 'pages/messenger/manage_notifications.html', context)

@login_required
def update_notification_group(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            group_id = data.get('group_id')
            action = data.get('action') 
            value = data.get('value')
            group = NotificationGroup.objects.get(id=group_id)
            if action == 'add_user':
                user = User.objects.get(id=value)
                group.users.add(user)
            elif action == 'remove_user':
                user = User.objects.get(id=value)
                group.users.remove(user)
            elif action == 'add_email':
                if value not in group.external_emails:
                    group.external_emails.append(value)
                    group.save()
            elif action == 'remove_email':
                if value in group.external_emails:
                    group.external_emails.remove(value)
                    group.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})