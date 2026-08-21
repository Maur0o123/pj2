#########
Checklist
#########

Descripción General
*******************

Este módulo gestiona la administración y el seguimiento de materiales utilizados en los procesos del sistema. Incluye modelos para checklist de materiales en sondas y casetas, formularios para la captura de datos, filtros personalizados en templates y vistas para la interacción con el usuario.

.. code-block:: bash   

    checklist/
    │── admin.py         # Configuración del panel de administración de Django
    │── apps.py          # Configuración de la aplicación Django
    │── forms.py         # Formularios utilizados dentro del módulo
    │── models.py        # Definición de modelos de datos
    │── urls.py          # Definición de rutas para las vistas del módulo
    │── views.py         # Lógica de controladores para las vistas
    │── templatetags/    # Filtros personalizados para templates
    │   │── custom_filters.py   # Definición de filtros personalizados
    │── migrations/      # Archivos de migración para la base de datos

Modelos de Datos (models.py)
****************************

El archivo models.py define las entidades principales que maneja el módulo.

ChecklistMaterialesSonda
========================

El modelo ChecklistMaterialesSonda representa el checklist de los materiales relacionados con las sondas. Cada entrada en este 
modelo corresponde a un ítem de material asignado a un sondaje específico, con información adicional sobre cantidad, estado, turno, entre otros.

- Campos:
    - ``item``: (ForeignKey) Relacionado con el modelo MaterialesSonda. Este campo indica el material que está siendo controlado en el checklist.
    - ``cantidad``: (IntegerField) La cantidad del material en el checklist. Este campo es opcional y tiene un valor predeterminado de 0.
    - ``creador``: (CharField) El nombre del creador del checklist. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``status``: (BooleanField) El estado del material en el checklist (activo o inactivo).
    - ``jornada``: (CharField) La jornada en la que se registró el checklist. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``etapa``: (CharField) La etapa de trabajo correspondiente. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``turno``: (CharField) El turno de trabajo relacionado con el checklist. Este campo es opcional.
    - ``sonda``: (ForeignKey) Relacionado con el modelo Sondas, este campo hace referencia a la sonda asociada al checklist.
    - ``sondajeCodigo``: (ForeignKey) Relacionado con el modelo Sondajes, este campo hace referencia al código del sondaje.
    - ``sondajeSerie``: (IntegerField) La serie del sondaje, con un rango de valores validado entre 3940 y 4400.
    - ``sondajeEstado``: (CharField) Estado del gemelo en el sondaje, con opciones predefinidas.
    - ``id_checklist``: (BigIntegerField) El ID único para cada checklist.
    - ``fecha_checklist``: (DateTimeField) La fecha en la que se realizó el checklist.
    - ``progreso``: (CharField) El progreso del checklist, con un valor predeterminado de "Creado".
    - ``fechacreacion``: (DateTimeField) La fecha y hora de creación del registro. Este campo es obligatorio y se asigna automáticamente con la fecha y hora actuales.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del checklist, mostrando el material y la cantidad.
    - ``crear_checklist(cls, creador)``: Método de clase que crea un checklist para cada material de sonda disponible, con una cantidad inicial de 0, y asignado al creador especificado.
- Metadatos:
    - ``verbose_name``: "Checklist Material Sonda".
    - ``verbose_name_plural``: "Checklist Materiales Sonda".
    - ``db_table``: checklist_documentos_materiales_sonda.

ChecklistMaterialesCaseta
=========================

El modelo ChecklistMaterialesCaseta representa el checklist de materiales utilizados en la caseta. Cada entrada en este 
modelo corresponde a un ítem de material registrado en el checklist, con detalles adicionales como cantidad, observaciones, turno y fecha de control.

- Campos
    - ``item``: (ForeignKey) Relación con MaterialesCaseta, indicando el material evaluado en el checklist.
    - ``b``: (IntegerField) Representa una cantidad específica del material (posiblemente cantidad de unidades en buen estado).
    - ``m``: (IntegerField) Representa otra cantidad específica del material (posiblemente cantidad de unidades en mal estado).
    - ``observacion``: (CharField) Campo para registrar observaciones adicionales (hasta 500 caracteres).
    - ``fecha_control``: (DateTimeField) Fecha en la que se realizó el control del material.
    - ``creador``: (CharField) Nombre de la persona que creó el checklist.
    - ``creador_cargo``: (CharField) Cargo de la persona que creó el checklist.
    - ``status``: (BooleanField) Estado del checklist (activo o inactivo).
    - ``turno``: (CharField) Indica el turno en que se realizó el checklist, con opciones predefinidas.
    - ``id_checklist``: (IntegerField) ID único del checklist.
    - ``fecha_checklist``: (DateTimeField) Fecha en la que se realizó el checklist.
    - ``fecha_revision``: (DateTimeField) Fecha en la que el checklist fue revisado.
    - ``observaciones_revision``: (CharField) Observaciones registradas durante la revisión.
    - ``supervisor``: (CharField) Nombre del supervisor que revisó el checklist.
    - ``fechacreacion``: (DateTimeField) Fecha y hora de creación del registro (se asigna automáticamente con la fecha actual).
    - ``fotografiaMaterial``: (ImageField) Imagen opcional del material registrado en el checklist. Se guarda en una carpeta dinámica según la fecha y turno.
