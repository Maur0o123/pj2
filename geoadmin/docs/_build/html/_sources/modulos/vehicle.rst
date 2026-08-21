#######
Vehicle
#######

Descripción General
*******************

El módulo vehicle gestiona la información relacionada con los vehículos, incluyendo sus datos técnicos, documentación asociada, infracciones, y mantenimiento. También permite administrar las características y condiciones de los vehículos de la flota.

.. code-block:: bash   

    vehicle/
    │── admin.py         # Configuración para la interfaz de administración de Django
    │── apps.py          # Configuración de la aplicación dentro del proyecto Django
    │── forms.py         # Formularios para la entrada de datos relacionados con los vehículos
    │── __init__.py      # Marca el directorio como un paquete de Python
    │── migrations/      # Archivos de migración para la base de datos
    │── models.py        # Definición de modelos de datos relacionados con los vehículos
    │── tasks.py         # Tareas para realizar acciones en segundo plano
    │── urls.py          # Configuración de rutas del módulo
    │── views.py         # Lógica para las vistas relacionadas con los vehículos




Modelos de Datos (models.py)
****************************

Este archivo define los modelos de datos que gestionan la información de los vehículos, tales como la información técnica, infracciones, y documentaciones.

Vehiculo
========

Este modelo se utiliza para gestionar la información de los vehículos en el sistema. Incluye datos sobre su adquisición, arriendo, mantenimiento y otros detalles relacionados con el estado del vehículo.

- Campos:
    - ``placaPatente``: (CharField) Placa patente única del vehículo.
    - ``tenencia``: (CharField) Tipo de tenencia del vehículo (arriendo, propiedad, etc.), con opciones definidas en tenencia.
    - ``fechaAdquisicion``: (DateTimeField) Fecha de adquisición del vehículo. Puede ser nula.
    - ``fechaArriendoInicial``: (DateTimeField) Fecha inicial de arriendo del vehículo. Puede ser nula.
    - ``fechaArriendoFinal``: (DateTimeField) Fecha final de arriendo del vehículo. Puede ser nula.
    - ``nombrePropietario``: (CharField) Nombre del propietario del vehículo.
    - ``rutPropietario``: (CharField) RUT del propietario del vehículo.
    - ``domicilio``: (CharField) Dirección del propietario del vehículo.
    - ``tipo``: (ForeignKey) Relacionado con el modelo Tipo, especifica el tipo de vehículo.
    - ``ano``: (ForeignKey) Relacionado con el modelo Ano, especifica el año del vehículo.
    - ``marca``: (ForeignKey) Relacionado con el modelo Marca, especifica la marca del vehículo.
    - ``modelo``: (ForeignKey) Relacionado con el modelo Modelo, especifica el modelo del vehículo.
    - ``numeroMotor``: (CharField) Número de motor del vehículo, único.
    - ``numeroChasis``: (CharField) Número de chasis del vehículo, único.
    - ``numeroVin``: (CharField) Número VIN del vehículo, único.
    - ``color``: (ForeignKey) Relacionado con el modelo Color, especifica el color del vehículo.
    - ``fechaVencimientoPermisoCirculacion``: (DateTimeField) Fecha de vencimiento del permiso de circulación.
    - ``fechaVencimientoRevisionTecnica``: (DateTimeField) Fecha de vencimiento de la revisión técnica.
    - ``fechaVencimientoSeguroObligatorio``: (DateTimeField) Fecha de vencimiento del seguro obligatorio.
    - ``fechaInstalacionGps``: (DateTimeField) Fecha de instalación del GPS, si aplica.
    - ``fechaVencimientoLamina``: (DateTimeField) Fecha de vencimiento de la lámina de seguridad.
    - ``fechaInstalacionBarraAntiVuelco``: (DateTimeField) Fecha de instalación de la barra anti vuelco.
    - ``fechaVencimientoTransportePrivado``: (DateTimeField) Fecha de vencimiento para transporte privado.
    - ``fechaCertificadoOperatividad``: (DateTimeField) Fecha de vencimiento del certificado de operatividad.
    - ``fechaCertificadoMantencion``: (DateTimeField) Fecha de vencimiento del certificado de mantención.
    - ``fechaCertificadoGrua``: (DateTimeField) Fecha de vencimiento del certificado de grúa.
    - ``tieneTag``: (CharField) Indica si el vehículo tiene un TAG asociado, con opciones definidas en opcion.
    - ``status``: (BooleanField) Estado del vehículo.
    - ``completado``: (IntegerField) Porcentaje de completitud del vehículo en relación con los documentos y certificados requeridos.
    - ``fechacreacion``: (DateTimeField) Fecha y hora de creación del registro del vehículo.
- Métodos:
    - ``calcular_completitud_vehiculo(self)``: Calcula el porcentaje de completitud del vehículo según los campos que deben ser completados. Verifica si los campos de información adicional del vehículo (como la instalación de GPS o la vigencia de ciertos certificados) están completos.
    - ``calculate_days_difference(self)``: Calcula la diferencia en días entre la fecha actual y las fechas de vencimiento de varios documentos relacionados con el vehículo, como permisos, revisiones técnicas y seguros.
    - ``__str__(self)``: Devuelve una representación del objeto que incluye la placaPatente del vehículo.
- Metadatos:
    - ``verbose_name``: "Vehiculo".
    - ``verbose_name_plural``: "Vehículos".
    - ``db_table``: 'vehicle_profile'.

InformacionTecnicaVehiculo
==========================

Este modelo almacena los detalles técnicos de un vehículo específico, incluidos aspectos como el tipo de tracción, la capacidad de carga, los tipos de aceites y filtros requeridos, y las frecuencias de mantenimiento.

