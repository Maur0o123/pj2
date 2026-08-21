Maintenance
===========

Descripción General
*******************

Este módulo permite gestionar solicitudes de mantenimiento de vehículos y maquinaria, incluyendo su historial, estado de progreso y empresa encargada del mantenimiento.

.. code-block:: bash   

    maintenance/
    │── admin.py        # Configuración del panel de administración de Django
    │── apps.py         # Configuración de la aplicación Django
    │── forms.py        # Formularios utilizados dentro del módulo
    │── models.py       # Definición de modelos de datos
    │── urls.py         # Definición de rutas para las vistas del módulo
    │── views.py        # Lógica de controladores para las vistas
    │── migrations/     # Archivos de migración para la base de datos

Modelos de Datos (models.py)
*****************************

Define las entidades utilizadas en el sistema para gestionar las solicitudes de mantenimiento y su historial.

NuevaSolicitudMantenimiento
---------------------------

El modelo NuevaSolicitudMantenimiento gestiona las solicitudes de mantenimiento de vehículos, registrando detalles como la información del solicitante, el vehículo, los problemas a resolver, y el progreso de la solicitud.

- Campos:
    - ``solicitante``: (ForeignKey) Relación con el modelo Usuario, indicando el usuario que realiza la solicitud.
    - ``telefono``: (IntegerField) Teléfono del solicitante.
    - ``vehiculo``: (ForeignKey) Relación con el modelo Vehiculo, indicando el vehículo al que se le solicita el mantenimiento.
    - ``faena``: (ForeignKey) Relación con el modelo Faena, indicando la faena asociada a la solicitud de mantenimiento.
    - ``patente``: (CharField) Patente del vehículo.
    - ``kilometraje``: (IntegerField) Kilometraje del vehículo al momento de la solicitud de mantenimiento.
    - ``progreso``: (CharField) Indica el progreso de la solicitud de mantenimiento (por ejemplo, "Creado", "En proceso").
    - ``empresaMantenimiento``: (ForeignKey) Relación con el modelo EmpresaServicios, indicando la empresa encargada del mantenimiento.
    - ``turno``: (CharField) El turno en el que se realizó la solicitud de mantenimiento.
    - ``problemas``: (ManyToManyField) Relación con el modelo TipoFallaVehiculo, a través del modelo intermedio SolicitudMantenimientoProblemas, indicando los problemas que presenta el vehículo.
    - ``comentario``: (CharField) Comentarios adicionales sobre la solicitud de mantenimiento.
    - ``avisoJefatura``: (CharField) Indica si se ha notificado a la jefatura directa del solicitante sobre la solicitud de mantenimiento.
    - ``status``: (BooleanField) Estado de la solicitud de mantenimiento (activo/inactivo).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se creó la solicitud de mantenimiento.
- Métodos:
    - ``generaNombre``: Función que genera dinámicamente el nombre y ruta de las imágenes de la solicitud de mantenimiento. Utiliza la patente del vehículo y la fecha de creación para crear una estructura de carpeta organizada para las imágenes subidas.
    - ``__str__(self)``: Devuelve una cadena que contiene los problemas asociados a la solicitud de mantenimiento.
- Imágenes:
    - ``fotografiaUno``: (ImageField) Imagen asociada a la solicitud, con un nombre de archivo generado dinámicamente.
    - ``fotografiaDos``: (ImageField) Otra imagen asociada a la solicitud.
    - ``fotografiaTres``: (ImageField) Otra imagen asociada a la solicitud.

HistorialSolicitudMantenimiento
-------------------------------

El modelo HistorialSolicitudMantenimiento permite realizar el seguimiento del historial de solicitudes de mantenimiento, guardando los cambios de progreso y actualizaciones relevantes sobre el estado de cada solicitud de mantenimiento.

- Campos:
    - ``solicitud``: (ForeignKey) Relación con el modelo NuevaSolicitudMantenimiento, indicando la solicitud de mantenimiento a la que pertenece este historial.
    - ``solicitante``: (ForeignKey) Relación con el modelo Usuario, indicando el usuario que está realizando el seguimiento o actualización de la solicitud de mantenimiento.
    - ``progreso``: (CharField) Indica el progreso de la solicitud de mantenimiento (por ejemplo, "En proceso", "Finalizado").
    - ``empresaMantenimiento``: (ForeignKey) Relación con el modelo EmpresaServicios, indicando la empresa que está realizando el mantenimiento.
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se registró la actualización o cambio en el historial de la solicitud de mantenimiento.
- Métodos:
    - ``__str__(self)``: Devuelve una cadena que contiene el progreso de la solicitud de mantenimiento.
- Metadatos:
    - ``verbose_name``: "Historial Registro de Mantenimiento".
    - ``verbose_name_plural``: "Historial Registros de Mantenimientos".
    - ``db_table``: maintenance_register_history.

Signal: create_historial_solicitud_mantenimiento
------------------------------------------------

La señal create_historial_solicitud_mantenimiento se ejecuta automáticamente cuando se guarda una nueva instancia del modelo NuevaSolicitudMantenimiento. Su objetivo es crear un registro en el modelo HistorialSolicitudMantenimiento cada vez que se crea una nueva solicitud de mantenimiento, almacenando el progreso inicial y la información del solicitante.