- Métodos
    - ``generaNombre(instance, filename)``: 
        Este método genera dinámicamente la ruta donde se almacenará la imagen del material:
        - Se usa la fecha del checklist y el turno para definir la carpeta de almacenamiento.
        - Se asigna un nombre único a la imagen basado en la fecha y el ID del material.
    - ``__str__(self)``: Devuelve una representación en cadena del checklist, mostrando el material evaluado.
    - ``crear_checklist(cls, creador)``: Método de clase que genera un checklist automático para todos los materiales de caseta disponibles, asignándolos al creador especificado.

- Metadatos
    - ``verbose_name``: "Checklist Material Caseta".
    - ``verbose_name_plural``: "Checklist Materiales Caseta".
    - ``db_table``: checklist_documentos_materiales_caseta.

Formularios (forms.py)
**********************

Contiene los formularios utilizados en las vistas.

ChecklistMaterialesSondaEntradaForm 
===================================

Se utiliza para registrar la entrada de materiales en una sonda dentro del sistema Django. Este formulario incluye campos para capturar información relevante como la fecha del checklist, el turno, la jornada, la sonda, el sondaje y otros detalles relacionados.

Campos del Formulario
---------------------

1. ``fecha_checklist_entrada``

    - Tipo: DateTimeField

    - Etiqueta: "Fecha Checklist"

    - Inicial: timezone.now

    - Widget: DateTimeInput (Solo lectura, con clase CSS form-control)

    - Descripción: Registra la fecha y hora en la que se realiza el checklist de entrada.

2. ``turno_entrada``

    - Tipo: ChoiceField

    - Etiqueta: "Turno"

    - Opciones: Definidas en la variable turno

    - Widget: Select (con clase CSS form-control)

    - Descripción: Permite seleccionar el turno en el que se registra la entrada.

3. ``jornada_entrada``

    - Tipo: ChoiceField

    - Etiqueta: "Jornada"

    - Opciones: Definidas en la variable jornada

    - Widget: Select (con clase CSS form-control)

    - Descripción: Permite seleccionar la jornada correspondiente a la entrada.

4. ``sonda_entrada``

    - Tipo: ModelChoiceField

    - Etiqueta: "Sonda"

    - QuerySet: Sondas.objects.filter(status=True)

    - Widget: Select (con clase CSS form-control)

    - Descripción: Permite seleccionar una sonda activa del sistema.

5. ``sondaje_entrada``

    - Tipo: ModelChoiceField

    - Etiqueta: "Sondaje"

    - QuerySet: Sondajes.objects.filter(status=True)

    - Widget: Select (con clase CSS form-control)

    - Descripción: Permite seleccionar un sondaje activo.

6. ``serie_entrada``

    - Tipo: CharField

    - Etiqueta: "N° Sondaje"

    - Widget: TextInput (con clase CSS form-control)

    - Descripción: Campo de texto para ingresar el número de sondaje correspondiente.

7. ``estado_entrada``

    - Tipo: ChoiceField

    - Etiqueta: "Gemelo"

    - Opciones: Lista con valores de gemelo, incluyendo una opción vacía inicial.

    - Widget: Select (con clase CSS form-control)

    - Requerido: No

    - Descripción: Permite seleccionar el estado gemelo del sondaje si aplica.


Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS form-control en los widgets para una mejor presentación en Bootstrap.

- Restricciones: Algunos campos como fecha_checklist_entrada son de solo lectura para evitar modificaciones manuales.

- Filtrado: Se utilizan queryset para asegurarse de que solo se muestren sondas y sondajes activos en las opciones del formulario.

ChecklistMaterialesSondaSalidaForm
==================================

Se utiliza para registrar la salida de materiales en una sonda dentro del sistema Django. Este formulario incluye campos para capturar información relevante como la fecha del checklist, el turno, la jornada, la sonda, el sondaje y otros detalles relacionados.

Campos del Formulario
---------------------

1. ``turno_salida``

      - Tipo: ChoiceField

      - Etiqueta: "Turno"

      - Opciones: Definidas en la variable turno

      - Widget: Select (con clase CSS form-control)

      - Descripción: Permite seleccionar el turno en el que se registra la salida.

