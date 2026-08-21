Api
===

La aplicación ``api`` implementa una ``API REST`` basada en ``Django REST Framework`` para exponer datos operacionales del sistema a clientes móviles, integraciones y tableros.

Cobertura actual
----------------

- autenticación con JWT
- catálogos y datos activos de sondaje
- sincronización de reportes operacionales
- sincronización de checklist de materiales
- consulta de vehículos, kilometrajes y asignaciones
- endpoints de dashboard para vehículos, inventario y sondaje
- lectura y escritura de reportes optimizados para terreno

Endpoints principales
---------------------

Autenticación
^^^^^^^^^^^^^

- ``POST /api/token/``: emisión de token JWT.
- ``POST /api/token/refresh/``: refresco de token JWT.

Catálogos y sincronización de sondaje
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``GET /api/data_perforaciones/``: catálogos activos y reportes vigentes para operación de sondaje.
- ``POST /api/save_reporte_operacional/``: guarda reporte operacional y sus entidades hijas dentro de una transacción.
- ``POST /api/save_reporte_materiales_sonda/``: sincroniza checklist de materiales de sonda y caseta.
- ``GET /api/read_report/``: lectura optimizada de reportes digitales.
- ``POST /api/save_report/``: persistencia de reportes digitales.
- ``GET /api/selector_report/``: selección de reportes según filtros operacionales.
- ``GET /api/reporte_avance_campana/``: datos para avance de campaña.

Vehículos
^^^^^^^^^

- ``GET /api/vehiculos/``: lista de vehículos.
- ``GET /api/vehiculos_kilometrajes/``: historial de kilometrajes.
- ``GET /api/vehiculos_faenas/``: asignación vehículo-faena.
- ``GET /api/vehiculos_kilometrajes_demo/``: variante demo para sincronización.

Dashboards
^^^^^^^^^^

- ``GET /api/dashboardVehiculos/``
- ``GET /api/dashboardInventarioVehiculo/``
- ``GET /api/dashboardInventarioSondaje/``
- ``GET /api/dashboardInventarioPrevencion/``
- ``GET /api/dashboardSondas/``
- ``GET /api/dashboard_sondaje_total/``
- ``GET /api/dashboard_sondaje_diario/``

Comportamiento relevante
------------------------

- La API mezcla endpoints de consulta y sincronización offline/online.
- ``SaveReporteOperacionalAPI`` usa ``transaction.atomic()`` para guardar reporte, perforaciones, controles, insumos, aditivos y observaciones de forma consistente.
- ``DataPerforacionesListView`` entrega en una sola respuesta catálogos maestros, opciones de turno/jornada/gemelo y data activa de reportes.
- Los endpoints de dashboard consumen información consolidada de módulos como ``vehicle``, ``inventory``, ``drilling`` y ``checklist``.
