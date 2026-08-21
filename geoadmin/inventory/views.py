from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.decorators import inventario_basico_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import FormNuevoItem, FormNuevaSeccion, FormNuevaDuracion, FormNuevaCategoria
from .forms import  FormSeccionSelect,FormCategorySelect
from .forms import  FormInventarioNuevoIngreso,FormInventarioNuevoEgreso,FormInventarioNuevoAjuste
from .models import Items, SeccionItems, CategoriaItems, DuracionItems, StockItems, StockEgresoItems,Faena,StockItemsHistorico
from messenger.views import notificacion_mantenedor_email, notificacion_admin_jefe_mantencion_email
from django.utils.datastructures import MultiValueDictKeyError
import hashlib
from .models import ProveedorInventario
from .models import IngresoCasaMatriz
from django.contrib import messages
from .models import BodegaInventario,StockUbicacionInventario, TraspasoBodegaInventario
from django.db import transaction
from django.db.models import Sum



#### CREAR ITEM
@login_required
@inventario_basico_required
def manage_inventario_crear_item(request):
    storage = messages.get_messages(request)
    storage.used = True
    #inventario_crear_item = list(ReporteError.objects.all().order_by('fechacreacion')) 
    items = Items.objects.all().order_by('item')
    context = {
        'items': items,  # Pasar las items al contexto
        'sidebarmain': 'system_inventario_crear_item',  
        'sidebarmenu': 'manage_inventory',
        'sidebarsubmenu': 'manage_secciones',
        'sidebarmain': 'system_inventario_stock',
        'sidebar': 'manage_inventario_crear_item',
    }
    return render(request,'pages/inventory/manage_inventario_crear_item.html', context)

@login_required  
@inventario_basico_required  
def new_inventario_crear_item(request):
    context = {
        'formularioseccion': FormSeccionSelect,
        'formnuevoitem': FormNuevoItem,   
        'sidebarmain': 'system_inventario_crear_item', 
        'sidebar': 'dashboard',
    }
    return render(request,'pages/inventory/new_inventario_crear_item.html', context)

@login_required
@inventario_basico_required
def cargar_secciones_por_item(request):
    seccion_id = request.GET.get('seccion_id')
    if seccion_id:
        categorias = CategoriaItems.objects.filter(seccion_id=seccion_id,status=True)
        data = [{'id': categoria.id, 'nombre': categoria.categoria} for categoria in categorias]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({}, status=400)

@login_required
@inventario_basico_required
def save_new_inventario_crear_item(request):

    if request.method == 'POST':

        item_name = request.POST.get('item')
        codigo_item = request.POST.get('codigo_item')
        categoria_id = request.POST.get('categoria')
        duracion = request.POST.get('duracion')

        duracion_instance = DuracionItems.objects.get(id=duracion)
        categoria_instance = CategoriaItems.objects.get(id=categoria_id)

        # Verificar si ya existe el código
        existing_codigo = Items.objects.filter(
            codigo_item=codigo_item
        )

        if existing_codigo.exists():

            return JsonResponse({
                'success': False,
                'errors': 'Ya existe un item con ese código.'
            }, status=400)

        # Verificar si ya existe el item
        existing_item = Items.objects.filter(
            item=item_name,
            categoria=categoria_instance
        )

        if existing_item.exists():

            return JsonResponse({
                'success': False,
                'errors': 'El item ya existe en esa categoría.'
            }, status=400)

        # Crear item
        nuevo_item = Items(
            codigo_item=codigo_item,
            categoria=categoria_instance,
            item=item_name,
            descripcion=request.POST.get('descripcion'),
            stock_minimo=request.POST.get('stock_minimo'),
            stock_maximo=request.POST.get('stock_maximo'),
            valor_neto=request.POST.get('valor_neto'),
            marca=request.POST.get('marca'),
            duracion=duracion_instance,
            status=True
        )

        nuevo_item.save()

        # Crear stock inicial
        try:

            stock_item = StockItems(
                categoria=categoria_instance,
                item=nuevo_item,
                cantidad=0,
                cantidad_actual=0,
                descripcion=request.POST.get('descripcion'),
                status=True,
                creador=f"{request.user.first_name} {request.user.last_name}",
            )

            stock_item.save()

        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': f'Error al guardar stock item: {str(e)}'
            }, status=500)

        return JsonResponse({'success': True})

    else:

        return redirect('new_inventario_crear_item')

@login_required
@inventario_basico_required
def status_item(request):
    print(request.POST)
    if request.method == 'POST': 
        item = Items.objects.get(id=request.POST['item'])

        if (item.status):
            Items.objects.filter(id=request.POST['item']).update(status=False)
            messages.success(request, 'Vehículo Deshabilitado Correctamente')
         
        else:            
            Items.objects.filter(id=request.POST['item']).update(status=True)

            messages.success(request, 'Vehículo Habilitado Correctamente')
        return redirect('manage_inventario_crear_item') 
    else:
        return redirect('manage_inventario_crear_item') 
