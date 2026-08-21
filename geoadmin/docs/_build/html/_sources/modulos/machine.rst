#######
Machine
#######

Descripción General
********************

Este módulo permite la administración de maquinaria en faena, incluyendo su mantenimiento, control de horómetros y kits de maquinaria.

.. code-block:: bash   

    machine/
    │── admin.py        # Configuración del panel de administración de Django
    │── apps.py         # Configuración de la aplicación Django
    │── forms.py        # Formularios utilizados dentro del módulo
    │── models.py       # Definición de modelos de datos
    │── urls.py         # Definición de rutas para las vistas del módulo
    │── views.py        # Lógica de controladores para las vistas
    │── migrations/     # Archivos de migración para la base de datos

Modelos de Datos (models.py)
****************************

Define las entidades utilizadas en el sistema para gestionar maquinaria, mantenimiento y horómetros.

Maquinaria
==========

El modelo Maquinaria representa la información detallada de cada equipo o maquinaria utilizada en las operaciones.

- Campos:
    - ``maquinaria``: (CharField) Nombre único de la maquinaria.
    - ``descripcion``: (CharField) Descripción única de la maquinaria.
    - ``fechaAdquisicion``: (DateTimeField) Fecha en que la maquinaria fue adquirida.
    - ``tipo``: (ForeignKey) Relación con TipoMaquinaria, identificando el tipo de maquinaria.
    - ``marca``: (ForeignKey) Relación con MarcaMaquinaria, indicando la marca de la maquinaria.
    - ``faena``: (ForeignKey) Relación con Faena, especificando en qué faena está asignada la maquinaria.
    - ``frecuenciaMantenimiento``: (IntegerField) Frecuencia de mantenimiento en horas.
    - ``status``: (BooleanField) Estado del registro (True para activo, False para inactivo).
    - ``fechacreacion``: (DateTimeField) Fecha de creación del registro.
    - ``fotografia``: (ImageField) Imagen de la maquinaria con un método de generación de nombre de archivo.
- Métodos:
    - ``generaNombre(instance, filename)``: Genera un nombre de archivo único basado en la fecha y el nombre de la maquinaria.
    - ``__str__(self)``: Retorna el nombre de la maquinaria como representación en cadena.
- Metadatos:
    - ``verbose_name``: "Maquinaria".
    - ``verbose_name_plural``: "Maquinarias".

MaquinariaFaena
===============

El modelo MaquinariaFaena representa la asignación de maquinarias a diferentes faenas mineras.

- Campos:
    - ``maquinaria``: (ForeignKey) Relación con Maquinaria, indicando qué maquinaria se asigna.
    - ``faena``: (ForeignKey) Relación con Faena, especificando la faena a la que pertenece la maquinaria.
    - ``status``: (BooleanField) Estado del registro (True para activo, False para inactivo).
    - ``creador``: (CharField) Usuario que creó el registro.
    - ``fechacreacion``: (DateTimeField) Fecha de creación del registro.
- Métodos:
    - ``__str__(self)``: Retorna el nombre de la maquinaria como representación en cadena.
- Metadatos:
    - ``verbose_name``: "Maquinaria Faena".
    - ``verbose_name_plural``: "Maquinarias Faenas".
    - ``db_table``: mining_machines.

NuevoHorometro
==============
    
El modelo NuevoHorometro permite registrar el estado del horómetro (indicador de horas de operación) de las maquinarias, así como detalles relacionados con su creación.

- Campos:
    - ``maquinaria``: (ForeignKey) Relación con el modelo Maquinaria, indicando la maquinaria asociada al horómetro.
    - ``horometro``: (IntegerField) Valor del horómetro actual de la maquinaria (en horas).
    - ``fechacreacion``: (DateTimeField) Fecha en la que se registró el horómetro.
    - ``creador``: (CharField) Usuario que creó el registro.
    - ``origen``: (CharField) Origen o fuente del registro del horómetro (opcional).
- Métodos:
    - ``__str__(self)``: Devuelve el nombre de la maquinaria como representación en cadena.
- Metadatos:
    - ``verbose_name``: "Horómetro Maquinaria".
    - ``verbose_name_plural``: "Horómetros Maquinarias".
    - ``db_table``: machine_horometres_registers.

KitsMaquinariaFaena
===================