- Detalles:
    - ``@receiver(post_save, sender=NuevaSolicitudMantenimiento)``: Esto indica que la función create_historial_solicitud_mantenimiento se ejecutará después de guardar una nueva instancia del modelo NuevaSolicitudMantenimiento (post_save). La señal se activa solo cuando se crea una nueva instancia (cuando created es True).
    - ``def create_historial_solicitud_mantenimiento``:
        - ``Parámetros``:
            - ``sender``: Es el modelo que dispara la señal, en este caso, NuevaSolicitudMantenimiento.
            - ``instance``: Es la instancia de NuevaSolicitudMantenimiento que acaba de ser guardada.
            - ``created``: Es un valor booleano que indica si la instancia fue creada (es True cuando la instancia es nueva).
            - ``**kwargs``: Argumentos adicionales que pueden ser pasados en la señal.
            - ``Acción``: Si la instancia es nueva (created es True), se crea un nuevo registro en el modelo HistorialSolicitudMantenimiento. Este registro contiene los siguientes datos:
                - ``solicitud``: Relación con la instancia de NuevaSolicitudMantenimiento recién creada.
                - ``solicitante``: Relación con el usuario que hizo la solicitud, usando instance.solicitante.
                - ``progreso``: El estado inicial del progreso de la solicitud, usando instance.progreso.

SolicitudMantenimientoProblemas
-------------------------------

El modelo SolicitudMantenimientoProblemas representa una relación entre los problemas de un vehículo, la solicitud de mantenimiento y detalles adicionales como el valor del servicio y una descripción.

- Campos:
    - ``fallaVehiculo (ForeignKey a TipoFallaVehiculo)``:Relaciona este modelo con el tipo de falla del vehículo. Hace referencia al modelo TipoFallaVehiculo, que probablemente describe diferentes tipos de fallas que pueden ocurrir en un vehículo.
    - ``verbose_name``: 'Falla Vehiculo'.
    - ``solicitudMantenimiento (ForeignKey a NuevaSolicitudMantenimiento)``:Relaciona el problema con la solicitud de mantenimiento a la que pertenece. Hace referencia al modelo NuevaSolicitudMantenimiento.
    - ``verbose_name``: 'Solicitud Mantenimiento'.
    - ``valorServicio (IntegerField)``: Representa el costo asociado al servicio para resolver el problema del vehículo. Este valor puede ser opcional, ya que es nullable y puede quedar en blanco.
    - ``verbose_name``: 'Valor Servicio'.
    - ``descripcion (CharField)``:Permite almacenar una descripción adicional sobre el problema o el servicio que se está proporcionando.
    - ``max_length``: 100 caracteres.
    - ``verbose_name``: 'Descripción'.

NuevaSolicitudMantenimientoMaquinaria
-------------------------------------

Este modelo permite registrar las solicitudes de mantenimiento de maquinaria, lo que facilita el seguimiento y control de las incidencias y reparaciones de equipos.

- Campos:
    - ``solicitante``: (ForeignKey) Relación con Usuario, indicando quién está realizando la solicitud.
    - ``telefono``: (IntegerField) Número de teléfono del solicitante.
    - ``maquinaria``: (ForeignKey) Relación con Maquinaria, indicando qué maquinaria necesita mantenimiento.
    - ``faena``: (ForeignKey) Relación con Faena, para saber en qué faena se encuentra la maquinaria.
    - ``horometro``: (IntegerField) Valor del horómetro, indica el tiempo de uso de la maquinaria.
    - ``progreso``: (CharField) Estado del progreso de la solicitud, con opciones definidas por progreso.
    - ``empresaMantenimiento``: (ForeignKey) Relación con EmpresaServicios, especificando la empresa encargada del mantenimiento.
    - ``turno``: (CharField) Turno en que se realiza el mantenimiento, definido por las opciones de turno.
    - ``problemas``: (ManyToManyField) Relación con FallaMaquinaria, para detallar los problemas que afectan a la maquinaria.
    - ``comentario``: (CharField) Comentarios adicionales sobre la solicitud.
    - ``avisoJefatura``: (CharField) Indica si se ha notificado a la jefatura directa sobre la solicitud.
    - ``status``: (BooleanField) Estado de la solicitud (True para activa, False para cerrada o resuelta).
    - ``fechacreacion``: (DateTimeField) Fecha y hora de creación del registro de la solicitud.
- Archivos de imágenes:
    - ``fotografiaUno``: (ImageField) Imagen relacionada con la solicitud.
    - ``fotografiaDos``: (ImageField) Segunda imagen asociada, opcional.
    - ``Método generaNombre``: Genera un nombre de archivo único basado en la fecha de la solicitud y el nombre de la maquinaria.
- Métodos:
    - ``__str__(self)``: Devuelve una cadena con los problemas asociados a la solicitud de mantenimiento.
- Metadatos:
    - ``verbose_name``: "Registro de Mantenimiento Maquinaria".
    - ``verbose_name_plural``: "Registros de Mantenimientos Maquinarias".
    - ``db_table``: maintenance_register_machines.

