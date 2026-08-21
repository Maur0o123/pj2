#########
Messenger
#########

Descripción General
*******************

Este módulo contiene la lógica básica para la gestión de mensajes. Incluye los archivos esenciales como la definición de modelos, vistas y rutas.

.. code-block:: bash   

    messenger/
    │── admin.py        # Configuración para la interfaz de administración de Django
    │── apps.py         # Configuración de la aplicación dentro del proyecto Django
    │── migrations/     # Archivos de migración para la base de datos
    │── models.py       # Definición de modelos de datos
    │── urls.py         # Configuración de rutas del módulo
    │── views.py        # Lógica para las vistas

Modelos de Datos (models.py)
****************************

Define las entidades utilizadas en el sistema, es decir, las estructuras que interactúan con la base de datos.

Actualmente no se utiliza ningun modelo.

Vistas (views.py)
*****************

Contiene la lógica para procesar las solicitudes y devolver respuestas.

send_sms_message
================

Esta función envía un mensaje SMS utilizando la API de Twilio.

Parámetros
----------

- ``numero``:  
  El número de teléfono al que se enviará el mensaje. Debe ser un número válido en formato de 9 dígitos (sin el ``+56``).
  
- ``mensaje``:  
  El contenido del mensaje a enviar.

Funcionamiento
--------------

- Se utiliza la API de Twilio para enviar el mensaje al número de teléfono especificado.
- Si el mensaje se envía correctamente, se devuelve un objeto de mensaje.
- Si ocurre algún error, se captura la excepción ``TwilioRestException`` y se retorna ``None``.

Retorno
-------

- Si el mensaje se envía correctamente, retorna el objeto de mensaje.
- Si ocurre un error, retorna ``None``.

---

send_email_message
==================

Esta función envía un correo electrónico utilizando el backend de correo configurado en Django.

Parámetros
----------

- ``to_email``:  
  La dirección de correo electrónico del destinatario.
  
- ``subject``:  
  El asunto del correo electrónico.

- ``message``:  
  El contenido del mensaje a enviar.

Funcionamiento
--------------

- Utiliza el método ``send_mail`` de Django para enviar el correo electrónico.
- Si el correo se envía correctamente, no retorna nada.
- Si ocurre algún error, captura la excepción y retorna un diccionario con el mensaje de error.

Retorno
-------

- Si el correo se envía correctamente, no retorna nada.
- Si ocurre un error, retorna un diccionario con la clave ``"error"`` y el mensaje de error.

---

notificacion_vehiculos_email
=============================

Esta función envía una notificación por correo electrónico sobre la acción realizada en un vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``vehiculo``:  
  El objeto del vehículo relacionado con la notificación.
  
- ``action``:  
  La acción realizada en el vehículo (por ejemplo, ``"editado"`` o ``"eliminado"``).

Funcionamiento
--------------

- Genera un mensaje con la información del vehículo, la acción realizada y el usuario que realizó la acción.
- Envía el mensaje a los destinatarios, que son los usuarios con rol ``JEFE_MANTENCION``.
- También se agrega un correo adicional a la lista de destinatarios.

Retorno
-------

- No retorna ningún valor. La notificación se envía por correo electrónico.

---

notificacion_maquinarias_email
===============================

Esta función envía una notificación por correo electrónico sobre la acción realizada en una maquinaria.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``maquinaria``:  
  El objeto de la maquinaria relacionada con la notificación.
  
- ``action``:  
  La acción realizada en la maquinaria (por ejemplo, ``"editada"`` o ``"eliminada"``).

Funcionamiento
--------------

- Genera un mensaje con la información de la maquinaria, la acción realizada y el usuario que realizó la acción.
- Envía el mensaje a los destinatarios, que son los usuarios con rol ``JEFE_MANTENCION``.
- También se agrega un correo adicional a la lista de destinatarios.

Retorno
-------

- No retorna ningún valor. La notificación se envía por correo electrónico.

---

notificacion_usuarios_email
============================

Esta función envía una notificación por correo electrónico sobre la acción realizada en un usuario.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``usuario``:  
  El objeto del usuario relacionado con la notificación.
  
