########
Drilling
########

Descripción General
*******************

Este módulo gestiona la información relacionada con las perforaciones, incluyendo detalles de perforaciones, aditivos, reportes operacionales y controles horarios. Permite el seguimiento del progreso, el estado de los sondajes y la administración de checklist asociados.

.. code-block:: bash   

    drilling/
    │── admin.py        # Configuración del panel de administración de Django
    │── apps.py         # Configuración de la aplicación Django
    │── forms.py        # Formularios utilizados dentro del módulo
    │── models.py       # Definición de modelos de datos
    │── urls.py         # Definición de rutas para las vistas del módulo
    │── views.py        # Lógica de controladores para las vistas
    │── migrations/     # Archivos de migración para la base de datos

Modelos de Datos (models.py)
****************************

Define las entidades utilizadas en el sistema para gestionar perforaciones y reportes.

ReportesOperacionales
=====================
    
El modelo ReportesOperacionales se utiliza para registrar y gestionar reportes digitales operacionales de perforación. Contiene información clave sobre los turnos de trabajo, la perforación realizada, el estado del sondaje y otros datos relevantes.

- Campos:
    - ``turno``: (CharField) Identifica el turno de trabajo en el que se realizó el reporte. Se elige a partir de opciones predefinidas.
    - ``fechacreacion``: (DateTimeField) Fecha y hora en la que se creó el reporte. Se asigna automáticamente con la fecha y hora actual.
    - ``fechaedicion``: (DateTimeField) Fecha y hora de la última edición del reporte. Se asigna automáticamente con la fecha y hora actual por defecto.
    - ``controlador``: (ForeignKey) Relación con el modelo Usuario, indicando quién es el controlador responsable del reporte.
    - ``perforista``: (ForeignKey) Relación con el modelo Perforistas, especificando quién realizó la perforación.
    - ``sonda``: (ForeignKey) Relación con el modelo Sondas, indicando qué sonda se utilizó.
    - ``sondajeCodigo``: (ForeignKey) Relación con el modelo Sondajes, asociando el reporte con un código de sondaje específico.
    - ``sondajeSerie``: (IntegerField) Número de serie del sondaje, con valores permitidos entre 3940 y 4400.
    - ``sondajeEstado``: (CharField) Estado del sondaje, conocido como "Gemelo". Puede tomar valores predefinidos o estar vacío.
    - ``metroInicial``: (DecimalField) Indica desde qué metro comenzó la perforación en el reporte.
    - ``metroFinal``: (DecimalField) Indica hasta qué metro se perforó en el reporte.
    - ``totalPerforado``: (DecimalField) Cantidad total de metros perforados en el turno registrado.
    - ``creador``: (CharField) Nombre del usuario que creó el registro.
    - ``progreso``: (CharField) Estado del progreso del reporte. Por defecto, se establece en "Creado".
    - ``correlativo``: (IntegerField) Número único correlativo del reporte.
    - ``status``: (BooleanField) Estado del reporte, indicando si está activo (True) o inactivo (False).
    - ``id_checklist``: (BigIntegerField) Identificador de un checklist asociado con el reporte.
- Métodos:
    - ``__str__(self)``: Retorna una representación en cadena del reporte, mostrando la sonda, el código de sondaje y la serie del sondaje.
- Metadatos:
    - ``verbose_name``: "Reporte Digital Operacional".
    - ``verbose_name_plural``: "Reportes Digitales Operacionales".
    - ``db_table``: drilling_reporte_digital_operacional.

DetallesPerforaciones
=====================
    
El modelo DetallesPerforaciones almacena información detallada sobre las perforaciones realizadas en cada reporte operacional. Se vincula con ReportesOperacionales y otros modelos relacionados para registrar características clave de la perforación.

- Campos:
    - ``reporte``: (ForeignKey) Relación con ReportesOperacionales, indicando a qué reporte pertenece el detalle de perforación.
    - ``diametros``: (ForeignKey) Relación con Diametros, especificando el diámetro de perforación utilizado.
    - ``perforado``: (DecimalField) Metros perforados en el detalle registrado.
    - ``desde``: (DecimalField) Indica desde qué metro comienza la perforación en este detalle.
    - ``hasta``: (DecimalField) Indica hasta qué metro llega la perforación en este detalle.
    - ``recuperacion``: (DecimalField) Cantidad de material recuperado de la perforación.
    - ``porcentajeRecuperacion``: (DecimalField) Porcentaje de recuperación del material perforado.
    - ``barra``: (IntegerField) Cantidad de barras utilizadas en la perforación.
    - ``largoBarra``: (DecimalField) Largo de cada barra utilizada, si aplica.
    - ``totalHtas``: (DecimalField) Total de horas trabajadas en la perforación.
    - ``contra``: (DecimalField) Horas de contratista en la operación.
    - ``tipoTerreno``: (ForeignKey) Relación con TipoTerreno, indicando el tipo de terreno donde se realizó la perforación.
    - ``orientacion``: (ForeignKey) Relación con Orientacion, indicando la orientación de la perforación.
    - ``fechacreacion``: (DateTimeField) Fecha y hora en la que se creó el detalle. Se asigna automáticamente.
    - ``status``: (BooleanField) Estado del detalle de perforación (True para activo, False para inactivo).