- Campos:
    - ``vehiculo``: (OneToOneField) Relacionado con el modelo Vehiculo, es una clave primaria que asocia esta información técnica con un vehículo específico.
    - ``tipoTraccion``: (CharField) El tipo de tracción del vehículo (por ejemplo, tracción delantera, trasera, o 4x4).
    - ``pesoBrutoVehicular``: (IntegerField) Peso bruto vehicular en kilogramos.
    - ``capacidadCarga``: (IntegerField) Capacidad de carga máxima del vehículo en kilogramos.
    - ``tipoNeumatico``: (CharField) Tipo de neumático utilizado en el vehículo.
    - ``tipoAceiteMotor``: (CharField) Tipo de aceite recomendado para el motor del vehículo.
    - ``tipoRefrigeranteMotor``: (CharField) Tipo de líquido refrigerante recomendado para el motor.
    - ``tipoFiltroAireMotor``: (CharField) Tipo de filtro de aire utilizado en el motor.
    - ``tipoFiltroCombustible``: (CharField) Tipo de filtro de combustible utilizado en el vehículo.
    - ``frecuenciaMantenimiento``: (IntegerField) La frecuencia de mantenimiento del vehículo, medida en kilómetros.
    - ``proximoMantenimiento``: (IntegerField) Kilómetros hasta el próximo mantenimiento programado.
    - ``proximoMantenimientoGrua``: (IntegerField) Horómetro que indica el próximo mantenimiento relacionado con la grúa.
- Métodos:
    - ``calcular_completitud_informacion_tecnica(self)``: Calcula el porcentaje de completitud de la información técnica del vehículo, verificando si los campos definidos en el modelo están completos o si requieren ser ocultados según el tipo de vehículo configurado. Utiliza el modelo OcultarOpcionesVehiculo para determinar qué campos deben ser visibles para el tipo de vehículo específico.
    - ``__str__(self)``: Devuelve una representación del objeto que incluye la vehiculo asociada (en este caso, el vehículo al que pertenece la información técnica).
- Metadatos:
    - ``verbose_name``: "Información Técnica de Vehiculo".
    - ``verbose_name_plural``: "Información Técnica de Vehiculo".
    - ``db_table``: 'vehicle_information'.

DocumentacionesVehiculo
=======================

Este modelo almacena las imágenes y documentos relacionados con la documentación de un vehículo, incluyendo registros de permisos, revisiones, certificados, fotografías del interior y exterior del vehículo, entre otros.

- Campos:
    - ``vehiculo``: (OneToOneField) Relacionado con el modelo Vehiculo, es una clave primaria que asocia esta documentación con un vehículo específico.
    - ``fotografiaPadron``: (ImageField) Fotografía del padrón vehicular.
    - ``fotografiaPermisoCirculacion``: (ImageField) Fotografía del permiso de circulación del vehículo.
    - ``fotografiaRevisionTecnica``: (ImageField) Fotografía de la revisión técnica del vehículo.
    - ``fotografiaRevisionTecnicaGases``: (ImageField) Fotografía de la revisión técnica de gases del vehículo.
    - ``fotografiaSeguroObligatorio``: (ImageField) Fotografía del seguro obligatorio.
    - ``fotografiaCertificadoGps``: (ImageField) Fotografía del certificado GPS del vehículo.
    - ``fotografiaCertificadoVarios``: (ImageField) Fotografía de certificados varios relacionados con el vehículo.
    - ``fotografiaCertificadoMantencion``: (ImageField) Fotografía del certificado de mantención del vehículo.
    - ``fotografiaCertificadoOperatividad``: (ImageField) Fotografía del certificado de operatividad del vehículo.
    - ``fotografiaCertificadoGrua``: (ImageField) Fotografía del certificado de grúa del vehículo.
    - ``fotografiaFacturaCompra``: (ImageField) Fotografía de la factura de compra del vehículo.
    - ``fotografiaSeguroAutomotriz``: (ImageField) Fotografía del seguro automotriz.
    - ``fotografiaCertificadoLamina``: (ImageField) Fotografía del certificado de lámina del vehículo.
    - ``fotografiaDocumentacionMiniBus``: (ImageField) Fotografía de la documentación relacionada con transporte privado (minibús).
    - ``fotografiaCertificadoBarraAntiVuelco``: (ImageField) Fotografía del certificado de barra anti-vuelco del vehículo.
    - ``fotografiaInteriorTablero``: (ImageField) Fotografía del interior del tablero del vehículo.
    - ``fotografiaInteriorCopiloto``: (ImageField) Fotografía del interior acompañante del vehículo.
    - ``fotografiaInteriorAtrasPiloto``: (ImageField) Fotografía del interior trasero, lado conductor.
    - ``fotografiaInteriorAtrasCopiloto``: (ImageField) Fotografía del interior trasero, lado copiloto.
    - ``fotografiaExteriorFrontis``: (ImageField) Fotografía del exterior del vehículo, frente.
    - ``fotografiaExteriorAtras``: (ImageField) Fotografía del exterior del vehículo, atrás.
    - ``fotografiaExteriorPiloto``: (ImageField) Fotografía del exterior, lado conductor.
    - ``fotografiaExteriorCopiloto``: (ImageField) Fotografía del exterior, lado copiloto.
- Métodos:
    - ``generaNombre(instance, filename)``: Genera un nombre de archivo único para las imágenes subidas, basándose en la placa patente del vehículo y la fecha actual. La ruta de la imagen se organiza por la placa patente y la fecha de subida.
    - ``calcular_completitud_documentaciones(self)``: Calcula el porcentaje de completitud de las documentaciones del vehículo, verificando si los campos de imágenes/documentos están completos o si deben ser ocultados según la configuración del tipo de vehículo. Utiliza el modelo OcultarOpcionesVehiculo para determinar qué campos deben ser visibles para el tipo de vehículo específico.
    - ``__str__(self)``: Devuelve una representación del objeto que incluye la vehiculo asociada (en este caso, el vehículo al que pertenece la documentación).
    - Metadatos:
    - ``verbose_name``: "Documentación Vehiculo".
    - ``verbose_name_plural``: "Documentación Vehículos".
    - ``db_table``: 'vehicle_documentation'.

Signal: create_documentacion_vehiculo
=====================================

Esta es una señal que se activa después de que un nuevo Vehiculo se guarda en la base de datos, y su propósito es crear automáticamente una instancia de DocumentacionesVehiculo asociada al vehículo recién creado.

