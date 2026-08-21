#########
Inventory
#########

Descripción General
*******************

El módulo ``inventory`` soporta la administración de stock para distintas faenas y secciones internas del negocio.

Capacidades actuales
********************

- creación de secciones de inventario
- creación de categorías por sección
- definición de duraciones de ítems
- creación de ítems con imagen, marca y stock mínimo/máximo
- control de stock con ingresos, egresos y ajustes
- historial de movimientos por ítem

Modelos principales
*******************

``SeccionItems``
================

Define la agrupación principal del inventario.

``CategoriaItems``
==================

Subclasificación dependiente de ``SeccionItems``.

``DuracionItems``
=================

Catálogo de duración o vida útil asociada a un ítem.

``Items``
=========

Ítem inventariable por faena, sección y categoría. Incluye descripción, stock mínimo, stock máximo, valor neto, marca e imagen.

``StockItems``
==============

Estado actual del stock por ítem.

``StockItemsHistorico``
=======================

Bitácora de movimientos de stock.

``StockEgresoItems``
====================

Registro detallado de entregas o egresos con receptor y observaciones.

Rutas del módulo
****************

Mantenedores:

- ``manage_inventario_crear_item``
- ``new_inventario_crear_item``
- ``save_new_inventario_crear_item``
- ``status_item``
- ``mostrar_registro_item/<int:id>``
- ``manage_inventario_crear_secciones``
- ``new_inventario_crear_secciones``
- ``save_new_inventario_crear_seccion``
- ``status_inventario_seccion``
- ``manage_inventario_crear_categorias``
- ``new_inventario_crear_categorias``
- ``save_new_inventario_crear_categoria``
- ``manage_inventario_crear_duraciones``
- ``new_inventario_crear_duraciones``
- ``save_new_inventario_crear_duracion``

Operación de stock:

- ``manage_inventario_stock``
- ``new_inventario_ingreso``
- ``new_inventario_egreso``
- ``new_inventario_ajuste``
- ``save_new_inventario_ingreso``
- ``save_new_inventario_egreso``
- ``save_new_inventario_ajuste``

Soporte AJAX:

- ``cargar_secciones_por_item``

Notas de implementación
***********************

- Al crear un ``Item`` también se crea su registro inicial en ``StockItems`` con cantidad cero.
- La combinación ``faena`` + ``seccion`` + ``categoria`` + ``item`` es única.
- El módulo está diseñado para uso administrativo y se protege con ``admin_required``.