- Métodos:
    - ``__str__(self)``: Retorna una representación en cadena del reporte al que pertenece el detalle.
- Metadatos:
    - ``verbose_name``: "Reporte Digital Perforación".
    - ``verbose_name_plural``: "Reportes Digitales Perforaciones".
    - ``db_table``: drilling_reporte_digital_perforaciones.

ControlesHorarios
=================

El modelo ControlesHorarios registra y gestiona los controles de horario de los reportes operacionales, permitiendo un seguimiento detallado del tiempo trabajado en cada operación de perforación.

- Campos:
    - ``reporte``: (ForeignKey) Relación con ReportesOperacionales, indicando a qué reporte pertenece el control de horario.
    - ``posicion``: (IntegerField) Número de orden o posición dentro del control horario.
    - ``inicio``: (TimeField) Hora de inicio de la actividad registrada en este control horario.
    - ``final``: (TimeField) Hora de finalización de la actividad registrada en este control horario.
    - ``total``: (TimeField) Total de horas trabajadas en esta actividad.
    - ``detalleControlHorario``: (ForeignKey) Relación con DetalleControlHorario, indicando el tipo de actividad o evento registrado en este control.
    - ``fechacreacion``: (DateTimeField) Fecha y hora en la que se creó el registro. Se asigna automáticamente.
    - ``status``: (BooleanField) Estado del control de horario (True para activo, False para inactivo).
- Métodos:
    - ``__str__(self)``: Retorna una representación en cadena del reporte al que pertenece el control horario.
- Metadatos:
    - ``verbose_name``: "Reporte Digital Control Horario".
    - ``verbose_name_plural``: "Reportes Digitales Control Horario".
    - ``db_table``: drilling_reporte_digital_control_horario.

DetalleAditivos
===============

El modelo DetalleAditivos permite registrar el uso de aditivos en los reportes operacionales de perforación, asegurando un control detallado de los insumos utilizados.

- Campos:
    - ``reporte``: (ForeignKey) Relación con ReportesOperacionales, identificando a qué reporte pertenece el registro del aditivo.
    - ``aditivo``: (ForeignKey) Relación con Aditivos, especificando el tipo de aditivo utilizado.
    - ``cantidad``: (IntegerField) Cantidad de aditivo usado, con un valor mínimo de 0 y un máximo de 1000.
    - ``fechacreacion``: (DateTimeField) Fecha y hora de creación del registro, asignada automáticamente.
    - ``status``: (BooleanField) Estado del registro (True para activo, False para inactivo).
- Métodos:
    - ``__str__(self)``: Retorna una representación en cadena del reporte al que pertenece el aditivo.
- Metadatos:
    - ``verbose_name``: "Reporte Digital Aditivo".
    - ``verbose_name_plural``: "Reportes Digitales Aditivos".
    - ``db_table``: drilling_reporte_digital_aditivos.

Insumos
=======

El modelo Insumos permite registrar los materiales e insumos utilizados en los reportes operacionales de perforación, facilitando un control detallado de los recursos empleados en cada proceso.

- Campos:
    - ``reporte``: (ForeignKey) Relación con ReportesOperacionales, identificando a qué reporte pertenece el registro de insumos.
    - ``corona``: (CharField) Tipo de corona utilizada en la perforación.
    - ``escareador``: (CharField) Tipo de escariador utilizado en la perforación.
    - ``cantidadAgua``: (ForeignKey) Relación con CantidadAgua, registrando la cantidad de agua en litros utilizada en la perforación.
    - ``casing``: (CharField) Tipo de casing utilizado en la perforación.
    - ``zapata``: (CharField) Tipo de zapata utilizada en la perforación.
    - ``status``: (BooleanField) Estado del registro (True para activo, False para inactivo).
- Métodos:
    - ``__str__(self)``: Retorna una representación en cadena del reporte al que pertenecen los insumos.
- Metadatos:
    - ``verbose_name``: "Reporte Digital Insumo".
    - ``verbose_name_plural``: "Reportes Digitales Insumos".
    - ``db_table``: drilling_reporte_digital_insumos.

LongitudPozos
=============
    
El modelo LongitudPozos almacena la información detallada sobre la longitud y componentes del pozo perforado en un reporte operacional.

- Campos:
    - ``reporte``: (ForeignKey) Relación con ReportesOperacionales, identificando el reporte al que pertenece el registro de longitud del pozo.
    - ``largoBarril``: (DecimalField) Largo del barril en metros, con valores entre 2.00 y 5.50.
    - ``largoBarra``: (DecimalField) Largo de la barra en metros, con valores entre 0.00 y 9.00.
    - ``puntoMuerto``: (DecimalField) Punto muerto en metros, con valores entre 0.00 y 5.00.
    - ``restoBarra``: (DecimalField) Longitud restante de la barra en metros.
    - ``numeroBarras``: (IntegerField) Cantidad total de barras utilizadas.
    - ``longitudPozo``: (DecimalField) Longitud total del pozo perforado en metros.
    - ``htaEnPozo``: (CharField) Indica si hay herramienta en el pozo (Sí o No).
    - ``mtsDeHta``: (DecimalField) Metros de herramienta dentro del pozo (opcional).
    - ``profundidadHta``: (DecimalField) Profundidad a la que queda la herramienta en el pozo (opcional).
    - ``status``: (BooleanField) Estado del registro (True para activo, False para inactivo).
