########
Planning
########

Descripción General
*******************

Este módulo está destinado a gestionar las funcionalidades relacionadas con la planificación dentro del proyecto. Proporciona la administración de recursos, la configuración de actividades, y las interacciones necesarias para la gestión eficiente de los procesos de planificación.

.. code-block:: bash   

    planning/
    │── admin.py         # Configuración para la interfaz de administración de Django
    │── apps.py          # Configuración de la aplicación dentro del proyecto Django
    │── forms.py         # Formularios para la entrada de datos
    │── __init__.py      # Marca el directorio como un paquete de Python
    │── migrations/      # Archivos de migración para la base de datos
    │── models.py        # Definición de modelos de datos
    │── urls.py          # Configuración de rutas del módulo
    │── views.py         # Lógica para las vistas

Modelos de Datos (models.py)
*****************************

Este archivo define los modelos de datos que interactúan con la base de datos del módulo, facilitando la gestión de la planificación.

PlanificacionFaenas
===================
    
Este modelo está diseñado para gestionar la planificación de faenas, asociando una faena con un tipo de vehículo y permitiendo la asignación de valores para cada mes, entre otros.

- Campos:
    - ``faena``: (ForeignKey) Relaciona el registro con una faena específica.
    - ``tipo``: (ForeignKey) Relaciona el registro con un tipo de vehículo específico.
    - ``mes``: (CharField) El mes al que corresponde la planificación, utilizando opciones predefinidas (como "Enero", "Febrero", etc.). Puede ser nulo o en blanco.
    - ``cantidad``: (IntegerField) El valor asociado a la planificación para el mes, como una cantidad de vehículos o recursos. Puede ser nulo o en blanco.
    - ``fechacreacion``: (DateTimeField) Fecha de creación del registro de planificación, con valor por defecto la fecha actual.
- Método:
    - ``__str__(self)``: Devuelve una representación del objeto, mostrando el nombre de la faena junto con el tipo de vehículo asociado.
- Metadatos:
    - ``verbose_name``: "Planificación por Faena y Tipo de Vehículo".
    - ``verbose_name_plural``: "Planificación por Faena y Tipo de Vehículos".
    - ``db_table``: planning_minning_type.

Formularios (forms.py)
**********************

Los formularios permiten crear o actualizar datos de manera sencilla desde la interfaz web.

FormPlanificacionFaenas
=======================

Este formulario permite ingresar la cantidad de recursos o actividades planificadas para una faena.

Campos del Formulario
----------------------

1. ``cantidad``  
    - Descripción: Número que representa la cantidad planificada.  
    - Requerido: Sí  

Consideraciones Adicionales
---------------------------

- La cantidad ingresada será utilizada en la planificación y gestión de faenas dentro del sistema.
- Asegura un registro estructurado y preciso de la planificación.


FormSelectFaena
===============

Este formulario permite seleccionar una faena para su planificación.

Campos del Formulario
----------------------

1. ``faena``  
    - Etiqueta: Seleccione Faena  
    - Descripción: Lista desplegable con las faenas disponibles ordenadas alfabéticamente.  
    - Requerido: Sí  

Consideraciones Adicionales
---------------------------

- La faena seleccionada se utiliza en la planificación de faenas dentro del sistema.
- Este formulario facilita la asignación de faenas de manera organizada.

FormSelectTipo
==============

Este formulario permite seleccionar el tipo de vehículo dentro del modelo ``PlanificacionFaenas``.

Campos del Formulario
----------------------

1. ``tipo``  
    - Tipo: ForeignKey a ``Tipo``  
    - Etiqueta: Seleccione Tipo Vehículo  
    - Descripción: Permite seleccionar un tipo de vehículo dentro de la planificación de faenas.  
    - Requerido: Sí  
    - Widget: Select  

Consideraciones Adicionales
---------------------------

- El campo ``tipo`` se llena con todas las instancias de ``Tipo`` ordenadas por su nombre.  


Vistas (views.py)
*****************

Las vistas contienen la lógica para procesar las solicitudes y devolver respuestas.

new_planning_select_mining
===========================

Esta función maneja la vista para la selección de planificación de faenas en minería.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de la vista de planificación.

Funcionamiento
--------------

- Recupera todos los tipos de planificación disponibles, ordenados por el campo ``tipo``.
- Recupera todos los meses disponibles para la planificación.
- Realiza una consulta para obtener la planificación de faenas agrupada por mes y tipo, con el total de cantidades sumadas.
- Obtiene el total de las cantidades agrupadas por mes.
- Renderiza la plantilla ``new_planning.html`` con los datos de planificación y los tipos de faena.

Retorno
-------

- Retorna el renderizado de la plantilla ``new_planning.html`` con el contexto que incluye los tipos de planificación, los meses, la planificación detallada y los totales por mes.

---

view_planning_mining
=====================

Esta función muestra la vista de planificación de faenas para minería.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de la vista de planificación.

Funcionamiento
--------------

- Recupera todos los tipos de planificación disponibles, ordenados por el campo ``tipo``.
- Recupera todos los meses disponibles para la planificación.
- Realiza una consulta para obtener la planificación de faenas agrupada por mes y tipo, con el total de cantidades sumadas.
- Obtiene el total de las cantidades agrupadas por mes.
- Define que se visualizarán todas las faenas disponibles.
- Renderiza la plantilla ``view_planning_minning.html`` con los datos de planificación y las faenas.

Retorno
-------

- Retorna el renderizado de la plantilla ``view_planning_minning.html`` con el contexto que incluye los tipos de planificación, los meses, la planificación detallada, el total por mes y el nombre de las faenas.

---

view_planning_type
===================