HistorialSolicitudMantenimientoMaquinaria
-----------------------------------------

Este modelo sirve para llevar un registro del historial de las solicitudes de mantenimiento de maquinaria, permitiendo realizar un seguimiento de su progreso a lo largo del tiempo.

- Campos:
    - ``solicitud``: (ForeignKey) Relación con NuevaSolicitudMantenimientoMaquinaria, asociando este historial a una solicitud específica.
    - ``solicitante``: (ForeignKey) Relación con Usuario, indicando quién está gestionando o realizando un seguimiento de la solicitud.
    - ``progreso``: (CharField) Estado del progreso de la solicitud, con opciones definidas por progreso.
    - ``empresaMantenimiento``: (ForeignKey) Relación con EmpresaServicios, indicando qué empresa está gestionando el mantenimiento de la maquinaria.
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se registró el historial de la solicitud.
- Métodos:
    - ``__str__(self)``: Devuelve el progreso de la solicitud como una cadena.
- Metadatos:
    - ``verbose_name``: "Historial Registro de Mantenimiento Maquinaria".
    - ``verbose_name_plural``: "Historial Registros de Mantenimientos Maquinarias".
    - ``db_table``: maintenance_register_history_machines.

Signal: create_historial_solicitud_mantenimiento_maquinaria
-----------------------------------------------------------

Esta es una señal que se activa automáticamente después de que se guarda una nueva instancia del modelo NuevaSolicitudMantenimientoMaquinaria. La señal crea un historial relacionado en el modelo HistorialSolicitudMantenimientoMaquinaria para registrar el progreso de la solicitud.

- Funcionamiento:
    - ``@receiver(post_save, sender=NuevaSolicitudMantenimientoMaquinaria)``: Se define una señal que se ejecuta después de que se guarda una nueva instancia del modelo NuevaSolicitudMantenimientoMaquinaria (evento post_save).

    - ``def create_historial_solicitud_mantenimiento_maquinaria(sender, instance, created, **kwargs)``: Define la función que manejará la señal. Recibe varios parámetros:
        - ``sender``: El modelo que envía la señal (en este caso, NuevaSolicitudMantenimientoMaquinaria).
        - ``instance``: La instancia del modelo que se ha guardado (en este caso, la nueva solicitud de mantenimiento de maquinaria).
        - ``created``: Un valor booleano que indica si la instancia fue creada por primera vez o si se actualizó.
        - ``kwargs``: Cualquier argumento adicional (no utilizado en este caso).
        - ``if created``: Verifica si la instancia es nueva (es decir, si se acaba de crear una nueva solicitud). Si es así, se crea una nueva entrada en el historial de solicitudes de mantenimiento.
    - ``HistorialSolicitudMantenimientoMaquinaria.objects.create(...)``: Si la solicitud es nueva, crea un nuevo registro en el modelo HistorialSolicitudMantenimientoMaquinaria, con la siguiente información:
        - ``solicitud``: La instancia recién creada de NuevaSolicitudMantenimientoMaquinaria.
        - ``solicitante``: El solicitante asociado a la nueva solicitud de mantenimiento.
        - ``progreso``: El progreso de la solicitud, tal como está definido en el modelo NuevaSolicitudMantenimientoMaquinaria.

SolicitudMantenimientoProblemasMaquinaria
-----------------------------------------

Este modelo relaciona las fallas de la maquinaria con las solicitudes de mantenimiento, permitiendo registrar los problemas específicos que requiere la maquinaria durante el mantenimiento.

- Campos:
    - ``fallaMaquinaria``: (ForeignKey) Relación con FallaMaquinaria, especificando el tipo de falla o problema detectado en la maquinaria.
    - ``solicitudMantenimiento``: (ForeignKey) Relación con NuevaSolicitudMantenimientoMaquinaria, asociando el problema de la maquinaria con una solicitud de mantenimiento en particular.
    - ``valorServicio``: (IntegerField) El valor del servicio asociado a la falla, con un valor entero opcional.
    - ``descripcion``: (CharField) Descripción detallada del problema de la maquinaria, permitiendo que el usuario ingrese más información.
- Metadatos:
    - ``verbose_name``: "Falla Maquinaria en Solicitud de Mantenimiento".
    - ``verbose_name_plural``: "Fallos Maquinaria en Solicitudes de Mantenimiento".
    - ``db_table``: maintenance_problem_request_machines.

Mantenimiento
-------------

Este modelo representa el estado de progreso de las solicitudes de mantenimiento de maquinaria, con distintas etapas definidas para cada solicitud.

- Campos:
    - ``progreso``: (CharField) Almacena el estado de progreso del mantenimiento mediante un conjunto de opciones predefinidas:
        - ``'1'``: "Solicitud"
        - ``'2'``: "En Mantención"
        - ``'3'``: "Segunda Revisión"
        - ``'4'``: "Terminada"
        - ``'5'``: "Anulada"