2. ``jornada_salida``

    - Tipo: ChoiceField

    - Etiqueta: "Jornada"

    - Opciones: Definidas en la variable jornada

    - Widget: Select (con clase CSS form-control)

    - Descripción: Permite seleccionar la jornada correspondiente a la salida.

3. ``sonda_salida``

    - Tipo: ModelChoiceField

    - Etiqueta: "Sonda"

    - QuerySet: Sondas.objects.filter(status=True)

    - Widget: Select (con clase CSS form-control)

    - Descripción: Permite seleccionar una sonda activa del sistema.

4. ``sondaje_salida``

    - Tipo: ModelChoiceField

    - Etiqueta: "Sondaje"

    - QuerySet: Sondajes.objects.filter(status=True)

    - Widget: Select (con clase CSS form-control)

    - Descripción: Permite seleccionar un sondaje activo.

5. ``serie_salida``

    - Tipo: CharField

    - Etiqueta: "N° Sondaje"

    - Widget: TextInput (con clase CSS form-control)

    - Descripción: Campo de texto para ingresar el número de sondaje correspondiente.

6. ``estado_salida``

    - Tipo: ChoiceField

    - Etiqueta: "Gemelo"

    - Opciones: Lista con valores de gemelo, incluyendo una opción vacía inicial.

    - Widget: Select (con clase CSS form-control)

    - Requerido: No

    - Descripción: Permite seleccionar el estado gemelo del sondaje si aplica.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS form-control en los widgets para una mejor presentación en Bootstrap.

- Restricciones: Algunos campos como fecha_checklist_salida son de solo lectura para evitar modificaciones manuales.

- Filtrado: Se utilizan queryset para asegurarse de que solo se muestren sondas y sondajes activos en las opciones del formulario.

ChecklistMaterialesCasetaFormTop
================================

Se utiliza para registrar la inspección de materiales en una caseta dentro del sistema Django. Este formulario incluye campos para capturar información relevante como la fecha del checklist, el turno, el responsable y su cargo.

Campos del Formulario
---------------------

1. ``fecha_checklist``

    - Tipo: DateTimeField

    - Etiqueta: "Fecha Checklist"

    - Inicial: timezone.now

    - Widget: DateTimeInput (Solo lectura, con clase CSS form-control)

    - Descripción: Registra la fecha y hora en la que se realiza el checklist de la caseta.

2. ``turno``

    - Tipo: ChoiceField

    - Etiqueta: "Turno"

    - Opciones: Definidas en la variable turno

    - Widget: Select (con clase CSS form-control)

    - Descripción: Permite seleccionar el turno en el que se registra la inspección.

3. ``responsable``

    - Tipo: CharField

    - Etiqueta: "Responsable"

    - Widget: TextInput (Solo lectura, con clase CSS form-control)

    - Descripción: Registra el nombre del responsable de la inspección.

4. ``cargo``

    - Tipo: CharField

    - Etiqueta: "Cargo"

    - Widget: TextInput (Solo lectura, con clase CSS form-control)

    - Descripción: Registra el cargo del responsable.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS form-control en los widgets para una mejor presentación en Bootstrap.

- Restricciones: Algunos campos como fecha_checklist, responsable y cargo son de solo lectura para evitar modificaciones manuales.

- Validaciones: Se pueden agregar validaciones adicionales en la vista para asegurar que los datos capturados sean correctos y consistentes.

ChecklistMaterialesCasetaFormBottom
===================================

Se utiliza para registrar la revisión de materiales en una caseta dentro del sistema Django. Este formulario incluye campos para capturar información relevante como la fecha de revisión, el supervisor a cargo y observaciones adicionales.

Campos del Formulario
---------------------

1. ``fecha_revision``

    - Tipo: DateTimeField

    - Etiqueta: "Fecha Revisión"

    - Inicial: timezone.now

    - Widget: DateTimeInput (Solo lectura, con clase CSS form-control)

    - Descripción: Registra la fecha y hora en la que se realiza la revisión de la caseta.

2. ``supervisor``

    - Tipo: CharField

    - Etiqueta: "Supervisor"

    - Widget: TextInput (Solo lectura, con clase CSS form-control)

    - Descripción: Registra el nombre del supervisor encargado de la revisión.

3. ``observaciones``

    - Tipo: CharField

    - Etiqueta: "Observaciones"

    - Requerido: No

    - Widget: Textarea (con clase CSS form-control, 40 columnas y 5 filas)

    - Descripción: Permite registrar cualquier observación adicional sobre la revisión de la caseta.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS form-control en los widgets para una mejor presentación en Bootstrap.

- Restricciones: Algunos campos como fecha_revision y supervisor son de solo lectura para evitar modificaciones manuales.

