##########
Prevencion
##########

Descripción General
*******************

El módulo ``prevencion`` ya se encuentra activo y cubre dos flujos principales:

- plantillas y documentos dinámicos de prevención por faena
- vigilancia médica de trabajadores expuestos a distintos riesgos

Capacidades actuales
********************

- mantenedor de plantillas por tipo de riesgo
- generación de documentos desde una estructura dinámica JSON
- adjuntos generales, por sección y por ítem
- historial, edición y eliminación lógica de documentos
- gestión de vigilancia médica con evidencias
- catálogos configurables para GES, área, cargo, exposición y seguimiento
- sincronización parcial de datos personales con ``UsuarioProfile``

Modelos principales
*******************

``PrevencionPlantilla``
=======================

Plantilla parametrizable por faena y tipo de riesgo. La estructura del documento se guarda en ``JSONField``.

Tipos soportados:

- ``condiciones``
- ``silice``
- ``ruido``
- ``hipobaria``
- ``psicosocial``
- ``tmert``
- ``mmc``

``PrevencionDocumento``
=======================

Instancia concreta de un documento generado desde una plantilla, con snapshot del contenido completo y evidencias.

``PrevencionEvidenciaGeneral`` y ``PrevencionEvidenciaSeccion``
===============================================================

Adjuntos asociados al documento, tanto globales como por sección.

``PrevencionEvidenciaItem``
===========================

Adjuntos asociados a filas o ítems específicos dentro de una sección del documento dinámico.

``VigilanciaOpcion``
====================

Catálogo dinámico para combos de vigilancia médica, con unicidad por tipo y valor.

``VigilanciaMedica``
====================

Ficha de vigilancia ocupacional del trabajador. Consolida datos personales, contractuales y controles para sílice, ruido, hipobaria y otros agentes.

``VigilanciaAdjunto``
=====================

Adjuntos complementarios vinculados a una vigilancia médica.

Rutas del módulo
****************

Plantillas:

- ``/prevencion/mantenedor/<str:tipo_slug>/``
- ``/prevencion/mantenedor/<str:tipo_slug>/nuevo/``
- ``/prevencion/mantenedor/<str:tipo_slug>/editar/<int:pk>/``
- ``/prevencion/mantenedor/eliminar/<int:pk>/``

Documentos:

- ``/prevencion/documento/nuevo/``
- ``/prevencion/documento/historial/``
- ``/prevencion/documento/ver/<int:pk>/``
- ``/prevencion/documento/editar/<int:pk>/``
- ``/prevencion/documento/eliminar/<int:pk>/``

Vigilancia médica:

- ``/prevencion/vigilancia/``
- ``/prevencion/vigilancia/nuevo/``
- ``/prevencion/vigilancia/editar/<int:pk>/``
- ``/prevencion/vigilancia/ver/<int:pk>/``
- ``/prevencion/vigilancia/opciones/<str:tipo_slug>/``
- ``/prevencion/vigilancia/opciones/<str:tipo_slug>/nuevo/``
- ``/prevencion/vigilancia/opciones/<str:tipo_slug>/guardar/``
- ``/prevencion/vigilancia/opciones/<str:tipo_slug>/estado/``

Endpoints auxiliares:

- ``/prevencion/ajax/load-plantillas/``
- ``/prevencion/ajax/get-structure/``
- ``/prevencion/api/buscar-usuario-rut/``
- rutas de eliminación de evidencias y adjuntos

Notas de implementación
***********************

- El módulo filtra visibilidad por ``faena`` según el perfil del usuario.
- La plantilla usa ``JSONField`` para permitir formularios dinámicos sin cambiar el esquema relacional en cada variación documental.
- La vigilancia médica calcula estados de gestión y vigencias a partir de los datos registrados y los adjuntos disponibles.