El modelo KitsMaquinariaFaena asocia un "kit de maquinaria" a una "faena" específica, permitiendo gestionar qué kits están disponibles o asignados a cada faena.

- Campos:
    - ``kitMaquinaria``: (ForeignKey) Relación con el modelo KitsMaquinaria, indicando el kit de maquinaria asignado.
    - ``faena``: (ForeignKey) Relación con el modelo Faena, indicando la faena a la que se asigna el kit de maquinaria.
    - ``fechacreacion``: (DateTimeField) Fecha en la que se registró la asignación del kit a la faena.
    - ``creador``: (CharField) Usuario que creó el registro de asignación.
    - ``status``: (BooleanField) Estado del registro, indicando si está activo o inactivo.
- Métodos:
    - ``__str__(self)``: Devuelve el nombre del kitMaquinaria como representación en cadena.
- Metadatos:
    - ``verbose_name``: "Kit Maquinaria por Faena".
    - ``verbose_name_plural``: "Kits Maquinarias por Faenas".
    - ``db_table``: machine_kits_machine_mining.
    - ``constraints``: Un UniqueConstraint que asegura que no haya duplicados para el par de campos faena y kitMaquinaria (esto significa que un mismo kit no puede ser asignado dos veces a la misma faena).

HistorialStockKitsMaquinariaFaena
=================================

El modelo HistorialStockKitsMaquinariaFaena gestiona los registros históricos de movimientos de stock de los kits de maquinaria asignados a faenas, permitiendo realizar un seguimiento del cambio de cantidades disponibles y sus descripciones.

- Campos:
    - ``kitMaquinaria``: (ForeignKey) Relación con el modelo KitsMaquinariaFaena, que indica el kit de maquinaria asociado al historial de stock.
    - ``faena``: (ForeignKey) Relación con el modelo Faena, indicando la faena asociada al historial de stock del kit de maquinaria.
    - ``stockMovimiento``: (IntegerField) Movimiento de stock, representando el cambio en la cantidad de kits (positivo o negativo).
    - ``stockActual``: (IntegerField) La cantidad actual de stock después del movimiento.
    - ``descripcion``: (CharField) Descripción del movimiento de stock (por ejemplo, "Ingreso", "Salida", "Ajuste").
    - ``fechacreacion``: (DateTimeField) Fecha en la que se registró el movimiento del stock.
    - ``creador``: (CharField) Usuario que registró el movimiento de stock.
    - ``status``: (BooleanField) Estado del registro, indicando si está activo o inactivo.
- Métodos:
    - ``__str__(self)``: Devuelve el nombre del kitMaquinaria como representación en cadena del registro.
- Metadatos:
    - ``verbose_name``: "Historial Stock Kit Maquinaria".
    - ``verbose_name_plural``: "Historial Stock Kits Maquinarias".
    - ``db_table``: machine_kits_stock_history.

Formularios (forms.py)
**********************

Contiene los formularios utilizados en las vistas.

FormMaquinaria
==============

Este formulario está diseñado para registrar información relacionada con la maquinaria, incluyendo el tipo, la marca, la faena a la que está asignada y otros detalles.

Campos del Formulario
----------------------

1. ``maquinaria``

    - Tipo: CharField
    - Etiqueta: No especificada (campo de texto libre para la identificación de la maquinaria).
    - Descripción: Campo para ingresar el nombre o número de identificación de la maquinaria.

2. ``descripcion``

    - Tipo: CharField (opcional)
    - Etiqueta: No especificada (campo de texto libre para describir la maquinaria o su función).
    - Descripción: Campo opcional para proporcionar una descripción adicional de la maquinaria.

3. ``fechaAdquisicion``

    - Tipo: DateTimeField
    - Etiqueta: Fecha de adquisición
    - Descripción: Fecha en la que la maquinaria fue adquirida.
    - Widget: Se utiliza un widget de tipo ``date`` para ingresar la fecha.

4. ``tipo``

    - Tipo: ForeignKey a ``TipoMaquinaria``
    - Etiqueta: Tipo de maquinaria
    - Descripción: Selección del tipo de maquinaria.
    - Requerido: Sí
    - Widget: Select, estilo centrado.

5. ``marca``

    - Tipo: ForeignKey a ``MarcaMaquinaria``
    - Etiqueta: Marca de maquinaria
    - Descripción: Selección de la marca de la maquinaria.
    - Requerido: Sí
    - Widget: Select, estilo centrado.