- Flexibilidad: El campo de observaciones es opcional, permitiendo registrar comentarios si es necesario.

Vistas (views.py)
*****************

Define la lógica para mostrar y procesar información en la interfaz.

manage_checklist_materiales_sonda
=================================

Esta vista es responsable de manejar el checklist de materiales de sonda, con restricciones de acceso a usuarios autorizados.

Decoradores
------------

1. ``@login_required``:  
   
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

2. ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   
   Este decorador verifica que el usuario tenga uno de los siguientes permisos:

   - Ser un administrador de sondajes.
   - Tener acceso a la base de datos.
   - Ser un supervisor autorizado.

Función
--------

La vista ``manage_checklist_materiales_sonda`` se encarga de obtener una lista de registros de checklist de materiales de sonda, la cual contiene los siguientes campos:

- ``id_checklist``: Identificador único del checklist.
- ``fecha_checklist``: Fecha en la que se realizó el checklist.
- ``turno``: Turno en el que se registró el checklist.
- ``jornada``: Jornada asociada al checklist.
- ``creador``: Usuario que creó el checklist.

La lista es filtrada y organizada por fecha (de manera descendente) para mostrar los registros más recientes primero. Solo se muestran los registros distintos basados en los campos mencionados.

Contexto
---------

Se pasa un diccionario al contexto que contiene:

- ``documentos``: La lista de registros obtenidos de la base de datos.
- ``sidebar``: Identificador para la barra lateral.
- ``sidebarmain``: Identificador principal para la barra lateral.

Retorno
-------

La vista renderiza la plantilla ``pages/checklist/manage_materiales_sonda.html``, pasando el contexto con los documentos y configuraciones de la barra lateral.

save_checklist_materiales_sonda_entrada
=======================================

Esta vista se encarga de guardar los datos enviados desde el formulario de entrada del checklist de materiales de sonda.

Decoradores
------------

1. ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
--------

La vista ``save_checklist_materiales_sonda_entrada`` realiza los siguientes pasos:

1. **Verificación del método HTTP**:  
   Solo acepta solicitudes ``POST``. Si no es una solicitud ``POST``, responde con un mensaje indicando que el formulario no es válido.

2. **Procesamiento del formulario**:  
   Si la solicitud es ``POST``, el formulario ``ChecklistMaterialesSondaEntradaForm`` se crea con los datos de la solicitud. Si el formulario es válido, realiza las siguientes operaciones:
   
   - Obtiene los datos del formulario y los limpia utilizando el método ``cleaned_data``.
   - Recupera objetos asociados de las tablas ``Sondas`` y ``Sondajes`` con los valores proporcionados.
   - Calcula el nuevo ID correlativo para el checklist, obteniendo el valor máximo de ``id_checklist`` y sumando 1.
   - Itera sobre los materiales de sonda activos y guarda o actualiza un registro de ``ChecklistMaterialesSonda`` para cada uno, asociando la cantidad y demás datos del formulario.

3. **Manejo de excepciones**:  
   Si ocurre un error durante el procesamiento del formulario o la inserción de los datos en la base de datos, se captura la excepción y se retorna un mensaje de error.

4. **Respuesta JSON**:
     
   - Si todo el proceso es exitoso, se retorna un JSON con ``{'success': True}``.
   - Si el formulario no es válido o hay un error durante el proceso, se retorna un JSON con ``{'success': False, 'message': 'El formulario no es válido.'}`` o un mensaje de error.

Retorno
-------

La vista devuelve una respuesta en formato JSON:

- ``{'success': True}``: Si el formulario se guardó correctamente.
- ``{'success': False, 'message': 'Error al guardar el formulario.'}``: Si hubo un error al guardar los datos.
- ``{'success': False, 'message': 'El formulario no es válido.'}``: Si el formulario no pasó la validación.

save_checklist_materiales_sonda_salida
======================================

Esta vista se encarga de guardar los datos enviados desde el formulario de salida del checklist de materiales de sonda.

Decoradores
------------

1. ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
--------

La vista ``save_checklist_materiales_sonda_salida`` realiza los siguientes pasos:

1. **Verificación del método HTTP**:  
   Solo acepta solicitudes ``POST``. Si no es una solicitud ``POST``, responde con un mensaje indicando que el formulario no es válido.

2. **Procesamiento del formulario**:  
   Si la solicitud es ``POST``, el formulario ``ChecklistMaterialesSondaSalidaForm`` se crea con los datos de la solicitud. Si el formulario es válido, realiza las siguientes operaciones:
   
   - Obtiene los datos del formulario y los limpia utilizando el método ``cleaned_data``.
   - Recupera objetos asociados de las tablas ``Sondas`` y ``Sondajes`` con los valores proporcionados.
   - Usa el ID del checklist recibido en el ``POST`` como el nuevo ID para actualizar los registros.
   - Itera sobre los materiales de sonda activos y guarda o actualiza un registro de ``ChecklistMaterialesSonda`` para cada uno, asociando la cantidad y demás datos del formulario.