- Métodos:
    - ``get_nombre_progreso``: (classmethod) Un método de clase que devuelve el nombre correspondiente al progreso del mantenimiento dado un número, usando las opciones definidas en progreso_choices. Si el número no se encuentra en las opciones, devuelve 'Desconocido'.
- Metadatos:
    - ``verbose_name``: "Mantenimiento".
    - ``verbose_name_plural``: "Mantenimientos".
    - ``db_table``: maintenance_register.

Formularios (forms.py)
*****************************

Contiene los formularios utilizados en las vistas.

FormNuevaSolicitudMantenimiento
-------------------------------

Este formulario permite la creación de una nueva solicitud de mantenimiento para un vehículo, permitiendo al usuario registrar detalles sobre el solicitante, el vehículo, el kilometraje, los problemas identificados y cualquier comentario adicional.

Campos del Formulario
^^^^^^^^^^^^^^^^^^^^^

1. ``solicitante``

    - Tipo: CharField
    - Etiqueta: Nombre Solicitante
    - Descripción: Nombre de la persona que está solicitando el mantenimiento.
    - Requerido: Sí (deshabilitado para edición)
    - Widget: TextInput, tipo ``text``

2. ``telefono``

    - Tipo: CharField
    - Etiqueta: Teléfono
    - Descripción: Teléfono del solicitante.
    - Requerido: No
    - Widget: TextInput, tipo ``text``

3. ``turno``

    - Tipo: CharField
    - Etiqueta: Turno (solo si corresponde)
    - Descripción: Turno de trabajo del solicitante (opcional).
    - Requerido: No
    - Widget: Select, estilo centrado.

4. ``vehiculo``

    - Tipo: ForeignKey a ``Vehiculo``
    - Etiqueta: Vehículo
    - Descripción: El vehículo para el que se solicita el mantenimiento.
    - Requerido: Sí
    - Widget: Select, estilo centrado.

5. ``kilometraje``

    - Tipo: IntegerField
    - Etiqueta: Kilometraje
    - Descripción: Kilometraje actual del vehículo al momento de la solicitud.
    - Requerido: Sí
    - Widget: TextInput, tipo ``number``

6. ``problemas``

    - Tipo: CharField
    - Etiqueta: Problemas
    - Descripción: Descripción de los problemas identificados en el vehículo.
    - Requerido: Sí
    - Widget: Select2MultipleWidget, con estilo ``width: 50%``

7. ``comentario``

    - Tipo: CharField
    - Etiqueta: Comentario
    - Descripción: Comentarios adicionales sobre la solicitud.
    - Requerido: No
    - Widget: Textarea, filas 2

Consideraciones Adicionales
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- El campo ``vehiculo`` muestra un listado de vehículos filtrados según los proporcionados al formulario. Si no se pasan vehículos, el campo será vacío.
- El campo ``problemas`` utiliza un widget especial para permitir la selección múltiple de problemas relacionados con el vehículo.
- El campo ``solicitante`` está deshabilitado, ya que se espera que sea completado automáticamente con el nombre del usuario que está creando la solicitud.

FormEditSolicitudMantenimiento
------------------------------

Este formulario permite la edición de una solicitud de mantenimiento para un vehículo ya registrado. Permite modificar detalles sobre el solicitante, el vehículo, el kilometraje, los problemas y comentarios adicionales.

Campos del Formulario
^^^^^^^^^^^^^^^^^^^^^

1. ``solicitante``  
    - Tipo: CharField  
    - Etiqueta: Nombre Solicitante  
    - Descripción: Nombre de la persona que está solicitando el mantenimiento.  
    - Requerido: Sí (deshabilitado para edición)  
    - Widget: TextInput, tipo ``text``  

2. ``telefono``  
    - Tipo: CharField  
    - Etiqueta: Teléfono  
    - Descripción: Teléfono del solicitante.  
    - Requerido: No  
    - Widget: TextInput, tipo ``text``  

3. ``turno``  
    - Tipo: CharField  
    - Etiqueta: Turno (solo si corresponde)  
    - Descripción: Turno de trabajo del solicitante (opcional).  
    - Requerido: No  
    - Widget: Select, estilo centrado.  

4. ``vehiculo``  
    - Tipo: ForeignKey a ``Vehiculo``  
    - Etiqueta: Vehículo  
    - Descripción: El vehículo para el que se solicita el mantenimiento.  
    - Requerido: Sí  
    - Widget: Select, estilo centrado.  

5. ``kilometraje``  
    - Tipo: IntegerField  
    - Etiqueta: Kilometraje  
    - Descripción: Kilometraje actual del vehículo al momento de la solicitud.  
    - Requerido: Sí  
    - Widget: TextInput, tipo ``text``  

6. ``problemas``  
    - Tipo: CharField  
    - Etiqueta: Problemas  
    - Descripción: Descripción de los problemas identificados en el vehículo.  
    - Requerido: No  
    - Widget: Select2MultipleWidget, con estilo ``width: 50%``  

7. ``comentario``  
    - Tipo: CharField  
    - Etiqueta: Comentario  
    - Descripción: Comentarios adicionales sobre la solicitud.  
    - Requerido: No  
    - Widget: Textarea, filas 2  