6. ``faena``

    - Tipo: ForeignKey a ``Faena``
    - Etiqueta: Faena a la que está asignada la maquinaria
    - Descripción: Selección de la faena a la que está asignada la maquinaria.
    - Requerido: Sí
    - Widget: Select, estilo centrado.

7. ``frecuenciaMantenimiento``

    - Tipo: CharField
    - Etiqueta: Frecuencia de mantenimiento
    - Descripción: Campo para especificar la frecuencia de mantenimiento de la maquinaria.
    - Widget: TextInput con tipo numérico.

Consideraciones Adicionales
---------------------------

- El campo ``faena`` está habilitado o deshabilitado en función del parámetro ``faena_disabled`` pasado al formulario.
- La selección de la faena, el tipo y la marca se filtra dinámicamente según los parámetros actuales pasados al formulario (``faena_actual``, ``marca_actual``, ``tipo_actual``).
- Los campos ``faena``, ``marca`` y ``tipo`` son obligatorios.
- El campo ``descripcion`` está marcado como opcional y no es obligatorio.

FormNuevoHorometro
===================

Este formulario está diseñado para registrar un nuevo horómetro asociado a una maquinaria específica.

Campos del Formulario
----------------------

1. ``maquinaria``

    - Tipo: ForeignKey a ``Maquinaria``
    - Etiqueta: Maquinaria
    - Descripción: Selección de la maquinaria para la cual se registra el nuevo horómetro.
    - Requerido: Sí
    - Widget: Select, estilo centrado.
    - Nota: El queryset para este campo se filtra dinámicamente en función de las maquinarias proporcionadas (si se pasan maquinarias como argumento) o se establece como un queryset vacío si no se proporcionan.

2. ``horometro``

    - Tipo: IntegerField
    - Etiqueta: Horómetro
    - Descripción: Campo numérico para ingresar el valor del horómetro asociado a la maquinaria seleccionada.
    - Requerido: Sí
    - Widget: TextInput con tipo numérico.

Consideraciones Adicionales
---------------------------

- El campo ``maquinaria`` se filtra dependiendo de las maquinarias pasadas al formulario mediante el parámetro ``maquinarias``. Si no se proporcionan, el campo tendrá un queryset vacío.

FormNuevoKitReparacionFaena
============================

Este formulario se utiliza para asociar un kit de maquinaria a una faena específica para tareas de reparación.

Campos del Formulario
----------------------

1. ``faena``

    - Tipo: ForeignKey a ``Faena``
    - Etiqueta: Faena
    - Descripción: Selección de la faena a la que se asociará el kit de reparación.
    - Requerido: Sí
    - Widget: Select, con estilo centrado.
    - Filtrado: Excluye faenas con el nombre ``SIN ASIGNAR`` y las ordena por nombre.

2. ``kitMaquinaria``

    - Tipo: ForeignKey a ``KitsMaquinaria``
    - Etiqueta: Kit de Maquinaria
    - Descripción: Selección del kit de maquinaria que se asociará a la faena.
    - Requerido: Sí
    - Widget: Select, con estilo centrado.
    - Filtrado: Se seleccionan los kits de maquinaria relacionados con la marca y tipo de maquinaria.
    - Etiqueta personalizada: La etiqueta de cada opción se personaliza mostrando el nombre del kit, la marca y el tipo de la maquinaria asociada a ese kit.

Consideraciones Adicionales
---------------------------

- El campo ``faena`` excluye faenas sin asignar, garantizando que solo se pueda asociar un kit a faenas válidas.
- El campo ``kitMaquinaria`` presenta una lista filtrada de kits de maquinaria, ordenada por nombre, con una etiqueta personalizada que incluye el nombre del kit, la marca y el tipo de maquinaria.

FormEditKitsMaquinariaFaena
============================

Este formulario se utiliza para editar un historial de stock de kits de maquinaria asignados a una faena. Permite ver la información del kit de maquinaria y su faena asociada, pero no permite editar estos campos.

Campos del Formulario
----------------------

1. ``kitMaquinaria``

    - Tipo: ForeignKey a ``KitsMaquinaria``
    - Etiqueta: Kit Reparación Maquinaria
    - Descripción: Muestra el kit de reparación de maquinaria asignado a la faena.
    - Requerido: Sí
    - Widget: Select, con estilo centrado.
    - Estado: Deshabilitado (no editable).