3. **Manejo de excepciones**:  
   Si ocurre un error durante el procesamiento del formulario o la inserción de los datos en la base de datos, se captura la excepción y se retorna un mensaje de error.

4. **Respuesta JSON**:  
   
   - Si todo el proceso es exitoso, se retorna un JSON con ``{'success': True}``.
   - Si el formulario no es válido o hay un error durante el proceso, se retorna un JSON con ``{'success': False, 'message': 'El formulario no es válido.'}`` o un mensaje de error.

Retorno
-------

La vista devuelve una respuesta en formato JSON:

- ``{'success': True}``: Si el formulario se guardó correctamente.
- ``{'success': False, 'message': 'Error al guardar el formulario.'}``: Si hubo un error al guardar los datos.
- ``{'success': False, 'message': 'El formulario no es válido.'}``: Si el formulario no pasó la validación.

edit_checklist_materiales_sonda
===============================

Esta vista permite editar un checklist de materiales de sonda, cargando los datos existentes para su modificación.

Decoradores
------------

1. ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

2. ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador restringe el acceso a usuarios que tengan uno de los siguientes roles: ``sondaje_admin``, ``base_datos``, o ``supervisor``.

Función
--------

La vista ``edit_checklist_materiales_sonda`` realiza los siguientes pasos:

1. **Manejo de ID del checklist a editar**:  
   Primero, intenta obtener el ID del checklist desde el ``POST`` de la solicitud, y lo almacena en la sesión bajo la clave ``'edit_id'``. Si no existe la clave ``'id'`` en el ``POST``, se recupera el ID previamente guardado en la sesión.

2. **Obtención de los datos del checklist**:  
   Con el ID del checklist, se obtiene el objeto correspondiente de ``ChecklistMaterialesSonda`` desde la base de datos. Se filtra utilizando el ID almacenado en la sesión.

3. **Inicialización del formulario**:  
   Se crea el formulario ``ChecklistMaterialesSondaEntradaForm`` y se inicializa con los valores actuales del checklist obtenido. El formulario se llena con la fecha, turno y jornada del checklist.

4. **Renderización del template**:  
   El contexto se prepara con el formulario, los datos del checklist y el ID del documento para pasar a la plantilla ``edit_materiales_sonda.html``, lo que permite al usuario ver y editar los valores.

Retorno
-------

La vista retorna una respuesta HTTP con el template ``edit_materiales_sonda.html`` y el siguiente contexto:

- ``'documento_id'``: El ID del checklist a editar.
- ``'form'``: El formulario con los valores iniciales del checklist.
- ``'checklist'``: Los datos del checklist que se están editando.
- ``'sidebar'``: Identificador para el sidebar.
- ``'sidebarmain'``: Identificador principal para el sidebar.

save_edit_checklist_materiales_sonda_entrada
============================================

Esta vista permite guardar los cambios en los materiales de un checklist de sonda en su etapa de "Entrada". La vista actualiza la cantidad de los materiales según lo enviado por el formulario.

Decoradores
------------

1. ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
--------

La vista ``save_edit_checklist_materiales_sonda_entrada`` realiza los siguientes pasos:

1. **Verificación de solicitud POST**:  
   La vista solo responde a solicitudes ``POST``. Si el método no es ``POST``, se devuelve un error indicando que el formulario no es válido.

2. **Iteración y actualización de cantidades**:  
   La vista recorre los elementos del ``POST`` buscando los campos que comienzan con ``'cantidad_'``. Por cada campo encontrado:

   - Se extrae el ID del material del campo ``'cantidad_'``, el cual se utiliza para encontrar el objeto correspondiente en ``ChecklistMaterialesSonda``.
   - Se actualiza el valor de ``cantidad`` del objeto con el nuevo valor recibido.
   
3. **Guardado de los cambios**:  
   Después de actualizar la cantidad de los materiales, se guarda el objeto actualizado en la base de datos utilizando ``checklist.save()``.

4. **Respuesta JSON**:  
   Si los cambios se guardan correctamente, se devuelve una respuesta JSON con ``{'success': True}``. Si no se recibe una solicitud válida, se devuelve un mensaje de error.

Retorno
-------

La vista retorna una respuesta JSON con los siguientes resultados:

- ``{'success': True}``: Si las cantidades de los materiales se actualizaron correctamente.
- ``{'success': False, 'message': 'El formulario no es válido.'}``: Si la solicitud no fue válida (no fue ``POST``).

save_edit_checklist_materiales_sonda_salida
===========================================