#### CREAR SECCION
@login_required
@inventario_basico_required
def manage_inventario_crear_secciones(request):
    storage = messages.get_messages(request)
    storage.used = True
    # Obtener todas las secciones desde el modelo
    secciones = SeccionItems.objects.all().order_by('seccion')  # Ordenar por el campo 'seccion'
    context = {
        'secciones': secciones,  # Pasar las secciones al contexto
        'sidebarmain': 'manage_system',
        'sidebarmenu': 'manage_inventory',
        'sidebarsubmenu': 'manage_secciones',
    }
    return render(request,'pages/inventory/manteiner/manage_inventario_crear_secciones.html', context)

@login_required 
@inventario_basico_required  
def new_inventario_crear_secciones(request):
    context = {
        'formnuevaseccion': FormNuevaSeccion,
        'sidebarmain': 'manage_system',
        'sidebarmenu': 'manage_inventory',
        'sidebarsubmenu': 'manage_secciones',
    }
    return render(request,'pages/inventory/manteiner/new_inventario_crear_secciones.html', context)

@login_required
@inventario_basico_required
def save_new_inventario_crear_seccion(request):
    if request.method == 'POST':
        
        form = FormNuevaSeccion(request.POST)
        if form.is_valid():
            nueva_seccion = form.save(commit=False)
            nueva_seccion.creador = f"{request.user.first_name} {request.user.last_name}"  # Asigna el creador
            nueva_seccion.status = True  
            nueva_seccion.save()
    
            return JsonResponse({'success': True})

        else:
            # Enviar errores si el formulario no es válido
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return redirect('new_inventario_crear_seccion')

@login_required 
@inventario_basico_required
def status_inventario_seccion(request):
    if request.method == 'POST': 
        seccion = SeccionItems.objects.get(id=request.POST['id'])
        if (seccion.status): 
            SeccionItems.objects.filter(id=request.POST['id']).update(status=False)
            notificacion_mantenedor_email(request,seccion,'secciones','deshabilitada')  
            messages.success(request, 'seccion Deshabilitado Correctamente')  
        else:
            SeccionItems.objects.filter(id=request.POST['id']).update(status=True)
            notificacion_mantenedor_email(request,seccion,'secciones','habilitada')  
            messages.success(request, 'seccion Habilitado Correctamente') 
        return redirect('manage_inventario_crear_secciones') 
#### CREAR CATEGORIAS
@login_required
@inventario_basico_required
def manage_inventario_crear_categorias(request):
    storage = messages.get_messages(request)
    storage.used = True
    #inventario_crear_seccion = list(ReporteError.objects.all().order_by('fechacreacion')) 

    # Obtener todas las categorias desde el modelo
    categorias = CategoriaItems.objects.all().order_by('categoria')  # Ordenar por el campo 'categoria'

    context = {
        'categorias' : categorias,
        'sidebarmain': 'manage_system',
        'sidebarmenu': 'manage_inventory',
        'sidebarsubmenu': 'manage_categorias',
    }
    return render(request,'pages/inventory/manteiner/manage_inventario_crear_categorias.html', context)

@login_required  
@inventario_basico_required 
def new_inventario_crear_categorias(request):
    context = {
        'formnuevacategoria': FormNuevaCategoria, 
        'sidebarmain': 'manage_system',
        'sidebarmenu': 'manage_inventory',
        'sidebarsubmenu': 'manage_categorias',
    }
    return render(request,'pages/inventory/manteiner/new_inventario_crear_categorias.html', context)

@login_required
@inventario_basico_required
def save_new_inventario_crear_categoria(request):

    if request.method == 'POST':

        formulario = FormNuevaCategoria(data=request.POST)

        if formulario.is_valid():

            try:

                CategoriaItems.objects.get(
                    categoria=request.POST['categoria']
                )

                return JsonResponse({
                    'success': False,
                    'errors': 'La categoría ya existe.'
                }, status=400)

            except CategoriaItems.DoesNotExist:

                categoria = CategoriaItems(
                    categoria=request.POST['categoria'],
                    status=True,
                    creador=request.user.first_name + " " + request.user.last_name,
                )

                categoria.save()

                notificacion_mantenedor_email(
                    request,
                    categoria,
                    'categoria Items',
                    'creada'
                )

                return JsonResponse({'success': True})

        else:

            return JsonResponse({
                'success': False,
                'errors': formulario.errors
            }, status=400)

    else:

        return redirect('new_inventario_crear_categoria')