2. ``faena``

    - Tipo: ForeignKey a ``Faena``
    - Etiqueta: Faena
    - Descripción: Muestra la faena asociada al historial de stock.
    - Requerido: Sí
    - Widget: Select, con estilo centrado.
    - Estado: Deshabilitado (no editable).

3. ``stockMovimiento``

    - Tipo: IntegerField
    - Etiqueta: Movimiento de Stock
    - Descripción: Campo para ingresar el movimiento de stock, indicando la cantidad que entra o sale del stock.
    - Requerido: Sí
    - Widget: TextInput con tipo ``number`` y clase ``form-control``.

4. ``stockActual``

    - Tipo: IntegerField
    - Etiqueta: Stock Actual
    - Descripción: Muestra la cantidad actual de stock disponible del kit de maquinaria.
    - Requerido: Sí
    - Widget: TextInput con tipo ``number`` y clase ``form-control``.
    - Estado: Deshabilitado (no editable).

5. ``descripcion``

    - Tipo: CharField
    - Etiqueta: Descripción
    - Descripción: Campo para agregar una descripción del movimiento de stock realizado.
    - Requerido: Sí
    - Widget: TextInput con clase ``form-control``.

Consideraciones Adicionales
---------------------------

- Los campos ``faena``, ``kitMaquinaria`` y ``stockActual`` están deshabilitados para evitar modificaciones.
- El formulario permite editar solo el ``stockMovimiento`` y la ``descripcion`` del movimiento de stock.

FormEditKitsMaquinariaFaenaAdd
===============================

Este formulario se utiliza para agregar nuevos registros de stock de kits de maquinaria asignados a una faena. Permite agregar el stock de un kit de maquinaria a la faena correspondiente y actualizar la información del stock.

Campos del Formulario
----------------------

1. ``kitMaquinaria``

    - Tipo: ForeignKey a ``KitsMaquinaria``
    - Etiqueta: Kit Reparación Maquinaria
    - Descripción: Muestra el kit de reparación de maquinaria asignado a la faena.
    - Requerido: Sí
    - Widget: Select, con estilo centrado.

2. ``faena``

    - Tipo: ForeignKey a ``Faena``
    - Etiqueta: Faena
    - Descripción: Muestra la faena asociada al historial de stock.
    - Requerido: Sí
    - Widget: Select, con estilo centrado.

3. ``stockMovimiento``

    - Tipo: IntegerField
    - Etiqueta: Movimiento de Stock
    - Descripción: Campo para ingresar el movimiento de stock, indicando la cantidad que entra o sale del stock.
    - Requerido: Sí
    - Widget: TextInput con tipo ``number`` y clase ``form-control``.

4. ``stockActual``

    - Tipo: IntegerField
    - Etiqueta: Stock Actual
    - Descripción: Muestra la cantidad actual de stock disponible del kit de maquinaria.
    - Requerido: Sí
    - Widget: TextInput con tipo ``number`` y clase ``form-control``.

Consideraciones Adicionales
---------------------------

- Los campos ``faena`` y ``kitMaquinaria`` son requeridos, ya que se deben asociar a una faena y a un kit específico.
- El campo ``stockMovimiento`` es requerido para indicar el movimiento de stock, mientras que el campo ``stockActual`` muestra el stock disponible después de dicho movimiento.

Vistas (views.py)
**********************

Define la lógica para mostrar y procesar información en la interfaz.

new_machine
=============

Esta vista se encarga de mostrar el formulario para crear una nueva máquina.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Se crea un contexto que incluye el formulario para la nueva máquina y los elementos para la barra lateral.
- Se renderiza la plantilla ``new_machine.html`` con el contexto proporcionado.

Retorno
-------

- La vista retorna el renderizado de la plantilla ``new_machine.html`` con el formulario y los elementos necesarios para la creación de una nueva máquina.

---

manage_machines
================

Esta vista permite gestionar las máquinas, mostrando una lista de las maquinarias disponibles según la faena del usuario.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Se obtiene el perfil del usuario logueado.
- Si la faena del usuario es ``SIN ASIGNAR``, se muestran todas las máquinas disponibles.
- Si el usuario tiene asignada una faena, se filtran las máquinas asociadas a esa faena.
- Se renderiza la plantilla ``manage_machines.html`` con la lista de máquinas y los datos de la faena del usuario.

