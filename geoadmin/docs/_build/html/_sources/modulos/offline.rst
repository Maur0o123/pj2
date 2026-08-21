#######
Offline
#######

Descripción General
*******************

Este módulo está diseñado para gestionar la funcionalidad offline del proyecto. Se encarga de realizar la administración básica de los datos necesarios para el funcionamiento en entornos sin conexión, manteniendo las funcionalidades esenciales del sistema.

.. code-block:: bash   

    offline/
    │── admin.py         # Configuración para la interfaz de administración de Django
    │── apps.py          # Configuración de la aplicación dentro del proyecto Django
    │── __init__.py      # Marca el directorio como un paquete de Python
    │── migrations/      # Archivos de migración para la base de datos
    │── models.py        # Definición de modelos de datos
    │── urls.py          # Configuración de rutas del módulo
    │── views.py         # Lógica para las vistas

Modelos de Datos (models.py)
****************************

Este archivo contiene la definición de los modelos de datos que se utilizan para interactuar con la base de datos en el módulo.

Actualmente no tiene modelos.

Vistas (views.py)
*****************

Las vistas contienen la lógica para procesar las solicitudes y devolver respuestas.

service_worker
===============

Esta función maneja la solicitud del Service Worker en la aplicación.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud del Service Worker.

Funcionamiento
--------------

- Recupera el archivo ``service-worker.js`` desde la carpeta estática de la aplicación.
- Devuelve el archivo como una respuesta HTTP con el tipo de contenido ``application/javascript``.

Retorno
-------

- Retorna el archivo ``service-worker.js`` como una respuesta ``FileResponse`` con el tipo de contenido adecuado.

---

sondajeOffline
===============

Esta función renderiza la vista de una página de "sondaje" en modo offline.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de la página offline.

Funcionamiento
--------------

- No requiere procesamiento de datos adicionales.
- Renderiza la plantilla ``homesondaje.html``, que es una vista para la sección de "sondaje" cuando la aplicación está en modo offline.

Retorno
-------

- Retorna el renderizado de la plantilla ``homesondaje.html`` con un contexto vacío.

---

reporteDigitalOffline
======================

Esta función renderiza la vista de un reporte digital en modo offline.

.. note::

   La función existe en ``views.py``, pero actualmente no está expuesta en ``urls.py``.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de la página offline.

Funcionamiento
--------------

- No requiere procesamiento de datos adicionales.
- Renderiza la plantilla ``new_reporte_digital.html``, que es una vista para la sección de "nuevo reporte digital" cuando la aplicación está en modo offline.

Retorno
-------

- Retorna el renderizado de la plantilla ``new_reporte_digital.html`` con un contexto vacío.

---

editarReporteDigitalOffline
============================

Esta función renderiza la vista para editar un reporte digital en modo offline.

.. note::

   La función existe en ``views.py``, pero actualmente no está expuesta en ``urls.py``.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de la página de edición del reporte digital.

Funcionamiento
--------------

- No requiere procesamiento de datos adicionales.
- Renderiza la plantilla ``edit_reporte_digital.html``, que es una vista para editar reportes digitales en modo offline.

Retorno
-------

- Retorna el renderizado de la plantilla ``edit_reporte_digital.html`` con un contexto vacío.



Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.

sondajeOffline
================

Ruta para gestionar el sondaje en modo offline.

URL
---

- ``/sondajeOffline/``

Vista asociada
--------------

- ``sondajeOffline``

---

service-worker.js
===================

Ruta para servir el archivo ``service-worker.js``.

URL
---

- ``/service-worker.js``

Vista asociada
--------------

- ``service_worker``