Esta vista permite guardar los cambios en los materiales de un checklist de sonda en su etapa de "Salida". La vista actualiza la cantidad de los materiales según lo enviado por el formulario.

Decoradores
------------

1. ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
--------

La vista ``save_edit_checklist_materiales_sonda_salida`` realiza los siguientes pasos:

1. **Verificación de solicitud POST**:  
   La vista solo responde a solicitudes ``POST``. Si el método no es ``POST``, se devuelve un error indicando que el formulario no es válido.

2. **Iteración y actualización de cantidades**:  
   La vista recorre los elementos del ``POST`` buscando los campos que comienzan con ``'cantidad_'``. Por cada campo encontrado:

   - Se extrae el ID del material del campo ``'cantidad_'``, el cual se utiliza para encontrar el objeto correspondiente en ``ChecklistMaterialesSonda``.
   - Se actualiza el valor de ``cantidad`` del objeto con el nuevo valor recibido.
   
3. **Guardado de los cambios**:  
   Después de actualizar la cantidad de los materiales, se guarda el objeto actualizado en la base de datos utilizando ``checklist.save()``.

4. **Respuesta JSON**:  
   Si los cambios se guardan correctamente, se devuelve una respuesta JSON con ``{'success': True}``. Si no se recibe una solicitud válida, se devuelve un mensaje de error.

Retorno
-------

La vista retorna una respuesta JSON con los siguientes resultados:

- ``{'success': True}``: Si las cantidades de los materiales se actualizaron correctamente.
- ``{'success': False, 'message': 'El formulario no es válido.'}``: Si la solicitud no fue válida (no fue ``POST``).

manage_checklist_materiales_caseta
==================================

Esta vista se encarga de gestionar y mostrar la lista de checklists de materiales de la caseta. Se filtra la información para mostrar los checklists más recientes, ordenados por la fecha de creación.

Decoradores
------------

1. ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

2. ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador permite el acceso solo a usuarios que tengan uno de los siguientes permisos:

   - ``sondaje_admin``
   - ``base_datos``
   - ``supervisor``

Función
--------

La vista ``manage_checklist_materiales_caseta`` realiza los siguientes pasos:

1. **Consulta de los checklists**:  
   Se obtiene una lista de checklists de materiales de la caseta a partir del modelo ``ChecklistMaterialesCaseta``. Se extraen los campos:

   - ``id_checklist``: El ID del checklist.
   - ``fecha_checklist``: La fecha en que se realizó el checklist.
   - ``creador``: El nombre del creador del checklist.
   - ``creador_cargo``: El cargo del creador del checklist.
   - ``turno``: El turno en que se realizó el checklist.
   - ``supervisor``: El supervisor encargado.

   La consulta agrupa los registros por los campos mencionados, eliminando duplicados mediante ``distinct()``, y ordena los resultados por la fecha del checklist en orden descendente.

2. **Contexto del template**:  
   Los datos obtenidos se pasan al contexto del template, de modo que se puedan mostrar en la plantilla ``manage_materiales_caseta.html``. Se incluyen las siguientes variables:
   
   - ``documentos``: La lista de checklists obtenida.
   - ``sidebar``: Una clave para destacar el área activa en la barra lateral (``'manage_checklist_materiales_caseta'``).
   - ``sidebarmain``: Una clave para indicar la sección principal de la barra lateral (``'system_checklist'``).

3. **Renderización del template**:  
   Finalmente, se renderiza el template ``manage_materiales_caseta.html`` con el contexto proporcionado.

Retorno
-------

La vista retorna el renderizado del template ``manage_materiales_caseta.html`` con los datos de los checklists.

new_checklist_materiales_caseta
===============================

Esta vista se encarga de crear un nuevo checklist de materiales para la caseta. Permite ingresar los datos de los materiales junto con algunos campos adicionales como el responsable, el turno y la fecha del checklist. También permite adjuntar fotografías para cada material.

Decoradores
------------

1. ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
--------

La vista ``new_checklist_materiales_caseta`` realiza los siguientes pasos:

1. **Solicitud POST**:  
   Si la solicitud es de tipo POST, se procesan los formularios:
   
   - ``formTop``: Recibe los datos del encabezado del checklist, como el responsable, turno, fecha y cargo.
   - ``formBottom``: Recibe los datos adicionales de los materiales, como las cantidades y las observaciones.

   Si el formulario ``formTop`` es válido, se realiza lo siguiente:

   1. **Obtener datos del formulario**:  
      Se extraen los siguientes valores del formulario:
     
      - ``responsable``: El nombre del responsable del checklist.
      - ``turno``: El turno en el que se realiza el checklist.
      - ``fecha_checklist``: La fecha en la que se realiza el checklist.
      - ``cargo``: El cargo del responsable.

   2. **Generar nuevo ID para el checklist**:  
      Se obtiene el último ID de checklist registrado y se le suma 1 para generar un nuevo ID correlativo.

   3. **Guardar materiales**:  
      Se recorren todos los materiales activos en el sistema (``MaterialesCaseta.objects.filter(status=True)``). Para cada material se extraen los siguientes datos del formulario:
      
      - ``b``: Cantidad de tipo B.
      - ``m``: Cantidad de tipo M.
      - ``observacion``: Observaciones del material.
      - ``fecha_str``: Fecha de control del material.
      - ``fotografia``: Fotografía del material.

      Luego se crea un nuevo registro en el modelo ``ChecklistMaterialesCaseta`` con los valores anteriores, junto con el ID de checklist generado.

   4. **Respuesta JSON**:  
      Si todo el proceso es exitoso, se retorna un JSON con el mensaje de éxito: ``{'success': True}``.

   Si el formulario no es válido, se retorna un mensaje de error: ``{'success': False, 'message': 'El formulario no es válido.'}``.

2. **Solicitud GET**:  
   Si la solicitud es de tipo GET, se inicializan los formularios con los siguientes datos:
   
   - ``formTop``: Se inicializa con el nombre del usuario autenticado y su rol.
   - ``formBottom``: Se inicializa como un formulario vacío.

   Además, se obtienen todos los materiales activos de la caseta (``MaterialesCaseta.objects.filter(status=True)``) para ser mostrados en el formulario.

   Los formularios y los materiales se pasan al contexto del template.

3. **Renderización del template**:  
   Se renderiza el template ``new_materiales_caseta.html`` con el contexto, que incluye los formularios y los materiales disponibles.

Retorno
-------

La vista retorna el renderizado del template ``new_materiales_caseta.html`` con los datos del formulario y los materiales, o una respuesta JSON con el resultado de la operación.

edit_checklist_materiales_caseta
================================

Esta vista permite editar un checklist de materiales de la caseta existente. Los usuarios pueden modificar los datos del checklist, como la fecha, el turno, el responsable, el cargo y las observaciones de revisión.

Decoradores
------------

1. ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

2. ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador restringe el acceso a usuarios con alguno de los siguientes permisos:
   
   - ``sondaje_admin``
   - ``base_datos``
   - ``supervisor``

Función
--------

La vista ``edit_checklist_materiales_caseta`` realiza los siguientes pasos:

1. **Obtener el ID del checklist a editar**:  
   Se obtiene el ID del checklist a editar a partir del formulario POST. Si el ID no está en la solicitud, se mantiene el ID almacenado previamente en la sesión.

2. **Consulta de los checklists**:  
   Se obtiene el checklist correspondiente al ``id_checklist`` desde el modelo ``ChecklistMaterialesCaseta``.

3. **Obtener los primeros datos para el formulario**:  
   Se extraen los primeros datos del checklist para usarlos como valores iniciales del formulario:
   
   - ``fecha_checklist``
   - ``turno``
   - ``creador`` (responsable)
   - ``creador_cargo`` (cargo del responsable)
   
   Estos datos se utilizan para inicializar el formulario ``ChecklistMaterialesCasetaFormTop``.

4. **Formulario de supervisor**:  
   Se inicializa un segundo formulario ``ChecklistMaterialesCasetaFormBottom`` con los datos del supervisor (nombre del usuario actual) y las observaciones de revisión del checklist.

5. **Contexto para el template**:  
   Los siguientes datos se pasan al contexto para ser utilizados en el template ``edit_materiales_caseta.html``:
   
   - ``documento_id``: El ID del checklist a editar.
   - ``formTop``: El formulario con los datos iniciales para la parte superior del checklist.
   - ``formBottom``: El formulario con los datos iniciales para la parte inferior del checklist.
   - ``checklist``: La lista de checklists filtrada.
   - ``sidebar``: Clave para resaltar el área activa en la barra lateral (``'manage_checklist_materiales_caseta'``).
   - ``sidebarmain``: Clave para la sección principal de la barra lateral (``'system_checklist'``).

6. **Renderización del template**:  
   Finalmente, se renderiza el template ``edit_materiales_caseta.html`` con el contexto proporcionado.

Retorno
-------

La vista retorna el renderizado del template ``edit_materiales_caseta.html``, que contiene los formularios para editar los datos del checklist.

save_edit_checklist_materiales_caseta
=====================================

Esta vista permite guardar los cambios en los materiales de un checklist de caseta. Los cambios incluyen la actualización de observaciones, fechas de control, fotografías y otros detalles del checklist.

Decoradores
------------

1. ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

2. ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que el usuario tenga permisos de administrador, base de datos o supervisor para acceder a la vista.

Función
--------

