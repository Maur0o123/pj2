from datetime import date, datetime
from django.core.mail import send_mail
from django.conf import settings
from .models import NotificationGroup

def get_changes_message(old_instance, new_instance):
    """
    Compara dos instancias de un modelo y devuelve una cadena con los cambios detectados.
    """
    if not old_instance:
        return ""
        
    changes = []
    # Lista de campos a ignorar (comúnmente metadatos o campos técnicos)
    ignore_fields = ['fechacreacion', 'completado', 'creador', 'id', 'pk', 'actual']
    
    for field in new_instance._meta.fields:
        if field.name in ignore_fields:
            continue
            
        old_val = getattr(old_instance, field.name)
        new_val = getattr(new_instance, field.name)
        
        # Normalizar para comparación (especialmente para fechas y strings)
        def normalize_for_comparison(val):
            if isinstance(val, (date, datetime)):
                return val.strftime('%Y-%m-%d')
            return val

        if normalize_for_comparison(old_val) != normalize_for_comparison(new_val):
            verbose_name = field.verbose_name or field.name
            
            # Formatear valores (manejar claves foráneas, fechas y opciones)
            def format_val(val, field):
                if val is None or val == '': return "Vacío"
                
                # Manejar booleanos de forma humana
                if isinstance(val, bool):
                    if field.name == 'status':
                        return "Habilitado" if val else "Deshabilitado"
                    return "Sí" if val else "No"

                # Si el campo tiene 'choices', intentamos obtener la etiqueta legible
                if field.choices:
                    return dict(field.choices).get(val, val)
                
                return str(val)

            changes.append(f"- {verbose_name}: {format_val(new_val, field)}")
            
    if changes:
        return "\n\nDetalle de cambios:\n" + "\n".join(changes)
    return ""

def notify_group(group_slug, subject, message):
    """
    Envía una notificación por correo electrónico a todos los usuarios
    y correos externos asociados a un grupo específico.
    """
    try:
        group = NotificationGroup.objects.get(slug=group_slug)
        
        # Recopilar emails de usuarios del sistema
        destinatarios = list(group.users.values_list('email', flat=True))
        
        # Añadir emails externos
        destinatarios.extend(group.external_emails)
        
        # Limpiar lista (quitar vacíos y duplicados)
        destinatarios = list(set([email for email in destinatarios if email]))
        
        # Integración con Notificaciones Internas (Campanita/Bandeja)
        try:
            from django.contrib.auth import get_user_model
            from prevencion.models import PrevencionNotificacionAprobacion
            from administration.middleware import get_current_user
            from django.utils import timezone
            from datetime import timedelta
            
            User = get_user_model()
            current_user = get_current_user()
            if not current_user or not current_user.is_authenticated:
                current_user = User.objects.filter(is_superuser=True).first()
                if not current_user:
                    current_user = User.objects.filter(is_active=True).first()
            
            time_threshold = timezone.now() - timedelta(minutes=2)
            
            for sys_user in group.users.filter(is_active=True):
                # Evitar registros duplicados de la misma alerta en un periodo corto
                exists = PrevencionNotificacionAprobacion.objects.filter(
                    destinatario=sys_user,
                    titulo=subject,
                    descripcion=message,
                    fechacreacion__gte=time_threshold
                ).exists()
                
                if not exists:
                    PrevencionNotificacionAprobacion.objects.create(
                        destinatario=sys_user,
                        solicitante=current_user or sys_user,
                        tipo_documento='sistema',
                        titulo=subject,
                        descripcion=message,
                    )
        except Exception as inner_ex:
            print(f"Error al registrar notificación interna en notify_group: {str(inner_ex)}")

        if not destinatarios:
            return False
            
        # Envío individual para mantener la privacidad de los destinatarios
        for email in destinatarios:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        return True
    except NotificationGroup.DoesNotExist:
        print(f"Error: El grupo con slug '{group_slug}' no existe.")
        return False
    except Exception as e:
        print(f"Error al enviar notificación: {str(e)}")
        return False

def notify_multiple_groups(group_slugs, subject, message):
    """
    Envía una notificación por correo electrónico a todos los usuarios
    y correos externos asociados a una lista de grupos, sin duplicar destinatarios.
    """
    try:
        destinatarios = set()
        system_users = set()
        for slug in group_slugs:
            try:
                group = NotificationGroup.objects.get(slug=slug)
                # Emails de usuarios
                for email in group.users.values_list('email', flat=True):
                    if email:
                        destinatarios.add(email)
                # Emails externos
                for email in group.external_emails:
                    if email:
                        destinatarios.add(email)
                # Guardar usuarios del sistema activos
                for u in group.users.filter(is_active=True):
                    system_users.add(u)
            except NotificationGroup.DoesNotExist:
                print(f"Error: El grupo con slug '{slug}' no existe.")

        # Integración con Notificaciones Internas (Campanita/Bandeja)
        if system_users:
            try:
                from django.contrib.auth import get_user_model
                from prevencion.models import PrevencionNotificacionAprobacion
                from administration.middleware import get_current_user
                from django.utils import timezone
                from datetime import timedelta
                
                User = get_user_model()
                current_user = get_current_user()
                if not current_user or not current_user.is_authenticated:
                    current_user = User.objects.filter(is_superuser=True).first()
                    if not current_user:
                        current_user = User.objects.filter(is_active=True).first()
                
                time_threshold = timezone.now() - timedelta(minutes=2)
                
                for sys_user in system_users:
                    # Evitar registros duplicados de la misma alerta en un periodo corto
                    exists = PrevencionNotificacionAprobacion.objects.filter(
                        destinatario=sys_user,
                        titulo=subject,
                        descripcion=message,
                        fechacreacion__gte=time_threshold
                    ).exists()
                    
                    if not exists:
                        PrevencionNotificacionAprobacion.objects.create(
                            destinatario=sys_user,
                            solicitante=current_user or sys_user,
                            tipo_documento='sistema',
                            titulo=subject,
                            descripcion=message,
                        )
            except Exception as inner_ex:
                print(f"Error al registrar notificación interna en notify_multiple_groups: {str(inner_ex)}")

        if not destinatarios:
            return False

        # Envío individual para mantener la privacidad de los destinatarios
        for email in destinatarios:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        return True
    except Exception as e:
        print(f"Error al enviar notificaciones a múltiples grupos: {str(e)}")
        return False
