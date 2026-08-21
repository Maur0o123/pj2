from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HistorialCambio
from django.utils.dateparse import parse_date
from datetime import datetime, time
from django.utils import timezone
from django.contrib.auth import get_user_model
from core.decorators import admin_or_base_datos_required

User = get_user_model()

@login_required
@admin_or_base_datos_required
def dashboard_global(request):
    request.session['seccion'] = 'administracion'
    logs = HistorialCambio.objects.none()
    
    generar = request.GET.get('generar')
    exportar = request.GET.get('export')
    
    usuario_seleccionado = request.GET.get('usuario', '').strip()
    rol = request.GET.get('rol', '').strip()
    fecha_a = request.GET.get('fecha_a')
    fecha_b = request.GET.get('fecha_b')

    ruts_con_cambios = list(
        HistorialCambio.objects.exclude(
            rut_usuario__isnull=True
        ).exclude(
            rut_usuario__exact=''
        ).values_list('rut_usuario', flat=True).distinct()
    )

    lista_usuarios = User.objects.filter(username__in=ruts_con_cambios).order_by('first_name')

    roles_disponibles = HistorialCambio.objects.exclude(
        rol_usuario__isnull=True
    ).exclude(
        rol_usuario__exact=''
    ).values_list('rol_usuario', flat=True).distinct().order_by('rol_usuario')

    if generar or exportar:
        logs = HistorialCambio.objects.all()
        
        if usuario_seleccionado:
            logs = logs.filter(rut_usuario__icontains=usuario_seleccionado)
            
        if rol:
            logs = logs.filter(rol_usuario__iexact=rol)
            
        if fecha_a:
            parsed_a = parse_date(fecha_a)
            if parsed_a:
                dt_a = datetime.combine(parsed_a, time.min)
                dt_a = timezone.make_aware(dt_a) if timezone.is_naive(dt_a) else dt_a
                logs = logs.filter(fecha_modificacion__gte=dt_a)
                
        if fecha_b:
            parsed_b = parse_date(fecha_b)
            if parsed_b:
                dt_b = datetime.combine(parsed_b, time.max)
                dt_b = timezone.make_aware(dt_b) if timezone.is_naive(dt_b) else dt_b
                logs = logs.filter(fecha_modificacion__lte=dt_b)
                
        logs = logs.order_by('-fecha_modificacion')[:1000]

        if exportar == 'true':
            response = HttpResponse(content_type='application/vnd.ms-excel; charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="auditoria_cambios.xls"'
            
            def formatear_celda(valor, seccion, request):
                if not valor or str(valor) == '-' or str(valor) == 'None':
                    return "Sin valor"
                
                v_str = str(valor)
                v_lower = v_str.lower()
                
                if '.png' in v_lower or '.jpg' in v_lower or '.jpeg' in v_lower:
                    url_absoluta = request.build_absolute_uri(f'/media/{v_str}')
                    return f'<a href="{url_absoluta}" target="_blank"><img src="{url_absoluta}" width="50" height="50" style="width: 50px; height: 50px; margin: 2px; border: none;"></a>'
                    
                if v_str == 'True':
                    return "Habilitado"
                if v_str == 'False':
                    return "Deshabilitado"
                    
                if '-' in v_str and len(v_str) == 10 and str(seccion).lower() == 'vehicle':
                    return v_str[:7]
                    
                return v_str.replace('\n', '<br>')

            nombres_secciones = {
                'vehicle': 'Vehículo', 'user': 'Usuario', 'prevencion': 'Prevención',
                'planning': 'Planificación', 'mining': 'Minería', 'maintenance': 'Mantenimiento',
                'machine': 'Maquinaria', 'inventory': 'Inventario', 'equipment': 'Equipos',
                'drilling': 'Perforación', 'documentation': 'Documentación', 'core': 'General',
                'checklist': 'Lista de Verificación'
            }

            html_content = """
            <html xmlns:x="urn:schemas-microsoft-com:office:excel">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <xml>
                    <x:ExcelWorkbook>
                        <x:ExcelWorksheets>
                            <x:ExcelWorksheet>
                                <x:Name>Historial</x:Name>
                                <x:WorksheetOptions>
                                    <x:DisplayGridlines/>
                                </x:WorksheetOptions>
                            </x:ExcelWorksheet>
                        </x:ExcelWorksheets>
                    </x:ExcelWorkbook>
                </xml>
                <style>
                    table { border-collapse: collapse; font-family: Calibri, sans-serif; }
                    th { background-color: #2a2e3f; color: #ffffff; font-weight: bold; padding: 10px; border: 1px solid #000000; text-align: center; }
                    td { padding: 5px; border: 1px solid #dddddd; vertical-align: middle; text-align: center; }
                    .txt-wrap { mso-number-format:"\@"; }
                </style>
            </head>
            <body>
                <table>
                    <thead>
                        <tr>
                            <th>RUT</th>
                            <th>Nombre Apellido</th>
                            <th>Rol</th>
                            <th>Sección</th>
                            <th>Acción</th>
                            <th>Registro Afectado</th>
                            <th>Fecha/Hora</th>
                            <th>Campo</th>
                            <th>Valor Anterior</th>
                            <th>Valor Nuevo</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            
            for h in logs:
                fecha_str = h.fecha_modificacion.strftime("%d/%m/%Y %H:%M") if h.fecha_modificacion else "-"
                
                seccion_key = str(h.seccion).lower() if h.seccion else ""
                seccion_fmt = nombres_secciones.get(seccion_key, str(h.seccion).capitalize() if h.seccion else "-")
                
                val_ant = formatear_celda(h.valor_anterior, h.seccion, request)
                val_nue = formatear_celda(h.valor_nuevo, h.seccion, request)
                
                altura_fila = 'style="height: 60px;"' if '<img' in val_ant or '<img' in val_nue else ''
                
                html_content += f"""
                        <tr {altura_fila}>
                            <td class="txt-wrap">{h.rut_usuario or "-"}</td>
                            <td>{h.nombre_usuario or "-"}</td>
                            <td>{h.rol_usuario or "-"}</td>
                            <td>{seccion_fmt}</td>
                            <td>{h.accion or "-"}</td>
                            <td>{h.nombre_registro or "-"}</td>
                            <td>{fecha_str}</td>
                            <td>{h.campo_modificado or "-"}</td>
                            <td class="txt-wrap">{val_ant}</td>
                            <td class="txt-wrap">{val_nue}</td>
                        </tr>
                """
                
            html_content += """
                    </tbody>
                </table>
            </body>
            </html>
            """
            
            response.write(html_content.encode('utf-8'))
            return response

    context = {
        'historial_cambios': logs,
        'lista_usuarios': lista_usuarios,
        'roles_disponibles': roles_disponibles,
        'seccion': 'administracion',
        'sidebar': 'dashboardAdministracion',
    }
    return render(request, 'main/homeadmin.html', context)