- ``action``:  
  La acción realizada sobre el usuario (por ejemplo, ``"editado"`` o ``"eliminado"``).

Funcionamiento
--------------

- Genera un mensaje con la información del usuario, la acción realizada y el usuario que realizó la acción.
- Envía el mensaje a un correo adicional, ya que en este caso no se especifican destinatarios dinámicos.

Retorno
-------

- No retorna ningún valor. La notificación se envía por correo electrónico.

notificacion_mantenedor_email
===============================

Esta función envía una notificación por correo electrónico a un mantenedor sobre una acción realizada en una sección específica.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``seccion``:  
  El nombre de la sección en la que se realizó la acción.

- ``nombre``:  
  El nombre del mantenedor sobre el cual se realizó la acción.

- ``action``:  
  La acción realizada sobre el mantenedor (por ejemplo, ``"editado"`` o ``"eliminado"``).

Funcionamiento
--------------

- Genera un mensaje con la información del mantenedor, la acción realizada y el usuario que realizó la acción.
- Envía el mensaje a los destinatarios, que en este caso son los correos adicionales especificados en la variable ``CORREO_ADICIONAL``.

Retorno
-------

- No retorna ningún valor. La notificación se envía por correo electrónico.

---

notificacion_mi_usuario_email
===============================

Esta función envía una notificación por correo electrónico sobre una acción realizada en un usuario específico.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``usuario``:  
  El objeto del usuario relacionado con la notificación.
  
- ``nombre``:  
  El nombre de la entidad (por ejemplo, ``"usuario"``) sobre la cual se realizó la acción.
  
- ``action``:  
  La acción realizada sobre el usuario (por ejemplo, ``"editado"`` o ``"eliminado"``).

Funcionamiento
--------------

- Genera un mensaje con la información del usuario, la acción realizada y el usuario que realizó la acción.
- Envía el mensaje al correo electrónico del usuario especificado.

Retorno
-------

- No retorna ningún valor. La notificación se envía por correo electrónico.

---

notificacion_admin_jefe_mantencion_email
=========================================

Esta función envía una notificación por correo electrónico a los administradores y jefes de mantención sobre una acción realizada en un documento.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``documento``:  
  El objeto del documento relacionado con la notificación.
  
- ``nombre``:  
  El nombre de la entidad (por ejemplo, ``"documento"``) sobre la cual se realizó la acción.
  
- ``action``:  
  La acción realizada sobre el documento (por ejemplo, ``"editado"`` o ``"eliminado"``).

Funcionamiento
--------------

- Genera un mensaje con la información del documento, la acción realizada y el usuario que realizó la acción.
- Envía el mensaje a los destinatarios, que son los usuarios con rol ``JEFE_MANTENCION`` y un correo adicional especificado en la variable ``CORREO_ADICIONAL``.

Retorno
-------

- No retorna ningún valor. La notificación se envía por correo electrónico.

---

notificacion_cambio_faena_vehiculo_email
=========================================

Esta función envía una notificación por correo electrónico sobre un cambio de faena en un vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``datos``:  
  El objeto que contiene la información sobre el vehículo y las faenas involucradas en el cambio.
  
- ``action``:  
  La acción realizada (por ejemplo, ``"cambiado"``).

Funcionamiento
--------------

- Genera un mensaje con la información del vehículo, las faenas involucradas y el usuario que realizó la acción.
- Envía el mensaje a los destinatarios, que son los jefes de mantención y supervisores asignados a la faena.

Retorno
-------

- No retorna ningún valor. La notificación se envía por correo electrónico.

---

notificacion_nuevo_mantenimiento_vehiculos_email_sms
======================================================

Esta función envía una notificación tanto por correo electrónico como SMS sobre un nuevo mantenimiento realizado en un vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``mantenimiento``:  
  El objeto de mantenimiento relacionado con el vehículo.
  
- ``problemas``:  
  La lista de problemas asociados al mantenimiento.
  
- ``progreso``:  
  El estado de progreso del mantenimiento.
  
- ``action``:  
  La acción realizada sobre el mantenimiento (por ejemplo, ``"registrado"`` o ``"actualizado"``).

Funcionamiento
--------------