- Funcionamiento:
    - ``@receiver(post_save, sender=Vehiculo)``: La señal se dispara cuando se guarda una nueva instancia del modelo Vehiculo en la base de datos. El decorador @receiver registra la función create_documentacion_vehiculo para que se ejecute después de que un objeto Vehiculo sea guardado exitosamente (evento post_save).
    - ``def create_documentacion_vehiculo(sender, instance, created, **kwargs)``: Esta función es ejecutada después de guardar el Vehiculo y su tarea es crear una nueva entrada en el modelo DocumentacionesVehiculo, asociada al vehículo que ha sido guardado.

        - ``sender``: El modelo que está generando la señal, en este caso, Vehiculo.
        - ``instance``: Es la instancia del Vehiculo que se acaba de guardar en la base de datos.
        - ``created``: Un valor booleano que indica si la instancia de Vehiculo fue creada (es True si se trata de una nueva entrada).
        - ``**kwargs``: Otros parámetros adicionales que podrían ser enviados, aunque no se están utilizando en esta función.
    - ``DocumentacionesVehiculo.objects.create(vehiculo=instance)``: Crea una nueva instancia del modelo DocumentacionesVehiculo y la asocia con el vehículo recién guardado (instance). Esto asegura que cada vehículo tenga una entrada de documentación inicial cuando se crea un nuevo vehículo en la base de datos.

create_informacion_vehiculo
===========================

Esta es una señal que activa post_save de Django para ejecutar una acción automáticamente después de que se guarda un objeto del modelo Vehiculo. En este caso, se crea un objeto relacionado en el modelo InformacionTecnicaVehiculo cada vez que se guarda un nuevo vehículo.

- Funcionamiento:
    - ``@receiver(post_save, sender=Vehiculo)``: Esta es la declaración de la señal post_save que se activa después de guardar una instancia del modelo Vehiculo. El sender especifica que la señal se activará cuando se guarde un objeto de tipo Vehiculo.
    - ``create_informacion_vehiculo(sender, instance, created, **kwargs)``: La función create_informacion_vehiculo se ejecuta cuando la señal se dispara.
        - ``sender``: El modelo que ha disparado la señal (en este caso, Vehiculo).
        - ``instance``: La instancia del objeto Vehiculo que se acaba de guardar.
        - ``created``: Un valor booleano que indica si la instancia fue recién creada (True) o si fue actualizada (False).
        - ``**kwargs``: Permite capturar otros parámetros adicionales.
    - ``InformacionTecnicaVehiculo.objects.create(vehiculo=instance)``: Después de guardar el objeto Vehiculo, se crea una nueva instancia del modelo InformacionTecnicaVehiculo, asociándola con el vehículo recién guardado.
    - Esto crea una relación de uno a uno entre el Vehiculo y la InformacionTecnicaVehiculo, asegurando que cada vehículo tenga su correspondiente información técnica al ser guardado.

InfraccionesVehiculo
====================

Este modelo almacena las infracciones o multas asociadas a un vehículo, con detalles como la fecha, descripción de la infracción, lugar, estado de pago y el valor de la multa.

- Campos:
    - ``vehiculo``: (ForeignKey) Relacionado con el modelo Vehiculo, es una clave foránea que asocia una infracción a un vehículo específico.
    - ``fechaInfraccion``: (DateTimeField) Fecha en que ocurrió la infracción.
    - ``infraccion``: (CharField) Descripción o detalle de la infracción cometida.
    - ``ciudadInfraccion``: (CharField) Ciudad o lugar donde se cometió la infracción.
    - ``estadoPagoInfraccion``: (CharField) Estado del pago de la infracción (por ejemplo, si está pagada o pendiente).
    - ``valorInfraccion``: (IntegerField) El valor monetario de la infracción.
- Métodos:
    - ``__str__(self)``: Devuelve una representación del objeto que incluye la vehiculo asociada (en este caso, el vehículo al que pertenece la infracción).
- Metadatos:
    - ``verbose_name``: "Información Infracción y Multas".
    - ``verbose_name_plural``: "Información Infracciones y Multas".
    - ``db_table``: 'vehicle_penalty'.

NuevoKilometraje
================

Este modelo registra el kilometraje actual de un vehículo, junto con otros detalles relacionados como la fecha de creación y el origen del registro.

- Campos:
    - ``vehiculo``: (ForeignKey) Relacionado con el modelo Vehiculo, es una clave foránea que asocia el registro del kilometraje a un vehículo específico.
    - ``kilometraje``: (IntegerField) Almacena el kilometraje actual del vehículo en el momento del registro.
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se registró el kilometraje. Se establece con el valor por defecto de la fecha y hora actual (timezone.now).
    - ``creador``: (CharField) Nombre o identificador del usuario que crea el registro del kilometraje.
    - ``origen``: (CharField) Un campo opcional para especificar el origen del registro (por ejemplo, si se registra manualmente, por GPS, etc.).
- Métodos:
    - ``__str__(self)``: Devuelve una representación del objeto que incluye la vehiculo asociada, facilitando la identificación del registro de kilometraje relacionado.
- Metadatos:
    - ``verbose_name``: "Kilometraje Vehicular".
    - ``verbose_name_plural``: "Kilometrajes Vehiculares".
    - ``db_table``: 'vehicle_kilometres_registers'.

Formularios (forms.py)
----------------------

Los formularios permiten que los usuarios creen o editen la información de los vehículos.

FormNuevoVehiculo
==================

Este formulario permite registrar un nuevo vehículo en el sistema, basándose en el modelo ``Vehiculo``.

Campos del Formulario
----------------------

1. ``placaPatente``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Placa patente del vehículo.

2. ``rutPropietario``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: RUT del propietario del vehículo.

3. ``tenencia``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Indica si el vehículo tiene tenencia.

4. ``fechaAdquisicion``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de adquisición del vehículo.

5. ``fechaArriendoInicial``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de inicio de arriendo del vehículo.

6. ``fechaArriendoFinal``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de fin de arriendo del vehículo.

7. ``nombrePropietario``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Nombre del propietario del vehículo.

8. ``domicilio``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Dirección del propietario.

9. ``tipo``  
    - Tipo: ForeignKey  
    - Requerido: Sí  
    - Descripción: Tipo de vehículo (por ejemplo, automóvil, camión).

10. ``marca``  
    - Tipo: ForeignKey  
    - Requerido: Sí  
    - Descripción: Marca del vehículo.

11. ``modelo``  
    - Tipo: ForeignKey  
    - Requerido: Sí  
    - Descripción: Modelo del vehículo.

12. ``ano``  
    - Tipo: ForeignKey  
    - Requerido: Sí  
    - Descripción: Año de fabricación del vehículo.

13. ``numeroMotor``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Número de motor del vehículo.

14. ``numeroChasis``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Número de chasis del vehículo.