- Métodos:
    - ``__str__(self)``: Retorna una representación en cadena del reporte al que pertenece la longitud del pozo.
- Metadatos:
    - ``verbose_name``: "Reporte Digital Longitud".
    - ``verbose_name_plural``: "Reportes Digitales Longitud".
    - ``db_table``: drilling_reporte_digital_longitud.

ObservacionesReportes
=====================

El modelo ObservacionesReportes almacena observaciones y comentarios adicionales sobre un reporte operacional.

- Campos:
    - ``reporte``: (ForeignKey) Relación con ReportesOperacionales, identificando el reporte al que pertenece la observación.
    - ``observaciones``: (TextField) Campo de texto de hasta 1000 caracteres para registrar comentarios u observaciones adicionales.
    - ``status``: (BooleanField) Estado del registro (True para activo, False para inactivo).
- Métodos:
    - ``__str__(self)``: Retorna una representación en cadena del reporte al que pertenece la observación.
- Metadatos:
    - ``verbose_name``: "Reporte Digital Observación".
    - ``verbose_name_plural``: "Reportes Digitales Observaciones".
    - ``db_table``: drilling_reporte_digital_observaciones.
    
Formularios (forms.py)
**********************

Contiene los formularios utilizados en las vistas.

FormReportesOperacionales
=========================

Este formulario se utiliza para gestionar los reportes operacionales asociados a las actividades de perforación y sondajes en el sistema. Permite ingresar y editar detalles sobre la perforación, el perforista, y la sonda, entre otros aspectos operacionales.

Campos del Formulario
----------------------

1. ``fechacreacion``
   
    - Tipo: DateField
    - Etiqueta: "Fecha de creación"
    - Widget: DateInput (con formato de fecha '%Y-%m-%d' y clase form-control)
    - Descripción: Indica la fecha en que se creó el reporte.

2. ``perforista``

    - Tipo: ForeignKey (relacionado con el modelo ``Perforistas``)
    - Etiqueta: "Perforista"
    - Widget: Select (con clase form-control)
    - Descripción: Selección del perforista encargado de la operación.

3. ``metroInicial``

    - Tipo: IntegerField
    - Etiqueta: "Metro Inicial"
    - Widget: NumberInput (con clase form-control)
    - Descripción: Indica el metro inicial de la perforación.

4. ``turno``

    - Tipo: CharField
    - Etiqueta: "Turno"
    - Widget: Select (con clase form-control)
    - Descripción: Selección del turno en el que se realizó la perforación.

5. ``sonda``

    - Tipo: ForeignKey (relacionado con el modelo ``Sondas``)
    - Etiqueta: "Sonda"
    - Widget: Select (con clase form-control)
    - Descripción: Selección de la sonda utilizada en la perforación.

6. ``metroFinal``

    - Tipo: IntegerField
    - Etiqueta: "Metro Final"
    - Widget: NumberInput (con clase form-control)
    - Descripción: Indica el metro final alcanzado en la perforación.

7. ``controlador``

    - Tipo: CharField
    - Etiqueta: "Controlador"
    - Widget: TextInput (con clase form-control)
    - Descripción: Nombre del controlador de la operación.

8. ``sondajeCodigo``

    - Tipo: ForeignKey (relacionado con el modelo ``Sondajes``)
    - Etiqueta: "Código de Sondaje"
    - Widget: Select (con clase form-control new-td)
    - Descripción: Selección del código del sondaje.

9.  ``sondajeSerie``

    - Tipo: IntegerField
    - Etiqueta: "Serie de Sondaje"
    - Widget: NumberInput (con clase form-control new-td, valores min: 3940, max: 4400)
    - Descripción: Número de serie del sondaje.

10. ``sondajeEstado``

    - Tipo: CharField
    - Etiqueta: "Estado de Sondaje"
    - Widget: Select (con clase form-control)
    - Descripción: Estado del sondaje (por ejemplo, activo, finalizado).

11. ``totalPerforado``

    - Tipo: IntegerField
    - Etiqueta: "Total Perforado"
    - Widget: NumberInput (con clase form-control)
    - Descripción: Total de metros perforados.

Consideraciones Adicionales
---------------------------

- Campos de solo lectura: Los campos ``fechacreacion``, ``metroInicial``, ``metroFinal``, ``totalPerforado``, y ``controlador`` se configuran como solo lectura, de modo que no pueden ser editados una vez que se han registrado.
- Validación: El formulario valida que ciertos campos, como ``perforista``, ``sondajeCodigo``, y ``sondajeSerie``, sean obligatorios, mientras que otros, como ``sondajeEstado``, son opcionales.
- Deshabilitar campos: Algunos campos, como ``sondajeCodigo`` y ``sonda``, pueden ser deshabilitados dependiendo de los parámetros

FormDetallesPerforaciones
=========================

Este formulario se utiliza para gestionar los detalles relacionados con las perforaciones, como los rangos de profundidad y el porcentaje de recuperación. Permite ingresar y editar la información específica de las perforaciones realizadas.

Campos del Formulario
----------------------

1. ``desde``

    - Tipo: IntegerField

    - Etiqueta: "Desde"

    - Widget: NumberInput (con clase form-control)

    - Descripción: Indica la profundidad inicial de la perforación.

    - Restricción: Este campo está configurado como solo lectura.