#### CREAR DURACIONES
@login_required
@inventario_basico_required
def manage_inventario_crear_duraciones(request):
    storage = messages.get_messages(request)
    storage.used = True
    #inventario_crear_seccion = list(ReporteError.objects.all().order_by('fechacreacion')) 

    # Obtener todas las secciones desde el modelo
    duracion = DuracionItems.objects.all().order_by('fechacreacion')  # Ordenar por el campo 'seccion'
    context = {
        'duraciones': duracion,
        'sidebarmain': 'manage_system',
        'sidebarmenu': 'manage_inventory',
        'sidebarsubmenu': 'manage_duraciones',
    }
    return render(request,'pages/inventory/manteiner/manage_inventario_crear_duraciones.html', context)

@login_required   
@inventario_basico_required
def new_inventario_crear_duraciones(request):
    context = {
        'formnuevaduracion': FormNuevaDuracion,   
        'sidebarmain': 'manage_system',
        'sidebarmenu': 'manage_inventory',
        'sidebarsubmenu': 'manage_duraciones',
    }
    return render(request,'pages/inventory/manteiner/new_inventario_crear_duraciones.html', context)

@login_required
@inventario_basico_required
def save_new_inventario_crear_duracion(request):

    if request.method == 'POST':
        form = FormNuevaDuracion(request.POST)
        if form.is_valid():
            nueva_duracion = form.save(commit=False)
            nueva_duracion.creador = f"{request.user.first_name} {request.user.last_name}"  # Asigna el creador
            nueva_duracion.status = True  
            nueva_duracion.save()    
            return JsonResponse({'success': True})
        else:
            # Enviar errores si el formulario no es válido
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        return redirect('new_inventario_crear_duracion')

#### STOCK
@login_required
@inventario_basico_required
def manage_inventario_stock(request):

    storage = messages.get_messages(request)
    storage.used = True
    # Obtener todas las categorias desde el modelo
    items = list(StockItems.objects.filter(status=True)) 

    
    context = {
        'items' : items,
        'sidebarmain': 'system_inventario_stock',
    }
    return render(request,'pages/inventory/manage_inventario_stock.html', context)


#### INGRESO
@login_required
@inventario_basico_required
def manage_inventario_ingreso(request):
    storage = messages.get_messages(request)
    storage.used = True

    context = {
        'sidebarmain': 'system_inventario_stock', 
    }
    return render(request,'pages/inventory/manage_inventario_ingreso.html', context)

@login_required  
@inventario_basico_required  
def new_inventario_ingreso(request):
    #print(request.POST)
    try:
        request.session['item_id'] = request.POST['item_id']          
        request.session['cantidad']=request.POST.get('cantidad',0)
        request.session['cantidad_actual']=request.POST.get('cantidad_actual',0)
        request.session['categoria'] = request.POST['categoria']
    except MultiValueDictKeyError:
        request.session['item_id'] = request.session['item_id']          
        request.session['cantidad'] = request.session['cantidad']
        request.session['cantidad_actual'] = request.session['cantidad_actual']
        request.session['categoria'] = request.session['categoria']

    item = Items.objects.get(id=request.session['item_id'])
    stock_items = StockItems.objects.get(item=item)
    stock_items_historico = StockItemsHistorico.objects.filter(
        movimiento="Ingreso",
        item=item
    ).order_by('-fechacreacion') 
    context = {
        'forminventarionuevoingreso': FormInventarioNuevoIngreso(initial={
                'item':item.item,
                'item_id':item.id,
                'categoria':item.categoria.categoria,
                'cantidad_actual':stock_items.cantidad_actual,
                }),  
            'sidebarmain': 'dashboardInventario',
            "item_id":item.id,
            "historicos": stock_items_historico,
            'sidebarmain': 'system_inventario_stock', 
    }
    return render(request,'pages/inventory/new_inventario_ingreso.html', context)

@login_required
@inventario_basico_required
def save_new_inventario_ingreso(request):
    print(request.POST)

    if request.method == 'POST':
        item = Items.objects.get(id=request.POST['item_id'])
        stock_items = StockItems.objects.get(item=item)
        stock_items.cantidad = int(request.POST.get('cantidad'))
        stock_items.cantidad_actual += int(request.POST.get('cantidad'))
        stock_items.save()

        try:
            stock_items_historico = StockItemsHistorico(
                categoria=item.categoria,
                item=item, 
                movimiento="Ingreso",
                cantidad=int(request.POST.get('cantidad')),
                descripcion=request.POST.get("descripcion"),
                creador=request.user.first_name + " " + request.user.last_name,
            )
        except Exception as e:
            print(f"Error al crear StockItemsHistorico: {e}")  # Muestra el error en la terminal
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
        print("PASO")
        print(stock_items_historico)
        stock_items_historico.save()          
        return JsonResponse({'success': True})

    else:
        return redirect('manage_inventario_stock')
    