15. ``numeroVin``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Número de VIN (número de identificación del vehículo).

16. ``color``  
    - Tipo: ForeignKey  
    - Requerido: Sí  
    - Descripción: Color del vehículo.

17. ``fechaVencimientoPermisoCirculacion``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de vencimiento del permiso de circulación.

18. ``fechaVencimientoRevisionTecnica``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de vencimiento de la revisión técnica.

19. ``fechaVencimientoSeguroObligatorio``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de vencimiento del seguro obligatorio.

20. ``fechaVencimientoLamina``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de vencimiento de la lámina de seguridad.

21. ``fechaInstalacionBarraAntiVuelco``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de instalación de la barra antivuelco.

22. ``fechaInstalacionGps``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de instalación del GPS en el vehículo.

23. ``fechaVencimientoTransportePrivado``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de vencimiento del transporte privado.

24. ``fechaCertificadoOperatividad``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de vencimiento del certificado de operatividad.

25. ``fechaCertificadoMantencion``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de vencimiento del certificado de mantención.

26. ``fechaCertificadoGrua``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha de vencimiento del certificado de grúa.

27. ``tieneTag``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Indica si el vehículo tiene un TAG.

Consideraciones Adicionales
---------------------------

- Se ocultan campos dependiendo de la configuración proporcionada al inicializar el formulario.
- Los campos relacionados con las fechas son opcionales y su visibilidad puede ser ajustada dinámicamente.
- La ``placaPatente`` y otros identificadores tienen restricciones de unicidad para evitar duplicados.

FormInformacionTecnica
========================

Este formulario permite registrar la información técnica de un vehículo, basándose en el modelo ``InformacionTecnicaVehiculo``.

Campos del Formulario
----------------------

1. ``tipoTraccion``  
    - Tipo: CharField  
    - Requerido: No  
    - Descripción: Tipo de tracción del vehículo (delantera, trasera, etc.).

2. ``pesoBrutoVehicular``  
    - Tipo: DecimalField  
    - Requerido: No  
    - Descripción: Peso bruto vehicular del vehículo.

3. ``capacidadCarga``  
    - Tipo: DecimalField  
    - Requerido: No  
    - Descripción: Capacidad de carga del vehículo.

4. ``tipoNeumatico``  
    - Tipo: CharField  
    - Requerido: No  
    - Descripción: Tipo de neumático utilizado en el vehículo.

5. ``tipoAceiteMotor``  
    - Tipo: CharField  
    - Requerido: No  
    - Descripción: Tipo de aceite utilizado en el motor del vehículo.

6. ``tipoRefrigeranteMotor``  
    - Tipo: CharField  
    - Requerido: No  
    - Descripción: Tipo de refrigerante utilizado en el motor.

7. ``tipoFiltroAireMotor``  
    - Tipo: CharField  
    - Requerido: No  
    - Descripción: Tipo de filtro de aire utilizado en el motor.

8. ``tipoFiltroCombustible``  
    - Tipo: CharField  
    - Requerido: No  
    - Descripción: Tipo de filtro de combustible utilizado en el vehículo.

9. ``frecuenciaMantenimiento``  
    - Tipo: DecimalField  
    - Requerido: No  
    - Descripción: Frecuencia del mantenimiento recomendado para el vehículo.

10. ``proximoMantenimiento``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha del próximo mantenimiento del vehículo.

11. ``proximoMantenimientoGrua``  
    - Tipo: DateField  
    - Requerido: No  
    - Descripción: Fecha del próximo mantenimiento de grúa del vehículo.

Consideraciones Adicionales
---------------------------

- Todos los campos relacionados con la información técnica del vehículo son opcionales.
- Los campos de tipo ``TextInput`` están configurados para aceptar entradas específicas, como números o texto, según corresponda.
  
FormDocumentacionVehiculo
==========================

Este formulario permite registrar la documentación relacionada con un vehículo, basándose en el modelo ``DocumentacionesVehiculo``.

Campos del Formulario
----------------------

1. ``fotografiaPadron``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del padrón del vehículo.

2. ``fotografiaPermisoCirculacion``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del permiso de circulación del vehículo.

3. ``fotografiaRevisionTecnica``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía de la revisión técnica del vehículo.

4. ``fotografiaRevisionTecnicaGases``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía de la revisión técnica de gases del vehículo.

5. ``fotografiaSeguroObligatorio``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del seguro obligatorio del vehículo.

6. ``fotografiaCertificadoGps``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del certificado de GPS del vehículo.

7. ``fotografiaCertificadoOperatividad``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del certificado de operatividad del vehículo.

8. ``fotografiaCertificadoMantencion``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del certificado de mantención del vehículo.

9. ``fotografiaCertificadoGrua``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del certificado de grúa del vehículo.

10. ``fotografiaCertificadoVarios``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía de otros certificados varios relacionados con el vehículo.

Consideraciones Adicionales
---------------------------

- Todos los campos son obligatorios, ya que cada uno representa un documento importante para el registro completo del vehículo.
  
FormDocumentacionVehiculoExterior
==================================

Este formulario permite registrar las fotografías del vehículo, específicamente las vistas exteriores, basándose en el modelo ``DocumentacionesVehiculo``.

Campos del Formulario
----------------------

1. ``fotografiaExteriorFrontis``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del frontis del vehículo (vista frontal).

2. ``fotografiaExteriorAtras``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía de la parte trasera del vehículo (vista posterior).

3. ``fotografiaExteriorPiloto``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del lado del piloto (vista lateral izquierda).

4. ``fotografiaExteriorCopiloto``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del lado del copiloto (vista lateral derecha).

Consideraciones Adicionales
---------------------------

- Todos los campos son obligatorios, ya que cada uno representa una vista clave para la evaluación y documentación visual del vehículo.
  
FormDocumentacionVehiculointerior
==================================

Este formulario permite registrar las fotografías del vehículo, específicamente las vistas interiores, basándose en el modelo ``DocumentacionesVehiculo``.

Campos del Formulario
----------------------

1. ``fotografiaInteriorTablero``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del tablero de instrumentos del vehículo.

2. ``fotografiaInteriorCopiloto``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del lado del copiloto (asiento y área frontal).

3. ``fotografiaInteriorAtrasPiloto``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del área trasera detrás del asiento del piloto.