2. ``hasta``

    - Tipo: IntegerField

    - Etiqueta: "Hasta"

    - Widget: NumberInput (con clase form-control)

    - Descripción: Indica la profundidad final de la perforación.

    - Restricción: Este campo está configurado como solo lectura.

3. ``porcentajeRecuperacion``

    - Tipo: DecimalField

    - Etiqueta: "Porcentaje de Recuperación"

    - Widget: NumberInput (con clase form-control)

    - Descripción: Indica el porcentaje de recuperación de los materiales durante la perforación.

    - Restricción: Este campo está configurado como solo lectura.

Consideraciones Adicionales
---------------------------

- Campos de solo lectura: Los campos ``desde``, ``hasta`` y ``porcentajeRecuperacion`` están configurados como solo lectura, lo que significa que no pueden ser editados una vez que se han ingresado.

- Modelo: Este formulario está basado en el modelo ``DetallesPerforaciones`` y se utiliza para gestionar los detalles específicos de las perforaciones realizadas en un proceso de sondaje o perforación.

- Validación: No se especifican validaciones adicionales en este formulario, pero los campos numéricos deberían seguir las reglas definidas en el modelo correspondiente.


FormControlesHorarios
======================

Este formulario se utiliza para gestionar los controles horarios relacionados con un proceso o tarea específica. Permite ingresar la hora de inicio, finalización y el cálculo del total de tiempo.

Campos del Formulario
----------------------

1. ``inicio``

    - Tipo: DateTimeField

    - Etiqueta: "Inicio"

    - Widget: TextInput (con clase tempus-dominus)

    - Descripción: Indica la hora de inicio del control horario.

    - Restricción: El widget tiene un autocomplete desactivado y se utiliza para ingresar fechas y horas.

2. ``final``

    - Tipo: DateTimeField

    - Etiqueta: "Final"

    - Widget: TextInput (con clase tempus-dominus)

    - Descripción: Indica la hora de finalización del control horario.

    - Restricción: El widget tiene un autocomplete desactivado y se utiliza para ingresar fechas y horas.

3. ``total``

    - Tipo: DurationField

    - Etiqueta: "Total"

    - Widget: NumberInput (con clase form-control)

    - Descripción: Calcula el total de tiempo transcurrido entre el inicio y final del control horario.

    - Restricción: Este campo está configurado como solo lectura, ya que su valor se calcula automáticamente a partir de los campos ``inicio`` y ``final``.

4. ``detalleControlHorario``

    - Tipo: CharField

    - Etiqueta: "Detalle del Control Horario"

    - Widget: TextInput (con clase form-control)

    - Descripción: Proporciona detalles adicionales sobre el control horario realizado.

    - Restricción: No se especifica ninguna restricción especial.

Consideraciones Adicionales
---------------------------

- Campo ``total`` como solo lectura: El campo ``total`` está configurado como solo lectura, lo que significa que no puede ser editado directamente, sino que se calcula automáticamente en función de los valores de ``inicio`` y ``final``.

- Widgets personalizados: Los campos ``inicio`` y ``final`` utilizan el widget ``tempus-dominus``, que permite ingresar las fechas y horas de manera más precisa, con un calendario emergente para facilitar la selección.

- Modelo: Este formulario está basado en el modelo ``ControlesHorarios`` y se utiliza para registrar el tiempo que se ha dedicado a una actividad o tarea específica.

FormInsumos
============

Este formulario se utiliza para gestionar los insumos necesarios en el proceso de perforación o trabajo relacionado. Permite registrar información sobre varios insumos, como la corona, escareador, cantidad de agua, casing y zapata.

Campos del Formulario
----------------------

1. ``corona``

    - Tipo: CharField

    - Etiqueta: "Corona"

    - Descripción: Representa la corona utilizada en el proceso.

    - Restricción: Este campo no es obligatorio.

2. ``escareador``

    - Tipo: CharField

    - Etiqueta: "Escareador"

    - Descripción: Representa el escareador utilizado en el proceso.

    - Restricción: Este campo no es obligatorio.

3. ``cantidadAgua``

    - Tipo: CharField

    - Etiqueta: "Cantidad de Agua"

    - Descripción: Representa la cantidad de agua utilizada o requerida.

    - Restricción: Este campo no es obligatorio.

4. ``casing``

    - Tipo: FloatField

    - Etiqueta: "Casing (mts)"

    - Descripción: Representa el valor de casing en metros.

    - Restricción: Este campo no es obligatorio.

    - Widget: NumberInput (con clase form-control)

5. ``zapata``

    - Tipo: CharField

    - Etiqueta: "Zapata"

    - Descripción: Representa la zapata utilizada en el proceso.

    - Restricción: Este campo no es obligatorio.

Consideraciones Adicionales
---------------------------

- Campos no obligatorios: Los campos ``corona``, ``escareador``, ``cantidadAgua``, ``casing`` y ``zapata`` están configurados como no obligatorios. Esto permite flexibilidad en el registro de los insumos, ya que no es necesario completar todos los campos.

- Etiqueta personalizada: El campo ``casing`` tiene una etiqueta personalizada ``"Casing (mts)"`` para indicar claramente la unidad de medida (metros).

- Widget de ``casing``: El campo ``casing`` utiliza un widget de entrada numérica con la clase ``form-control`` para mejorar la entrada de datos en la interfaz de usuario.

