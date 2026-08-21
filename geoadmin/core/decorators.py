from functools import wraps
from django.shortcuts import redirect

def _get_profile(user):
    if not user.is_authenticated: return None
    if hasattr(user, 'usuarioprofile'): return user.usuarioprofile
    return None

def handle_unauthorized(profile, seccion):
    """Determina la redirección cuando no se cumplen los permisos."""
    if not profile:
        return redirect('edit_my_profile')
        
    map_secciones = {
        'vehicular': profile.seccionVehicular,
        'sondaje': profile.seccionSondaje,
        'prevencion': profile.seccionPrevencion,
        'inventario': profile.seccionInventario,
        'administracion': profile.seccionAdministracion,
    }
    
    if seccion in map_secciones and map_secciones[seccion] == 'SIN ASIGNAR':
        return redirect('/select')
        
    return redirect('edit_my_profile')

def admin_or_base_datos_required(view_func):
    """Acceso restringido a ADMINISTRADOR o BASE DATOS según la sección activa."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        seccion = request.session.get('seccion', '')
        profile = _get_profile(request.user)
        roles_permitidos = ['ADMINISTRADOR', 'BASE DATOS']
        
        if profile:
            if seccion == 'vehicular' and profile.seccionVehicular in roles_permitidos: return view_func(request, *args, **kwargs)
            if seccion == 'sondaje' and profile.seccionSondaje in roles_permitidos: return view_func(request, *args, **kwargs)
            if seccion == 'prevencion' and profile.seccionPrevencion in roles_permitidos: return view_func(request, *args, **kwargs)
            if seccion == 'inventario' and profile.seccionInventario in roles_permitidos: return view_func(request, *args, **kwargs)
            if seccion == 'administracion' and profile.seccionAdministracion in roles_permitidos: return view_func(request, *args, **kwargs)
        
        return handle_unauthorized(profile, seccion)
    return _wrapped_view

def mantenedor_sistema_required(view_func):
    """Acceso a mantenedores de sistema según roles específicos por sección."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        seccion = request.session.get('seccion', '')
        profile = _get_profile(request.user)
        
        if profile:
            roles_admin = ['ADMINISTRADOR', 'BASE DATOS']
            if seccion == 'vehicular' and profile.seccionVehicular in roles_admin: return view_func(request, *args, **kwargs)
            if seccion == 'sondaje' and profile.seccionSondaje in roles_admin: return view_func(request, *args, **kwargs)
            if seccion == 'prevencion' and profile.seccionPrevencion in ['ADMINISTRADOR', 'BASE DATOS', 'PREVENCIONISTA']: return view_func(request, *args, **kwargs)
            if seccion == 'inventario' and profile.seccionInventario in roles_admin: return view_func(request, *args, **kwargs)
            if seccion == 'administracion' and profile.seccionAdministracion in roles_admin: return view_func(request, *args, **kwargs)
        
        return handle_unauthorized(profile, seccion)
    return _wrapped_view

def capacitaciones_y_docs_required(view_func):
    """Acceso a Capacitaciones y Documentos para cualquier usuario con rol asignado."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        seccion = request.session.get('seccion', '')
        profile = _get_profile(request.user)
        
        if profile:
            if seccion == 'vehicular' and profile.seccionVehicular != 'SIN ASIGNAR': return view_func(request, *args, **kwargs)
            if seccion == 'sondaje' and profile.seccionSondaje != 'SIN ASIGNAR': return view_func(request, *args, **kwargs)
            if seccion == 'prevencion' and profile.seccionPrevencion != 'SIN ASIGNAR': return view_func(request, *args, **kwargs)
            if seccion == 'inventario' and profile.seccionInventario != 'SIN ASIGNAR': return view_func(request, *args, **kwargs)
            if seccion == 'administracion' and profile.seccionAdministracion != 'SIN ASIGNAR': return view_func(request, *args, **kwargs)
        
        return handle_unauthorized(profile, seccion)
    return _wrapped_view

def vehicular_basico_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = _get_profile(request.user)
        roles = ['CONDUCTOR', 'JEFE MANTENCION', 'SUPERVISOR', 'BASE DATOS', 'ADMINISTRADOR']
        if profile and profile.seccionVehicular in roles: return view_func(request, *args, **kwargs)
        return handle_unauthorized(profile, 'vehicular')
    return _wrapped_view

def vehicular_avanzado_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = _get_profile(request.user)
        roles = ['JEFE MANTENCION', 'SUPERVISOR', 'BASE DATOS', 'ADMINISTRADOR']
        if profile and profile.seccionVehicular in roles: return view_func(request, *args, **kwargs)
        return handle_unauthorized(profile, 'vehicular')
    return _wrapped_view

def vehicular_admin_db_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = _get_profile(request.user)
        roles = ['ADMINISTRADOR', 'BASE DATOS']
        if profile and profile.seccionVehicular in roles: return view_func(request, *args, **kwargs)
        return handle_unauthorized(profile, 'vehicular')
    return _wrapped_view

def sondaje_reportes_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = _get_profile(request.user)
        roles = ['JEFE MANTENCION', 'CONTROLADOR', 'SUPERVISOR', 'BASE DATOS', 'ADMINISTRADOR']
        if profile and profile.seccionSondaje in roles:
            return view_func(request, *args, **kwargs)
        return handle_unauthorized(profile, 'sondaje')
    return _wrapped_view

def sondaje_avanzado_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = _get_profile(request.user)
        roles = ['JEFE MANTENCION', 'SUPERVISOR', 'BASE DATOS', 'ADMINISTRADOR']
        if profile and profile.seccionSondaje in roles: 
            return view_func(request, *args, **kwargs)
        return handle_unauthorized(profile, 'sondaje')
    return _wrapped_view

def sondaje_estadisticas_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = _get_profile(request.user)
        roles = ['SUPERVISOR', 'BASE DATOS', 'ADMINISTRADOR']
        if profile and profile.seccionSondaje in roles: return view_func(request, *args, **kwargs)
        return handle_unauthorized(profile, 'sondaje')
    return _wrapped_view

def prevencion_riesgo_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = _get_profile(request.user)
        roles = ['ADMINISTRADOR', 'BASE DATOS', 'PREVENCIONISTA', 'SUPERVISOR']
        if profile and profile.seccionPrevencion in roles: return view_func(request, *args, **kwargs)
        return handle_unauthorized(profile, 'prevencion')
    return _wrapped_view

def inventario_basico_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = _get_profile(request.user)
        roles = ['ADMINISTRADOR', 'BASE DATOS']
        if profile and profile.seccionInventario in roles:
            return view_func(request, *args, **kwargs)
        return handle_unauthorized(profile, 'inventario')
    return _wrapped_view

def prevencion_mantenedor_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = _get_profile(request.user)
        roles = ['ADMINISTRADOR', 'BASE DATOS', 'PREVENCIONISTA']
        if profile and profile.seccionPrevencion in roles: return view_func(request, *args, **kwargs)
        return handle_unauthorized(profile, 'prevencion')
    return _wrapped_view