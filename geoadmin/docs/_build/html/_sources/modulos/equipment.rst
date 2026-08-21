#########
Equipment
#########

Descripción General
*******************

El módulo ``equipment`` administra equipamiento no vehicular de faena, separado de la maquinaria pesada del módulo ``machine``.

Capacidades actuales
********************

- mantenedor de tipos de equipo
- mantenedor de marcas o modelos de equipo
- registro de equipos por faena y área
- control básico de mantención próxima y última mantención
- activación y desactivación de registros

Modelos principales
*******************

``TipoEquipo``
==============

Catálogo maestro de tipos de equipo.

``MarcaEquipo``
===============

Asocia una marca o modelo a un ``TipoEquipo``.

``NuevoEquipamiento``
=====================

Registro operacional del equipo. Incluye:

- ``tipo``
- ``marca``
- ``faena``
- ``area``
- ``ultimaMantencion``
- ``frecuencia``
- ``proximaMantencion``
- ``notasAdicionales``
- ``status``

Rutas del módulo
****************

- ``manage_types_equipment``
- ``new_type_equipment``
- ``save_new_type_equipment``
- ``status_type_equipment``
- ``manage_brands_equipment``
- ``new_brand_equipment``
- ``save_new_brand_equipment``
- ``status_brand_equipment``
- ``manage_equipments``
- ``new_equipment``
- ``save_new_equipment``
- ``status_equipment``
- ``edit_equipment``
- ``save_edit_equipment``
- ``cargar_marcas_por_tipo``

Notas de implementación
***********************

- Las vistas están protegidas con ``login_required`` y ``admin_required``.
- El módulo dispara notificaciones vía ``messenger`` al crear o deshabilitar registros.
- La mantención se modela con fechas y frecuencia en meses, suficiente para control administrativo liviano.