FormAditivos
=============

Este formulario se utiliza para gestionar los aditivos y su cantidad en el proceso correspondiente. Permite registrar la selección del aditivo y la cantidad requerida.

Campos del Formulario
----------------------

1. ``aditivo``

    - Tipo: ForeignKey (relacionado con el modelo ``DetalleAditivos``)

    - Etiqueta: "Aditivo"

    - Descripción: Representa el aditivo que se está utilizando.

    - Restricción: Este campo es obligatorio y se presenta como un campo de selección (dropdown).

    - Widget: Select (con clase ``form-control`` y atributo ``autocomplete: "off"``)

2. ``cantidad``

    - Tipo: FloatField

    - Etiqueta: "Cantidad"

    - Descripción: Representa la cantidad del aditivo a utilizar.

    - Restricción: Este campo es obligatorio y se presenta como un campo de entrada numérica.

    - Widget: NumberInput (con clase ``form-control`` y atributo ``autocomplete: "off"``)

Consideraciones Adicionales
---------------------------

- Widget de ``aditivo``: El campo ``aditivo`` usa un widget de selección para elegir el aditivo de una lista de opciones disponibles. Se ha agregado el atributo ``autocomplete: "off"`` para mejorar la experiencia de usuario.

- Widget de ``cantidad``: El campo ``cantidad`` utiliza un widget de entrada numérica para asegurar que se ingrese un valor válido y numérico. También se incluye el atributo ``autocomplete: "off"`` para evitar el autocompletado del navegador.

FormLongitudPozos
=================

Este formulario está diseñado para registrar las características y detalles de los pozos en cuanto a su longitud y otros parámetros relacionados.

Campos del Formulario
----------------------

1. ``largoBarril``

    - Tipo: FloatField

    - Etiqueta: "Largo Barril"

    - Descripción: Representa el largo del barril en metros.

    - Restricción: Campo numérico, con un rango entre 2.0 y 5.5 metros.

    - Widget: NumberInput (con rango mínimo de 2.0 y máximo de 5.5)

2. ``puntoMuerto``

    - Tipo: FloatField

    - Etiqueta: "Punto Muerto"

    - Descripción: Representa el punto muerto en metros.

    - Restricción: Campo numérico, con un rango entre 0.1 y 5.0 metros.

    - Widget: NumberInput (con rango mínimo de 0.1 y máximo de 5.0)

3. ``restoBarra``

    - Tipo: FloatField

    - Etiqueta: "Resto Barra"

    - Descripción: Representa el resto de la barra en el pozo.

    - Restricción: Este campo es solo de lectura (readonly) y no es obligatorio.

    - Widget: NumberInput (solo lectura)

4. ``numeroBarras``

    - Tipo: IntegerField

    - Etiqueta: "Número de Barras"

    - Descripción: Representa el número de barras en el pozo.

    - Restricción: Este campo es solo de lectura (readonly) y no es obligatorio.

    - Widget: NumberInput (solo lectura)

5. ``longitudPozo``

    - Tipo: FloatField

    - Etiqueta: "Longitud del Pozo"

    - Descripción: Representa la longitud total del pozo en metros.

    - Restricción: Este campo es solo de lectura (readonly) y no es obligatorio.

    - Widget: NumberInput (solo lectura)

6. ``htaEnPozo``

    - Tipo: ChoiceField

    - Etiqueta: "Queda Hta. en el Pozo"

    - Descripción: Representa si queda HTA en el pozo.

    - Restricción: Este campo es obligatorio.

    - Widget: Select (con clase ``form-control``)

7. ``mtsDeHta``

    - Tipo: FloatField

    - Etiqueta: "Metros de Hta."

    - Descripción: Representa los metros de HTA en el pozo.

    - Restricción: Este campo es obligatorio y debe ser un valor numérico mayor o igual a 0.0.

    - Widget: NumberInput (con mínimo de 0.0)

8. ``profundidadHta``

    - Tipo: FloatField

    - Etiqueta: "Profundidad a la que queda (mts)"

    - Descripción: Representa la profundidad a la que se encuentra el HTA en el pozo.

    - Restricción: Este campo es obligatorio y debe ser un valor numérico mayor o igual a 0.0.

    - Widget: NumberInput (con mínimo de 0.0)

Consideraciones Adicionales
---------------------------

- Campos de solo lectura: Los campos ``restoBarra``, ``numeroBarras``, y ``longitudPozo`` están configurados como solo lectura para evitar que el usuario los edite. 

- Campos obligatorios: Los campos ``htaEnPozo``, ``mtsDeHta`` y ``profundidadHta`` son obligatorios y deben ser completados antes de enviar el formulario.

- Rango de valores: Se han establecido restricciones numéricas en varios campos, como ``largoBarril``, ``puntoMuerto``, ``mtsDeHta`` y ``profundidadHta``, para garantizar que los valores ingresados sean válidos dentro de los límites establecidos.

FormObservacionesReportes
=========================

Este formulario está diseñado para registrar las observaciones asociadas a un reporte.

Campos del Formulario
----------------------