#### EGRESO

@login_required  
@inventario_basico_required  
def new_inventario_egreso(request):
    try:
        request.session['item_id'] = request.POST['item_id']          
        request.session['cantidad']=request.POST.get('cantidad',0)
        request.session['cantidad_actual']=request.POST.get('cantidad_actual',0)
        request.session['categoria'] = request.POST['categoria']
    except MultiValueDictKeyError:
        request.session['item_id'] = request.session['item_id']          
        request.session['cantidad'] = request.session['cantidad']
        request.session['cantidad_actual'] = request.session['cantidad_actual']
        request.session['categoria'] = request.session['categoria']

    item = Items.objects.get(id=request.session['item_id'])
    stock_items = StockItems.objects.get(item=item)

    stock_items_historico = StockItemsHistorico.objects.filter(
        movimiento="Egreso",
        item=item
    ).order_by('-fechacreacion') 

    context = {
        'forminventarionuevoegreso': FormInventarioNuevoEgreso(initial={
            'item':item.item,
            'item_id':item.id,
            'categoria':item.categoria.categoria,
            'cantidad':stock_items.cantidad_actual,
            }),  
        'sidebarmain': 'system_inventario_stock', 
        "item_id":item.id,
        "historicos": stock_items_historico
    }
    
    return render(request,'pages/inventory/new_inventario_egreso.html', context)
        
@login_required
@inventario_basico_required
def save_new_inventario_egreso(request):
    print(request.POST)
    if request.method == 'POST':
        try:
            item = Items.objects.get(id=request.POST['item_id'])
            stock_items = StockItems.objects.get(item=item)

            if int(stock_items.cantidad_actual) < int(request.POST.get('cantidad_actual')):
                return JsonResponse({'success': False, 'message': 'No hay suficiente stock'})
            
            else:
                stock_items.cantidad = int(request.POST.get('cantidad_actual'))
                stock_items.cantidad_actual += (int(request.POST.get('cantidad_actual')))*-1
                stock_items.save()
                print(1)

                stock_items_historico = StockItemsHistorico(
                    categoria=item.categoria,
                    item=item, 
                    movimiento="Egreso",   
                    cantidad=int(request.POST.get('cantidad')),
                    descripcion=request.POST.get("descripcion"),
                    rut_receptor=request.POST.get("rut_receptor"),
                    cargo_receptor=request.POST.get("cargo_receptor"),
                    nombre_receptor=request.POST.get("nombre_receptor"),
                    creador=request.user.first_name + " " + request.user.last_name,
                )
                print(2)
                stock_items_historico.save()  
                return JsonResponse({'success': True})

        except Exception as e:
            print(f"Error al crear StockItemsHistorico: {e}")  # Muestra el error en la terminal
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    else:
        return redirect('manage_inventario_stock')

    
#### AJUSTE

@login_required  
@inventario_basico_required  
def new_inventario_ajuste(request):
    print(request.POST)
    try:
        request.session['item_id'] = request.POST['item_id']          
        request.session['cantidad']=request.POST.get('cantidad',0)
        request.session['cantidad_actual']=request.POST.get('cantidad_actual',0)
        request.session['categoria'] = request.POST['categoria']
    except MultiValueDictKeyError:
        request.session['item_id'] = request.session['item_id']          
        request.session['cantidad'] = request.session['cantidad']
        request.session['cantidad_actual'] = request.session['cantidad_actual']
        request.session['categoria'] = request.session['categoria']

    item = Items.objects.get(id=request.session['item_id'])
    stock_items = StockItems.objects.get(item=item)
    stock_items_historico = StockItemsHistorico.objects.filter(
        movimiento="Ajuste",
        item=item
    ).order_by('-fechacreacion') 
    context = {
        'forminventarionuevoajuste': FormInventarioNuevoAjuste(initial={
            'item':item.item,
            'item_id':item.id,
            'categoria':item.categoria.categoria,
            'cantidad_actual':stock_items.cantidad_actual,
            }),  
        'sidebarmain': 'system_inventario_stock', 
        "item_id":item.id,
        "historicos": stock_items_historico
    }
    return render(request,'pages/inventory/new_inventario_ajuste.html', context)