Esta función muestra la vista de planificación por tipo de vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de la vista de planificación por tipo.

Funcionamiento
--------------

- Recupera todas las faenas disponibles, ordenadas por el campo ``faena``.
- Recupera todos los meses disponibles para la planificación.
- Realiza una consulta para obtener la planificación de faenas agrupada por mes y tipo, con el total de cantidades sumadas.
- Obtiene el total de las cantidades agrupadas por mes.
- Define que se visualizarán todos los vehículos disponibles.
- Renderiza la plantilla ``view_planning_type.html`` con los datos de planificación y los tipos de vehículos.

Retorno
-------

- Retorna el renderizado de la plantilla ``view_planning_type.html`` con el contexto que incluye las faenas, los meses, la planificación detallada, el total por mes y el tipo de vehículo.

edit_planning_mining
=====================

Esta función maneja la edición de la planificación de faenas para minería.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de edición de la planificación.

Funcionamiento
--------------

- Verifica si la solicitud es un ``POST``.
- Recupera la faena seleccionada mediante el parámetro ``faena`` de la solicitud.
- Obtiene la planificación de faenas asociada a la faena seleccionada.
- Calcula el total de la cantidad de planificación por mes.
- Recupera todos los tipos disponibles de planificación ordenados por ``tipo``.
- Organiza la información de la planificación, los meses y los tipos en listas.
- Devuelve un ``JsonResponse`` con la información organizada.

Retorno
-------

- Retorna un ``JsonResponse`` con los tipos de planificación, la planificación por mes y tipo, el total por mes, y la faena seleccionada.

---

get_planning_mining
====================

Esta función maneja la obtención de la planificación de faenas para minería.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de obtención de planificación.

Funcionamiento
--------------

- Verifica si la solicitud es un ``POST``.
- Recupera la faena seleccionada mediante el parámetro ``faena`` de la solicitud.
- Obtiene la planificación de faenas asociada a la faena seleccionada.
- Calcula el total de la cantidad de planificación por mes.
- Recupera todos los tipos disponibles de planificación ordenados por ``tipo``.
- Organiza la información de la planificación, los meses y los tipos en listas.
- Devuelve un ``JsonResponse`` con la información organizada.

Retorno
-------

- Retorna un ``JsonResponse`` con los tipos de planificación, la planificación por mes y tipo, el total por mes.

---

get_planning_type
==================

Esta función maneja la obtención de la planificación por tipo de vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de obtención de planificación por tipo.

Funcionamiento
--------------

- Verifica si la solicitud es un ``POST``.
- Recupera el tipo de vehículo seleccionado mediante el parámetro ``tipo`` de la solicitud.
- Obtiene la planificación de faenas asociada al tipo de vehículo seleccionado.
- Calcula el total de la cantidad de planificación por mes.
- Recupera todas las faenas disponibles, ordenadas por ``faena``.
- Cuenta los vehículos disponibles para el tipo de vehículo seleccionado.
- Organiza la información de la planificación, los meses, los tipos de faenas y el stock de vehículos en listas.
- Devuelve un ``JsonResponse`` con la información organizada.

Retorno
-------

- Retorna un ``JsonResponse`` con las faenas, la planificación por mes y faena, el total por mes y la cantidad de vehículos disponibles para el tipo seleccionado.

---

update_planning_value
======================

Esta función maneja la actualización de valores de planificación.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de actualización de valores de planificación.

Funcionamiento
--------------

- La función está marcada como ``@csrf_exempt``, lo que significa que no requiere protección CSRF.
- Su funcionamiento dependerá del código que se complete después del decorador. Es probable que reciba parámetros relacionados con los valores de planificación y los actualice en la base de datos.

Retorno
-------

- No se especifica un retorno en este fragmento de código, pero se espera que devuelva una respuesta (probablemente un ``JsonResponse`` o una redirección).


Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.


new_planning_select_mining
===========================

Ruta para crear un nuevo plan de minería seleccionando un tipo de minería.

URL
---

- ``/new_planning_select_mining``

Vista asociada
--------------

- ``new_planning_select_mining``

---

view_planning_mining
====================

Ruta para ver el plan de minería.

URL
---

- ``/view_planning_mining``

Vista asociada
--------------

- ``view_planning_mining``

---

view_planning_type
===================

Ruta para ver el tipo de planificación.

URL
---

- ``/view_planning_type``

Vista asociada
--------------

- ``view_planning_type``

---

edit_planning_mining
====================

Ruta para editar el plan de minería.

URL
---

- ``/edit_planning_mining``

Vista asociada
--------------

- ``edit_planning_mining``

---

get_planning_mining
====================

Ruta para obtener los datos del plan de minería.

URL
---

- ``/get_planning_mining``

Vista asociada
--------------

- ``get_planning_mining``

---

get_planning_type
==================

Ruta para obtener el tipo de planificación.

URL
---

- ``/get_planning_type``

Vista asociada
--------------

- ``get_planning_type``

---

update_planning_value
======================

Ruta para actualizar el valor del plan de minería.

URL
---

- ``/update_planning_value``

Vista asociada
--------------

- ``update_planning_value``

---

new_planning_drilling
======================

Ruta para crear una nueva planificación asociada al programa de sondaje.

URL
---

- ``/new_planning_drilling``

Vista asociada
--------------

- ``new_planning_drilling``

---

edit_drilling_program
======================

Ruta para editar un programa de perforación.

URL
---

- ``/edit_drilling_program``

Vista asociada
--------------

- ``edit_drilling_program``

---

update_drilling_program
========================

Ruta para actualizar los valores del programa de perforación.

URL
---

- ``/update_drilling_program``

Vista asociada
--------------

- ``update_drilling_program``
