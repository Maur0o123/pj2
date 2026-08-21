######
Mining
######

Descripción General
*******************

Este módulo gestiona la asignación de vehículos a faenas, incluyendo la administración de documentos asociados a cada faena. Contiene los archivos necesarios para la interacción con la base de datos, la interfaz de administración y la lógica de vistas.

.. code-block:: bash   

    mining/
    │── admin.py       # Configuración para la interfaz de administración de Django
    │── apps.py        # Configuración de la aplicación dentro del proyecto Django
    │── forms.py       # Definición de formularios para la creación y edición de datos
    │── migrations/    # Archivos de migración para la base de datos
    │── models.py      # Definición de modelos de datos
    │── urls.py        # Configuración de rutas del módulo
    │── views.py       # Lógica para las vistas

Modelos de Datos (models.py)
****************************

Define las entidades utilizadas en el sistema, es decir, las estructuras que interactúan con la base de datos.

VehiculoAsignado
================

Este modelo gestiona la asignación de vehículos a faenas específicas, registrando tanto la faena actual como la anterior, junto con las fechas de traspaso de un vehículo entre faenas.

- Campos:
    - ``vehiculo``: (ForeignKey) Relacionado con el modelo Vehiculo, almacena el vehículo asignado a la faena. Puede ser nulo o en blanco.
    - ``faena``: (ForeignKey) Relacionado con el modelo Faena, representa la faena actual en la que está asignado el vehículo.
    - ``faenaAnterior``: (CharField) Guarda el nombre de la faena anterior en la que estuvo asignado el vehículo.
    - ``fechaInicial``: (DateTimeField) Fecha de inicio del traspaso del vehículo a la nueva faena. Puede ser nula o en blanco.
    - ``fechaFinal``: (DateTimeField) Fecha final del traspaso, es decir, el momento en el que el vehículo dejó de estar asignado a la faena anterior. Puede ser nula o en blanco.
    - ``creador``: (CharField) Nombre del creador o responsable de la asignación del vehículo.
    - ``status``: (BooleanField) Estado del vehículo asignado (activo o inactivo).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en la que se creó el registro de asignación.
- Método:
    - ``__str__(self)``: Devuelve una representación del objeto, mostrando el nombre del vehículo asignado.
- Metadatos:
    - ``verbose_name``: "Vehículo en Faena".
    - ``verbose_name_plural``: "Vehículos en Faena".
    - ``db_table``: mining_vehicles.

DocumentoPorFaena
=================

Este modelo se utiliza para gestionar los documentos asociados a una faena y sus respectivos vehículos, almacenando la información relevante sobre la faena, patente y los documentos asociados.

- Campos:
    - ``faena``: (CharField) El nombre de la faena. Puede ser nulo.
    - ``patente``: (CharField) La patente del vehículo asociado a la faena. Puede ser nulo.
    - ``tipoDocumento``: (CharField) Tipo de documento que se está registrando (por ejemplo, licencia, certificado, etc.). Puede ser nulo.
    - ``fechaVencimiento``: (DateTimeField) La fecha de vencimiento del documento. Puede ser nulo o en blanco.
    - ``creador``: (CharField) El nombre del creador o responsable de la carga del documento. Puede ser nulo.
    - ``status``: (BooleanField) El estado del documento (activo/inactivo).
    - ``fechacreacion``: (DateTimeField) Fecha de creación del registro de documento, con valor por defecto la fecha actual.
- Método:
    - ``generaNombre(instance, filename)``: Genera un nombre de archivo único para los documentos subidos, basándose en la patente del vehículo, la faena y la fecha/hora de carga. El archivo se guarda en una ruta que incluye estos datos, organizando los documentos por faena y vehículo.
    - ``__str__(self)``: Devuelve una representación del objeto, mostrando el nombre de la faena junto con el nombre del archivo del documento.
- Metadatos:
    - ``verbose_name``: "Documento por Faena".
    - ``verbose_name_plural``: "Documentos por Faena".
    - ``db_table``: mining_documents.

Formularios (forms.py)
**********************

Contiene los formularios utilizados en las vistas.

FormVehiculoAsignacion
========================

Este formulario permite asignar un vehículo a una faena específica, registrando información clave sobre la asignación.

Campos del Formulario
----------------------

1. ``vehiculo``  
    - Etiqueta: Vehículo  
    - Descripción: Vehículo asignado.  
    - Deshabilitado: Sí  

2. ``faenaAnterior``  
    - Etiqueta: Faena Actual  
    - Descripción: Última faena en la que estuvo asignado el vehículo.  
    - Deshabilitado: Sí  