@login_required
@inventario_basico_required
def save_new_inventario_ajuste(request):
    print(request.POST)

    if request.method == 'POST':
        item = Items.objects.get(id=request.POST['item_id'])
        stock_items = StockItems.objects.get(item=item)
        stock_items.cantidad = int(request.POST.get('cantidad'))
        stock_items.cantidad_actual += int(request.POST.get('cantidad'))
        stock_items.save()

        try:
            stock_items_historico = StockItemsHistorico(
                faena=item.faena,
                seccion=item.seccion,
                categoria=item.categoria,
                item=item, 
                movimiento="Ajuste",
                cantidad=int(request.POST.get('cantidad')),
                descripcion=request.POST.get("descripcion"),
                creador=request.user.first_name + " " + request.user.last_name,
            )
        except Exception as e:
            print(f"Error al crear StockItemsHistorico: {e}")  # Muestra el error en la terminal
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
        print("PASO")
        print(stock_items_historico)
        stock_items_historico.save()          
        return JsonResponse({'success': True})

    else:
        return redirect('manage_inventario_stock')
    

@login_required
@inventario_basico_required
def mostrar_registro_item(request, id):
    item_ver = Items.objects.get(id=id)
    context = {
        'item_ver': item_ver,
        'sidebarmain': 'system_report_error',
    }
    return render(request,'pages/inventory/mostrarregistroitem.html', context)

@login_required
def manage_inventario_movimientos(request):

    ingresos = IngresoCasaMatriz.objects.filter(
        status=True
    ).select_related(
        'proveedor',
        'item'
    ).order_by('-fechacreacion')

    grupos = {}
    
    stocks_cm = StockUbicacionInventario.objects.filter(
        tipo_ubicacion='CASA_MATRIZ',
        bodega=None
    ).select_related('item').order_by('item__item')

    for ingreso in ingresos:
        clave = f"{ingreso.proveedor_id}_{ingreso.fechacreacion.strftime('%Y%m%d%H%M%S')}"

        if clave not in grupos:
            grupos[clave] = {
                'fecha': ingreso.fechacreacion,
                'proveedor': ingreso.proveedor,
                'creador': ingreso.creador,
                'valor_total_venta': 0,
                'items': []
            }

        grupos[clave]['valor_total_venta'] += ingreso.valor_neto or 0
        grupos[clave]['items'].append(ingreso)

    movimientos = sorted(
        grupos.values(),
        key=lambda x: x['fecha'],
        reverse=True
    )

    context = {
        'movimientos': movimientos,
        'sidebarmain': 'system_inventario_stock',
        'sidebar': 'manage_inventario_movimientos',
        'stocks_cm': stocks_cm,
    }

    return render(request, 'pages/inventory/manage_inventario_movimientos.html', context)


@login_required
def manage_inventario_bodegas(request):
    context = {
        'bodegas': [],
        'sidebarmain': 'system_inventario_stock',
        'sidebar': 'manage_inventario_bodegas',
    }
    return render(request, 'pages/inventory/manage_inventario_bodegas.html', context)

@login_required
@inventario_basico_required
def edit_inventario_item(request, id):

    item = Items.objects.get(id=id)

    form = FormNuevoItem(instance=item)

    
    form.fields['categoria'].disabled = True
    

    form.fields['codigo_item'].widget.attrs['readonly'] = True
    form.fields['item'].widget.attrs['readonly'] = True
    form.fields['marca'].widget.attrs['readonly'] = True
    context = {
        'formnuevoitem': form,
        'item_edit': item,
        'sidebarmain': 'system_inventario_crear_item',
        'sidebar': 'dashboard',
    }

    return render(
        request,
        'pages/inventory/new_inventario_crear_item.html',
        context
    )
@login_required
@inventario_basico_required
def update_inventario_item(request, id):

    item = Items.objects.get(id=id)

    if request.method == 'POST':

        item.stock_minimo = request.POST.get('stock_minimo')
        item.stock_maximo = request.POST.get('stock_maximo')
        item.valor_neto = request.POST.get('valor_neto')
        item.descripcion = request.POST.get('descripcion')

        duracion = request.POST.get('duracion')

        if duracion:
            item.duracion_id = duracion

        item.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

@login_required
@inventario_basico_required
def status_inventario_categoria(request):
    if request.method == 'POST':
        categoria = CategoriaItems.objects.get(id=request.POST['id'])

        if categoria.status:
            categoria.status = False
            messages.success(request, 'Categoría Deshabilitada Correctamente')
        else:
            categoria.status = True
            messages.success(request, 'Categoría Habilitada Correctamente')

        categoria.save()

    return redirect('manage_inventario_crear_categorias')

@login_required
@inventario_basico_required
def status_inventario_duracion(request):
    if request.method == 'POST':
        duracion = DuracionItems.objects.get(id=request.POST['id'])

        if duracion.status:
            duracion.status = False
            messages.success(request, 'Duración Deshabilitada Correctamente')
        else:
            duracion.status = True
            messages.success(request, 'Duración Habilitada Correctamente')

        duracion.save()

    return redirect('manage_inventario_crear_duraciones')