Consideraciones Adicionales
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- El campo ``vehiculo`` muestra un listado de vehículos filtrados según los proporcionados al formulario. Si no se pasan vehículos, el campo será vacío.

- El campo ``problemas`` utiliza un widget especial para permitir la selección múltiple de problemas relacionados con el vehículo.

- El campo ``solicitante`` está deshabilitado, ya que se espera que sea completado automáticamente con el nombre del usuario que está editando la solicitud.

FormProcesarSolicitudMantenimiento
----------------------------------

Este formulario permite procesar una solicitud de mantenimiento, actualizando el estado de la solicitud y asignando la empresa encargada del mantenimiento.

Campos del Formulario
^^^^^^^^^^^^^^^^^^^^^

1. ``progreso``  
    - Tipo: CharField  
    - Etiqueta: Estado Solicitud  
    - Descripción: Indica el estado actual de la solicitud de mantenimiento.  
    - Requerido: Sí  
    - Widget: Select, con opciones predefinidas para los estados de la solicitud.  

2. ``empresaMantenimiento``  
    - Tipo: ForeignKey a ``EmpresaMantenimiento``  
    - Etiqueta: Empresa de Mantenimiento  
    - Descripción: Empresa encargada de realizar el mantenimiento del vehículo.  
    - Requerido: Sí  
    - Widget: Select  

Consideraciones Adicionales
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- El campo ``progreso`` permite seleccionar el estado de la solicitud. Es un campo obligatorio.

- El campo ``empresaMantenimiento`` es obligatorio y permite asignar una empresa de mantenimiento al proceso de la solicitud.

FormEditSolicitudMantenimientoMaquinaria
----------------------------------------

Este formulario permite la edición de una solicitud de mantenimiento de maquinaria previamente creada.

Campos del Formulario
^^^^^^^^^^^^^^^^^^^^^

1. ``solicitante``  
    - Etiqueta: Nombre Solicitante  
    - Descripción: Nombre de la persona que solicita el mantenimiento.  
    - Requerido: Sí  
    - Widget: TextInput  
    - Deshabilitado: Sí  

2. ``telefono``  
    - Etiqueta: Teléfono  
    - Descripción: Teléfono de contacto del solicitante.  
    - Requerido: No  
    - Widget: TextInput  

3. ``turno``  
    - Etiqueta: Turno (solo si corresponde)  
    - Descripción: Turno de trabajo del solicitante, si aplica.  
    - Requerido: No  
    - Widget: Select  

4. ``maquinaria``  
    - Etiqueta: Maquinaria  
    - Descripción: Maquinaria que requiere el mantenimiento.  
    - Requerido: Sí  
    - Widget: Select  

5. ``horometro``  
    - Etiqueta: Horómetro  
    - Descripción: Indica el valor actual del horómetro de la maquinaria.  
    - Requerido: Sí  
    - Widget: TextInput  

6. ``problemas``  
    - Etiqueta: Problemas  
    - Descripción: Lista de problemas detectados en la maquinaria.  
    - Requerido: No  
    - Widget: Select2MultipleWidget  

7. ``comentario``  
    - Etiqueta: Comentario  
    - Descripción: Comentarios adicionales del solicitante.  
    - Requerido: No  
    - Widget: Textarea  

Consideraciones Adicionales
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``solicitante`` es un campo obligatorio y está deshabilitado para su edición.
- ``turno`` es opcional.
- ``problemas`` es opcional y permite múltiples selecciones.
- ``maquinaria`` se filtra para mostrar solo las disponibles según el contexto.

FormProcesarSolicitudMantenimientoMaquinaria
--------------------------------------------

Este formulario permite actualizar el estado de una solicitud de mantenimiento de maquinaria.

Campos del Formulario
^^^^^^^^^^^^^^^^^^^^^

1. ``progreso``  
    - Etiqueta: Estado Solicitud  
    - Descripción: Indica el estado actual de la solicitud de mantenimiento.  
    - Requerido: Sí  

2. ``empresaMantenimiento``  
    - Etiqueta: Empresa de Mantenimiento  
    - Descripción: Empresa encargada de realizar el mantenimiento.  
    - Requerido: No  

Consideraciones Adicionales
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``progreso`` es obligatorio para registrar el estado de la solicitud.
- ``empresaMantenimiento`` no es obligatorio, permitiendo flexibilidad en el registro de la información.


Vistas (views.py)
*****************

Define la lógica para mostrar y procesar información en la interfaz.

new_maintenance_request
-----------------------

Esta vista permite crear una nueva solicitud de mantenimiento para un vehículo.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
^^^^^^^^^^^^^^

- Se obtiene el perfil del usuario a partir del modelo ``UsuarioProfile``.
- Si el usuario no tiene una faena asignada, se muestran todos los vehículos activos.
- Si el usuario tiene una faena asignada, solo se muestran los vehículos asignados a esa faena.
- Se renderiza el formulario ``FormNuevaSolicitudMantenimiento`` con la lista de vehículos y el nombre del solicitante.

Retorno
^^^^^^^

- Se renderiza la plantilla ``new_maintenance_request.html`` con el formulario para crear la solicitud de mantenimiento.