Retorno
-------

- La vista retorna el renderizado de la plantilla ``manage_machines.html`` con las máquinas y la información de la faena del usuario.

save_new_machine
=================

Esta vista maneja la creación de una nueva máquina, validando el formulario y guardando los datos correspondientes.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Si la solicitud es de tipo ``POST``, se obtiene la instancia de tipo, marca y faena de la máquina a partir de los datos del formulario.
- Se valida el formulario de la máquina y se verifican los campos de fecha de adquisición y frecuencia de mantenimiento.
- Si el formulario es válido, se guarda la nueva máquina y se crea una relación con la faena.
- Se envía una notificación por correo electrónico indicando que la máquina fue creada.
- Se muestra un mensaje de éxito y se redirige a la vista ``manage_machines``.
- Si el formulario no es válido, se muestra un mensaje de error y se vuelve a mostrar el formulario.

Retorno
-------

- Si el formulario es válido, se redirige a la vista ``manage_machines`` con un mensaje de éxito.
- Si el formulario no es válido, se vuelve a renderizar el formulario con un mensaje de error.

---

status_machine
===============

Esta vista permite cambiar el estado de la máquina, habilitándola o deshabilitándola.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Si la solicitud es de tipo ``POST``, se obtiene la máquina correspondiente a partir del ID proporcionado.
- Si la máquina está habilitada, se deshabilita y se envía una notificación por correo electrónico.
- Si la máquina está deshabilitada, se habilita nuevamente y se envía una notificación por correo electrónico.
- Se muestra un mensaje de éxito y se redirige a la vista ``manage_machines``.

Retorno
-------

- La vista redirige a la vista ``manage_machines`` con un mensaje de éxito, dependiendo de si la máquina fue habilitada o deshabilitada correctamente.

edit_machine_profile
=====================

Esta vista permite editar el perfil de una máquina existente.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Si la solicitud es de tipo ``POST``, se obtiene la máquina que se desea editar a partir de la sesión.
- Se obtiene la información relacionada con la máquina, incluyendo las solicitudes de mantenimiento, historial de faenas, horómetros, y los valores actuales de tipo, marca, y faena.
- Se prepara un formulario de edición con los datos actuales de la máquina y se pasa a la plantilla.
- Dependiendo del rol del usuario, el campo de faena puede estar deshabilitado.
- Finalmente, la vista renderiza el formulario de edición de la máquina.

Retorno
-------

- La vista retorna un formulario prellenado con los datos actuales de la máquina a editar.

---

save_edit_machine_profile
==========================

Esta vista guarda los cambios realizados en el perfil de una máquina existente.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Si la solicitud es de tipo ``POST``, se validan los campos de fecha de adquisición y frecuencia de mantenimiento.
- Se actualizan los datos de la máquina, incluida su relación con la faena.
- Si la faena cambia, se actualiza la relación ``MaquinariaFaena`` para reflejar este cambio.
- Después de guardar los cambios, se envía una notificación por correo electrónico indicando que la máquina fue actualizada.
- Finalmente, se muestra un mensaje de éxito y se redirige a la vista ``manage_machines``.

Retorno
-------

- Si los datos se actualizan correctamente, se redirige a la vista ``manage_machines`` con un mensaje de éxito.
- Si ocurre un error, se muestra un mensaje de error y se vuelve a renderizar el formulario de edición de la máquina.

cargar_marca_por_tipo
=====================

Esta vista carga las marcas asociadas a un tipo de maquinaria específico.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- La vista recibe un parámetro ``tipo_id`` a través de la solicitud ``GET``.
- Si el ``tipo_id`` está presente, se buscan las marcas asociadas a ese tipo de maquinaria.
- Se retorna una respuesta JSON con las marcas encontradas, mostrando su ``id`` y ``nombre``.
- Si no se encuentra el parámetro ``tipo_id``, se devuelve un error con el código de estado ``400``.

Retorno
-------

- Si se encuentra el parámetro ``tipo_id``, se devuelve una respuesta JSON con la lista de marcas.
- Si el parámetro no está presente, se devuelve una respuesta con código de estado ``400``.

---

new_horometro_register
=======================