- Genera un mensaje con la información del vehículo, el mantenimiento realizado, los problemas asociados, el progreso y el usuario que realizó la acción.
- Envía el mensaje a los destinatarios por correo electrónico (jefes de mantención, supervisores y un correo adicional).
- También envía el mensaje por SMS a los destinatarios, que incluyen administradores, jefes de mantención y supervisores.

Retorno
-------

- No retorna ningún valor. Las notificaciones se envían por correo electrónico y SMS.

notificacion_update_mantenimiento_vehiculos_email_sms
======================================================

Esta función envía una notificación sobre una actualización de mantenimiento realizada en un vehículo, tanto por correo electrónico como por SMS.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``mantenimiento``:  
  El objeto del mantenimiento relacionado con el vehículo.
  
- ``problemas``:  
  La lista de problemas asociados al mantenimiento.
  
- ``progreso``:  
  El estado de progreso del mantenimiento.
  
- ``action``:  
  La acción realizada sobre el mantenimiento (por ejemplo, ``"actualizado"``).

Funcionamiento
--------------

- Genera un mensaje con la información del vehículo, el mantenimiento realizado, los problemas asociados, el progreso y el usuario que realizó la acción.
- Envía el mensaje a los destinatarios por correo electrónico (jefes de mantención, supervisores y un correo adicional).
- También envía el mensaje por SMS a los destinatarios, que incluyen administradores, jefes de mantención y supervisores.

Retorno
-------

- No retorna ningún valor. Las notificaciones se envían por correo electrónico y SMS.

---

notificacion_nuevo_mantenimiento_maquinaria_email_sms
======================================================

Esta función envía una notificación sobre un nuevo mantenimiento realizado en una maquinaria, tanto por correo electrónico como por SMS.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``mantenimiento``:  
  El objeto del mantenimiento relacionado con la maquinaria.
  
- ``problemas``:  
  La lista de problemas asociados al mantenimiento.
  
- ``progreso``:  
  El estado de progreso del mantenimiento.
  
- ``action``:  
  La acción realizada sobre el mantenimiento (por ejemplo, ``"registrado"``).

Funcionamiento
--------------

- Genera un mensaje con la información de la maquinaria, el mantenimiento realizado, los problemas asociados, el progreso y el usuario que realizó la acción.
- Envía el mensaje a los destinatarios por correo electrónico (jefes de mantención, supervisores y un correo adicional).
- También envía el mensaje por SMS a los destinatarios, que incluyen administradores, jefes de mantención y supervisores.

Retorno
-------

- No retorna ningún valor. Las notificaciones se envían por correo electrónico y SMS.

---

notificacion_update_mantenimiento_maquinaria_email_sms
=======================================================

Esta función envía una notificación sobre una actualización de mantenimiento realizada en una maquinaria, tanto por correo electrónico como por SMS.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener la información del usuario que realizó la acción.
  
- ``mantenimiento``:  
  El objeto del mantenimiento relacionado con la maquinaria.
  
- ``problemas``:  
  La lista de problemas asociados al mantenimiento.
  
- ``progreso``:  
  El estado de progreso del mantenimiento.
  
- ``action``:  
  La acción realizada sobre el mantenimiento (por ejemplo, ``"actualizado"``).

Funcionamiento
--------------

- Genera un mensaje con la información de la maquinaria, el mantenimiento realizado, los problemas asociados, el progreso y el usuario que realizó la acción.
- Envía el mensaje a los destinatarios por correo electrónico (jefes de mantención, supervisores y un correo adicional).
- También envía el mensaje por SMS a los destinatarios, que incluyen administradores, jefes de mantención y supervisores.

Retorno
-------

- No retorna ningún valor. Las notificaciones se envían por correo electrónico y SMS.

---

notificacion_celery_email
===========================

Esta función envía una notificación de prueba utilizando el sistema Celery.

Parámetros
----------

- No recibe parámetros. 

Funcionamiento
--------------

- Envía un correo electrónico a un destinatario de prueba especificado en la variable ``CORREO_CELERY``.
  
Retorno
-------

- No retorna ningún valor. La notificación se envía por correo electrónico.

Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.

Actualmente  este archivo  no  contiene datos.