4. ``fotografiaInteriorAtrasCopiloto``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del área trasera detrás del asiento del copiloto.

Consideraciones Adicionales
---------------------------

- Todos los campos son obligatorios, ya que cada uno representa una vista clave para la evaluación y documentación visual del vehículo en su interior.
  
FormInfraccionesVehiculo
==========================

Este formulario permite registrar las infracciones asociadas a un vehículo, basándose en el modelo ``InfraccionesVehiculo``.

Campos del Formulario
----------------------

1. ``infraccion``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Descripción de la infracción cometida.  
    - Widget: Textarea con clases personalizadas de estilo.

2. ``fechaInfraccion``  
    - Tipo: DateField  
    - Requerido: Sí  
    - Descripción: Fecha en que se cometió la infracción.  
    - Widget: DateTimeInput con formato de fecha (tipo ``date``).

3. ``ciudadInfraccion``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Ciudad donde ocurrió la infracción.

4. ``estadoPagoInfraccion``  
    - Tipo: CharField  
    - Requerido: Sí  
    - Descripción: Estado de pago de la infracción (ej. pagada, pendiente).

5. ``valorInfraccion``  
    - Tipo: DecimalField  
    - Requerido: Sí  
    - Descripción: Valor monetario asociado a la infracción.  
    - Widget: TextInput con validación de valores numéricos.

Consideraciones Adicionales
---------------------------

- El campo ``fechaInfraccion`` tiene un rango mínimo desde el año 1920.
- El campo ``valorInfraccion`` está restringido a un máximo de 10 caracteres y un valor mínimo de 0.
  
FormNuevoKilometraje
====================

Este formulario se utiliza para registrar un nuevo kilometraje de un vehículo, basándose en el modelo ``NuevoKilometraje``.

Campos del Formulario
----------------------

1. ``vehiculo``  
    - Tipo: ForeignKey (Relación con el modelo ``Vehiculo``)  
    - Requerido: Sí  
    - Descripción: Vehículo al que se le está registrando el kilometraje.  
    - Widget: Select con un estilo personalizado centrado.  

2. ``kilometraje``  
    - Tipo: IntegerField  
    - Requerido: Sí  
    - Descripción: Kilometraje registrado para el vehículo.  
    - Widget: TextInput con validación numérica y clases personalizadas.

Consideraciones Adicionales
---------------------------

- El campo ``vehiculo`` se filtra según los vehículos proporcionados en el parámetro ``vehiculos`` al inicializar el formulario.
- El campo ``kilometraje`` acepta solo números.


Vistas (views.py)
*****************

Las vistas contienen la lógica para manejar las interacciones relacionadas con los vehículos, como la visualización y edición de su información.

new_vehicle
===========

Vista para crear un nuevo vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud para crear un nuevo vehículo.

Requisitos
----------

- La vista está protegida por el decorador ``@login_required``, lo que significa que solo los usuarios autenticados pueden acceder a esta vista.
- El formulario ``FormNuevoVehiculo`` se utiliza para crear un nuevo vehículo.

Funcionamiento
--------------

- La función muestra un formulario para crear un nuevo vehículo.
- La vista incluye un contexto que contiene el formulario ``FormNuevoVehiculo`` y los elementos relacionados con la barra lateral para la gestión de vehículos.
- La vista se renderiza utilizando la plantilla ``pages/vehicle/new_vehicle.html``.

Retorno
-------

- Retorna la vista renderizada con el formulario para crear un nuevo vehículo y los elementos de la barra lateral.

---

manage_vehicles
================

Vista para gestionar los vehículos asignados.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud para ver y gestionar vehículos.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_or_jefe_mantencion_or_supervisor_required``, lo que significa que solo los usuarios autenticados con roles de administrador, jefe de mantención o supervisor pueden acceder a esta vista.
  
Funcionamiento
--------------

- Se obtiene el perfil del usuario actual mediante ``UsuarioProfile``.
- Si el usuario tiene asignada una faena específica, los vehículos que se mostrarán estarán filtrados por esa faena.
- Si la faena del usuario es "SIN ASIGNAR", se muestran todos los vehículos asignados con el estado ``True``, ordenados por la fecha de creación.
- Además, se obtiene una lista de vehículos completados, que se muestra en la interfaz.
- La vista incluye un contexto con los vehículos asignados y completados, así como los elementos relacionados con la barra lateral para la gestión de vehículos.

Retorno
-------

- Retorna la vista renderizada con los vehículos asignados y completados y los elementos de la barra lateral para la gestión de vehículos.

save_new_vehicle
=================

Vista para guardar un nuevo vehículo en la base de datos.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud para guardar un nuevo vehículo.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_required``, lo que significa que solo los usuarios autenticados con privilegios de administrador pueden acceder a esta vista.
- El formulario ``FormNuevoVehiculo`` es utilizado para la validación y captura de los datos del nuevo vehículo.

Funcionamiento
--------------

- La función comienza validando y obteniendo las instancias de los modelos ``Tipo``, ``Ano``, ``Marca``, ``Modelo``, y ``Color`` con base en los valores enviados en el formulario.
- Se valida si el campo ``rutPropietario`` corresponde a un RUT chileno válido utilizando ``rut_chile.is_valid_rut()``.
- Si el formulario es válido, se crea una nueva instancia del modelo ``Vehiculo`` con los datos proporcionados en el formulario, y se guarda en la base de datos.
- Luego, se asigna el vehículo creado a una faena con el estado "SIN ASIGNAR" en el modelo ``VehiculoAsignado``.
- Se envía una notificación por correo electrónico sobre el vehículo creado.
- Si el formulario no es válido o el RUT no es correcto, se devuelve un mensaje de error y se vuelve a mostrar el formulario.

Retorno
-------

- Si el formulario es válido, se redirige a la vista ``manage_vehicles`` después de guardar el vehículo correctamente.
- Si el formulario no es válido o el RUT es incorrecto, se vuelve a renderizar el formulario con mensajes de error.

---

status_vehicle
===============

Vista para cambiar el estado de un vehículo (habilitar/deshabilitar).

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud para cambiar el estado de un vehículo.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_required``, lo que significa que solo los usuarios autenticados con privilegios de administrador pueden acceder a esta vista.

Funcionamiento
--------------