Esta vista permite registrar un nuevo horómetro para una maquinaria.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista obtiene el perfil del usuario autenticado y verifica a qué faena pertenece.
- Si el usuario no tiene faena asignada, se obtienen todas las maquinarias con ``status=True``.
- Si el usuario tiene faena asignada, se filtran las maquinarias por la faena correspondiente.
- Se prepara un formulario para el registro de horómetro con las maquinarias disponibles.
- Finalmente, la vista renderiza la plantilla con el formulario de nuevo horómetro.

Retorno
-------

- La vista renderiza una plantilla que incluye un formulario para registrar un nuevo horómetro.

save_new_horometro_register
===========================

Esta vista guarda un nuevo registro de horómetro para una maquinaria.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista recibe una solicitud ``POST`` con los datos del horómetro y la maquinaria.
- Se obtiene la maquinaria correspondiente al ``id`` proporcionado en el ``POST``.
- Se crea un nuevo registro en la base de datos con la maquinaria seleccionada, el valor del horómetro y el usuario que lo creó.
- El registro se guarda correctamente en la base de datos.

Retorno
-------

- Si la solicitud es exitosa, se devuelve una respuesta JSON con la clave ``success`` en ``True``.
- Si no es una solicitud ``POST``, se redirige al formulario de registro de horómetro.

---

machine_pdf_view
================

Esta vista genera un archivo PDF con información de una maquinaria.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista recibe una solicitud ``POST`` con el ``id`` de la maquinaria.
- Se obtiene la maquinaria correspondiente mediante el ``id`` proporcionado.
- Se genera un archivo PDF utilizando una plantilla HTML y los datos de la maquinaria.
- El archivo PDF se guarda en el sistema de archivos y se genera un enlace de acceso.

Retorno
-------

- Si el PDF se genera con éxito, se devuelve una respuesta JSON con la URL del archivo PDF.
- Si ocurre un error al generar el PDF, se devuelve una respuesta JSON con un mensaje de error.
- Si no es una solicitud ``POST``, se redirige a la página de gestión de maquinarias.

manage_machines_kits_repair
===========================

Esta vista maneja la visualización de los kits de reparación de maquinaria en faena.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista obtiene los registros de ``HistorialStockKitsMaquinariaFaena`` con el estado ``True``.
- Los kits de reparación se ordenan por la fecha de creación en orden descendente.
- Se pasan los kits obtenidos al contexto para ser renderizados en la plantilla correspondiente.

Retorno
-------

- Se devuelve un ``render`` con la plantilla ``manage_machines_kits_repair.html``, pasando los kits de faena y datos relacionados con la barra lateral.

---

new_machines_kits_repair
=========================

Esta vista maneja la creación de un nuevo kit de reparación de maquinaria en faena.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista solo muestra el formulario para crear un nuevo kit de reparación de maquinaria.
- El formulario utilizado es ``FormNuevoKitReparacionFaena``.

Retorno
-------

- Se devuelve un ``render`` con la plantilla ``new_machines_kits_repair.html``, pasando el formulario y datos relacionados con la barra lateral.

save_new_machines_kits_repair
==============================

Esta vista maneja la creación y almacenamiento de un nuevo kit de reparación de maquinaria en faena.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista recibe una solicitud ``POST`` con los datos del formulario ``FormNuevoKitReparacionFaena``.
- Si el formulario es válido, se guarda un nuevo kit de reparación de maquinaria.
- Luego, se crea un historial de stock para el kit de maquinaria y se asocia con la faena correspondiente.
- Si ocurre un error de integridad, se devuelve un mensaje de error.

Retorno
-------

- Se devuelve un ``JsonResponse`` con un mensaje de éxito si el proceso es exitoso.
- En caso de error, se devuelve un ``JsonResponse`` con el error detallado.

---

status_machines_kits_repair
===========================

Esta vista maneja el cambio de estado de los kits de reparación de maquinaria.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista recibe una solicitud ``POST`` con el identificador de un kit de reparación de maquinaria.
- Si el kit está habilitado, se deshabilita, y si está deshabilitado, se habilita.
- Se muestra un mensaje de éxito tras actualizar el estado del kit.

Retorno
-------

- Se redirige a la vista ``manage_machines_kits_repair`` después de actualizar el estado del kit.

edit_machines_kits_repair
==========================