@login_required
def manage_proveedores(request):
    proveedores = ProveedorInventario.objects.all().order_by('nombre')

    context = {
        'proveedores': proveedores,
        'sidebarmain': 'system_inventario_stock',
        'sidebar': 'manage_proveedores',
    }

    return render(request, 'pages/inventory/manage_proveedores.html', context)


@login_required
def new_proveedor(request):
    if request.method == 'POST':
        ProveedorInventario.objects.create(
            nombre=request.POST.get('nombre'),
            rut=request.POST.get('rut'),
            correo=request.POST.get('correo'),
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion'),
            creador=f"{request.user.first_name} {request.user.last_name}",
            status=True,
        )

        return redirect('manage_proveedores')

    context = {
        'sidebarmenu': 'manage_proveedores',
        'sidebarsubmenu': 'manage_proveedor',
    }

    return render(request, 'pages/inventory/new_proveedor.html', context)

@login_required
def edit_proveedor(request, id):
    proveedor = ProveedorInventario.objects.get(id=id)

    if request.method == 'POST':
        proveedor.nombre = request.POST.get('nombre')
        proveedor.rut = request.POST.get('rut')
        proveedor.correo = request.POST.get('correo')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.save()

        return redirect('manage_proveedores')

    context = {
        'proveedor': proveedor,
        'sidebarmenu': 'manage_proveedores',
        'sidebarsubmenu': 'manage_proveedor',
    }

    return render(request, 'pages/inventory/new_proveedor.html', context)


@login_required
def status_proveedor(request):
    if request.method == 'POST':
        proveedor = ProveedorInventario.objects.get(id=request.POST['id'])

        if proveedor.status:
            proveedor.status = False
            messages.success(request, 'Proveedor Deshabilitado Correctamente')
        else:
            proveedor.status = True
            messages.success(request, 'Proveedor Habilitado Correctamente')

        proveedor.save()

    return redirect('manage_proveedores')

@login_required
def new_ingreso_cm(request):

    proveedores = ProveedorInventario.objects.filter(
        status=True
    ).order_by('nombre')

    items = Items.objects.filter(
        status=True
    ).order_by('item')

    if request.method == 'POST':

        proveedor_id = request.POST.get('proveedor')

        items_ids = request.POST.getlist('items[]')
        cantidades_buenos = request.POST.getlist('cantidad_buenos[]')
        
        valores_netos = request.POST.getlist('valor_neto[]')
        observaciones = request.POST.getlist('observaciones[]')
        imagenes = request.FILES.getlist('imagenes[]')

        for index, item_id in enumerate(items_ids):

            if not item_id:
                continue

            IngresoCasaMatriz.objects.create(
                proveedor_id=proveedor_id,
                item_id=item_id,
                cantidad_buenos=int(cantidades_buenos[index] or 0),
                cantidad_malos=0,
                valor_neto=int(valores_netos[index] or 0),
                observacion=observaciones[index] if index < len(observaciones) else '',
                imagen=imagenes[index] if index < len(imagenes) else None,
                creador=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                status=True
            )

            stock_cm, creado = StockUbicacionInventario.objects.get_or_create(
                item_id=item_id,
                tipo_ubicacion='CASA_MATRIZ',
                bodega=None,
                defaults={
                    'cantidad_buenos': 0,
                    'cantidad_malos': 0
                }
            )

            stock_cm.cantidad_buenos += int(cantidades_buenos[index] or 0)
            stock_cm.cantidad_malos += 0
            stock_cm.save()

        messages.success(
            request,
            'Ingreso guardado con éxito'
        )

        return redirect('manage_inventario_movimientos')

    context = {
        'proveedores': proveedores,
        'items': items,
        'sidebarmain': 'system_inventario_stock',
        'sidebar': 'manage_inventario_movimientos',
    }

    return render(
        request,
        'pages/inventory/new_ingreso_cm.html',
        context
    )


@login_required
def manage_new_bodega(request):

    bodegas = BodegaInventario.objects.all().order_by('-fechacreacion')

    context = {
        'bodegas': bodegas,
        'sidebarmain': 'system_inventario_bodegas',
        'sidebar': 'manage_new_bodega',
    }

    return render(request, 'pages/inventory/manage_new_bodega.html', context)


@login_required
def new_bodega(request):

    if request.method == 'POST':
        BodegaInventario.objects.create(
            nombre=request.POST.get('nombre'),
            direccion=request.POST.get('direccion'),
            descripcion=request.POST.get('descripcion'),
            creador=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            status=True
        )

        messages.success(request, 'Bodega creada con éxito')
        return redirect('manage_new_bodega')

    context = {
        'sidebarmain': 'system_inventario_bodegas',
        'sidebar': 'manage_new_bodega',
    }

    return render(request, 'pages/inventory/new_bodega.html', context)