3. ``creador``  
    - Etiqueta: Asignado Por  
    - Descripción: Persona responsable de la asignación.  
    - Deshabilitado: Sí  

4. ``faena``  
    - Etiqueta: Faena Siguiente  
    - Descripción: Nueva faena a la que será asignado el vehículo.  
    - Requerido: Sí  

5. ``fechaInicial``  
    - Etiqueta: Fecha de Inicio  
    - Descripción: Fecha en la que se efectúa la asignación.  
    - Requerido: Sí  
    - Deshabilitado: Sí  

Consideraciones Adicionales
---------------------------

- ``faenaAnterior`` y ``creador`` están deshabilitados para evitar modificaciones manuales.  
- ``vehiculo`` no se puede editar, asegurando que la asignación sea coherente.  
- ``fechaInicial`` se establece automáticamente para evitar inconsistencias en la asignación.  


Vistas (views.py)
*****************

Contiene la lógica para procesar las solicitudes y devolver respuestas.

manage_vehicles_mining
======================

Esta función maneja la visualización de vehículos y sus asignaciones a faenas. 

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información relacionada con el usuario autenticado y las sesiones.

Funcionamiento
--------------

- Recupera la lista de vehículos activos y los vehículos asignados a faenas.
- Asocia a cada vehículo la faena asignada correspondiente o muestra "SIN ASIGNAR" si no está asignado.
- Renderiza la página ``manage_vehicles_mining.html`` con la lista de vehículos y las asignaciones de faenas.

Retorno
-------

- Renderiza la plantilla ``manage_vehicles_mining.html`` con el contexto de los vehículos y asignaciones.

---

edit_vehicle_mining
===================

Esta función permite editar la información de un vehículo asignado a una faena.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la sesión y los datos enviados por el usuario.

Funcionamiento
--------------

- Recupera los datos del vehículo y su historial de asignaciones.
- Obtiene los tipos de documentos de faena disponibles para la asignación.
- Renderiza la plantilla ``edit_vehicle_mining.html`` con los datos del vehículo y las asignaciones de faena.

Retorno
-------

- Renderiza la plantilla ``edit_vehicle_mining.html`` con el contexto del vehículo y sus asignaciones.

---

save_edit_vehicle_mining
=========================

Esta función guarda los cambios realizados en la asignación de un vehículo a una faena y los documentos asociados.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para recuperar los datos enviados por el formulario.

Funcionamiento
--------------

- Actualiza los documentos de faena asociados al vehículo, ya sea cambiando los documentos existentes o agregando nuevos.
- Actualiza la fecha de vencimiento de los documentos si es necesario.
- Si se ha cambiado la faena asignada, actualiza la asignación y crea un nuevo registro de asignación.
- Envía una notificación por correo sobre el cambio de faena.
- Redirige al usuario a la página de administración de vehículos después de guardar los cambios.

Retorno
-------

- Redirige a la página ``manage_vehicles_mining`` después de guardar los cambios.

---

select_documents_mining
========================

Esta función maneja la selección de documentos asociados a una faena y vehículo específicos a través de una solicitud AJAX.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener los datos enviados por el formulario mediante AJAX.

Funcionamiento
--------------

- Recupera la lista de documentos asociados a la faena seleccionada.
- Verifica si existen documentos previamente cargados para el vehículo y faena seleccionados.
- Devuelve una respuesta JSON con los documentos y sus detalles, incluyendo el tipo de documento, la URL del archivo, y la fecha de vencimiento.

Retorno
-------

- Retorna una respuesta JSON con la lista de documentos asociados a la faena y vehículo, o un error si la solicitud no es válida.

Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.

manage_vehicles_mining
=======================

Ruta para gestionar los vehículos de minería.

URL
---

- ``/manage_vehicles_mining``

Vista asociada
--------------

- ``manage_vehicles_mining``

---

edit_vehicle_mining
====================

Ruta para editar un vehículo de minería.

URL
---

- ``/edit_vehicle_mining``

Vista asociada
--------------

- ``edit_vehicle_mining``

---

save_edit_vehicle_mining
==========================

Ruta para guardar los cambios en el vehículo de minería.

URL
---

- ``/save_edit_vehicle_mining``

Vista asociada
--------------

- ``save_edit_vehicle_mining``

---

select_documents_mining
========================

Ruta para seleccionar los documentos de minería asociados al vehículo.

URL
---

- ``/select_documents_mining``

Vista asociada
--------------

- ``select_documents_mining``