---

save_new_maintenance_request
----------------------------

Esta vista maneja la creación de una nueva solicitud de mantenimiento para un vehículo.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
^^^^^^^^^^^^^^

- La vista recibe una solicitud ``POST`` con los datos del formulario ``FormNuevaSolicitudMantenimiento``.
- Se procesan las fotografías enviadas en la solicitud, usando la función ``procesar_fotografia_dos``.
- Se obtiene el vehículo y la faena asociada.
- Se crea un registro en el modelo ``NuevaSolicitudMantenimiento`` con los datos del formulario.
- Se crean los registros relacionados con los problemas reportados para el vehículo.
- Se crea un nuevo registro de kilometraje en el modelo ``NuevoKilometraje``.
- Se envía una notificación por email y SMS informando sobre la nueva solicitud.

Retorno
^^^^^^^

- Si la solicitud es procesada con éxito, se redirige a la vista ``new_maintenance_request`` y se muestra un mensaje de éxito.
- Si no, se redirige de nuevo a la vista ``new_maintenance_request``.

manage_maintenance_request
--------------------------

Esta vista permite gestionar las solicitudes de mantenimiento para los vehículos.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.
   
- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles de administrador, jefe de mantención o supervisor.

Funcionamiento
^^^^^^^^^^^^^^

- Se obtiene el perfil del usuario a partir del modelo ``UsuarioProfile``.
- Si el usuario no tiene una faena asignada, se muestran todas las solicitudes de mantenimiento.
- Si el usuario tiene una faena asignada, se filtran las solicitudes por faena.
- Se renderiza la plantilla ``manage_maintenance_request.html`` con las solicitudes de mantenimiento y el progreso.

Retorno
^^^^^^^

- Se renderiza la plantilla ``manage_maintenance_request.html`` con la lista de solicitudes y las opciones de progreso.

---

edit_maintenance_request
------------------------

Esta vista permite editar una solicitud de mantenimiento existente.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.
   
- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles de administrador, jefe de mantención o supervisor.

Funcionamiento
^^^^^^^^^^^^^^

- Se intenta obtener el ``origen_id`` y el ``solicitud_id`` de la solicitud desde la solicitud ``POST``.
- Si no se encuentran, se usan los valores almacenados en la sesión.
- Se obtiene la solicitud de mantenimiento a partir del ``solicitud_id``.
- Se obtienen los registros históricos de la solicitud y los problemas asociados.
- Si el usuario no tiene una faena asignada, se muestran todos los vehículos activos.
- Si el usuario tiene una faena asignada, solo se muestran los vehículos asignados a esa faena.
- Se renderiza el formulario de edición ``FormEditSolicitudMantenimiento`` con los datos de la solicitud y los vehículos.
- Se renderiza el formulario para procesar la solicitud ``FormProcesarSolicitudMantenimiento`` con el progreso y la empresa de mantenimiento.
- Se envía la información de las fotografías asociadas a la solicitud.

Retorno
^^^^^^^

- Se renderiza la plantilla ``edit_maintenance_request.html`` con los formularios de edición y los datos relacionados con la solicitud de mantenimiento.

save_edit_maintenance_request
-----------------------------

Esta vista permite guardar los cambios en una solicitud de mantenimiento existente.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.
   
- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles de administrador, jefe de mantención o supervisor.

Funcionamiento
^^^^^^^^^^^^^^

- Si se recibe una solicitud ``POST``, se procesan los datos y se actualizan los campos de la solicitud de mantenimiento.
- Si se proporciona una empresa de mantenimiento, se asocia a la solicitud.
- Los problemas asociados a la solicitud se actualizan según los datos enviados.
- Las fotografías de la solicitud se procesan, y si es necesario, se actualizan con las nuevas imágenes.
- Si el progreso de la solicitud cambia o la empresa de mantenimiento cambia, se crea un nuevo historial para reflejar la actualización.
- Se actualizan los valores de los servicios asociados a los problemas de la solicitud, y se manejan errores si el valor excede el máximo permitido.
- Se envían notificaciones sobre la actualización de la solicitud.

Retorno
^^^^^^^

- Se redirige al usuario a la vista de ``manage_maintenance_request`` si la solicitud se procesa correctamente.
- Si hay un error en el proceso, se muestra un mensaje de error y se redirige a la vista de ``edit_maintenance_request``.

---

status_maintenance_request
--------------------------

Esta vista permite cambiar el estado de una solicitud de mantenimiento.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.
   
- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles de administrador, jefe de mantención o supervisor.

Funcionamiento
^^^^^^^^^^^^^^

- Si se recibe una solicitud ``POST``, se obtiene la solicitud de mantenimiento correspondiente.
- Si la solicitud está activa, se cambia su estado a "Terminada".
- Si la solicitud está terminada, se cambia su estado a "Activa".
- El cambio de estado se guarda y se muestra un mensaje de éxito al usuario.

Retorno
^^^^^^^

- Se redirige a la vista de ``manage_maintenance_request`` después de realizar el cambio de estado.

new_maintenance_machine_request
-------------------------------