La vista ``save_edit_checklist_materiales_caseta`` realiza los siguientes pasos:

1. **Verificación de solicitud POST**:  
   La vista solo responde a solicitudes ``POST``. Si el método no es ``POST``, se devuelve un error indicando que el formulario no es válido.

2. **Extracción de datos del formulario**:  
   Se extraen los valores de los campos de la solicitud POST:
   
   - ``turno``: El turno del checklist.
   - ``fecha_revision``: La fecha de revisión convertida a formato ``datetime``.
   - ``observaciones_revision``: Observaciones adicionales sobre la revisión.
   - ``supervisor``: El supervisor que realizó la revisión.

3. **Iteración y actualización de materiales**:  
   La vista recorre los elementos del ``POST`` buscando los campos que comienzan con ``'observacion_'``. Por cada campo encontrado:
   
   - Se extrae el ID del material del campo ``'observacion_'``.
   - Se actualizan varios atributos del objeto ``ChecklistMaterialesCaseta`` correspondiente al material:
  
       - ``b`` y ``m``: Se actualizan con los valores obtenidos.
       - ``observacion``: Se actualiza con el valor de la observación.
       - ``fecha_control``: Se actualiza la fecha de control convertida a formato ``datetime``.
       - ``turno``, ``fecha_revision``, ``observaciones_revision`` y ``supervisor``: Se actualizan con los valores obtenidos.
  
   - Si se sube una nueva fotografía, se actualiza el campo ``fotografiaMaterial``.

4. **Guardado de los cambios**:  
   Después de actualizar los valores de los materiales, se guarda el objeto actualizado en la base de datos utilizando ``checklist.save()``.

5. **Respuesta JSON**:  
   Si los cambios se guardan correctamente, se devuelve una respuesta JSON con ``{'success': True}``. Si no se recibe una solicitud válida, se devuelve un mensaje de error.

Retorno
-------

La vista retorna una respuesta JSON con los siguientes resultados:

- ``{'success': True}``: Si los cambios se guardaron correctamente.
- ``{'success': False, 'message': 'El formulario no es válido.'}``: Si la solicitud no fue válida (no fue ``POST``).

Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.

save_checklist_materiales_sonda_entrada
=======================================

Ruta para guardar el checklist de materiales para la entrada de sondas.

URL
---

- ``/save_checklist_materiales_sonda_entrada``

Vista asociada
--------------

- ``save_checklist_materiales_sonda_entrada``

save_checklist_materiales_sonda_salida
======================================

Ruta para guardar el checklist de materiales para la salida de sondas.

URL
---

- ``/save_checklist_materiales_sonda_salida``

Vista asociada
--------------

- ``save_checklist_materiales_sonda_salida``

edit_checklist_materiales_sonda
===============================

Ruta para editar el checklist de materiales de la sonda.

URL
---

- ``/edit_checklist_materiales_sonda``

Vista asociada
--------------

- ``edit_checklist_materiales_sonda``


manage_checklist_materiales_sonda
=================================

Ruta para gestionar el checklist de materiales de la sonda.

URL
---

- ``/manage_checklist_materiales_sonda``

Vista asociada
--------------

- ``manage_checklist_materiales_sonda``

save_edit_checklist_materiales_sonda_entrada
============================================

Ruta para guardar la edición del checklist de materiales para la entrada de sondas.

URL
---

- ``/save_edit_checklist_materiales_sonda_entrada``

Vista asociada
--------------

- ``save_edit_checklist_materiales_sonda_entrada``

save_edit_checklist_materiales_sonda_salida
===========================================

Ruta para guardar la edición del checklist de materiales para la salida de sondas.

URL
---

- ``/save_edit_checklist_materiales_sonda_salida``

Vista asociada
--------------

- ``save_edit_checklist_materiales_sonda_salida``


new_checklist_materiales_caseta
===============================

Ruta para crear un nuevo checklist de materiales para casetas.

URL
---

- ``/new_checklist_materiales_caseta``

Vista asociada
--------------

- ``new_checklist_materiales_caseta``


edit_checklist_materiales_caseta
================================

Ruta para editar el checklist de materiales de las casetas.

URL
---

- ``/edit_checklist_materiales_caseta``

Vista asociada
--------------

- ``edit_checklist_materiales_caseta``


manage_checklist_materiales_caseta
==================================

Ruta para gestionar el checklist de materiales de las casetas.

URL
---

- ``/manage_checklist_materiales_caseta``

Vista asociada
--------------

- ``manage_checklist_materiales_caseta``

save_edit_checklist_materiales_caseta
=====================================

Ruta para guardar la edición del checklist de materiales de las casetas.

URL
---

- ``/save_edit_checklist_materiales_caseta``

Vista asociada
--------------

- ``save_edit_checklist_materiales_caseta``

