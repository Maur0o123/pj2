from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

from . import views
from .views import (#manage_inventario_ajuste, manage_inventario_egreso, manage_inventario_ingreso,
                    manage_inventario_crear_item,new_inventario_crear_item, 
                    cargar_secciones_por_item,save_new_inventario_crear_item,status_item,
                    manage_inventario_crear_secciones,new_inventario_crear_secciones,save_new_inventario_crear_seccion,
                    status_inventario_seccion,
                    save_new_inventario_ingreso,save_new_inventario_egreso,
                    manage_inventario_crear_categorias, new_inventario_crear_categorias, save_new_inventario_crear_categoria,
                    manage_inventario_crear_duraciones, new_inventario_crear_duraciones, save_new_inventario_crear_duracion,
                    manage_inventario_stock,new_inventario_ajuste,new_inventario_ingreso,new_inventario_egreso  ,
                    save_new_inventario_ingreso,save_new_inventario_egreso,save_new_inventario_ajuste,
                    mostrar_registro_item,manage_inventario_movimientos,manage_inventario_bodegas,edit_inventario_item,update_inventario_item,
                    status_inventario_categoria,status_inventario_duracion,manage_proveedores,new_proveedor,edit_proveedor,status_proveedor,
                    new_ingreso_cm,new_bodega,manage_new_bodega,edit_bodega,status_bodega,new_traspaso_bodega,obtener_stock_ubicacion,
                    manage_bodegas,obtener_stock_bodega,update_stock_bodega,obtener_historial_stock_bodega

                    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #ITEMS

    #path('manage_inventario_ingreso', manage_inventario_ingreso, name="manage_inventario_ingreso"),
    #path('manage_inventario_egreso', manage_inventario_egreso, name="manage_inventario_egreso"),
    #path('manage_inventario_ajuste', manage_inventario_ajuste, name="manage_inventario_ajuste"),
    path('manage_inventario_crear_item', manage_inventario_crear_item, name="manage_inventario_crear_item"),
    path('new_inventario_crear_item', new_inventario_crear_item, name="new_inventario_crear_item"),
    path('cargar_secciones_por_item', cargar_secciones_por_item, name="cargar_secciones_por_item"),
    path('save_new_inventario_crear_item', save_new_inventario_crear_item, name="save_new_inventario_crear_item"),
    path('status_item', status_item, name="status_item"),
    path('mostrar_registro_item/<int:id>', mostrar_registro_item, name="mostrar_registro_item"),
    # SECCIONES
    path('manage_inventario_crear_secciones', manage_inventario_crear_secciones, name="manage_inventario_crear_secciones"),
    path('new_inventario_crear_secciones', new_inventario_crear_secciones, name="new_inventario_crear_secciones"),
    path('save_new_inventario_crear_seccion', save_new_inventario_crear_seccion, name="save_new_inventario_crear_seccion"),
    path('status_inventario_seccion', status_inventario_seccion, name="status_inventario_seccion"),
    
    # CATEGORIAS
    path('manage_inventario_crear_categorias', manage_inventario_crear_categorias, name="manage_inventario_crear_categorias"),
    path('new_inventario_crear_categorias', new_inventario_crear_categorias, name="new_inventario_crear_categorias"),
    path('save_new_inventario_crear_categoria', save_new_inventario_crear_categoria, name="save_new_inventario_crear_categoria"),
    # DURACION
    path('manage_inventario_crear_duraciones', manage_inventario_crear_duraciones, name="manage_inventario_crear_duraciones"),
    path('new_inventario_crear_duraciones', new_inventario_crear_duraciones, name="new_inventario_crear_duraciones"),
    path('save_new_inventario_crear_duracion', save_new_inventario_crear_duracion, name="save_new_inventario_crear_duracion"),
    # STOCK 
    path('manage_inventario_stock', manage_inventario_stock, name="manage_inventario_stock"),
    path('new_inventario_ajuste', new_inventario_ajuste, name="new_inventario_ajuste"),
    path('new_inventario_ingreso', new_inventario_ingreso, name="new_inventario_ingreso"),
    path('new_inventario_egreso', new_inventario_egreso, name="new_inventario_egreso"),
    path('save_new_inventario_ingreso', save_new_inventario_ingreso, name="save_new_inventario_ingreso"),
    path('save_new_inventario_egreso', save_new_inventario_egreso, name="save_new_inventario_egreso"),
    path('save_new_inventario_ajuste', save_new_inventario_ajuste, name="save_new_inventario_ajuste"),
    path('manage_inventario_movimientos',manage_inventario_movimientos,name='manage_inventario_movimientos'),
    path('manage_inventario_bodegas',manage_inventario_bodegas,name='manage_inventario_bodegas'),
    path('edit_inventario_item/<int:id>',edit_inventario_item,name='edit_inventario_item'),
    path('update_inventario_item/<int:id>',update_inventario_item,name='update_inventario_item'),
    path('status_inventario_categoria',status_inventario_categoria,name='status_inventario_categoria'),
    path('status_inventario_duracion',status_inventario_duracion,name='status_inventario_duracion'),
    path('manage_proveedores',manage_proveedores,name='manage_proveedores'),
    path('new_proveedor',new_proveedor,name='new_proveedor'),
    path('edit_proveedor/<int:id>', views.edit_proveedor, name='edit_proveedor'),
    path('status_proveedor', views.status_proveedor, name='status_proveedor'),
    path('new_ingreso_cm',new_ingreso_cm,name='new_ingreso_cm'),
    path('manage_new_bodega', views.manage_new_bodega, name='manage_new_bodega'),
    path('new_bodega', views.new_bodega, name='new_bodega'),
    path('edit_bodega/<int:id>', views.edit_bodega, name='edit_bodega'),
    path('status_bodega', views.status_bodega, name='status_bodega'),
    path('new_traspaso_bodega', views.new_traspaso_bodega, name='new_traspaso_bodega'),
    path('obtener_stock_ubicacion', views.obtener_stock_ubicacion, name='obtener_stock_ubicacion'),
    path('manage_bodegas', views.manage_bodegas, name='manage_bodegas'),
    path('obtener_stock_bodega', views.obtener_stock_bodega, name='obtener_stock_bodega'),
    path('update_stock_bodega', views.update_stock_bodega, name='update_stock_bodega'),
    path('obtener_historial_stock_bodega', views.obtener_historial_stock_bodega, name='obtener_historial_stock_bodega'),

]