Esta vista permite crear una nueva solicitud de mantenimiento para maquinaria.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
^^^^^^^^^^^^^^

- Se obtiene el perfil del usuario logueado y se verifica si está asignado a una faena.
- Si no está asignado, se muestran todas las maquinarias disponibles; de lo contrario, se muestran solo las maquinarias asociadas a la faena del usuario.
- Se obtienen todas las fallas asociadas a las maquinarias y se muestran en la interfaz.
- Se renderiza un formulario donde el usuario puede llenar los detalles de la solicitud, como el solicitante, teléfono, maquinaria y los problemas a reportar.

Retorno
^^^^^^^

- La vista retorna el formulario de nueva solicitud de mantenimiento para maquinaria, junto con las maquinarias y fallas disponibles.

---

save_new_maintenance_machine_request
------------------------------------

Esta vista guarda una nueva solicitud de mantenimiento para maquinaria.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
^^^^^^^^^^^^^^

- Si se recibe una solicitud ``POST``, se procesan los datos de la solicitud.
- Se obtiene la maquinaria seleccionada y el solicitante.
- Los problemas seleccionados (fallas) se asocian a la solicitud.
- Se procesan las fotografías de la solicitud si están presentes (fotografía Uno y Dos).
- Se obtiene la faena de la maquinaria seleccionada.
- Se guarda una nueva solicitud de mantenimiento para la maquinaria, incluyendo detalles como horómetro, turno, comentarios, etc.
- Si el problema contiene la falla "Mantención mayor", se asigna el origen como "Mantención mayor", de lo contrario se usa "Mantención".
- Se registra el nuevo horómetro para la maquinaria.
- Se envía una notificación por correo electrónico y SMS sobre la nueva solicitud de mantenimiento.

Retorno
^^^^^^^

- Si la solicitud se guarda correctamente, se muestra un mensaje de éxito y se redirige a la vista de creación de nuevas solicitudes.
- Si ocurre un error, se redirige nuevamente a la misma vista para intentar nuevamente.

manage_maintenance_machine_request
----------------------------------

Esta vista permite gestionar las solicitudes de mantenimiento para maquinaria.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso solo a usuarios con permisos de administrador, jefe de mantención o supervisor.

Funcionamiento
^^^^^^^^^^^^^^

- Se obtiene el perfil del usuario logueado y se verifica si está asignado a una faena.
- Si el usuario está asignado a una faena, se filtran las solicitudes de mantenimiento de maquinaria asociadas a esa faena. De lo contrario, se muestran todas las solicitudes.
- Las solicitudes se ordenan por la fecha de creación en orden descendente.
- Se renderiza una vista con las solicitudes de mantenimiento y las opciones de progreso disponibles.

Retorno
^^^^^^^

- La vista retorna un listado de las solicitudes de mantenimiento para maquinaria con la opción de gestionar su progreso.

---

edit_maintenance_machine_request
--------------------------------

Esta vista permite editar una solicitud de mantenimiento para maquinaria.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso solo a usuarios con permisos de administrador, jefe de mantención o supervisor.

Funcionamiento
^^^^^^^^^^^^^^

- Se recuperan los datos de la solicitud de mantenimiento seleccionada a través de la sesión o el ``POST``.
- Se obtiene el historial de la solicitud de mantenimiento.
- Se recuperan los problemas asociados a la solicitud de mantenimiento.
- Se obtiene la maquinaria seleccionada en la solicitud.
- Se procesan las fotografías de la solicitud de mantenimiento (si están presentes) y se extraen sus extensiones.
- Se obtiene la faena del usuario logueado y, en función de eso, se filtran las maquinarias disponibles.
- Se renderiza un formulario de edición de la solicitud de mantenimiento junto con su historial y las opciones de progreso.

Retorno
^^^^^^^

- La vista retorna un formulario para editar la solicitud de mantenimiento, mostrando la información actual, problemas asociados, fotografías y el historial de la solicitud.

save_edit_maintenance_machine_request
-------------------------------------

Esta vista permite guardar la edición de una solicitud de mantenimiento para maquinaria.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_or_jefe_mantencion_or_supervisor_required``:  
   Restringe el acceso solo a usuarios con permisos de administrador, jefe de mantención o supervisor.

Funcionamiento
^^^^^^^^^^^^^^

- Se actualiza la solicitud de mantenimiento de maquinaria con los datos enviados por el formulario.
- Si se ha seleccionado una empresa de mantenimiento, se actualiza el campo ``empresaMantenimiento``.
- Se actualiza la información de la solicitud, como teléfono, turno, maquinaria, horómetro, progreso, y comentario.
- Se procesan las fotografías asociadas a la solicitud y se guardan los cambios.
- Si el progreso de la solicitud o la empresa de mantenimiento ha cambiado, se guarda un historial de la solicitud.
- Se actualizan los valores de servicio y las descripciones asociadas a los problemas de mantenimiento.
- Se envía una notificación sobre la actualización de la solicitud.
- Se redirige a la vista de gestión de solicitudes de mantenimiento para maquinaria.

Retorno
^^^^^^^