@login_required
def edit_bodega(request, id):

    bodega = get_object_or_404(BodegaInventario, id=id)

    if request.method == 'POST':
        bodega.nombre = request.POST.get('nombre')
        bodega.direccion = request.POST.get('direccion')
        bodega.descripcion = request.POST.get('descripcion')
        bodega.save()

        messages.success(request, 'Bodega editada con éxito')
        return redirect('manage_new_bodega')

    context = {
        'bodega': bodega,
        'sidebarmain': 'system_inventario_bodegas',
        'sidebar': 'manage_new_bodega',
    }

    return render(request, 'pages/inventory/edit_bodega.html', context)


@login_required
def status_bodega(request):

    if request.method == 'POST':
        bodega = get_object_or_404(BodegaInventario, id=request.POST.get('id'))
        bodega.status = not bodega.status
        bodega.save()

        if bodega.status:
            messages.success(request, 'Bodega habilitada correctamente')
        else:
            messages.success(request, 'Bodega deshabilitada correctamente')

    return redirect('manage_new_bodega')
@login_required
def edit_bodega(request, id):

    bodega = get_object_or_404(BodegaInventario, id=id)

    if request.method == 'POST':

        bodega.nombre = request.POST.get('nombre')
        bodega.direccion = request.POST.get('direccion')
        bodega.descripcion = request.POST.get('descripcion')

        bodega.save()

        messages.success(request, 'Bodega editada correctamente')

        return redirect('manage_new_bodega')

    context = {
        'bodega': bodega,
        'sidebarmain': 'system_inventario_bodegas',
        'sidebar': 'manage_new_bodega',
    }

    return render(
        request,
        'pages/inventory/edit_bodega.html',
        context
    )

@login_required
def new_traspaso_bodega(request):
    sincronizar_stock_casa_matriz()
    bodegas = BodegaInventario.objects.filter(status=True).order_by('nombre')

    if request.method == 'POST':

        origen_tipo = request.POST.get('origen_tipo')
        origen_bodega_id = request.POST.get('origen_bodega') or None

        destino_tipo = request.POST.get('destino_tipo')
        destino_bodega_id = request.POST.get('destino_bodega') or None

        items_ids = request.POST.getlist('items[]')
        cantidades_buenos = request.POST.getlist('cantidad_buenos[]')
        

        with transaction.atomic():

            for index, item_id in enumerate(items_ids):

                if not item_id:
                    continue

                cantidad_buenos = int(cantidades_buenos[index] or 0)
                

                if cantidad_buenos <= 0:
                    continue

                stock_origen = StockUbicacionInventario.objects.select_for_update().get(
                    item_id=item_id,
                    tipo_ubicacion=origen_tipo,
                    bodega_id=origen_bodega_id
                )

                if stock_origen.cantidad_buenos < cantidad_buenos:
                    raise ValueError('Stock insuficiente para realizar el traspaso.')

                stock_destino, creado = StockUbicacionInventario.objects.select_for_update().get_or_create(
                    item_id=item_id,
                    tipo_ubicacion=destino_tipo,
                    bodega_id=destino_bodega_id,
                    defaults={
                        'cantidad_buenos': 0,
                        'cantidad_malos': 0
                    }
                )

                stock_origen.cantidad_buenos -= cantidad_buenos
                stock_origen.save()

                stock_destino.cantidad_buenos += cantidad_buenos
                stock_destino.save()

                TraspasoBodegaInventario.objects.create(
                    item_id=item_id,
                    origen_tipo=origen_tipo,
                    origen_bodega_id=origen_bodega_id,
                    destino_tipo=destino_tipo,
                    destino_bodega_id=destino_bodega_id,
                    cantidad_buenos=cantidad_buenos,
                    cantidad_malos=0,
                    creador=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
                )

        messages.success(request, 'Traspaso realizado correctamente')
        return redirect('manage_inventario_movimientos')

    context = {
        'bodegas': bodegas,
        'sidebarmain': 'system_inventario_stock',
        'sidebar': 'manage_inventario_movimientos',
    }

    return render(request, 'pages/inventory/new_traspaso_bodega.html', context)

@login_required
def obtener_stock_ubicacion(request):

    tipo = request.GET.get('tipo')
    bodega_id = request.GET.get('bodega') or None

    data = []

    if tipo == 'CASA_MATRIZ':

        items = Items.objects.filter(status=True).order_by('item')

        for item in items:

            stock = StockUbicacionInventario.objects.filter(
                item=item,
                tipo_ubicacion='CASA_MATRIZ',
                bodega=None
            ).first()

            data.append({
                'item_id': item.id,
                'item': item.item,
                'codigo_item': item.codigo_item,
                'buenos': stock.cantidad_buenos if stock else 0,
                'malos': 0,
            })

    else:

        stocks = StockUbicacionInventario.objects.filter(
            tipo_ubicacion='BODEGA',
            bodega_id=bodega_id
        ).select_related('item').order_by('item__item')

        for stock in stocks:
            data.append({
                'item_id': stock.item.id,
                'item': stock.item.item,
                'codigo_item': stock.item.codigo_item,
                'buenos': stock.cantidad_buenos,
                'malos': 0,
            })

    return JsonResponse({
        'success': True,
        'stocks': data
    })