1. ``observaciones``

    - Tipo: CharField

    - Etiqueta: No tiene etiqueta visible, se ha configurado para que el campo no tenga etiqueta (label vacío).

    - Descripción: Campo para registrar cualquier observación adicional relacionada con el reporte.

    - Restricción: Este campo no es obligatorio.

    - Widget: Textarea (utilizado por defecto para campos de texto largo)

Consideraciones Adicionales
---------------------------

- Etiqueta vacía: El campo ``observaciones`` no tiene etiqueta visible, ya que se ha configurado con una etiqueta vacía.

- Campo opcional: El campo ``observaciones`` no es obligatorio. Esto significa que el usuario puede dejar este campo vacío si no tiene ninguna observación que registrar.


Vistas (views.py)
*****************

Define la lógica para mostrar y procesar información en la interfaz.

new_reporte_digital
===================

Esta vista muestra un formulario para crear un nuevo reporte digital de perforación. Proporciona varias secciones con campos relacionados con el reporte de perforación, incluyendo detalles de perforación, control horario, aditivos, insumos, y más.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_controlador_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles específicos relacionados con la administración de sondajes, controladores, base de datos o supervisores.

Funcionamiento
--------------

- Se obtiene el perfil de usuario para validar si la faena está asignada. Si no está asignada, redirige a la página de edición de perfil.
- Se consultan varios modelos relacionados con el reporte, como ``DetalleControlHorario``, ``Diametros``, ``TipoTerreno``, ``Orientacion``, ``Aditivos``, y ``Sondajes``, para poblar los formularios y opciones del reporte.
- Se renderiza un formulario con los datos obtenidos y las variables de configuración de barra lateral para la navegación dentro del sistema.

Retorno
-------

- Se retorna un renderizado de la página ``new_reporte_digital.html`` con el contexto cargado, que incluye los formularios, los datos del usuario y las variables de configuración de barra lateral.

---

save_reporte_digital
====================

Esta vista guarda los datos de un reporte digital de perforación cuando se envía el formulario correspondiente. Crea varias entidades relacionadas con el reporte, como detalles de perforación, controles horarios, insumos y observaciones.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_controlador_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles específicos relacionados con la administración de sondajes, controladores, base de datos o supervisores.

Funcionamiento
--------------

- Se recibe la información enviada por el formulario en un ``POST`` y se crea o actualiza un reporte operacional basado en los datos proporcionados.
- La creación de registros en modelos como ``DetallesPerforaciones``, ``ControlesHorarios``, ``Insumos``, ``DetalleAditivos``, ``LongitudPozos``, y ``ObservacionesReportes`` se maneja dentro de una transacción atómica para asegurar la integridad de los datos.
- Si algún paso falla, se captura la excepción y se proporciona un mensaje de error específico.

Retorno
-------

- Si la transacción es exitosa, se redirige al usuario a la vista ``manage_mis_reportes_digitales``.
- Si ocurre un error, se retorna una respuesta JSON con el error específico.

---

obtener_metro_inicial
=====================

Esta vista obtiene información sobre un reporte de perforación específico basado en los parámetros enviados, tales como ``sondajeCodigo``, ``sondajeSerie``, ``sondajeEstado`` y ``id_checklist``.

Decoradores
-----------

- ``@require_GET``:  
   Solo permite solicitudes GET.

- ``@sondaje_admin_or_controlador_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles específicos relacionados con la administración de sondajes, controladores, base de datos o supervisores.

Funcionamiento
--------------

- Se consulta un reporte específico de ``ReportesOperacionales`` utilizando los parámetros proporcionados en la solicitud.
- Si se encuentra el reporte, se devuelve la información detallada en formato JSON, incluyendo los detalles de perforación, insumos, y longitud del pozo.
- Si no se encuentra el reporte, se devuelve un JSON con datos vacíos.

Retorno
-------

- Se retorna un ``JsonResponse`` con la información del reporte de perforación y los datos relacionados. En caso de no encontrar el reporte, se retornan datos vacíos.

manage_mis_reportes_digitales
==============================

Esta vista muestra los reportes digitales de un usuario dependiendo de su faena asignada. Si el usuario tiene asignada una faena, se mostrarán los reportes correspondientes a esa faena. En caso contrario, los reportes estarán disponibles para administradores.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_controlador_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Obtiene el perfil del usuario con ``UsuarioProfile.objects.get(user=request.user)``.
- Si el usuario no tiene una faena asignada, y es un ``ADMINISTRADOR``, se filtran los reportes de ``ChecklistMaterialesSonda`` con estado ``'Por Corregir'`` y etapa ``"Entrada"``.
- Si el usuario tiene asignada una faena, los reportes se filtran por la faena del usuario.
- Se obtiene el reporte con la fecha de creación más reciente.
- Los resultados se ordenan por fecha de creación en orden descendente.

Retorno
-------

- Se retorna un renderizado de la página ``manage_mis_reportes_digitales.html`` con el contexto cargado, que incluye:
  - ``reportes``: Lista de reportes filtrados y ordenados.
  - ``sidebar``: Menú lateral para navegación.
  - ``sidebarmain``: Menú principal.

---

manage_revisar_reportes_digitales
=================================

Esta vista muestra los reportes digitales que están en estado ``'Corregido'`` o ``'Por Revisar'``, según el perfil del usuario.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Similar a la vista ``manage_mis_reportes_digitales``, pero filtrando reportes que están en estado ``'Corregido'`` o ``'Por Revisar'``.
- Los reportes se ordenan por fecha de creación más reciente.