- Si todo se procesa correctamente, se redirige a la vista de gestión de solicitudes de mantenimiento para maquinaria.
- Si ocurre un error, se muestra un mensaje de error y se redirige a la página de edición de la solicitud.

---

maintenance_pdf_view
--------------------

Esta vista genera un PDF de una solicitud de mantenimiento para vehículos.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
^^^^^^^^^^^^^^

- Se recupera la solicitud de mantenimiento correspondiente a través de su ``solicitud_id``.
- Se obtiene el historial de la solicitud, los problemas asociados y las fotografías de la solicitud.
- Se crea un archivo PDF con la información de la solicitud y el historial de la solicitud.
- El PDF se guarda temporalmente en el servidor y se genera una URL para su descarga.

Retorno
^^^^^^^

- La vista retorna un ``JsonResponse`` con la URL del PDF generado y un mensaje de éxito.
- Si ocurre un error durante la generación del PDF, se retorna un mensaje de error.

---

maintenance_machine_pdf_view
----------------------------

Esta vista genera un PDF de una solicitud de mantenimiento para maquinaria.

Decoradores
^^^^^^^^^^^

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
^^^^^^^^^^^^^^

- Se recupera la solicitud de mantenimiento correspondiente a través de su ``solicitud_id``.
- Se obtiene el historial de la solicitud, los problemas asociados y las fotografías de la solicitud.
- Se crea un archivo PDF con la información de la solicitud y el historial de la solicitud.
- El PDF se guarda temporalmente en el servidor y se genera una URL para su descarga.

Retorno
^^^^^^^

- La vista retorna un ``JsonResponse`` con la URL del PDF generado y un mensaje de éxito.
- Si ocurre un error durante la generación del PDF, se retorna un mensaje de error.



Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.

new_maintenance_request
-----------------------

Ruta para crear una nueva solicitud de mantención.

URL
^^^

- ``/new_maintenance_request``

Vista asociada
^^^^^^^^^^^^^^

- ``new_maintenance_request``

---

save_new_maintenance_request
----------------------------

Ruta para guardar una nueva solicitud de mantención.

URL
^^^

- ``/save_new_maintenance_request``

Vista asociada
^^^^^^^^^^^^^^

- ``save_new_maintenance_request``

---

manage_maintenance_request
--------------------------

Ruta para gestionar las solicitudes de mantención.

URL
^^^

- ``/manage_maintenance_request``

Vista asociada
^^^^^^^^^^^^^^

- ``manage_maintenance_request``

---

edit_maintenance_request
------------------------

Ruta para editar una solicitud de mantención.

URL
^^^

- ``/edit_maintenance_request``

Vista asociada
^^^^^^^^^^^^^^

- ``edit_maintenance_request``

---

save_edit_maintenance_request
-----------------------------

Ruta para guardar los cambios en la solicitud de mantención.

URL
^^^

- ``/save_edit_maintenance_request``

Vista asociada
^^^^^^^^^^^^^^

- ``save_edit_maintenance_request``

---

status_maintenance_request
--------------------------

Ruta para gestionar el estado de la solicitud de mantención.

URL
^^^

- ``/status_maintenance_request``

Vista asociada
^^^^^^^^^^^^^^

- ``status_maintenance_request``

---

new_maintenance_machine_request
-------------------------------

Ruta para crear una nueva solicitud de mantención de máquina.

URL
^^^

- ``/new_maintenance_machine_request``

Vista asociada
^^^^^^^^^^^^^^

- ``new_maintenance_machine_request``

---

save_new_maintenance_machine_request
------------------------------------

Ruta para guardar una nueva solicitud de mantención de máquina.

URL
^^^

- ``/save_new_maintenance_machine_request``

Vista asociada
^^^^^^^^^^^^^^

- ``save_new_maintenance_machine_request``

---

manage_maintenance_machine_request
----------------------------------

Ruta para gestionar las solicitudes de mantención de máquinas.

URL
^^^

- ``/manage_maintenance_machine_request``

Vista asociada
^^^^^^^^^^^^^^

- ``manage_maintenance_machine_request``

---

edit_maintenance_machine_request
--------------------------------

Ruta para editar una solicitud de mantención de máquina.

URL
^^^

- ``/edit_maintenance_machine_request``

Vista asociada
^^^^^^^^^^^^^^

- ``edit_maintenance_machine_request``

---

save_edit_maintenance_machine_request
-------------------------------------

Ruta para guardar los cambios en la solicitud de mantención de máquina.

URL
^^^

- ``/save_edit_maintenance_machine_request``

Vista asociada
^^^^^^^^^^^^^^

- ``save_edit_maintenance_machine_request``

---

maintenance_pdf_view
--------------------

Ruta para generar la vista PDF de una solicitud de mantención.

URL
^^^

- ``/maintenance_pdf_view``

Vista asociada
^^^^^^^^^^^^^^

- ``maintenance_pdf_view``

---

maintenance_machine_pdf_view
----------------------------

Ruta para generar la vista PDF de una solicitud de mantención de máquina.

URL
^^^

- ``/maintenance_machine_pdf_view``

Vista asociada
^^^^^^^^^^^^^^

- ``maintenance_machine_pdf_view``