Esta vista permite editar los detalles de un kit de reparación de maquinaria en faena.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista recibe una solicitud ``POST`` con el identificador del kit y de la faena a editar.
- Se obtiene el kit más reciente asociado a la faena seleccionada.
- Se generan dos formularios: uno para editar los detalles del kit y otro para agregar detalles adicionales al kit de reparación.
- El historial de modificaciones del kit en faena se pasa al contexto.

Retorno
-------

- Se renderiza la plantilla ``edit_machines_kits_repair.html`` con los formularios y el historial del kit.

---

save_edit_machines_kits_repair
===============================

Esta vista maneja la actualización de los detalles de un kit de reparación de maquinaria en faena.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista recibe una solicitud ``POST`` con los datos del formulario ``FormEditKitsMaquinariaFaena``.
- Si el formulario es válido, los detalles del kit de reparación en faena se actualizan en la base de datos.
- Se guarda un nuevo registro en el historial de cambios para el kit de reparación.

Retorno
-------

- Se redirige a la vista ``manage_machines_kits_repair`` después de guardar los cambios.

Rutas (urls.py)
**********************

Define las rutas de acceso a las vistas del módulo.

manage_machines
================

Ruta para gestionar las máquinas.

URL
---

- ``/manage_machines``

Vista asociada
--------------

- ``manage_machines``

---

new_machine
============

Ruta para crear una nueva máquina.

URL
---

- ``/new_machine``

Vista asociada
--------------

- ``new_machine``

---

save_new_machine
=================

Ruta para guardar una nueva máquina.

URL
---

- ``/save_new_machine``

Vista asociada
--------------

- ``save_new_machine``

---

status_machine
================

Ruta para gestionar el estado de la máquina.

URL
---

- ``/status_machine``

Vista asociada
--------------

- ``status_machine``

---

edit_machine_profile
======================

Ruta para editar el perfil de una máquina.

URL
---

- ``/edit_machine_profile``

Vista asociada
--------------

- ``edit_machine_profile``

---

save_edit_machine_profile
===========================

Ruta para guardar los cambios en el perfil de la máquina.

URL
---

- ``/save_edit_machine_profile``

Vista asociada
--------------

- ``save_edit_machine_profile``

---

cargar_marca_por_tipo
=======================

Ruta para cargar la marca según el tipo de máquina.

URL
---

- ``/cargar_marca_por_tipo``

Vista asociada
--------------

- ``cargar_marca_por_tipo``

---

machine_pdf_view
=================

Ruta para generar la vista PDF de la máquina.

URL
---

- ``/machine_pdf_view``

Vista asociada
--------------

- ``machine_pdf_view``

---

new_horometro_register
========================

Ruta para crear un nuevo registro de horómetro.

URL
---

- ``/new_horometro_register``

Vista asociada
--------------

- ``new_horometro_register``

---

save_new_horometro_register
=============================

Ruta para guardar el nuevo registro de horómetro.

URL
---

- ``/save_new_horometro_register``

Vista asociada
--------------

- ``save_new_horometro_register``

---

manage_machines_kits_repair
============================

Ruta para gestionar los kits de reparación de las máquinas.

URL
---

- ``/manage_machines_kits_repair``

Vista asociada
--------------

- ``manage_machines_kits_repair``

---

new_machines_kits_repair
=========================

Ruta para crear un nuevo kit de reparación para las máquinas.

URL
---

- ``/new_machines_kits_repair``

Vista asociada
--------------

- ``new_machines_kits_repair``

---

save_new_machines_kits_repair
===============================

Ruta para guardar el nuevo kit de reparación de máquinas.

URL
---

- ``/save_new_machines_kits_repair``

Vista asociada
--------------

- ``save_new_machines_kits_repair``

---

edit_machines_kits_repair
===========================

Ruta para editar un kit de reparación de máquinas.

URL
---

- ``/edit_machines_kits_repair``

Vista asociada
--------------

- ``edit_machines_kits_repair``

---

status_machines_kits_repair
============================

Ruta para gestionar el estado de los kits de reparación de máquinas.

URL
---

- ``/status_machines_kits_repair``

Vista asociada
--------------

- ``status_machines_kits_repair``

---

save_edit_machines_kits_repair
===============================

Ruta para guardar los cambios en el kit de reparación de máquinas.

URL
---

- ``/save_edit_machines_kits_repair``

Vista asociada
--------------

- ``save_edit_machines_kits_repair``

