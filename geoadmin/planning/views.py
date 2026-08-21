from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FormPlanificacionFaenas, FormSelectFaena, FormSelectTipo, FormSelectCampana
from .models import PlanificacionFaenas, PlanificacionCampanas, PlanificacionPrograma
from django.http import JsonResponse
from django.core import serializers
from core.models import Faena, Tipo, Campana, Programa
from core.choices import meses
from django.db.models import Sum
from vehicle.models import Vehiculo
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from core.decorators import vehicular_admin_db_required, sondaje_estadisticas_required

def vehicular_admin_required(view_func):
    """Acceso restringido estrictamente a ADMINISTRADOR de la sección vehicular."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('logincustom')
        profile = getattr(request.user, 'usuarioprofile', None)
        if request.user.is_superuser or (profile and profile.seccionVehicular == 'ADMINISTRADOR'):
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return _wrapped_view


@login_required    
@vehicular_admin_required
def new_planning_select_mining(request):
    tipos = Tipo.objects.filter(status=True).order_by('tipo')
    todos_meses = meses
    #planificacion = PlanificacionFaenas.objects.all()
    planificacion = PlanificacionFaenas.objects.values('mes', 'tipo').annotate(total_cantidad=Sum('cantidad')).order_by('mes', 'tipo')
    total_meses = PlanificacionFaenas.objects.values('mes').annotate(total_cantidad=Sum('cantidad')).order_by('mes')
    context = {
        'tipos': tipos,
        'meses': todos_meses,
        'planificacion': planificacion,
        'total_meses': total_meses,
        'formselectfaena': FormSelectFaena,
        'sidebar': 'new_planning_mining',
        'sidebarmain': 'system_planning',
    }
    return render(request,'pages/planning/new_planning.html', context)

@login_required    
@vehicular_admin_db_required
def view_planning_mining(request):
    tipos = Tipo.objects.filter(status=True).order_by('tipo')
    todos_meses = meses
    #planificacion = PlanificacionFaenas.objects.all()
    planificacion = PlanificacionFaenas.objects.values('mes', 'tipo').annotate(total_cantidad=Sum('cantidad')).order_by('mes', 'tipo')
    total_meses = PlanificacionFaenas.objects.values('mes').annotate(total_cantidad=Sum('cantidad')).order_by('mes')
    faena = "TODAS LAS FAENAS"
    context = {
        'tipos': tipos,
        'meses': todos_meses,
        'planificacion': planificacion,
        'total_meses': total_meses,
        'faena': faena,
        'formselectfaena': FormSelectFaena,
        'sidebar': 'view_planning_mining',
        'sidebarmain': 'system_planning',
    }
    return render(request,'pages/planning/view_planning_minning.html', context)

@login_required    
@vehicular_admin_db_required
def view_planning_type(request):
    faenas = Faena.objects.all().order_by('faena')
    todos_meses = meses
    #planificacion = PlanificacionFaenas.objects.all()
    planificacion = PlanificacionFaenas.objects.values('mes', 'tipo').annotate(total_cantidad=Sum('cantidad')).order_by('mes', 'tipo')
    total_meses = PlanificacionFaenas.objects.values('mes').annotate(total_cantidad=Sum('cantidad')).order_by('mes')
    tipo = "TODOS LOS VEHICULOS"
    context = {
        'faenas': faenas,
        'meses': todos_meses,
        'planificacion': planificacion,
        'total_meses': total_meses,
        'tipo_vehiculo': tipo,
        'formselecttipo': FormSelectTipo,
        'sidebar': 'view_planning_type',
        'sidebarmain': 'system_planning',
    }
    return render(request,'pages/planning/view_planning_type.html', context)

@login_required    
@vehicular_admin_required
def edit_planning_mining(request):
    if request.method == 'POST':
        faena = Faena.objects.get(id=request.POST['faena'])
        planificacion = PlanificacionFaenas.objects.filter(faena=faena)
        total_meses = PlanificacionFaenas.objects.filter(faena=faena).values('mes').annotate(total_cantidad=Sum('cantidad')).order_by('mes')
        tipos = Tipo.objects.all().order_by('tipo')
        tipos_list = list(tipos.values('id', 'tipo'))
        planificacion_list = list(planificacion.values('mes', 'tipo', 'cantidad'))
        total_meses_list = list(total_meses.values('mes', 'total_cantidad'))
        todos_meses = meses
        data = {
            'tipos': tipos_list,
            'planificacion': planificacion_list,
            'meses': todos_meses,
            'total_meses': total_meses_list,
            'faena': faena.faena,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)
    
@login_required    
@vehicular_admin_db_required
def get_planning_mining(request):
    if request.method == 'POST':
        faena = Faena.objects.get(id=request.POST['faena'])
        planificacion = PlanificacionFaenas.objects.filter(faena=faena)
        total_meses = PlanificacionFaenas.objects.filter(faena=faena).values('mes').annotate(total_cantidad=Sum('cantidad')).order_by('mes')
        tipos = Tipo.objects.filter(status=True).order_by('tipo')
        tipos_list = list(tipos.values('id', 'tipo'))
        planificacion_list = list(planificacion.values('mes', 'tipo', 'cantidad'))
        total_meses_list = list(total_meses.values('mes', 'total_cantidad'))
        todos_meses = meses
        data = {
            'tipos': tipos_list,
            'planificacion': planificacion_list,
            'meses': todos_meses,
            'total_meses': total_meses_list,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)
    
@login_required    
@vehicular_admin_db_required
def get_planning_type(request):
    if request.method == 'POST':
        tipo = Tipo.objects.get(id=request.POST['tipo'])
        planificacion = PlanificacionFaenas.objects.filter(tipo=tipo)
        total_meses = PlanificacionFaenas.objects.filter(tipo=tipo).values('mes').annotate(total_cantidad=Sum('cantidad')).order_by('mes')
        faenas = Faena.objects.filter(status=True).order_by('faena')
        faenas_list = list(faenas.values('id', 'faena'))
        planificacion_list = list(planificacion.values('mes', 'faena', 'cantidad'))
        total_meses_list = list(total_meses.values('mes', 'total_cantidad'))
        todos_meses = meses
        stock_vehiculos = Vehiculo.objects.filter(tipo=tipo, status=True).count()
        data = {
            'faenas': faenas_list,
            'planificacion': planificacion_list,
            'meses': todos_meses,
            'total_meses': total_meses_list,
            'disponibles': stock_vehiculos,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)
    
@csrf_exempt
@vehicular_admin_required
def update_planning_value(request):
    if request.method == 'POST':
        faena = request.POST.get('faena')
        mes = request.POST.get('mes')
        tipo_id = request.POST.get('tipo')
        cantidad = request.POST.get('cantidad')

        # Validations
        if not (mes and tipo_id and faena and cantidad):
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
        
        try:
            cantidad = int(cantidad)
        except ValueError:
            return JsonResponse({'error': 'Cantidad no válida'}, status=400)
        
        try:
            faena = Faena.objects.get(faena=faena)
            tipo = Tipo.objects.get(id=tipo_id)
        except (Faena.DoesNotExist, Tipo.DoesNotExist):
            return JsonResponse({'error': 'Faena o Tipo no válido'}, status=400)
        
        # Fetch or create the planning entry
        planificacion, created = PlanificacionFaenas.objects.update_or_create(
            faena=faena,
            tipo=tipo,
            mes=mes,
            defaults={'cantidad': cantidad}
        )
        
        return JsonResponse({'success': 'Cantidad actualizada'})
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

@login_required    
@sondaje_estadisticas_required
def new_planning_drilling(request):
    campanas = Campana.objects.all(). order_by('campana')
    todos_meses = meses
    planificacion = PlanificacionCampanas.objects.values('mes', 'campana').annotate(total_cantidad=Sum('plan')).order_by('mes', 'campana')
    total_meses = PlanificacionCampanas.objects.values('mes').annotate(total_cantidad=Sum('plan')).order_by('mes')
    context = {
        'campanas': campanas,
        'meses': todos_meses,
        'planificacion': planificacion,
        'total_meses': total_meses,
        'formselectCampana': FormSelectCampana,
        'sidebar': 'new_planning_drilling',
        'sidebarmain': 'system_report_drilling',
    }
    return render(request,'pages/planning/new_planning_drilling.html', context)

@login_required    
@sondaje_estadisticas_required
def edit_drilling_program(request):
    if request.method == 'POST':
        campana_id = request.POST.get('campana')
        try:
            campana = Campana.objects.get(id=campana_id)
        except Campana.DoesNotExist:
            return JsonResponse({'error': 'La campaña seleccionada no existe.'}, status=404)

        planificacion = PlanificacionPrograma.objects.filter(campana=campana)
        total_meses = PlanificacionCampanas.objects.filter(campana=campana).values('mes').annotate(total_plan=Sum('plan')).order_by('mes')
        campanas = Campana.objects.all().order_by('campana')
        campanas_list = list(campanas.values('id', 'campana'))
        programas = Programa.objects.filter(campana=campana).order_by('programa')
        if not programas.exists():
            return JsonResponse(
                {'error': f'La campaña {campana.campana} no tiene programas asociados.'},
                status=400
            )
        programas_list = list(programas.values('id', 'programa'))
        planificacion_list = list(planificacion.values('mes', 'campana', 'programa', 'ano', 'plan', 'realMensual', 'acumuladoPlan', 'acumuladoReal'))
        total_meses_list = list(total_meses.values('mes', 'total_plan'))
        todos_meses = meses
        anoInicial = campana.anoInicial
        anoFinal = campana.anoFinal
        data = {
            'campanas': campanas_list,
            'programas': programas_list,
            'planificacion': planificacion_list,
            'meses': todos_meses,
            'total_meses': total_meses_list,
            'campana': campana.campana,
            'anoInicial': anoInicial,
            'anoFinal': anoFinal,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

from decimal import Decimal, InvalidOperation
@csrf_exempt
@sondaje_estadisticas_required
def update_drilling_program(request):
    # Mapeo de tipo de campo a los campos reales del modelo
    CAMPO_MAP = {
        'plan': 'plan',
        'realMensual': 'realMensual',
        'acumuladoPlan': 'acumuladoPlan',
        'acumuladoReal': 'acumuladoReal',
    }
    if request.method == 'POST':
        # Recibir parámetros del POST
        mes = request.POST.get('mes')
        programa_id = request.POST.get('programa')
        campo = request.POST.get('tipo')  # El campo representa 'plan', 'realMensual', etc.
        cantidad_raw = request.POST.get('cantidad')
        ano = request.POST.get('ano')
        
        # 1. Validamos que los datos obligatorios estén presentes antes de hacer consultas
        if not all([mes, programa_id, campo, ano]):
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
            
        cantidad_normalizada = cantidad_raw.replace(',', '.') if cantidad_raw else None
        try:
            cantidad = Decimal(cantidad_normalizada) if cantidad_normalizada else None
        except (InvalidOperation, TypeError):
            return JsonResponse({'error': 'Cantidad no válida'}, status=400)
            
        # 2. Consultamos el programa y obtenemos su campaña asociada de forma segura
        try:
            programa = Programa.objects.get(id=programa_id)
            campana = programa.campana
        except Programa.DoesNotExist:
            return JsonResponse({'error': 'Programa no válido'}, status=400)
        if campo not in CAMPO_MAP:
            return JsonResponse({'error': 'Campo no válido'}, status=400)
        # Obtener el nombre real del campo en el modelo
        campo_real = CAMPO_MAP[campo]

        # Se obtiene la planificación correspondiente para el mes, programa y campaña
        planificacion, created = PlanificacionPrograma.objects.update_or_create(
            programa=programa,
            ano=ano,
            mes=mes,
            campana=campana,  # Añadimos la campaña
            defaults={campo_real: cantidad}  # Usamos el campo dinámico para guardar la cantidad
        )

        return JsonResponse({'success': f'Cantidad actualizada correctamente para {campo}', 'created': created})

    return JsonResponse({'error': 'Solicitud no válida'}, status=400)