Retorno
-------

- Se retorna un renderizado de la página ``manage_revisar_reportes_digitales.html`` con el contexto cargado.

---

manage_todos_reportes_digitales
================================

Esta vista muestra todos los reportes digitales de un usuario en estado ``'Por Corregir'`` o ``'Corregido'``.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Similar a las vistas anteriores, pero se filtran todos los reportes sin restricción de estado (``'Por Corregir'`` o ``'Corregido'``).
- Los reportes se ordenan por fecha de creación más reciente.

Retorno
-------

- Se retorna un renderizado de la página ``manage_todos_reportes_digitales.html`` con el contexto cargado.

progreso_reporte_digital
=========================

Esta vista maneja el cambio de estado de un reporte digital. Se realiza una validación de las horas totales de control horario y, si es correcta, se actualiza el estado del reporte.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_controlador_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- El reporte se obtiene a través del ID del checklist enviado en el formulario ``POST``.
- Se calculan las horas totales de control horario a partir de los ``ControlesHorarios`` asociados al reporte.
- Si las horas no son exactamente 12:00, se muestra un mensaje de error.
- Si las horas son correctas, se cambia el estado del reporte y del checklist:
  
  - Si el reporte está en estado ``'Creado'``, se actualiza a ``'Por Revisar'``.
  - Si el reporte está en estado ``'Por Corregir'``, se actualiza a ``'Corregido'``.
  
- Los mensajes informan del resultado de la operación.

Retorno
-------

- Si las horas no son correctas, se redirige de vuelta a la vista ``manage_mis_reportes_digitales`` con un mensaje de error.
- Si la operación fue exitosa, se redirige también a ``manage_mis_reportes_digitales`` con un mensaje de éxito.
- En caso de error, se muestra un mensaje y se redirige igualmente.

---

progreso_reporte_digital_corregir
==================================

Esta vista maneja el estado de un reporte digital, enviándolo para corrección. Si el reporte se encuentra en el estado adecuado, se actualiza a ``'Por Corregir'``.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Se obtiene el reporte mediante el ID del checklist.
- Si el reporte está en estado ``'Por Revisar'`` o ``'Corregido'``, se actualiza su estado a ``'Por Corregir'``.
- Si no es posible realizar la actualización debido a que el estado no es adecuado, se muestra un mensaje de error.
- Si el reporte aún no ha sido completado, se informa al usuario para que lo complete antes de enviarlo a corrección.

Retorno
-------

- En caso de éxito, el reporte se redirige a la vista ``manage_revisar_reportes_digitales`` con un mensaje de éxito.
- Si ocurre un error, se muestra un mensaje y se redirige a la misma vista con una notificación del error.

progreso_reporte_digital_aprobar
================================

Esta vista maneja la aprobación de un reporte digital. Si el reporte se encuentra en el estado adecuado, su progreso se actualiza a ``'Aprobado'``. Si el reporte no se encuentra en un estado adecuado, se muestra un mensaje de error.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Se obtiene el reporte mediante el ID del checklist.
- Si el reporte está en estado ``'Por Revisar'`` o ``'Corregido'``, se actualiza su estado a ``'Aprobado'``.
- Si el reporte no puede ser aprobado, se muestra un mensaje de error.
- Si el reporte no está completado, se muestra un mensaje solicitando completar el reporte antes de aprobarlo.

Retorno
-------

- En caso de éxito, el reporte se redirige a la vista ``manage_revisar_reportes_digitales`` con un mensaje de éxito.
- Si ocurre un error, se muestra un mensaje y se redirige a la misma vista con una notificación del error.

editar_reporte_digital
=======================

Esta vista permite editar un reporte digital existente. Se cargan los datos del reporte y del checklist correspondiente, permitiendo editar los detalles de los mismos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_controlador_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Se obtiene el reporte a editar mediante el ID del checklist guardado en la sesión.
- Se cargan los datos de los checklists de entrada y salida si existen.
- Si el reporte ya está aprobado o corregido, se muestra la información correspondiente.
- Los formularios de entrada y salida se completan con los datos del checklist, y se configuran para lectura solamente si corresponde.
- Si no existen ciertos datos, se notifica y se configuran formularios por defecto.

Retorno
-------

- El contexto incluye los formularios de entrada y salida, y los detalles del reporte, permitiendo al usuario editar y actualizar la información.
- Se redirige a la plantilla ``edit_reporte_digital.html`` con los datos cargados y procesados.

save_editar_reporte_digital
=============================

Esta vista se encarga de guardar o editar un reporte digital. Realiza varias actualizaciones de datos, validaciones y crea nuevos registros según la información proporcionada en el formulario.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_controlador_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Verifica si la solicitud es de tipo ``POST``.
- Si el valor de ``sondajeEstado`` es ``'---------'``, se establece como vacío, de lo contrario se asigna el valor proporcionado en el formulario.
- Inicia una transacción atómica para realizar varias actualizaciones de datos en diferentes modelos:
  
    - Se obtiene el reporte correspondiente por el ID del checklist y se marca como ``False`` (inactivo).
    - Se actualizan los detalles de perforación, controles horarios, insumos, aditivos, longitud de pozos y observaciones para desactivarlos.
    - Se crea un nuevo reporte con los datos proporcionados y se asocia a las tablas relacionadas.
    - Se verifican y crean registros en las secciones de perforación, control horario, insumos, aditivos, longitud de pozo y observaciones.

