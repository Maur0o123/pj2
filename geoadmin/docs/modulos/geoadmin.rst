##########
Geoadmin
##########

Descripción General
*******************

El paquete ``geoadmin`` contiene la configuración global del proyecto Django: settings, arranque ASGI/WSGI, configuración de Celery y el enrutamiento principal de toda la plataforma.

Archivos principales
********************

.. code-block:: bash

    geoadmin/
    │── __init__.py
    │── asgi.py
    │── celery.py
    │── production.py
    │── settings.py
    │── urls.py
    │── wsgi.py

Responsabilidades
*****************

- Registrar las aplicaciones instaladas del sistema.
- Configurar middleware, base de datos, estáticos y media.
- Exponer el panel administrativo de Django.
- Integrar las rutas de todas las apps funcionales.
- Declarar manejadores globales de error ``400``, ``403``, ``404``, ``413`` y ``500``.

Rutas Globales (urls.py)
************************

El archivo ``geoadmin/urls.py`` centraliza las inclusiones del proyecto.

Ruta administrativa
===================

- ``/isamax/`` -> ``admin.site.urls``

Rutas incluidas sin prefijo
===========================

Las siguientes apps cuelgan directamente desde la raíz del sitio:

- ``include('core.urls')``
- ``include('user.urls')``
- ``include('vehicle.urls')``
- ``include('mining.urls')``
- ``include('maintenance.urls')``
- ``include('machine.urls')``
- ``include('documentation.urls')``
- ``include('messenger.urls')``
- ``include('planning.urls')``
- ``include('drilling.urls')``
- ``include('offline.urls')``
- ``include('api.urls')``
- ``include('checklist.urls')``
- ``include('inventory.urls')``
- ``include('equipment.urls')``

Rutas con prefijo
=================

- ``/prevencion/`` -> ``include('prevencion.urls')``

Archivos estáticos y media
**************************

- ``STATIC_URL`` se sirve usando ``static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)``.
- ``MEDIA_URL`` se sirve usando ``static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)``.
- En ``DEBUG`` también se fuerza la publicación de ``MEDIA_URL`` para desarrollo local.

Configuraciones complementarias
*******************************

``settings.py``
===============

Define la configuración base del proyecto: base de datos, autenticación, internacionalización, aplicaciones instaladas, archivos estáticos, templates y variables de entorno.

``production.py``
=================

Contiene los ajustes específicos del despliegue productivo.

``celery.py``
=============

Inicializa Celery para tareas asíncronas del sistema.

``asgi.py`` y ``wsgi.py``
=========================

Exponen la aplicación para servidores compatibles con ASGI y WSGI.