- La función obtiene el vehículo basado en la placa patente proporcionada en la solicitud.
- Verifica si el vehículo está habilitado o deshabilitado.
- Si el vehículo está habilitado y no está asignado a ninguna faena, el estado del vehículo se cambia a deshabilitado (``status=False``) y se envía una notificación por correo electrónico.
- Si el vehículo está asignado a una faena, se muestra un mensaje de error indicando que debe desasignarse primero de la faena.
- Si el vehículo está deshabilitado, se cambia su estado a habilitado (``status=True``) y se envía una notificación por correo electrónico.

Retorno
-------

- Después de cambiar el estado del vehículo, se redirige a la vista ``manage_vehicles`` con un mensaje indicando si el cambio fue exitoso o si hubo algún problema.

edit_vehicle_profile
=====================

Vista para editar el perfil de un vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud para editar el perfil de un vehículo.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_or_jefe_mantencion_or_supervisor_required``, lo que significa que solo los usuarios autenticados con los roles de administrador, jefe de mantención o supervisor pueden acceder a esta vista.

Funcionamiento
--------------

- Se maneja el proceso de edición del perfil de un vehículo.
- La función intenta obtener el valor de ``placaPatente`` desde la solicitud POST, o si no está presente, se usa el valor almacenado en la sesión.
- Con el valor de ``placaPatente``, se obtienen los datos del vehículo correspondiente, sus documentos y otra información relevante como infracciones, solicitudes de mantenimiento, y los detalles técnicos del vehículo.
- Si existen fotografías asociadas al vehículo, se recuperan las URL de estas imágenes y sus extensiones.
- Se formatean las fechas para mostrarlas correctamente en el formulario de edición.
- El contexto para la plantilla incluye todos los datos del vehículo, las infracciones, las solicitudes de mantenimiento y los formularios para editar el vehículo y la información técnica.
  
Retorno
-------

- Retorna la vista renderizada con los detalles del vehículo y los formularios necesarios para su edición.

save_edit_vehicle_profile
==========================

Vista para guardar la edición del perfil de un vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de edición y actualización de los datos del perfil de un vehículo.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_or_jefe_mantencion_or_supervisor_required``, lo que significa que solo los usuarios autenticados con roles de administrador, jefe de mantención o supervisor pueden acceder a esta vista.
- La función también valida el RUT del propietario del vehículo para asegurar que sea correcto.

Funcionamiento
--------------

1. La función primero valida los campos del formulario para asegurarse de que no estén vacíos utilizando la función ``validar_campo_vacio``.
2. Valida el RUT del propietario con la función ``rut_chile.is_valid_rut``. Si el RUT no es válido, se muestra un mensaje de error y se vuelve a mostrar el formulario de edición.
3. Si el RUT es válido, se actualizan los campos del vehículo (como fecha de adquisición, marca, modelo, etc.) en el modelo ``Vehiculo``.
4. Los campos de la ``InformacionTecnicaVehiculo`` también se actualizan, como peso bruto vehicular, capacidad de carga, tipo de neumáticos, etc.
5. La documentación del vehículo (como certificados y permisos) se actualiza mediante las imágenes proporcionadas en el formulario utilizando la función ``procesar_fotografia``.
6. La función calcula el porcentaje de completitud del perfil del vehículo considerando los campos completados en los modelos ``Vehiculo``, ``InformacionTecnicaVehiculo`` y ``DocumentacionesVehiculo``.
7. Se envía una notificación por correo electrónico sobre la actualización del vehículo.
8. Finalmente, se muestra un mensaje de éxito y se redirige a la vista de gestión de vehículos.

Retorno
-------

- Si el RUT es válido y la actualización es exitosa, se redirige a la vista ``manage_vehicles`` y se muestra un mensaje de éxito.
- Si el RUT es incorrecto, se muestra un mensaje de error y se vuelve a renderizar el formulario de edición.

hide_options_vehicle
=====================

Vista para ocultar opciones de un vehículo basadas en su tipo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener los datos enviados en la solicitud POST, como el tipo de vehículo, para devolver las opciones correspondientes.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_or_jefe_mantencion_or_supervisor_required``, lo que significa que solo los usuarios autenticados con roles de administrador, jefe de mantención o supervisor pueden acceder a esta vista.

Funcionamiento
--------------

1. La función recibe una solicitud POST, donde se envía el tipo de vehículo mediante el campo ``tipo_vehiculo``.
2. Se busca el objeto ``OcultarOpcionesVehiculo`` correspondiente al tipo de vehículo proporcionado en la solicitud.
3. Si se encuentra el objeto, se serializa a un formato Python utilizando el serializador de Django para devolverlo en un formato adecuado.
4. Se crea un diccionario ``data`` que contiene las opciones del vehículo serializadas.
5. Finalmente, se devuelve una respuesta JSON con las opciones del vehículo.

Retorno
-------

- Si la solicitud es exitosa, se devuelve un ``JsonResponse`` con las opciones del vehículo basadas en el tipo proporcionado.
- Si la solicitud no es válida (por ejemplo, si no se recibe una solicitud POST), se devuelve un ``JsonResponse`` con un mensaje de error y un código de estado 400 (solicitud no válida).

save_penalty
=============

Vista para guardar una nueva infracción (multa) asociada a un vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener los datos enviados en la solicitud POST, como los detalles de la infracción (placa, fecha, ciudad, etc.).

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_required``, lo que significa que solo los usuarios autenticados con rol de administrador pueden acceder a esta vista.

Funcionamiento
--------------

1. La función recibe una solicitud POST con los detalles de la infracción: placa del vehículo, fecha, ciudad, infracción, estado de pago y valor de la infracción.
2. Se busca el vehículo correspondiente a la patente proporcionada en la solicitud.
3. Se crea una nueva instancia de ``InfraccionesVehiculo`` y se guarda en la base de datos.
4. Se devuelve una respuesta JSON con un mensaje de éxito si la multa se crea correctamente.

Retorno
-------

- Si la solicitud es exitosa, se devuelve un ``JsonResponse`` con un mensaje indicando que la multa fue creada correctamente.
- Si la solicitud no es válida, se devuelve un ``JsonResponse`` con un mensaje de error y un código de estado 400 (solicitud no válida).
  
---

new_kilometraje_register
=========================

Vista para mostrar el formulario de registro de un nuevo kilometraje para un vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener los datos del usuario autenticado y determinar los vehículos disponibles según su faena.

