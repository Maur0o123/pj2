from django.db import models
from .middleware import get_current_user

import inspect

def obtener_rol_exacto_seccion(user, app_label):
    try:
        perfil = user.usuarioprofile
    except:
        return "SIN ASIGNAR"

    seccion_visual = None
    for frame_record in inspect.stack():
        req = frame_record[0].f_locals.get('request')
        if req and hasattr(req, 'session'):
            seccion_visual = req.session.get('seccion')
            break

    secciones_dict = {
        'vehicular': ('Registro Vehicular', perfil.seccionVehicular),
        'sondaje': ('Sondajes', perfil.seccionSondaje),
        'prevencion': ('Prevención', perfil.seccionPrevencion),
        'inventario': ('Inventario', perfil.seccionInventario),
        'administracion': ('Administración', perfil.seccionAdministracion),
    }

    if seccion_visual and seccion_visual in secciones_dict:
        nombre_sec, rol_sec = secciones_dict[seccion_visual]
        if rol_sec not in [None, '', 'SIN ASIGNAR', 'No']:
            return f"{rol_sec} ({nombre_sec})"

    app_label = str(app_label).lower()
    mapeo_app = {
        'vehicle': 'vehicular', 'maintenance': 'vehicular', 'machine': 'vehicular',
        'drilling': 'sondaje', 'planning': 'sondaje', 'checklist': 'sondaje', 'mining': 'sondaje',
        'prevencion': 'prevencion',
        'inventory': 'inventario', 'equipment': 'inventario',
        'user': 'administracion', 'core': 'administracion', 'administration': 'administracion'
    }

    seccion_db = mapeo_app.get(app_label, 'administracion')
    nombre_sec_db, rol_sec_db = secciones_dict.get(seccion_db, ('Administración', "SIN ASIGNAR"))

    if rol_sec_db not in [None, '', 'SIN ASIGNAR', 'No']:
        return f"{rol_sec_db} ({nombre_sec_db})"

    for key, (nombre, valor) in secciones_dict.items():
        if valor not in [None, '', 'SIN ASIGNAR', 'No']:
            return f"{valor} ({nombre})"

    return "SIN ASIGNAR"


class AuditableQuerySet(models.QuerySet):

    def delete(self):
        from administration.models import HistorialCambio
        user = get_current_user()
        
        if user and user.is_authenticated:
            for registro in self:
                HistorialCambio.objects.create(
                    rut_usuario=user.username,
                    nombre_usuario=f"{user.first_name} {user.last_name}",
                    rol_usuario=obtener_rol_exacto_seccion(user, registro._meta.app_label),
                    seccion=registro._meta.app_label,
                    modelo_afectado=registro.__class__.__name__,
                    registro_id=registro.pk,
                    nombre_registro=f"{registro._meta.verbose_name.title()} ({str(registro)})",
                    accion='Eliminado',
                    campo_modificado='Registro Completo',
                    valor_anterior=str(registro),
                    valor_nuevo='-'
                )
        return super().delete()
    
    def update(self, **kwargs):
        from administration.models import HistorialCambio
        
        registros_afectados = list(self)
        filas_actualizadas = super().update(**kwargs)
        user = get_current_user()
        
        if not user or not user.is_authenticated:
            return filas_actualizadas

        def normalizar_vacio(valor):
            if valor is None or str(valor).strip() == "" or str(valor) == "None":
                return ""
            return str(valor)

        for registro in registros_afectados:
            for campo, valor_nuevo_bruto in kwargs.items():
                try:
                    campo_meta = registro._meta.get_field(campo)
                except Exception:
                    continue 
        
                registrar_cambio = False
                valor_antiguo_str = ""
                valor_nuevo_str = ""

                if isinstance(campo_meta, models.ForeignKey):
                    antiguo_id = getattr(registro, campo_meta.attname)
                    nuevo_id = getattr(valor_nuevo_bruto, 'pk', valor_nuevo_bruto)
                    
                    if normalizar_vacio(antiguo_id) != normalizar_vacio(nuevo_id):
                        registrar_cambio = True
                        instancia_antigua = getattr(registro, campo_meta.name)
                        valor_antiguo_str = str(instancia_antigua) if instancia_antigua else "-"
                        
                        try:
                            if nuevo_id:
                                instancia_nueva = campo_meta.related_model.objects.get(pk=nuevo_id)
                                valor_nuevo_str = str(instancia_nueva)
                            else:
                                valor_nuevo_str = "-"
                        except Exception:
                            valor_nuevo_str = str(nuevo_id)

                elif isinstance(campo_meta, (models.DateField, models.DateTimeField)):
                    valor_antiguo_real = getattr(registro, campo)
                    antiguo_formato = valor_antiguo_real.strftime('%Y-%m-%d') if valor_antiguo_real else ""
                    nuevo_formato = str(valor_nuevo_bruto)[:10] if valor_nuevo_bruto else ""
                    
                    if normalizar_vacio(antiguo_formato) != normalizar_vacio(nuevo_formato):
                        registrar_cambio = True
                        if registro._meta.app_label == 'vehicle':
                            valor_antiguo_str = antiguo_formato[:7] if antiguo_formato else "-"
                            valor_nuevo_str = nuevo_formato[:7] if nuevo_formato else "-"
                        else:
                            valor_antiguo_str = antiguo_formato if antiguo_formato else "-"
                            valor_nuevo_str = nuevo_formato if nuevo_formato else "-"

                else:
                    valor_antiguo_real = getattr(registro, campo)
                    if normalizar_vacio(valor_antiguo_real) != normalizar_vacio(valor_nuevo_bruto):
                        registrar_cambio = True
                        valor_antiguo_str = str(valor_antiguo_real) if valor_antiguo_real is not None and valor_antiguo_real != "" else "-"
                        valor_nuevo_str = str(valor_nuevo_bruto) if valor_nuevo_bruto is not None and valor_nuevo_bruto != "" else "-"

                if registrar_cambio:
                    HistorialCambio.objects.create(
                        rut_usuario=user.username,
                        nombre_usuario=f"{user.first_name} {user.last_name}",
                        rol_usuario=obtener_rol_exacto_seccion(user, registro._meta.app_label),
                        seccion=registro._meta.app_label,
                        modelo_afectado=registro.__class__.__name__,
                        registro_id=registro.pk,
                        nombre_registro=f"{registro._meta.verbose_name.title()} ({str(registro)})",
                        accion='Editado',
                        campo_modificado=campo_meta.verbose_name or campo,
                        valor_anterior=valor_antiguo_str,
                        valor_nuevo=valor_nuevo_str
                    )
    
        return filas_actualizadas