@login_required
def manage_bodegas(request):

    bodegas = BodegaInventario.objects.filter(
        status=True
    ).order_by('nombre')

    context = {
        'bodegas': bodegas,
        'sidebarmain': 'system_inventario_bodegas',
        'sidebar': 'manage_bodegas',
    }

    return render(
        request,
        'pages/inventory/manage_bodegas.html',
        context
    )

@login_required
def obtener_stock_bodega(request):

    bodega_id = request.GET.get('bodega_id')

    stocks = StockUbicacionInventario.objects.filter(
        tipo_ubicacion='BODEGA',
        bodega_id=bodega_id
    ).select_related('item').order_by('item__item')

    data = []

    for stock in stocks:
        data.append({
            'stock_id': stock.id,
            'item_id': stock.item.id,
            'codigo_item': stock.item.codigo_item or '',
            'nombre_item': stock.item.item or '',
            'stock_minimo': stock.item.stock_minimo or '',
            'stock_maximo': stock.item.stock_maximo or '',
            'stock_buenos': stock.cantidad_buenos or 0,
            'stock_malos': stock.cantidad_malos or 0,
            'stock_alarma': stock.stock_alarma or 0,
        })

    return JsonResponse({
        'success': True,
        'stocks': data
    })

def sincronizar_stock_casa_matriz():
    items = Items.objects.filter(status=True)

    for item in items:
        totales = IngresoCasaMatriz.objects.filter(
            item=item,
            status=True
        ).aggregate(
            total_buenos=Sum('cantidad_buenos')
        )

        total_buenos = totales['total_buenos'] or 0

        stock_cm, creado = StockUbicacionInventario.objects.get_or_create(
            item=item,
            tipo_ubicacion='CASA_MATRIZ',
            bodega=None,
            defaults={
                'cantidad_buenos': 0,
                'cantidad_malos': 0
            }
        )

        if creado:
            stock_cm.cantidad_buenos = total_buenos
            stock_cm.cantidad_malos = 0
            stock_cm.save()

@login_required
def update_stock_bodega(request):

    if request.method == 'POST':

        stock = get_object_or_404(
            StockUbicacionInventario,
            id=request.POST.get('stock_id')
        )

        stock.item.stock_minimo = request.POST.get('stock_minimo') or 0
        stock.item.stock_maximo = request.POST.get('stock_maximo') or 0
        stock.item.save()

        stock.cantidad_buenos = request.POST.get('stock_buenos') or 0
        stock.cantidad_malos = request.POST.get('stock_malos') or 0
        stock.stock_alarma = request.POST.get('stock_alarma') or 0
        stock.save()

        return JsonResponse({
            'success': True,
            'message': 'Stock actualizado correctamente'
        })

    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    }, status=400)


@login_required
def obtener_historial_stock_bodega(request):

    bodega_id = request.GET.get('bodega_id')
    item_id = request.GET.get('item_id')

    ingresos = TraspasoBodegaInventario.objects.filter(
        destino_tipo='BODEGA',
        destino_bodega_id=bodega_id,
        item_id=item_id
    ).order_by('-fechacreacion')

    egresos = TraspasoBodegaInventario.objects.filter(
        origen_tipo='BODEGA',
        origen_bodega_id=bodega_id,
        item_id=item_id
    ).order_by('-fechacreacion')

    historial = []

    for ingreso in ingresos:
        historial.append({
            'fecha': ingreso.fechacreacion.strftime('%Y-%m-%d %H:%M'),
            'tipo': 'Ingreso',
            'cantidad': ingreso.cantidad_buenos,
            'origen_destino': 'Casa Matriz',
            'responsable': ingreso.creador or ''
        })

    for egreso in egresos:
        historial.append({
            'fecha': egreso.fechacreacion.strftime('%Y-%m-%d %H:%M'),
            'tipo': 'Egreso',
            'cantidad': ingreso.cantidad_buenos,
            'origen_destino': egreso.destino_bodega.nombre if egreso.destino_bodega else 'Casa Matriz',
            'responsable': egreso.creador or ''
        })

    historial = sorted(
        historial,
        key=lambda x: x['fecha'],
        reverse=True
    )

    return JsonResponse({
        'success': True,
        'historial': historial
    })  