Requisitos
----------

- La vista está protegida por el decorador ``@login_required``, lo que significa que solo los usuarios autenticados pueden acceder a esta vista.

Funcionamiento
--------------

1. Se obtiene el perfil del usuario autenticado.
2. Dependiendo de la faena del usuario, se obtienen los vehículos disponibles:
   - Si el usuario no tiene faena asignada, se muestran todos los vehículos activos, excluyendo los de tipo 7.
   - Si el usuario tiene una faena asignada, se muestran solo los vehículos asignados a esa faena.
3. Se prepara el contexto con el formulario ``FormNuevoKilometraje`` y los vehículos disponibles.
4. La vista renderiza el formulario para que el usuario ingrese un nuevo kilometraje.

Retorno
-------

- Devuelve un ``HttpResponse`` con el formulario de kilometraje para el vehículo seleccionado.

---

save_new_kilometraje_register
==============================

Vista para guardar un nuevo registro de kilometraje de un vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener los datos enviados en la solicitud POST, como el vehículo y el kilometraje.

Requisitos
----------

- La vista está protegida por el decorador ``@login_required``, lo que significa que solo los usuarios autenticados pueden acceder a esta vista.

Funcionamiento
--------------

1. La función recibe una solicitud POST con los datos del vehículo y el kilometraje.
2. Se obtiene el vehículo correspondiente al ID proporcionado en la solicitud.
3. Se crea un nuevo registro de kilometraje asociado al vehículo.
4. El nuevo kilometraje se guarda en la base de datos.
5. Se devuelve una respuesta JSON con un mensaje de éxito si el registro se guarda correctamente.

Retorno
-------

- Si la solicitud es exitosa, se devuelve un ``JsonResponse`` con un mensaje indicando que el kilometraje fue registrado correctamente.
- Si la solicitud no es válida (por ejemplo, si no es POST), se redirige a la vista para registrar un nuevo kilometraje.

---

vehicle_pdf_view
=================

Vista para generar un PDF con la documentación y la información técnica de un vehículo.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener los datos enviados en la solicitud POST, como la patente del vehículo.

Requisitos
----------

- La vista está protegida por el decorador ``@login_required``, lo que significa que solo los usuarios autenticados pueden acceder a esta vista.

Funcionamiento
--------------

1. La función recibe una solicitud POST con la patente del vehículo.
2. Se obtiene el vehículo correspondiente a la patente proporcionada.
3. Se buscan las opciones de visibilidad de la documentación del vehículo (por ejemplo, si las imágenes de la documentación deben ser incluidas en el PDF).
4. Para cada documento relevante del vehículo, se verifica si debe incluirse en el PDF. Si es así, se obtiene el archivo de imagen correspondiente.
5. Se crea el contexto necesario para generar el PDF, incluyendo información del vehículo, su documentación, la información técnica y las imágenes.
6. Se utiliza la biblioteca ``pisa`` para generar el PDF a partir de una plantilla HTML.
7. El PDF generado se guarda en el servidor y se devuelve la URL de acceso al archivo PDF en formato JSON.

Retorno
-------

- Si el PDF se genera correctamente, se devuelve un ``JsonResponse`` con la URL del archivo PDF y un mensaje de éxito.
- Si ocurre un error al generar el PDF, se devuelve un ``JsonResponse`` con un mensaje de error.
- Si la solicitud no es válida (por ejemplo, si no es POST), se redirige a la vista de gestión de vehículos.

report_vehicles_kilometrajes
=============================

Vista para mostrar el reporte de kilometrajes de vehículos.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para manejar la solicitud de la vista y preparar el contexto para renderizar la plantilla correspondiente.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_required``, lo que significa que solo los usuarios autenticados con rol de administrador pueden acceder a esta vista.

Funcionamiento
--------------

1. Se crea un diccionario de contexto que incluye los parámetros necesarios para renderizar la vista.
2. Se renderiza la plantilla ``report_vehicles_kilometrajes.html`` con el contexto generado.

Retorno
-------

- Devuelve un ``HttpResponse`` con la plantilla de reporte de kilometrajes de vehículos.

---

report_vehicles_general
========================

Vista para mostrar el reporte general de vehículos.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para manejar la solicitud de la vista y preparar el contexto para renderizar la plantilla correspondiente.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_required``, lo que significa que solo los usuarios autenticados con rol de administrador pueden acceder a esta vista.

Funcionamiento
--------------

1. Se crea un diccionario de contexto que incluye los parámetros necesarios para renderizar la vista.
2. Se renderiza la plantilla ``report_vehicles_general.html`` con el contexto generado.

Retorno
-------

- Devuelve un ``HttpResponse`` con la plantilla de reporte general de vehículos.

---

report_vehicles_faenas
=======================

Vista para mostrar el reporte de vehículos por faenas.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para manejar la solicitud de la vista y preparar el contexto para renderizar la plantilla correspondiente.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_required``, lo que significa que solo los usuarios autenticados con rol de administrador pueden acceder a esta vista.

Funcionamiento
--------------

1. Se crea un diccionario de contexto que incluye los parámetros necesarios para renderizar la vista.
2. Se renderiza la plantilla ``report_vehicles_faenas.html`` con el contexto generado.

Retorno
-------

- Devuelve un ``HttpResponse`` con la plantilla de reporte de vehículos por faenas.

---

report_vehicles_camionetas_ano
===============================

Vista para mostrar el reporte de camionetas por año.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para manejar la solicitud de la vista y preparar el contexto para renderizar la plantilla correspondiente.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_required``, lo que significa que solo los usuarios autenticados con rol de administrador pueden acceder a esta vista.

Funcionamiento
--------------

1. Se crea un diccionario de contexto que incluye los parámetros necesarios para renderizar la vista.
2. Se renderiza la plantilla ``report_vehicles_camionetas_ano.html`` con el contexto generado.

Retorno
-------

- Devuelve un ``HttpResponse`` con la plantilla de reporte de camionetas por año.

---

report_vehicles_camionetas_faenas
==================================

Vista para mostrar el reporte de camionetas por faena.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para manejar la solicitud de la vista y preparar el contexto para renderizar la plantilla correspondiente.

Requisitos
----------

- La vista está protegida por los decoradores ``@login_required`` y ``@admin_required``, lo que significa que solo los usuarios autenticados con rol de administrador pueden acceder a esta vista.