- Dependiendo del origen del reporte (``my_report``, ``check_report``, ``all_report``), se redirige a la vista correspondiente.

Retorno
-------

- Si la operación es exitosa, se redirige a la vista correspondiente según el origen del reporte.
- En caso de error, se devuelve una respuesta JSON con el mensaje de error y se indica que el usuario debe revisar los datos e intentar nuevamente.

obtener_estado_sonda
=====================

Esta vista obtiene el último reporte operacional asociado a una sonda, excluyendo aquellos con el progreso ``Aprobado``.

Decoradores
-----------

- ``@require_GET``:  
   Restringe el acceso a solicitudes de tipo ``GET``.

- ``@sondaje_admin_or_controlador_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con los permisos adecuados.

Funcionamiento
--------------

- Se obtiene el ID de la sonda desde los parámetros ``GET`` de la solicitud.
- Se busca el último reporte operacional asociado a la sonda y que tenga el estado ``status=True``, excluyendo los reportes cuyo progreso sea ``Aprobado``.
- El reporte encontrado es el más reciente según la fecha de creación.

Retorno
-------

- Se retorna un objeto ``JsonResponse`` con los datos del reporte, en formato JSON, con un código de estado 200.

reporte_digital_pdf_view
=========================

Esta vista permite generar un archivo PDF con los detalles de un reporte digital, incluyendo perforaciones, control horario, aditivos, insumos, longitud de pozo y observaciones.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- Verifica si la solicitud es de tipo ``POST``.
- Se obtiene el checklist de materiales de la sonda mediante el ID proporcionado en el formulario.
- Se busca el reporte operacional asociado al checklist, junto con los detalles relacionados como perforaciones, control horario, aditivos, insumos, longitud de pozo y observaciones.
- Se renderiza una plantilla HTML con los datos del reporte utilizando el contexto proporcionado.
- Se genera un archivo PDF a partir del HTML renderizado usando ``pisa``.
- El archivo PDF se guarda en un subdirectorio específico bajo ``MEDIA_ROOT``.
- Se devuelve una respuesta JSON con la URL del archivo PDF generado.

Retorno
-------

- Si la generación del PDF es exitosa, se retorna una respuesta JSON con la URL del PDF y un mensaje de éxito.
- En caso de error, se devuelve un mensaje de error adecuado.

Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.

new_reporte_digital
====================

Ruta para crear un nuevo reporte digital.

URL
---

- ``/new_reporte_digital``

Vista asociada
--------------

- ``new_reporte_digital``

---

save_reporte_digital
=====================

Ruta para guardar el reporte digital.

URL
---

- ``/save_reporte_digital``

Vista asociada
--------------

- ``save_reporte_digital``

---

obtener-metro-inicial
======================

Ruta para obtener el metro inicial.

URL
---

- ``/obtener-metro-inicial/``

Vista asociada
--------------

- ``obtener_metro_inicial``

---

manage_mis_reportes_digitales
===============================

Ruta para gestionar los reportes digitales del usuario.

URL
---

- ``/manage_mis_reportes_digitales``

Vista asociada
--------------

- ``manage_mis_reportes_digitales``

---

manage_revisar_reportes_digitales
===================================

Ruta para gestionar y revisar los reportes digitales.

URL
---

- ``/manage_revisar_reportes_digitales``

Vista asociada
--------------

- ``manage_revisar_reportes_digitales``

---

manage_todos_reportes_digitales
==================================

Ruta para gestionar todos los reportes digitales.

URL
---

- ``/manage_todos_reportes_digitales``

Vista asociada
--------------

- ``manage_todos_reportes_digitales``

---

progreso_reporte_digital
==========================

Ruta para visualizar el progreso del reporte digital.

URL
---

- ``/progreso_reporte_digital``

Vista asociada
--------------

- ``progreso_reporte_digital``

---

progreso_reporte_digital_corregir
===================================

Ruta para corregir el progreso de un reporte digital.

URL
---

- ``/progreso_reporte_digital_corregir``

Vista asociada
--------------

- ``progreso_reporte_digital_corregir``

---

progreso_reporte_digital_aprobar
===================================

Ruta para aprobar el progreso de un reporte digital.

URL
---

- ``/progreso_reporte_digital_aprobar``

Vista asociada
--------------

- ``progreso_reporte_digital_aprobar``

---

editar_reporte_digital
========================

Ruta para editar un reporte digital.

URL
---

- ``/editar_reporte_digital``

Vista asociada
--------------

- ``editar_reporte_digital``

---

save_editar_reporte_digital
=============================

Ruta para guardar la edición del reporte digital.

URL
---

- ``/save_editar_reporte_digital``

Vista asociada
--------------

- ``save_editar_reporte_digital``

---

obtener-estado-sonda
======================

Ruta para obtener el estado de la sonda.

URL
---

- ``/obtener-estado-sonda/``

Vista asociada
--------------

- ``obtener_estado_sonda``

---

reporte_digital_pdf_view
==========================

Ruta para generar y ver el reporte digital en formato PDF.

URL
---

- ``/reporte_digital_pdf_view``

Vista asociada
--------------

- ``reporte_digital_pdf_view``

