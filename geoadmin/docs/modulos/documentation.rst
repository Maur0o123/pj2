#############
Documentation
#############

Descripción General
*******************

El módulo ``documentation`` concentra procesos de generación documental y exportación para distintas áreas del sistema.

Actualmente se usa principalmente para:

- consulta de documentación minera general
- generación masiva de PDF para vehículos
- exportación a Excel y PDF
- reportes generales de sondaje

Archivos principales
********************

.. code-block:: bash

    documentation/
    │── apps.py
    │── urls.py
    │── views.py
    │── models.py

Nota sobre modelos
******************

El archivo ``models.py`` existe, pero actualmente no define modelos propios. La app opera principalmente como capa de vistas y generación de documentos a partir de información de otros módulos.

Rutas del módulo
****************

- ``view_general_mining_documents``: visualización de documentos generales asociados a faenas.
- ``select_massive_vehicles``: selección de vehículos para generación masiva.
- ``request_massive_vehicle_pdf``: construcción de solicitud para PDF masivo.
- ``generar_excel/``: exportación tabular.
- ``generar_pdf/``: exportación en PDF.
- ``manage_report_drilling``: administración de reportes de sondaje.
- ``report_drilling_general``: reporte general de perforación.