Funcionamiento
--------------

1. Se crea un diccionario de contexto que incluye los parámetros necesarios para renderizar la vista.
2. Se renderiza la plantilla ``report_vehicles_camionetas_faenas.html`` con el contexto generado.

Retorno
-------

- Devuelve un ``HttpResponse`` con la plantilla de reporte de camionetas por faena.


Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.

new_vehicle
============

Ruta para crear un nuevo vehículo.

URL
---

- ``/new_vehicle``

Vista asociada
--------------

- ``new_vehicle``

---

manage_vehicles
================

Ruta para gestionar vehículos.

URL
---

- ``/manage_vehicles``

Vista asociada
--------------

- ``manage_vehicles``

---

save_new_vehicle
=================

Ruta para guardar un nuevo vehículo.

URL
---

- ``/save_new_vehicle``

Vista asociada
--------------

- ``save_new_vehicle``

---

status_vehicle
===============

Ruta para ver el estado de un vehículo.

URL
---

- ``/status_vehicle``

Vista asociada
--------------

- ``status_vehicle``

---

edit_vehicle_profile
=====================

Ruta para editar el perfil de un vehículo.

URL
---

- ``/edit_vehicle_profile``

Vista asociada
--------------

- ``edit_vehicle_profile``

---

save_edit_vehicle_profile
===========================

Ruta para guardar los cambios en el perfil de un vehículo.

URL
---

- ``/save_edit_vehicle_profile``

Vista asociada
--------------

- ``save_edit_vehicle_profile``

---

hide_options_vehicle
======================

Ruta para ocultar opciones de un vehículo.

URL
---

- ``/hide_options_vehicle``

Vista asociada
--------------

- ``hide_options_vehicle``

---

save_penalty
=============

Ruta para guardar una penalización de un vehículo.

URL
---

- ``/save_penalty``

Vista asociada
--------------

- ``save_penalty``

---

new_kilometraje_register
==========================

Ruta para registrar un nuevo kilometraje.

URL
---

- ``/new_kilometraje_register``

Vista asociada
--------------

- ``new_kilometraje_register``

---

save_new_kilometraje_register
===============================

Ruta para guardar un nuevo registro de kilometraje.

URL
---

- ``/save_new_kilometraje_register``

Vista asociada
--------------

- ``save_new_kilometraje_register``

---

vehicle_pdf_view
=================

Ruta para ver el PDF de un vehículo.

URL
---

- ``/vehicle_pdf_view``

Vista asociada
--------------

- ``vehicle_pdf_view``

---

report_vehicles_kilometrajes
==============================

Ruta para ver el reporte de kilometrajes de vehículos.

URL
---

- ``/report_vehicles_kilometrajes``

Vista asociada
--------------

- ``report_vehicles_kilometrajes``

---

report_vehicles_general
========================

Ruta para ver el reporte general de vehículos.

URL
---

- ``/report_vehicles_general``

Vista asociada
--------------

- ``report_vehicles_general``

---

report_vehicles_camionetas_faenas
===================================

Ruta para ver el reporte de camionetas por faenas.

URL
---

- ``/report_vehicles_camionetas_faenas``

Vista asociada
--------------

- ``report_vehicles_camionetas_faenas``

---

report_vehicles_camionetas_ano
===============================

Ruta para ver el reporte de camionetas por año.

URL
---

- ``/report_vehicles_camionetas_ano``

Vista asociada
--------------

- ``report_vehicles_camionetas_ano``

---

report_vehicles_faenas
=======================

Ruta para ver el reporte de vehículos por faenas.

URL
---

- ``/report_vehicles_faenas``

Vista asociada
--------------

- ``report_vehicles_faenas``

Tareas (tasks.py)
*****************

Las tareas permiten realizar acciones en segundo plano, como enviar recordatorios de mantenimiento o actualizar el estado del vehículo.

create_vehicle_pdf
==================

Genera un archivo PDF para un vehículo, utilizando las opciones de ocultar documentación
y la información del vehículo disponible en la base de datos. La tarea se ejecuta de manera
sincrónica en el hilo actual y puede demorar dependiendo del número de archivos asociados
al vehículo.

Parámetros
----------

- ``request``: Objeto de la solicitud HTTP.
- ``vehiculo``: Instancia del modelo ``Vehiculo`` que representa el vehículo para el cual se generará el PDF.

Proceso
-------

1. Se obtienen las opciones de ocultar documentación para el vehículo en base al tipo de vehículo.
2. Se obtiene la documentación e información técnica del vehículo.
3. Se preparan las imágenes relacionadas con la documentación del vehículo, las cuales se procesan en múltiples hilos.
4. Se renderiza una plantilla HTML con la información y documentación del vehículo.
5. Se convierte la plantilla HTML a PDF utilizando ``pisa`` y se guarda en una ubicación temporal.

Resultado
---------

Devuelve la ruta del archivo PDF generado.

URL
---

No tiene una URL asociada directamente, ya que es una función que se ejecuta en el backend, probablemente vinculada a una vista o tarea.

---

create_zip_file
================

Genera un archivo ZIP que contiene varios archivos PDF. La tarea se ejecuta de manera sincrónica.

Parámetros
----------

- ``pdf_files``: Lista de rutas de archivos PDF que se incluirán en el archivo ZIP.

Proceso
-------

1. Se crea un archivo ZIP en una carpeta temporal.
2. Se agregan los archivos PDF especificados en el archivo ZIP.

Resultado
---------

Devuelve la ruta del archivo ZIP generado.

---

generate_vehicle_pdfs_and_send_email
=====================================

Genera PDFs para los vehículos y envía un correo electrónico notificando sobre el proceso. Esta es una tarea asíncrona que utiliza Celery para ejecutarse en segundo plano.

Proceso
-------

1. Se llama a la función ``notificacion_celery_email()`` para enviar el correo de notificación.
2. Se espera 60 segundos (``time.sleep(60)``).
3. Se vuelve a llamar a ``notificacion_celery_email()`` para enviar otro correo de notificación.

Resultado
---------

Devuelve el mensaje "done" una vez que el proceso se ha completado.

Nota
----

Este es un proceso asíncrono ejecutado por Celery, lo que permite que el proceso se realice en segundo plano mientras la aplicación continúa su ejecución normal.

