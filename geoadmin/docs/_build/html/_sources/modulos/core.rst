####
Core
####

Descripción General
*******************

El módulo core es el núcleo del sistema y proporciona funcionalidades esenciales que sirven de base para otros módulos del proyecto. Contiene definiciones clave como modelos de datos, decoradores, utilidades y señales que son utilizadas en distintas partes de la aplicación.

.. code-block:: bash   

    core/
    │── admin.py         # Configuración del panel de administración de Django
    │── apps.py          # Configuración de la aplicación Django
    │── choices.py       # Definición de opciones predefinidas para modelos
    │── decorators.py    # Decoradores personalizados para vistas y funciones
    │── forms.py         # Formularios utilizados dentro del módulo
    │── models.py        # Definición de modelos de datos
    │── signals.py       # Señales de Django para ejecución de lógica basada en eventos
    │── urls.py          # Definición de rutas para las vistas del módulo
    │── utils.py         # Funciones auxiliares reutilizables
    │── views.py         # Lógica de controladores para las vistas
    │── migrations/      # Archivos de migración para la base de datos

Modelos de Datos (models.py)
****************************

El archivo models.py define las entidades principales que maneja el módulo.

Genero
======

El modelo Genero se utiliza para almacenar información sobre los géneros de los usuarios.

- Campos:
    - ``genero``: CharField (máximo 50 caracteres, único). Representa el nombre del género.
    - ``creador``: CharField (máximo 50 caracteres). Representa el creador del género (opcional).
    - ``status``: BooleanField. Indica el estado del género (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación del género. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Genero".
    - ``verbose_name_plural``: "Generos".
    - ``db_table``: "user_genero".

Ciudad
======

El modelo Ciudad se utiliza para almacenar las ciudades relacionadas con los usuarios.

- Campos:
    - ``ciudad``: CharField (máximo 50 caracteres, único). Representa el nombre de la ciudad.
    - ``creador``: CharField (máximo 50 caracteres). Representa el creador de la ciudad (opcional).
    - ``status``: BooleanField. Indica el estado de la ciudad (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación de la ciudad. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Ciudad"
    - ``verbose_name_plural``: "Ciudades"
    - ``db_table``: "user_ciudad"

Nacionalidad
============

El modelo Nacionalidad se utiliza para almacenar las nacionalidades de los usuarios.

- Campos:
    - ``nacionalidad``: CharField (máximo 50 caracteres, único). Representa el nombre de la nacionalidad.
    - ``creador``: CharField (máximo 50 caracteres). Representa el creador de la nacionalidad (opcional).
    - ``status``: BooleanField. Indica el estado de la nacionalidad (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación de la nacionalidad. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Nacionalidad"
    - ``verbose_name_plural``: "Nacionalidades"
    - ``db_table``: "user_nacionalidad"

Año(ano)
========

El modelo Ano representa los años en los que los vehículos pueden ser registrados.

- Campos:
    - ``ano``: CharField (máximo 50 caracteres, único). Representa el año.
    - ``creador``: CharField (máximo 50 caracteres). Representa el creador del año (opcional).
    - ``status``: BooleanField. Indica el estado del año (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación del año. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Año"
    - ``verbose_name_plural``: "Años"
    - ``db_table``: "vehicle_ano"

Marca
=====

El modelo Marca representa las marcas de los vehículos.

- Campos:
    - ``marca``: CharField (máximo 50 caracteres, único). Representa el nombre de la marca.
    - ``creador``: CharField (máximo 50 caracteres). Representa el creador de la marca (opcional).
    - ``status``: BooleanField. Indica el estado de la marca (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación de la marca. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Marca"
    - ``verbose_name_plural``: "Marcas"
    - ``db_table``: "vehicle_marca"

Modelo
======

El modelo Modelo representa los modelos de vehículos.

- Campos:
    - ``modelo``: CharField (máximo 50 caracteres, único). Representa el nombre del modelo.
    - ``creador``: CharField (máximo 50 caracteres). Representa el creador del modelo (opcional).
    - ``status``: BooleanField. Indica el estado del modelo (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación del modelo. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Modelo"
    - ``verbose_name_plural``: "Modelos"
    - ``db_table``: "vehicle_modelo"

Color
=====

El modelo Color representa los colores disponibles para los vehículos.

- Campos:
    - ``color``: CharField (máximo 50 caracteres, único). Representa el color.
    - ``creador``: CharField (máximo 50 caracteres). Representa el creador del color (opcional).
    - ``status``: BooleanField. Indica el estado del color (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación del color. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Color"
    - ``verbose_name_plural``: "Colores"
    - ``db_table``: "vehicle_color"

Tipo
====

El modelo Tipo representa los diferentes tipos de vehículos.

- Campos:
    - ``tipo``: CharField (máximo 50 caracteres, único). Representa el tipo de vehículo.
    - ``creador``: CharField (máximo 50 caracteres). Representa el creador del tipo (opcional).
    - ``status``: BooleanField. Indica el estado del tipo (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación del tipo. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Tipo"
    - ``verbose_name_plural``: "Tipos"
    - ``db_table``: "vehicle_tipo"

Signal: create_informacion_vehiculo
===================================

Este código utiliza el decorador @receiver para crear una función que se ejecuta automáticamente después de que se guarde una instancia del modelo Tipo en la base de datos.

- Funcionamiento:
    - ``@receiver(post_save, sender=Tipo)``: Este decorador le indica a Django que la función create_informacion_vehiculo debe ejecutarse cada vez que se guarda (crea o actualiza) una instancia del modelo Tipo.

    - ``post_save``: Es un tipo de señal que se dispara después de que un objeto se haya guardado en la base de datos.
    - ``sender=Tipo``: Especifica que el signal se activará cuando el modelo Tipo se guarde.
    - ``def create_informacion_vehiculo(sender, instance, created, kwargs)``: 
        - Esta es la función que se ejecuta cuando se dispara el signal. 
        - Recibe varios parámetros:
            - ``sender``: El modelo que ha enviado la señal (Tipo en este caso).
            - ``instance``: La instancia del objeto que ha sido guardado.
            - ``created``: Un valor booleano que indica si la instancia es nueva (True si se ha creado una nueva instancia).
            - ``kwargs``: Otros parámetros adicionales que Django podría pasar.
            - ``OcultarOpcionesVehiculo.objects.create(tipo_vehiculo=instance.tipo)``: Después de que se guarda una instancia del modelo Tipo, esta línea crea una nueva instancia del modelo OcultarOpcionesVehiculo con el campo tipo_vehiculo igual al tipo del objeto Tipo recién guardado. Esto sugiere que cada vez que se cree un nuevo tipo de vehículo, se genera automáticamente una nueva entrada en OcultarOpcionesVehiculo relacionada con ese tipo de vehículo.

Faena 
=====

El modelo Faena se utiliza para almacenar las faenas mineras.

- Campos:
    - ``faena``: CharField (máximo 100 caracteres, único). Representa el nombre de la faena.
    - ``descripcion``: CharField (máximo 500 caracteres). Descripción de la faena.
    - ``creador``: CharField (máximo 50 caracteres). Creador de la faena (opcional).
    - ``status``: BooleanField. Indica el estado de la faena (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación de la faena. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Faena"
    - ``verbose_name_plural``: "Faenas"
    - ``db_table``: "mining_profile"

TipoDocumentoFaena
==================

El modelo TipoDocumentoFaena se utiliza para almacenar los tipos de documentos asociados a una faena.

- Campos:
    - ``faena``: ForeignKey (a Faena). La faena a la que pertenece el tipo de documento.
    - ``documento``: CharField (máximo 100 caracteres). Tipo de documento de la faena.
    - ``creador``: CharField (máximo 50 caracteres). Creador del tipo de documento (opcional).
    - ``status``: BooleanField. Indica el estado del tipo de documento (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación del tipo de documento. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Tipo Documento Faena"
    - ``verbose_name_plural``: "Tipos Documentos Faena"
    - ``db_table``: "mining_document_type"

EmpresaServicios
================

El modelo EmpresaServicios representa las empresas de mantenimiento de vehículos.

- Campos:
    - ``empresa``: CharField (máximo 100 caracteres, único). Nombre de la empresa.
    - ``descripcion``: CharField (máximo 500 caracteres). Descripción de la empresa.
    - ``direccion``: CharField (máximo 500 caracteres). Dirección de la empresa.
    - ``rut``: CharField (máximo 50 caracteres). RUT de la empresa.
    - ``telefono``: IntegerField. Teléfono de la empresa.
    - ``creador``: CharField (máximo 50 caracteres). Creador de la empresa (opcional).
    - ``status``: BooleanField. Indica el estado de la empresa (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación de la empresa. Valor por defecto: la fecha y hora actual.
- Metadatos:
    ``verbose_name``: "Empresa de Mantenimiento"
    ``verbose_name_plural``: "Empresas de Mantenimiento"
    ``db_table``: "companies_profile"

EmpresaTipoServicios
====================

El modelo EmpresaTipoServicios representa los servicios de mantenimiento que una empresa puede ofrecer.

- Campos:
    - ``empresa``: ForeignKey (a EmpresaServicios). La empresa que ofrece el servicio.
    - ``servicio``: CharField (máximo 100 caracteres). Tipo de servicio de mantenimiento que la empresa ofrece.
    - ``creador``: CharField (máximo 50 caracteres). Creador del servicio (opcional).
    - ``status``: BooleanField. Indica el estado del servicio (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación del servicio. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Servicio de Mantenimiento"
    - ``verbose_name_plural``: "Servicios de Mantenimiento"
    - ``db_table``: "companies_maintenance_services"

CategoriaFallaVehiculo
======================

El modelo CategoriaFallaVehiculo representa las categorías de fallas de los vehículos.

- Campos:
    - ``categoria``: CharField (máximo 200 caracteres, único). Nombre de la categoría de falla.
    - ``creador``: CharField (máximo 50 caracteres). Creador de la categoría de falla (opcional).
    - ``status``: BooleanField. Indica el estado de la categoría de falla (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación de la categoría de falla. Valor por defecto: la fecha y hora actual.

- Metadatos:
    - ``verbose_name``: "Tipo Categoría de Falla"
    - ``verbose_name_plural``: "Tipos Categorías de Fallas"
    - ``db_table``: "vehicle_categories_failure"


TipoFallaVehiculo
=================

El modelo TipoFallaVehiculo se utiliza para almacenar los tipos específicos de fallas dentro de una categoría.

- Campos:
    - ``categoria``: ForeignKey (a CategoriaFallaVehiculo). La categoría a la que pertenece el tipo de falla.
    - ``falla``: CharField (máximo 200 caracteres). Descripción de la falla.
    - ``creador``: CharField (máximo 50 caracteres). Creador del tipo de falla (opcional).
    - ``status``: BooleanField. Indica el estado del tipo de falla (opcional).
    - ``fechacreacion``: DateTimeField. Fecha y hora de la creación del tipo de falla. Valor por defecto: la fecha y hora actual.
- Metadatos:
    - ``verbose_name``: "Tipo de Falla"
    - ``verbose_name_plural``: "Tipos de Fallas"
    - ``db_table``: "vehicle_failure"

OcultarOpcionesVehiculo
=======================

El modelo OcultarOpcionesVehiculo almacena las opciones relacionadas con la ocultación de datos de vehículos, con diferentes campos que permiten definir varios aspectos del vehículo. Cada opción está relacionada con un tipo de vehículo.

- Campos:
    - ``tipo_vehiculo``: (CharField) Nombre del tipo de vehículo. Máximo 100 caracteres.
    - ``placaPatente``: (CharField) Indica si la patente es requerida. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``rutPropietario``: (CharField) Indica si el Rut del propietario es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaAdquisicion``: (CharField) Indica si la fecha de adquisición es requerida. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``nombrePropietario``: (CharField) Indica si el nombre del propietario es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``domicilio``: (CharField) Indica si el domicilio es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``tipo``: (CharField) Indica si el tipo de vehículo es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``marca``: (CharField) Indica si la marca del vehículo es requerida. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``modelo``: (CharField) Indica si el modelo del vehículo es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``ano``: (CharField) Indica si el año del vehículo es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``numeroMotor``: (CharField) Indica si el número de motor es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``numeroChasis``: (CharField) Indica si el número de chasis es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``numeroVin``: (CharField) Indica si el número VIN es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``color``: (CharField) Indica si el color del vehículo es requerido. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaVencimientoPermisoCirculacion``: (CharField) Indica si la fecha de vencimiento del permiso de circulación es requerida. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaVencimientoRevisionTecnica``: (CharField) Indica si la fecha de vencimiento de la revisión técnica es requerida. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaVencimientoSeguroObligatorio``: (CharField) Indica si la fecha de vencimiento del seguro obligatorio es requerida. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaVencimientoLamina``: (CharField) Indica si la fecha de vencimiento de la lámina es opcional. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaInstalacionBarraAntiVuelco``: (CharField) Indica si la fecha de instalación de la barra anti vuelco es opcional. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaInstalacionGps``: (CharField) Indica si la fecha de instalación de GPS es opcional. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaCertificadoOperatividad``: (CharField) Indica si la fecha del certificado de operatividad es opcional. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaCertificadoMantencion``: (CharField) Indica si la fecha del certificado de mantención es opcional. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaCertificadoGrua``: (CharField) Indica si la fecha del certificado de grúa es opcional. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fechaVencimientoTransportePrivado``: (CharField) Indica si la fecha de vencimiento del transporte privado es opcional. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``tieneTag``: (CharField) Indica si el vehículo tiene tag. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``tipoTraccion``: (CharField) Tipo de tracción del vehículo. Máximo 10 caracteres.
    - ``pesoBrutoVehicular``: (CharField) Peso bruto vehicular. Máximo 10 caracteres.
    - ``capacidadCarga``: (CharField) Capacidad de carga del vehículo. Máximo 10 caracteres.
    - ``tipoNeumatico``: (CharField) Tipo de neumático del vehículo. Máximo 10 caracteres.
    - ``tipoAceiteMotor``: (CharField) Tipo de aceite de motor. Máximo 10 caracteres.
    - ``tipoRefrigeranteMotor``: (CharField) Tipo de refrigerante de motor. Máximo 10 caracteres.
    - ``tipoFiltroAireMotor``: (CharField) Tipo de filtro de aire del motor. Máximo 10 caracteres.
    - ``tipoFiltroCombustible``: (CharField) Tipo de filtro de combustible. Máximo 10 caracteres.
    - ``frecuenciaMantenimiento``: (CharField) Frecuencia de mantenimiento (en kilómetros). Máximo 10 caracteres.
    - ``proximoMantenimiento``: (CharField) Próximo mantenimiento (en kilómetros). Máximo 10 caracteres.
    - ``proximoMantenimientoGrua``: (CharField) Próximo mantenimiento de grúa (en horómetros). Máximo 10 caracteres.
    - ``fotografiaFacturaCompra``: (CharField) Factura de compra del vehículo. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaPadron``: (CharField) Padrón vehicular. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaPermisoCirculacion``: (CharField) Permiso de circulación. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaRevisionTecnica``: (CharField) Revisión técnica. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaRevisionTecnicaGases``: (CharField) Revisión técnica de gases. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaSeguroObligatorio``: (CharField) Seguro obligatorio. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaSeguroAutomotriz``: (CharField) Seguro automotriz. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaCertificadoGps``: (CharField) Certificado de GPS. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaCertificadoMantencion``: (CharField) Certificado de mantención. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaCertificadoOperatividad``: (CharField) Certificado de operatividad. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaCertificadoGrua``: (CharField) Certificado de grúa. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaCertificadoLamina``: (CharField) Certificado de lámina. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaCertificadoBarraAntiVuelco``: (CharField) Certificado de barra anti vuelco. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaDocumentacionMiniBus``: (CharField) Documentación de transporte privado (mini bus). Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaInteriorTablero``: (CharField) Fotografía del interior del tablero. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaInteriorCopiloto``: (CharField) Fotografía del interior del copiloto. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaInteriorAtrasPiloto``: (CharField) Fotografía interior atrás (piloto). Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaInteriorAtrasCopiloto``: (CharField) Fotografía interior atrás (copiloto). Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaExteriorFrontis``: (CharField) Fotografía exterior del frontis. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaExteriorAtras``: (CharField) Fotografía exterior atrás. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaExteriorPiloto``: (CharField) Fotografía exterior lado piloto. Máximo 10 caracteres. Opciones: "Si", "No".
    - ``fotografiaExteriorCopiloto``: (CharField) Fotografía exterior lado copiloto. Máximo 10 caracteres. Opciones: "Si", "No".
- Métodos:
    - ``__str__(self)``: Devuelve el tipo de vehículo (tipo_vehiculo).
- Metadatos:
    - ``verbose_name``: "Ocultar Información de Vehículo".
    - ``verbose_name_plural``: "Ocultar Información de Vehículos".
    - ``db_table``: vehicle_hide_options.

TipoDocumentoFaenaGeneral
=========================
    
El modelo TipoDocumentoFaenaGeneral está diseñado para gestionar los tipos de documentos asociados a las faenas generales. Esto incluye la información sobre el documento, como el tipo, el creador y su estado, así como la ruta de almacenamiento para los archivos relacionados.

- Campos:
    - ``faena``: (ForeignKey) Relacionado con el modelo Faena. Indica la faena a la que está asociado el documento.
    - ``nombredocumento``: (CharField) Nombre del tipo de documento relacionado con la faena. Máximo 100 caracteres.
    - ``creador``: (CharField) Nombre del creador del documento. Máximo 50 caracteres.
    - ``status``: (BooleanField) Estado del documento. Puede ser True o False.
    - ``fechacreacion``: (DateTimeField) Fecha de creación del documento. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve el nombre de la faena junto con el tipo de documento, permitiendo una representación legible del objeto, que puede ser útil para su visualización en la interfaz administrativa.

    - ``generaNombre(instance, filename)``: Método estático utilizado para generar dinámicamente el nombre del archivo de un documento subido. La ruta de almacenamiento se estructura como documentacion_general_faena/<nombre_faena>/<fecha>.<extension>, donde:
      - ``nombre_faena``: Se obtiene de la faena asociada, en mayúsculas.
      - ``fecha``: Se genera la fecha y hora actual en formato YYYYMMDD_HHMMSS.
      - ``extension``: Es la extensión del archivo subido.
      - ``archivodocumento``: (ImageField) Campo para almacenar el documento en formato imagen. La ruta de carga del archivo se define a través del método generaNombre. En caso de que no se suba un archivo, se establece un archivo predeterminado: 'base/no-imagen.png'.

- Metadatos:
    - ``verbose_name``: "Tipo Documento Faena".
    - ``verbose_name_plural``: "Tipos Documentos Faena".
    - ``db_table``: mining_document_type_general.

TipoMaquinaria
==============
    
El modelo TipoMaquinaria está diseñado para gestionar los tipos o modelos de maquinaria utilizados en un contexto industrial o de faena. Permite almacenar información sobre el tipo de maquinaria, quién la creó, su estado y cuándo fue creada.

- Campos:
    - ``tipo``: (CharField) Nombre del tipo de maquinaria. Este campo es único, lo que significa que no puede haber dos tipos de maquinaria con el mismo nombre. Tiene un máximo de 50 caracteres.
    - ``creador``: (CharField) Nombre del creador del tipo de maquinaria. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado del tipo de maquinaria. Puede ser True (activo) o False (inactivo).
    - ``fechacreacion``: (DateTimeField) Fecha de creación del registro del tipo de maquinaria. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve el nombre del tipo de maquinaria como una cadena de texto. Esto facilita la visualización en la interfaz administrativa y en otros lugares donde se necesite una representación legible del objeto.
- Metadatos:
    - ``verbose_name``: "Modelo".
    - ``verbose_name_plural``: "Modelos".
    - ``db_table``: machine_type.

MarcaMaquinaria
===============

El modelo MarcaMaquinaria está diseñado para gestionar las marcas o modelos específicos dentro de un tipo de maquinaria. Permite asociar cada marca o modelo a un tipo de maquinaria, además de almacenar detalles sobre su creador, estado y fecha de creación.

- Campos:
    - ``tipo``: (ForeignKey) Relaciona el modelo con un tipo de maquinaria (TipoMaquinaria). Este campo es opcional, y se utiliza para especificar el tipo de maquinaria al que pertenece la marca o modelo.
    - ``marca``: (CharField) Nombre de la marca o modelo de la maquinaria. Tiene un máximo de 50 caracteres.
    - ``creador``: (CharField) Nombre del creador del registro de la marca o modelo. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado de la marca o modelo. Puede ser True (activo) o False (inactivo).
    - ``fechacreacion``: (DateTimeField) Fecha en la que se creó el registro de la marca o modelo. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve el nombre de la marca o modelo de la maquinaria como una cadena de texto. Esto facilita la visualización en la interfaz administrativa y en otros lugares donde se necesite una representación legible del objeto.
- Metadatos:
    - ``verbose_name``: "Marca o Modelo".
    - ``verbose_name_plural``: "Marca o Modelos".
    - ``db_table``: machine_model.

KitsMaquinaria
==============
    
El modelo KitsMaquinaria está diseñado para gestionar los kits de reparación asociados a diferentes marcas o modelos de maquinaria. Cada kit tiene un stock mínimo y máximo para asegurar que se mantenga una cantidad adecuada disponible para las reparaciones.

- Campos:
    - ``marcaMaquina``: (ForeignKey) Relaciona el modelo con la marca o modelo de maquinaria (MarcaMaquinaria). Este campo es opcional y permite asociar un kit de reparación a un tipo específico de maquinaria.
    - ``nombreKit``: (CharField) Nombre del kit de reparación. Tiene un máximo de 50 caracteres.
    - ``stockMinimo``: (IntegerField) Cantidad mínima de kits de reparación disponible en inventario. Este campo es opcional.
    - ``stockMaximo``: (IntegerField) Cantidad máxima de kits de reparación que deben mantenerse en inventario. Este campo es opcional.
    - ``creador``: (CharField) Nombre del creador del registro del kit. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado del kit de reparación. Puede ser True (activo) o False (inactivo).
    - ``fechacreacion``: (DateTimeField) Fecha en la que se creó el registro del kit de reparación. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve el nombre del kit de reparación como una cadena de texto. Esto facilita la visualización en la interfaz administrativa y en otros lugares donde se necesite una representación legible del objeto.
- Metadatos:
    - ``verbose_name``: "Marca o Modelo" (este nombre podría estar mejor adaptado a "Kit de Reparación").
    - ``verbose_name_plural``: "Marca o Modelos" (igual, este nombre podría ser "Kits de Reparación").
    - ``db_table``: machine_kit_machine.

FallaMaquinaria
===============

El modelo FallaMaquinaria está diseñado para gestionar las fallas en las máquinas, asociando cada tipo de falla con un kit de maquinaria específico. Esto permite hacer un seguimiento de los tipos de fallas que ocurren en las máquinas y asociarlas a los kits de reparación necesarios.

- Campos:
    - ``kitMaquinaria``: (ForeignKey) Relaciona una falla con un kit de maquinaria específico (KitsMaquinaria). Este campo es opcional y permite asociar un tipo de falla con un kit de reparación determinado.
    - ``falla``: (CharField) Descripción del tipo de falla en la maquinaria. Tiene un máximo de 50 caracteres.
    - ``creador``: (CharField) Nombre del creador del registro de la falla. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado de la falla. Puede ser True (activa) o False (inactiva).
    - ``fechacreacion``: (DateTimeField) Fecha en la que se creó el registro de la falla. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve el tipo de falla como una cadena de texto. Esto facilita la visualización en la interfaz administrativa y en otros lugares donde se necesite una representación legible del objeto.
- Metadatos:
    - ``verbose_name``: "Falla en Máquina".
    - ``verbose_name_plural``: "Fallas en Máquinas".
    - ``db_table``: machine_failure.

FechasImportantes
=================

El modelo FechasImportantes se utiliza para gestionar fechas clave dentro de un sistema, asociando una descripción con una fecha de vencimiento que se define en términos de mes.

- Campos:
    - ``descripcion``: (CharField) Descripción de la fecha importante. Es un campo de texto con un máximo de 50 caracteres.
    - ``fechaVencimiento``: (CharField) Fecha de vencimiento, representada por el mes de vencimiento. Se utiliza un campo de tipo CharField con un máximo de 20 caracteres y un conjunto de opciones predeterminadas (meses). Este campo es opcional.
    - ``creador``: (CharField) Nombre del creador del registro. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado de la fecha importante. Puede ser True (activa) o False (inactiva).
    - ``fechacreacion``: (DateTimeField) Fecha en la que se creó el registro. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve la descripción de la fecha como una cadena de texto. Esto facilita la visualización en la interfaz administrativa y en otros lugares donde se necesite una representación legible del objeto.
- Metadatos:
    - ``verbose_name``: "Fecha Importante".
    - ``verbose_name_plural``: "Fechas Importantes".
    - ``db_table``: vehicle_important_dates.

ReporteError
============

El modelo ReporteError se utiliza para gestionar los reportes de errores dentro del sistema, permitiendo almacenar la descripción del error, detalles adicionales y el estado del reporte.

- Campos:
    - ``creador``: (CharField) Nombre del usuario que reporta el error. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``descripcion``: (CharField) Descripción breve del error. Este campo tiene un máximo de 50 caracteres.
    - ``detalle``: (CharField) Detalle del error, proporcionando una descripción más extensa del incidente. Este campo tiene un máximo de 500 caracteres.
    - ``status``: (BooleanField) Estado del reporte. Indica si el error ha sido resuelto (True) o sigue pendiente (False).
    - ``fechacreacion``: (DateTimeField) Fecha en que se creó el reporte. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve la descripción del error como una cadena de texto. Este método facilita la representación legible del objeto en interfaces como el administrador de Django.
- Metadatos:
    - ``verbose_name``: "Reporte de Error".
    - ``verbose_name_plural``: "Reporte de Errores".
    - ``db_table``: report_errors.

AyudaManuales
=============

El modelo AyudaManuales se utiliza para almacenar documentos relacionados con ayudas o manuales dentro del sistema, permitiendo organizar los archivos por sección y gestionar los detalles asociados a ellos.

- Campos:
    - ``seccion``: (CharField) Sección a la que pertenece el documento. Se utiliza un conjunto de opciones predefinidas (en choices=secciones) para clasificar el tipo de manual o ayuda. Este campo tiene un máximo de 100 caracteres.
    - ``nombredocumento``: (CharField) Nombre del documento. Este campo es opcional y tiene un máximo de 100 caracteres.
    - ``creador``: (CharField) Nombre del creador del documento. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado del documento. Indica si el documento está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) Fecha en que se creó el documento. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que consiste en la sección y el nombre del documento. Facilita la identificación del objeto en interfaces como el administrador de Django.

    - ``generaNombre(instance, filename)``: Función que genera un nombre único para el archivo cargado. Se basa en la sección del documento (en mayúsculas), la fecha y la extensión del archivo para crear un nombre de archivo único. Campos adicionales:
        - ``archivodocumento``: (ImageField) Campo para almacenar el archivo del documento (imagen). Utiliza la función generaNombre para definir el nombre y la ruta del archivo. Si no se carga un archivo, se asigna un valor predeterminado ('base/no-imagen.png').
- Metadatos:
    - ``verbose_name``: "Documento Ayuda y Manual".
    - ``verbose_name_plural``: "Documentos Ayuda y Manuales".
    - ``db_table``: documents_help_manuals.

Sondas
======

El modelo Sondas se utiliza para representar las sondas utilizadas en el contexto de minería o perforación, permitiendo almacenar información relevante sobre ellas.

- Campos:
    - ``sonda``: (CharField) Nombre o identificador de la sonda. Este campo es opcional y tiene un máximo de 100 caracteres.
    - ``creador``: (CharField) Nombre del creador de la entrada. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado de la sonda. Indica si la sonda está activa (True) o inactiva (False).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se creó la entrada. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que consiste en el nombre de la sonda. Esto facilita su identificación en interfaces de usuario como el administrador de Django.
- Metadatos:
    - ``verbose_name``: "Sonda Minera".
    - ``verbose_name_plural``: "Sondas Mineras".
    - ``db_table``: drilling_probe.

Sondajes
========

El modelo Sondajes se utiliza para almacenar y gestionar los sondajes realizados en una faena minera, permitiendo asociarlos a una faena específica y mantener un registro de su estado y creador.

- Campos:
    - ``faena``: (ForeignKey) Relaciona cada sondaje con una faena específica. Este campo es una clave foránea que apunta al modelo Faena. El campo es opcional (null=True), y si se elimina la faena asociada, se eliminarán los sondajes correspondientes.
    - ``sondaje``: (CharField) Nombre o identificador del sondaje. Este campo es opcional y tiene un máximo de 100 caracteres.
    - ``creador``: (CharField) Nombre del creador de la entrada. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado del sondaje. Indica si el sondaje está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se creó la entrada. Se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que consiste en el nombre del sondaje. Esto facilita su identificación en interfaces de usuario como el administrador de Django.
- Metadatos:
    - ``verbose_name``: "Sondaje Minero".
    - ``verbose_name_plural``: "Sondajes Mineros".
    - ``db_table``: drilling_drilling.

Diametros
=========

El modelo Diametros se utiliza para almacenar y gestionar los diámetros de los sondajes realizados en la faena minera. Cada diámetro se asocia con información sobre su creador y estado.

- Campos:
    - ``diametro``: (CharField) Nombre o valor del diámetro. Este campo es opcional y tiene un máximo de 100 caracteres. Representa el diámetro de la sonda utilizada.
    - ``creador``: (CharField) Nombre del creador de la entrada. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado del diámetro. Indica si el diámetro está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se creó la entrada. Este campo es obligatorio y se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que consiste en el valor del diámetro. Esto facilita su identificación en interfaces de usuario como el administrador de Django.
- Metadatos:
    - ``verbose_name``: "Diametro".
    - ``verbose_name_plural``: "Diametros".
    - ``db_table``: drilling_diameter.

TipoTerreno
===========

El modelo TipoTerreno se utiliza para almacenar y gestionar los tipos de terrenos asociados a los sondajes en una faena minera. Cada tipo de terreno se asocia con información sobre su creador y estado.

- Campos:
    - ``tipoTerreno``: (CharField) Nombre o descripción del tipo de terreno. Este campo es opcional y tiene un máximo de 100 caracteres.
    - ``creador``: (CharField) Nombre del creador de la entrada. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado del tipo de terreno. Indica si el terreno está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se creó la entrada. Este campo es obligatorio y se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que consiste en el nombre o descripción del tipo de terreno. Esto facilita su identificación en interfaces de usuario como el administrador de Django.
- Metadatos:
    - ``verbose_name``: "Tipo Terreno".
    - ``verbose_name_plural``: "Tipo Terrenos".
    - ``db_table``: drilling_land_type.

Orientacion
===========

El modelo Orientacion se utiliza para almacenar y gestionar las orientaciones de los sondajes realizados en una faena minera. Cada orientación está asociada con información sobre su creador y estado.

- Campos:
    - ``orientacion``: (CharField) Descripción o nombre de la orientación. Este campo es opcional y tiene un máximo de 100 caracteres.
    - ``creador``: (CharField) Nombre del creador de la entrada. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado de la orientación. Indica si la orientación está activa (True) o inactiva (False).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se creó la entrada. Este campo es obligatorio y se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que consiste en la orientación registrada. Esto facilita su identificación en interfaces de usuario como el administrador de Django.
- Metadatos:
    - ``verbose_name``: "Orientacion".
    - ``verbose_name_plural``: "Orientaciones".
    - ``db_table``: drilling_orientation.

Perforistas
===========

El modelo Perforistas se utiliza para registrar a los perforistas, es decir, las personas o entidades responsables de realizar las perforaciones en una faena minera. Cada perforista está asociado con su estado y con la información de creación del registro.

- Campos:
    - ``perforista``: (CharField) Nombre del perforista. Este campo es opcional y tiene un máximo de 100 caracteres.
    - ``creador``: (CharField) Nombre del creador de la entrada. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado del perforista. Indica si el perforista está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se creó la entrada. Este campo es obligatorio y se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que consiste en el nombre del perforista registrado. Esto facilita su identificación en interfaces de usuario como el administrador de Django.
- Metadatos:
    - ``verbose_name``: "Perforista".
    - ``verbose_name_plural``: "Perforistas".
    - ``db_table``: drilling_perforista.

DetalleControlHorario
=====================

El modelo DetalleControlHorario se utiliza para almacenar los detalles relacionados con el control de horarios de las actividades de perforación. Cada entrada contiene información sobre el detalle de una actividad de control horario, así como su estado y la información del creador.

- Campos:
    - ``detalle``: (CharField) Descripción del detalle relacionado con el control de horario. Este campo es opcional y tiene un máximo de 100 caracteres.
    - ``creador``: (CharField) Nombre del creador de la entrada. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado del detalle. Indica si está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se creó la entrada. Este campo es obligatorio y se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que consiste en el detalle registrado. Esto facilita su identificación en interfaces de usuario como el administrador de Django.
- Metadatos:
    - ``verbose_name``: "Detalle Control Horario".
    - ``verbose_name_plural``: "Detalles Control Horario".
    - ``db_table``: drilling_details.

Corona
======
    
El modelo Corona se utiliza para almacenar los diferentes tipos de coronas utilizadas en los procesos de perforación. Cada entrada representa una corona con su respectivo detalle, creador, estado y fecha de creación.

- Campos:
    - ``corona``: (CharField) Nombre o tipo de la corona utilizada en la perforación. Este campo es opcional y tiene un máximo de 100 caracteres.
    - ``creador``: (CharField) Nombre del creador de la entrada. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) Estado de la corona. Indica si está activa (True) o inactiva (False).
    - ``fechacreacion``: (DateTimeField) Fecha y hora en que se creó la entrada. Este campo es obligatorio y se asigna automáticamente la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que consiste en el nombre de la corona registrada. Esto facilita su identificación en interfaces de usuario como el administrador de Django.
- Metadatos:
    - ``verbose_name``: "Corona".
    - ``verbose_name_plural``: "Coronas".
    - ``db_table``: drilling_corona.

Escareador
==========

El modelo Escareador representa los diferentes tipos de escareadores utilizados en los procesos de perforación. Cada registro almacena información sobre el escareador, como su nombre, creador, estado y fecha de creación.

- Campos:
    - ``escareador``: (CharField) El nombre o tipo de escareador. Este campo es opcional y tiene un límite de 100 caracteres.
    - ``creador``: (CharField) El nombre del creador de la entrada del escareador. Este campo es opcional y tiene un máximo de 50 caracteres.
    - ``status``: (BooleanField) El estado del escareador. Indica si está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) La fecha y hora de creación del registro del escareador. Este campo es obligatorio y se asigna automáticamente a la fecha y hora actuales si no se especifica otra.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que es el nombre del escareador registrado. Esto facilita la visualización de los escareadores en el administrador de Django o interfaces relacionadas.
- Metadatos:
    - ``verbose_name``: "Escareador".
    - ``verbose_name_plural``: "Escareadores".
    - ``db_table``: drilling_escareador.

CantidadAgua
============

El modelo CantidadAgua se utiliza para registrar la cantidad de agua utilizada en las actividades de perforación. Este modelo guarda la información sobre los litros de agua, el creador del registro, el estado de la entrada y la fecha de creación.

- Campos:
    - ``cantidadAgua``: (IntegerField) La cantidad de agua en litros utilizada en la actividad de perforación. Este campo es opcional.
    - ``creador``: (CharField) El nombre del creador de la entrada. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``status``: (BooleanField) El estado del registro de agua, indicando si está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) La fecha y hora en que se crea el registro. Este campo es obligatorio y se asigna automáticamente con la fecha y hora actuales.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que es la cantidad de agua registrada en litros. Esto facilita la visualización de la cantidad de agua en el administrador de Django o interfaces relacionadas.
- Metadatos:
    - ``verbose_name``: "Litros Agua".
    - ``verbose_name_plural``: "Litros Agua".
    - ``db_table``: drilling_cant_water.

Aditivos
========

El modelo Aditivos se utiliza para registrar los diferentes aditivos que se emplean durante las actividades de perforación. Este modelo almacena información sobre el aditivo utilizado, el creador del registro, su estado y la fecha de creación.

- Campos:
    - ``aditivo``: (CharField) El nombre del aditivo utilizado en la actividad de perforación. Este campo es opcional y tiene un límite de 100 caracteres.
    - ``creador``: (CharField) El nombre del creador del registro. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``status``: (BooleanField) El estado del registro del aditivo, indicando si está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) La fecha y hora en que se crea el registro. Este campo es obligatorio y se asigna automáticamente con la fecha y hora actuales.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que es el nombre del aditivo. Esto facilita la visualización del aditivo en el administrador de Django o en interfaces relacionadas.
- Metadatos:
    - ``verbose_name``: "Aditivo".
    - ``verbose_name_plural``: "Aditivos".
    - ``db_table``: drilling_aditivos.

Casing
======

El modelo Casing se utiliza para registrar los tipos de casing (tubos) utilizados en las actividades de perforación. Este modelo almacena información sobre el tipo de casing, el creador del registro, su estado y la fecha de creación.

- Campos:
    - ``casing``: (CharField) El nombre o tipo del casing utilizado en la actividad de perforación. Este campo es opcional y tiene un límite de 100 caracteres.
    - ``creador``: (CharField) El nombre del creador del registro. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``status``: (BooleanField) El estado del registro del casing, indicando si está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) La fecha y hora en que se crea el registro. Este campo es obligatorio y se asigna automáticamente con la fecha y hora actuales.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que es el nombre o tipo del casing. Esto facilita la visualización del casing en el administrador de Django o en interfaces relacionadas.
- Metadatos:
    - ``verbose_name``: "Casing".
    - ``verbose_name_plural``: "Casing".
    - ``db_table``: drilling_casing.

Zapata
======

El modelo Zapata se utiliza para registrar los tipos de zapatas (elementos utilizados en la perforación) en las actividades mineras. Este modelo almacena información sobre el tipo de zapata, el creador del registro, su estado y la fecha de creación.

- Campos:
    - ``zapata``: (CharField) El nombre o tipo de zapata utilizada en la perforación. Este campo es opcional y tiene un límite de 100 caracteres.
    - ``creador``: (CharField) El nombre del creador del registro. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``status``: (BooleanField) El estado del registro de la zapata, indicando si está activa (True) o inactiva (False).
    - ``fechacreacion``: (DateTimeField) La fecha y hora en que se crea el registro. Este campo es obligatorio y se asigna automáticamente con la fecha y hora actuales.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que es el nombre o tipo de zapata. Esto facilita la visualización de la zapata en el administrador de Django o en interfaces relacionadas.
- Metadatos:
    - ``verbose_name``: "Zapata".
    - ``verbose_name_plural``: "Zapatas".
    - ``db_table``: drilling_zapata.

LargoBarra
==========

El modelo LargoBarra se utiliza para registrar las longitudes de las barras utilizadas en las actividades de perforación. Este modelo almacena información sobre el largo de la barra en metros, el creador del registro, su estado y la fecha de creación.

- Campos:
    - ``largoBarra``: (IntegerField) El largo de la barra en metros. Este campo es opcional y almacena el valor numérico de la longitud.
    - ``creador``: (CharField) El nombre del creador del registro. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``status``: (BooleanField) El estado del registro de la barra, indicando si está activa (True) o inactiva (False).
    - ``fechacreacion``: (DateTimeField) La fecha y hora en que se crea el registro. Este campo es obligatorio y se asigna automáticamente con la fecha y hora actuales.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del modelo, que es el largo de la barra. Esto facilita la visualización del largo en el administrador de Django o en interfaces relacionadas.
- Metadatos:
    - ``verbose_name``: "Largo Barra".
    - ``verbose_name_plural``: "Largo Barras".
    - ``db_table``: drilling_largo_barra.

Recomendacion
=============

El modelo Recomendacion se utiliza para almacenar las recomendaciones relacionadas con los pozos de perforación y sus características. Este modelo incluye detalles sobre el pozo, la sonda, las mediciones y las coordenadas asociadas, así como el estado de la recomendación y el creador del registro.

- Campos:
    - ``recomendacion``: (CharField) Una breve descripción o título de la recomendación. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``pozo``: (CharField) El nombre o identificación del pozo. Este campo es opcional y también tiene un límite de 50 caracteres.
    - ``sonda``: (ForeignKey) Relación con el modelo Sondas, indicando la sonda asociada a la recomendación. Este campo es opcional.
    - ``fecha_inicio``: (DateTimeField) La fecha de inicio de la recomendación. Este campo es opcional.
    - ``sector``: (CharField) El sector donde se encuentra la recomendación. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``azimut``: (IntegerField) El valor del azimut, con un rango entre 0 y 360. Este campo es opcional.
    - ``inclinacion``: (DecimalField) El valor de la inclinación en grados, con hasta dos decimales. Este campo es opcional.
    - ``largo_programado``: (DecimalField) El largo programado de la perforación en metros, con hasta dos decimales. Este campo es opcional.
    - ``largo_real``: (DecimalField) El largo real de la perforación en metros, con hasta dos decimales. Este campo es opcional.
    - ``este``: (DecimalField) Coordenada Este de la perforación, con hasta tres decimales. Este campo es opcional.
    - ``norte``: (DecimalField) Coordenada Norte de la perforación, con hasta tres decimales. Este campo es opcional.
    - ``cota``: (DecimalField) Cota de la perforación, con hasta tres decimales. Este campo es opcional.
    - ``creador``: (CharField) El nombre del creador del registro. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``status``: (BooleanField) El estado de la recomendación, indicando si está activa (True) o inactiva (False).
    - ``fechacreacion``: (DateTimeField) La fecha y hora en que se crea el registro. Este campo es obligatorio y se asigna automáticamente con la fecha y hora actuales.
- Métodos:
    - ``format_decimal(self, value)``: Método que formatea los valores decimales de las coordenadas y medidas para evitar decimales innecesarios. Si el valor es None, retorna None.
    - ``__str__(self)``: Devuelve una representación en cadena de la recomendación, mostrando el nombre de la recomendación, seguido de las coordenadas Este y Norte, o el largo real, según el caso.
- Metadatos:
    - ``verbose_name``: "Recomendacion".
    - ``verbose_name_plural``: "Recomendaciones".
    - ``db_table``: drilling_recommendation.

MaterialesSonda
===============
    
El modelo MaterialesSonda se utiliza para almacenar los materiales relacionados con las sondas de perforación. Este modelo incluye el nombre del material, el creador del registro, el estado del material, y la fecha en que fue creado el registro.

- Campos:
    - ``material``: (CharField) El nombre del material relacionado con la sonda de perforación. Este campo es opcional y tiene un límite de 100 caracteres.
    - ``creador``: (CharField) El nombre del creador del registro. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``status``: (BooleanField) El estado del material, indicando si está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) La fecha y hora en que se crea el registro. Este campo es obligatorio y se asigna automáticamente con la fecha y hora actuales.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del material, mostrando el nombre del material.
- Metadatos:
    - ``verbose_name``: "Material Sonda".
    - ``verbose_name_plural``: "Materiales Sonda".
    - ``db_table``: checklist_materiales_sonda.

MaterialesCaseta
================

El modelo MaterialesCaseta se utiliza para almacenar los materiales relacionados con las casetas de operación. Similar al modelo de materiales de sonda, este modelo incluye información sobre el material, el creador del registro, el estado del material y la fecha en que fue creado el registro.

- Campos:
    - ``material``: (CharField) El nombre del material relacionado con la caseta de operación. Este campo es opcional y tiene un límite de 100 caracteres.
    - ``creador``: (CharField) El nombre del creador del registro. Este campo es opcional y tiene un límite de 50 caracteres.
    - ``status``: (BooleanField) El estado del material, indicando si está activo (True) o inactivo (False).
    - ``fechacreacion``: (DateTimeField) La fecha y hora en que se crea el registro. Este campo es obligatorio y se asigna automáticamente con la fecha y hora actuales.
- Métodos:
    - ``__str__(self)``: Devuelve una representación en cadena del material, mostrando el nombre del material.
- Metadatos:
    - ``verbose_name``: "Material Caseta".
    - ``verbose_name_plural``: "Materiales Caseta".
    - ``db_table``: checklist_materiales_caseta.
    

Decoradores (decorators.py)
***************************

Contiene funciones decoradoras para mejorar la seguridad y funcionalidad de las vistas.

is_admin
========

Verifica si el usuario autenticado tiene el rol de "ADMINISTRADOR".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene el rol de "ADMINISTRADOR" y está autenticado, de lo contrario, devuelve ``False``.

is_jefe_mantencion
===================

Verifica si el usuario autenticado tiene el rol de "JEFE MANTENCION".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene el rol de "JEFE MANTENCION" y está autenticado, de lo contrario, devuelve ``False``.

is_supervisor
=============

Verifica si el usuario autenticado tiene el rol de "SUPERVISOR".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene el rol de "SUPERVISOR" y está autenticado, de lo contrario, devuelve ``False``.

is_conductor
============

Verifica si el usuario autenticado tiene el rol de "CONDUCTOR".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene el rol de "CONDUCTOR" y está autenticado, de lo contrario, devuelve ``False``.

is_trabajador
=============

Verifica si el usuario autenticado tiene el rol de "TRABAJADOR".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene el rol de "TRABAJADOR" y está autenticado, de lo contrario, devuelve ``False``.

is_controlador
==============

Verifica si el usuario autenticado tiene el rol de "CONTROLADOR".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene el rol de "CONTROLADOR" y está autenticado, de lo contrario, devuelve ``False``.

is_base_datos
=============

Verifica si el usuario autenticado tiene el rol de "BASE DATOS".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene el rol de "BASE DATOS" y está autenticado, de lo contrario, devuelve ``False``.

is_admin_or_jefe_mantencion
============================

Verifica si el usuario autenticado tiene el rol de "ADMINISTRADOR" o "JEFE MANTENCION".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene el rol de "ADMINISTRADOR" o "JEFE MANTENCION" y está autenticado, de lo contrario, devuelve ``False``.

is_admin_or_controlador_or_base_datos_or_supervisor
====================================================

Verifica si el usuario autenticado tiene uno de los roles: "ADMINISTRADOR", "CONTROLADOR", "BASE DATOS", o "SUPERVISOR".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene uno de los roles mencionados y está autenticado, de lo contrario, devuelve ``False``.

is_admin_or_base_datos_or_supervisor
====================================

Verifica si el usuario autenticado tiene uno de los roles: "ADMINISTRADOR", "BASE DATOS", o "SUPERVISOR".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene uno de los roles mencionados y está autenticado, de lo contrario, devuelve ``False``.

controlador_or_base_datos
=========================

Verifica si el usuario autenticado tiene uno de los roles: "CONTROLADOR" o "BASE DATOS".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene uno de los roles mencionados y está autenticado, de lo contrario, devuelve ``False``.

is_admin_or_jefe_mantencion_or_supervisor
=========================================

Verifica si el usuario autenticado tiene uno de los roles: "ADMINISTRADOR", "JEFE MANTENCION", o "SUPERVISOR".

Parámetros
----------

- ``user``: El usuario autenticado.

Resultado
---------

Devuelve ``True`` si el usuario tiene uno de los roles mencionados y está autenticado, de lo contrario, devuelve ``False``.

vehicle_admin_required
======================

Decorador para vistas que requiere que el usuario tenga el rol de "ADMINISTRADOR". Si el usuario no tiene este rol, se redirige al "dashboard".

Parámetros
----------

- ``view_func``: La vista que se va a envolver con el decorador.

Proceso
-------

Verifica si el usuario tiene el rol de "ADMINISTRADOR". Si no lo tiene, redirige al "dashboard". De lo contrario, ejecuta la vista normalmente.

admin_or_jefe_mantencion_required
=================================

Decorador para vistas que requiere que el usuario tenga el rol de "ADMINISTRADOR" o "JEFE MANTENCION". Si el usuario no tiene estos roles, se redirige al "dashboard".

Parámetros
----------

- ``view_func``: La vista que se va a envolver con el decorador.

Proceso
-------

Verifica si el usuario tiene el rol de "ADMINISTRADOR" o "JEFE MANTENCION". Si no lo tiene, redirige al "dashboard". De lo contrario, ejecuta la vista normalmente.

admin_or_jefe_mantencion_or_supervisor_required
===============================================

Decorador para vistas que requiere que el usuario tenga el rol de "ADMINISTRADOR", "JEFE MANTENCION", o "SUPERVISOR". Si el usuario no tiene estos roles, se redirige al "dashboard".

Parámetros
----------

- ``view_func``: La vista que se va a envolver con el decorador.

Proceso
-------

Verifica si el usuario tiene el rol de "ADMINISTRADOR", "JEFE MANTENCION", o "SUPERVISOR". Si no lo tiene, redirige al "dashboard". De lo contrario, ejecuta la vista normalmente.

sondaje_admin_or_controlador_or_base_datos_or_supervisor_required
=================================================================

Decorador para vistas relacionadas con el "sondaje" que requiere que el usuario tenga el rol de "ADMINISTRADOR", "CONTROLADOR", "BASE DATOS", o "SUPERVISOR". Si el usuario no tiene estos roles, se redirige al "dashboardSondaje".

Parámetros
----------

- ``view_func``: La vista que se va a envolver con el decorador.

Proceso
-------

Verifica si el usuario tiene el rol de "ADMINISTRADOR", "CONTROLADOR", "BASE DATOS", o "SUPERVISOR". Si no lo tiene, redirige al "dashboardSondaje". De lo contrario, ejecuta la vista normalmente.

sondaje_admin_or_base_datos_or_supervisor_required
==================================================

Decorador para vistas relacionadas con el "sondaje" que requiere que el usuario tenga el rol de "ADMINISTRADOR", "BASE DATOS", o "SUPERVISOR". Si el usuario no tiene estos roles, se redirige al "dashboardSondaje".

Parámetros
----------

- ``view_func``: La vista que se va a envolver con el decorador.

Proceso
-------

Verifica si el usuario tiene el rol de "ADMINISTRADOR", "BASE DATOS", o "SUPERVISOR". Si no lo tiene, redirige al "dashboardSondaje". De lo contrario, ejecuta la vista normalmente.

admin_required
==============

Decorador para vistas que requiere que el usuario tenga el rol de "ADMINISTRADOR". Si el usuario no tiene este rol, se redirige a diferentes dashboards según la sección de la sesión (vehicular, sondaje, prevención o inventario).

Parámetros
----------

- ``view_func``: La vista que se va a envolver con el decorador.

Proceso
-------

Verifica si el usuario tiene el rol de "ADMINISTRADOR". Si no lo tiene, redirige al dashboard correspondiente dependiendo de la sección de la sesión. De lo contrario, ejecuta la vista normalmente.


Formularios (forms.py)
**********************

Contiene los formularios utilizados en las vistas.

FormGenero
==========

Este formulario se utiliza para gestionar la información relacionada con el modelo Genero dentro del sistema Django. Permite la creación y edición de registros en la base de datos.

Campos del Formulario

1. ``genero``

    - Tipo: CharField (definido en el modelo Genero)

    - Etiqueta: "Género"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre del género correspondiente.

``Consideraciones Adicionales``

- Diseño: Se utiliza la clase CSS form-control en el widget para mejorar la presentación en Bootstrap.

- Modelo: Este formulario está basado en el modelo Genero y solo permite la gestión del campo "genero".

- Facilidad de uso: La configuración del widget mejora la experiencia del usuario al ingresar los datos.

FormCiudad
==========

Este formulario se utiliza para gestionar la información relacionada con el modelo Ciudad dentro del sistema Django. Permite la creación y edición de registros en la base de datos.

Campos del Formulario

1. ``ciudad``

    - Tipo: CharField (definido en el modelo Ciudad)

    - Etiqueta: "Ciudad"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre de la ciudad correspondiente.

``Consideraciones Adicionales``

- Diseño: Se utiliza la clase CSS form-control en el widget para mejorar la presentación en Bootstrap.

- Modelo: Este formulario está basado en el modelo Ciudad y solo permite la gestión del campo "ciudad".

- Facilidad de uso: La configuración del widget mejora la experiencia del usuario al ingresar los datos.

FormNacionalidad
================

Este formulario se utiliza para gestionar la información relacionada con el modelo Nacionalidad dentro del sistema Django. Permite la creación y edición de registros en la base de datos.

Campos del Formulario

1. ``nacionalidad``

    - Tipo: CharField (definido en el modelo Nacionalidad)

    - Etiqueta: "Nacionalidad"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre de la nacionalidad correspondiente.

``Consideraciones Adicionales``

- Diseño: Se utiliza la clase CSS form-control en el widget para mejorar la presentación en Bootstrap.

- Modelo: Este formulario está basado en el modelo Nacionalidad y solo permite la gestión del campo "nacionalidad".

- Facilidad de uso: La configuración del widget mejora la experiencia del usuario al ingresar los datos.

FormAno
=======

Este formulario se utiliza para gestionar la información relacionada con el modelo Ano dentro del sistema Django. Permite la creación y edición de registros en la base de datos.

Campos del Formulario

1. ``ano``

    - Tipo: CharField (definido en el modelo Ano)

    - Etiqueta: "Año"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el valor del año correspondiente.

``Consideraciones Adicionales``

- Diseño: Se utiliza la clase CSS form-control en el widget para mejorar la presentación en Bootstrap.

- Modelo: Este formulario está basado en el modelo Ano y solo permite la gestión del campo "ano".

- Facilidad de uso: La configuración del widget mejora la experiencia del usuario al ingresar los datos.

FormMarca
=========

Este formulario se utiliza para gestionar la información relacionada con el modelo Marca dentro del sistema Django. Permite la creación y edición de registros en la base de datos.

Campos del Formulario

1. ``marca``

    - Tipo: CharField (definido en el modelo Marca)

    - Etiqueta: "Marca"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre de la marca correspondiente.

``Consideraciones Adicionales``

- Diseño: Se utiliza la clase CSS form-control en el widget para mejorar la presentación en Bootstrap.

- Modelo: Este formulario está basado en el modelo Marca y solo permite la gestión del campo "marca".

- Facilidad de uso: La configuración del widget mejora la experiencia del usuario al ingresar los datos.

FormModelo
==========

Este formulario se utiliza para gestionar la información relacionada con el modelo Modelo dentro del sistema Django. Permite la creación y edición de registros en la base de datos.

Campos del Formulario

1. ``modelo``

    - Tipo: CharField (definido en el modelo Modelo)

    - Etiqueta: "Modelo"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre del modelo correspondiente.

``Consideraciones Adicionales``

- Diseño: Se utiliza la clase CSS form-control en el widget para mejorar la presentación en Bootstrap.

- Modelo: Este formulario está basado en el modelo Modelo y solo permite la gestión del campo "modelo".

- Facilidad de uso: La configuración del widget mejora la experiencia del usuario al ingresar los datos.

FormColor
=========

Este formulario se utiliza para gestionar la información relacionada con el modelo Color dentro del sistema Django. Permite la creación y edición de registros en la base de datos.

Campos del Formulario

1. ``color``

    - Tipo: CharField (definido en el modelo Color)

    - Etiqueta: "Color"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre del color correspondiente.

``Consideraciones Adicionales``

- Diseño: Se utiliza la clase CSS form-control en el widget para mejorar la presentación en Bootstrap.

- Modelo: Este formulario está basado en el modelo Color y solo permite la gestión del campo "color".

- Facilidad de uso: La configuración del widget mejora la experiencia del usuario al ingresar los datos.

FormTipo
========

Este formulario se utiliza para gestionar la información relacionada con el modelo Tipo dentro del sistema Django. Permite la creación y edición de registros en la base de datos.

Campos del Formulario

1. ``tipo``

    - Tipo: CharField (definido en el modelo Tipo)

    - Etiqueta: "Tipo"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre del tipo correspondiente.

``Consideraciones Adicionales``

- Diseño: Se utiliza la clase CSS form-control en el widget para mejorar la presentación en Bootstrap.

- Modelo: Este formulario está basado en el modelo Tipo y solo permite la gestión del campo "tipo".

- Facilidad de uso: La configuración del widget mejora la experiencia del usuario al ingresar los datos.

FormNuevaFaena
==============

Este formulario se utiliza para gestionar la información relacionada con el modelo Faena dentro del sistema Django. Permite la creación y edición de registros en la base de datos, con la posibilidad de deshabilitar el campo "faena" según necesidad.

Campos del Formulario

1. ``faena``

    - Tipo: CharField (definido en el modelo Faena)

    - Etiqueta: "Faena"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre de la faena correspondiente.

    - Configuración especial: Puede deshabilitarse según el valor del parámetro ``faena_disabled``.

2. ``descripcion``

    - Tipo: CharField (definido en el modelo Faena)

    - Etiqueta: "Descripción de la Faena (Opcional)"

    - Widget: Textarea (con clase CSS textinput form-control)

    - Requerido: No

    - Descripción: Permite ingresar una descripción opcional de la faena.

``Consideraciones Adicionales``

- Diseño: Se utilizan clases CSS form-control en los widgets para mejorar la presentación en Bootstrap.

- Modelo: Este formulario está basado en el modelo Faena y permite la gestión de los campos "faena" y "descripcion".

- Flexibilidad: El campo "faena" puede ser deshabilitado dependiendo del valor de ``faena_disabled`` al inicializar el formulario.

FormNuevaEmpresaServicios
=========================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``EmpresaServicios`` dentro del sistema Django. Permite la creación y edición de los datos de una empresa, incluyendo su nombre, RUT, teléfono, dirección y descripción.

Campos del Formulario
----------------------

1. ``empresa``

    - Tipo: CharField (definido en el modelo EmpresaServicios)

    - Etiqueta: "Empresa"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre de la empresa.

    - Configuración especial:
        - Este campo puede ser deshabilitado, según el valor del parámetro ``empresa_disabled`` pasado al inicializar el formulario.

2. ``rut``

    - Tipo: CharField (definido en el modelo EmpresaServicios)

    - Etiqueta: "RUT"

    - Widget: TextInput (con tipo text, placeholder "Sin puntos ni guión", clase CSS inputs, y un evento onkeyup que ejecuta la función formatRutEmpresa(this))

    - Descripción: Permite ingresar el RUT de la empresa.

    - Configuración especial:
        - Este campo puede ser deshabilitado, según el valor del parámetro rut_disabled pasado al inicializar el formulario.
        - Tiene un máximo de 12 caracteres.

3. ``telefono``

    - Tipo: CharField (definido en el modelo EmpresaServicios)

    - Etiqueta: "Teléfono"

    - Widget: TextInput (con tipo number, placeholder "9XXXXXXXX", clase CSS inputs, y un evento onkeyup que ejecuta la función formatTelefono(this))

    - Descripción: Permite ingresar el número de teléfono de la empresa.

    - Configuración especial:
        - Este campo tiene un rango de valores entre 100000000 y 999999999, y un máximo de 9 caracteres.

4. ``direccion``

    - Tipo: CharField (definido en el modelo EmpresaServicios)

    - Etiqueta: "Dirección"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar la dirección de la empresa.

5. ``descripcion``

    - Tipo: CharField (definido en el modelo EmpresaServicios)

    - Etiqueta: "Descripción de la Empresa (Opcional)"

    - Widget: Textarea (con clase CSS textinput form-control)

    - Descripción: Permite ingresar una descripción de la empresa. Este campo es opcional.

    - Configuración especial: Se establece como no obligatorio.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación de los campos del formulario.

- Modelo: Este formulario está basado en el modelo ``EmpresaServicios`` y permite la gestión de los campos ``empresa``, ``rut``, ``telefono``, ``direccion`` y ``descripcion``.

- Configuración especial: Los campos ``empresa`` y ``rut`` pueden ser deshabilitados mediante los parámetros ``empresa_disabled`` y ``rut_disabled``, respectivamente, al inicializar el formulario.


FormEmpresaTipoServicios
========================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``EmpresaTipoServicios`` dentro del sistema Django. Permite la selección de una empresa y el ingreso del tipo de servicio correspondiente.

Campos del Formulario
---------------------

1. ``empresa``

    - Tipo: ForeignKey (definido en el modelo EmpresaTipoServicios)

    - Etiqueta: "Empresa"

    - Widget: Select (alineado al centro mediante estilo CSS)

    - Descripción: Permite seleccionar una empresa de la lista de opciones disponibles.

    - Configuración especial:
        - El queryset se filtra utilizando la función get_filtered_queryset con la empresa actual y un campo de orden.

2. ``servicio``

    - Tipo: CharField (definido en el modelo EmpresaTipoServicios)

    - Etiqueta: "Tipo de Servicio"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el tipo de servicio asociado a la empresa.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación de los campos del formulario.

- Modelo: Este formulario está basado en el modelo ``EmpresaTipoServicios`` y permite la gestión de los campos ``empresa`` y ``servicio``.

- Filtrado de empresas: El campo ``empresa`` se filtra mediante la función ``get_filtered_queryset`` utilizando la empresa actual y un campo de orden.

FormTipoFallaVehiculo
======================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``TipoFallaVehiculo`` dentro del sistema Django. Permite la selección de una categoría de falla y el ingreso del tipo de falla correspondiente.

Campos del Formulario
----------------------

1. ``categoria``

    - Tipo: ForeignKey (definido en el modelo TipoFallaVehiculo)

    - Etiqueta: "Categoría"

    - Widget: Select (alineado al centro mediante estilo CSS)

    - Descripción: Permite seleccionar una categoría de la lista de opciones disponibles.

    - Configuración especial:
        - El queryset se filtra utilizando la función get_filtered_queryset con la categoría actual y un campo de orden.

2. ``falla``

    - Tipo: CharField (definido en el modelo TipoFallaVehiculo)

    - Etiqueta: "Tipo de Falla"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el tipo de falla asociado a la categoría seleccionada.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación de los campos del formulario.

- Modelo: Este formulario está basado en el modelo ``TipoFallaVehiculo`` y permite la gestión de los campos ``categoria`` y ``falla``.

- Filtrado de categorías: El campo ``categoria`` se filtra mediante la función ``get_filtered_queryset`` utilizando la categoría actual y un campo de orden.

FormCategoriaFallaVehiculo
==========================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``CategoriaFallaVehiculo`` dentro del sistema Django. Permite el ingreso del nombre de una categoría de falla.

Campos del Formulario
---------------------

1. ``categoria``

    - Tipo: CharField (definido en el modelo ``CategoriaFallaVehiculo``)

    - Etiqueta: "Categoría"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar el nombre de la categoría de falla.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza la clase CSS ``textinput form-control`` para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``CategoriaFallaVehiculo`` y permite la gestión del campo ``categoria``.

FormOcultarOpcionesVehiculoAdicional
====================================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``OcultarOpcionesVehiculo`` dentro del sistema Django. Permite el ingreso de fechas de vencimiento e instalación de varios elementos relacionados con el vehículo, además de gestionar la opción de si tiene o no un ``Tag``.

Campos del Formulario
----------------------

1. ``fechaVencimientoLamina``

    - Tipo: DateField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fecha de Vencimiento de Lámina"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar la fecha de vencimiento de la lámina del vehículo.

2. ``fechaInstalacionBarraAntiVuelco``

    - Tipo: DateField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fecha de Instalación de Barra Anti-Vuelco"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar la fecha de instalación de la barra anti-vuelco del vehículo.

3. ``fechaInstalacionGps``

    - Tipo: DateField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fecha de Instalación de GPS"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar la fecha de instalación del GPS en el vehículo.

4. ``fechaVencimientoTransportePrivado``

    - Tipo: DateField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fecha de Vencimiento de Transporte Privado"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar la fecha de vencimiento de la autorización de transporte privado.

5. ``fechaCertificadoOperatividad``

    - Tipo: DateField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fecha del Certificado de Operatividad"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar la fecha del certificado de operatividad del vehículo.

6. ``fechaCertificadoMantencion``

    - Tipo: DateField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fecha del Certificado de Mantención"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar la fecha del certificado de mantención del vehículo.

7. ``fechaCertificadoGrua``

    - Tipo: DateField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fecha del Certificado de Grúa"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar la fecha del certificado de grúa para el vehículo.

8. ``tieneTag``

    - Tipo: BooleanField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "¿Tiene Tag?"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite marcar si el vehículo tiene o no un ``Tag`` asociado.

Consideraciones Adicionales
---------------------------

- Diseño: No se han especificado configuraciones especiales para los widgets de los campos.

- Modelo: Este formulario está basado en el modelo ``OcultarOpcionesVehiculo`` y permite la gestión de los campos ``fechaVencimientoLamina``, ``fechaInstalacionBarraAntiVuelco``, ``fechaInstalacionGps``, ``fechaVencimientoTransportePrivado``, ``fechaCertificadoOperatividad``, ``fechaCertificadoMantencion``, ``fechaCertificadoGrua`` y ``tieneTag``.

FormOcultarOpcionesVehiculoTecnica
==================================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``OcultarOpcionesVehiculo`` dentro del sistema Django. Permite el ingreso de datos técnicos sobre el vehículo, como tipo de tracción, peso bruto vehicular, capacidad de carga, entre otros.

Campos del Formulario
---------------------

1. ``tipoTraccion``

    - Tipo: CharField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Tipo de Tracción"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar el tipo de tracción del vehículo.

2. ``pesoBrutoVehicular``

    - Tipo: DecimalField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Peso Bruto Vehicular"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar el peso bruto vehicular.

3. ``capacidadCarga``

    - Tipo: DecimalField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Capacidad de Carga"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar la capacidad de carga del vehículo.

4. ``tipoNeumatico``

    - Tipo: CharField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Tipo de Neumático"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar el tipo de neumático del vehículo.

5. ``tipoAceiteMotor``

    - Tipo: CharField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Tipo de Aceite de Motor"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar el tipo de aceite utilizado en el motor.

6. ``tipoRefrigeranteMotor``

    - Tipo: CharField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Tipo de Refrigerante de Motor"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar el tipo de refrigerante utilizado en el motor.

7. ``tipoFiltroAireMotor``

    - Tipo: CharField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Tipo de Filtro de Aire de Motor"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar el tipo de filtro de aire utilizado en el motor.

8. ``tipoFiltroCombustible``

    - Tipo: CharField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Tipo de Filtro de Combustible"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar el tipo de filtro de combustible utilizado en el vehículo.

9. ``frecuenciaMantenimiento``

    - Tipo: CharField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Frecuencia de Mantenimiento"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite ingresar la frecuencia de mantenimiento del vehículo.

10. ``proximoMantenimiento``

     - Tipo: DateField (definido en el modelo ``OcultarOpcionesVehiculo``)
  
     - Etiqueta: "Próximo Mantenimiento"
  
     - Widget: (sin configuración especial de widget)
  
     - Descripción: Permite ingresar la fecha del próximo mantenimiento programado para el vehículo.

11. ``proximoMantenimientoGrua``

     - Tipo: DateField (definido en el modelo ``OcultarOpcionesVehiculo``)

     - Etiqueta: "Próximo Mantenimiento de Grúa"

     - Widget: (sin configuración especial de widget)

     - Descripción: Permite ingresar la fecha del próximo mantenimiento de la grúa asociada al vehículo.

Consideraciones Adicionales
---------------------------

- Diseño: No se han especificado configuraciones especiales para los widgets de los campos.

- Modelo: Este formulario está basado en el modelo ``OcultarOpcionesVehiculo`` y permite la gestión de los campos ``tipoTraccion``, ``pesoBrutoVehicular``, ``capacidadCarga``, ``tipoNeumatico``, ``tipoAceiteMotor``, ``tipoRefrigeranteMotor``, ``tipoFiltroAireMotor``, ``tipoFiltroCombustible``, ``frecuenciaMantenimiento``, ``proximoMantenimiento`` y ``proximoMantenimientoGrua``.

FormOcultarOpcionesVehiculoDocumentacion
========================================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``OcultarOpcionesVehiculo`` dentro del sistema Django. Permite el ingreso de fotografías de diferentes documentos y certificados asociados al vehículo.

Campos del Formulario
---------------------

1. ``fotografiaFacturaCompra``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía de la Factura de Compra"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía de la factura de compra del vehículo.

2. ``fotografiaPadron``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Padrón"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del padrón del vehículo.

3. ``fotografiaPermisoCirculacion``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Permiso de Circulación"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del permiso de circulación del vehículo.

4. ``fotografiaRevisionTecnica``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía de la Revisión Técnica"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del certificado de revisión técnica del vehículo.

5. ``fotografiaRevisionTecnicaGases``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía de la Revisión Técnica de Gases"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del certificado de revisión técnica de gases del vehículo.

6. ``fotografiaSeguroObligatorio``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Seguro Obligatorio"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del seguro obligatorio del vehículo.

7. ``fotografiaSeguroAutomotriz``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Seguro Automotriz"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del seguro automotriz del vehículo.

8. ``fotografiaCertificadoGps``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Certificado de GPS"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del certificado de GPS del vehículo.

9. ``fotografiaCertificadoMantencion``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Certificado de Mantención"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del certificado de mantención del vehículo.

10. ``fotografiaCertificadoOperatividad``

     - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

     - Etiqueta: "Fotografía del Certificado de Operatividad"

     - Widget: (sin configuración especial de widget)

     - Descripción: Permite cargar una fotografía del certificado de operatividad del vehículo.

11. ``fotografiaCertificadoGrua``

     - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

     - Etiqueta: "Fotografía del Certificado de Grúa"

     - Widget: (sin configuración especial de widget)

     - Descripción: Permite cargar una fotografía del certificado de grúa del vehículo.

12. ``fotografiaCertificadoLamina``

     - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

     - Etiqueta: "Fotografía del Certificado de Lámina"

     - Widget: (sin configuración especial de widget)

     - Descripción: Permite cargar una fotografía del certificado de lámina del vehículo.

13. ``fotografiaCertificadoBarraAntiVuelco``

     - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

     - Etiqueta: "Fotografía del Certificado de Barra Anti-Vuelco"

     - Widget: (sin configuración especial de widget)

     - Descripción: Permite cargar una fotografía del certificado de barra anti-vuelco del vehículo.

14. ``fotografiaDocumentacionMiniBus``

     - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

     - Etiqueta: "Fotografía de la Documentación del Mini-Bus"

     - Widget: (sin configuración especial de widget)

     - Descripción: Permite cargar una fotografía de la documentación asociada al mini-bus.

Consideraciones Adicionales
---------------------------

- Diseño: No se han especificado configuraciones especiales para los widgets de los campos.

- Modelo: Este formulario está basado en el modelo ``OcultarOpcionesVehiculo`` y permite la gestión de los campos ``fotografiaFacturaCompra``, ``fotografiaPadron``, ``fotografiaPermisoCirculacion``, ``fotografiaRevisionTecnica``, ``fotografiaRevisionTecnicaGases``, ``fotografiaSeguroObligatorio``, ``fotografiaSeguroAutomotriz``, ``fotografiaCertificadoGps``, ``fotografiaCertificadoMantencion``, ``fotografiaCertificadoOperatividad``, ``fotografiaCertificadoGrua``, ``fotografiaCertificadoLamina``, ``fotografiaCertificadoBarraAntiVuelco`` y ``fotografiaDocumentacionMiniBus``.

FormOcultarOpcionesVehiculoInterior
===================================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``OcultarOpcionesVehiculo`` dentro del sistema Django. Permite el ingreso de fotografías del interior del vehículo, incluyendo el tablero, los asientos de copiloto y piloto, y los asientos traseros.

Campos del Formulario
---------------------

1. ``fotografiaInteriorTablero``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Interior del Tablero"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del tablero interior del vehículo.

2. ``fotografiaInteriorCopiloto``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Interior del Copiloto"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del asiento de copiloto del vehículo.

3. ``fotografiaInteriorAtrasPiloto``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Interior Atras Piloto"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía de la parte trasera del asiento del piloto del vehículo.

4. ``fotografiaInteriorAtrasCopiloto``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Interior Atras Copiloto"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía de la parte trasera del asiento del copiloto del vehículo.

Consideraciones Adicionales
---------------------------

- Diseño: No se han especificado configuraciones especiales para los widgets de los campos.

- Modelo: Este formulario está basado en el modelo ``OcultarOpcionesVehiculo`` y permite la gestión de los campos ``fotografiaInteriorTablero``, ``fotografiaInteriorCopiloto``, ``fotografiaInteriorAtrasPiloto`` y ``fotografiaInteriorAtrasCopiloto``.

FormOcultarOpcionesVehiculoExterior
===================================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``OcultarOpcionesVehiculo`` dentro del sistema Django. Permite el ingreso de fotografías del exterior del vehículo, incluyendo las vistas del frente, la parte trasera, los lados de piloto y copiloto.

Campos del Formulario
---------------------

1. ``fotografiaExteriorFrontis``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Exterior Frontis"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía de la parte frontal del vehículo.

2. ``fotografiaExteriorAtras``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Exterior Atras"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía de la parte trasera del vehículo.

3. ``fotografiaExteriorPiloto``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Exterior Piloto"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del lado del piloto del vehículo.

4. ``fotografiaExteriorCopiloto``

    - Tipo: ImageField (definido en el modelo ``OcultarOpcionesVehiculo``)

    - Etiqueta: "Fotografía del Exterior Copiloto"

    - Widget: (sin configuración especial de widget)

    - Descripción: Permite cargar una fotografía del lado del copiloto del vehículo.

Consideraciones Adicionales
---------------------------

- Diseño: No se han especificado configuraciones especiales para los widgets de los campos.

- Modelo: Este formulario está basado en el modelo ``OcultarOpcionesVehiculo`` y permite la gestión de los campos ``fotografiaExteriorFrontis``, ``fotografiaExteriorAtras``, ``fotografiaExteriorPiloto`` y ``fotografiaExteriorCopiloto``.

FormTipoDocumentoFaenaGeneral
=============================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``TipoDocumentoFaenaGeneral`` dentro del sistema Django. Permite la selección de una faena y el ingreso del nombre del documento correspondiente.

Campos del Formulario
---------------------

1. ``faena``

    - Tipo: ForeignKey (definido en el modelo ``TipoDocumentoFaenaGeneral``)

    - Etiqueta: "Faena"

    - Widget: Select (alineado al centro mediante estilo CSS)

    - Descripción: Permite seleccionar una faena de la lista de opciones disponibles.

    - Configuración especial:
        - Se filtra el queryset utilizando la función ``get_filtered_queryset`` con la faena actual y un campo de orden.
        - Se excluye la opción "SIN ASIGNAR".

2. ``nombredocumento``

    - Tipo: CharField (definido en el modelo ``TipoDocumentoFaenaGeneral``)

    - Etiqueta: "Nombre del Documento"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar el nombre del documento asociado a la faena.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación de los campos del formulario.

- Modelo: Este formulario está basado en el modelo ``TipoDocumentoFaenaGeneral`` y permite la gestión de los campos ``faena`` y ``nombredocumento``.

- Filtrado de faenas: El campo ``faena`` se filtra mediante la función ``get_filtered_queryset`` utilizando la faena actual y un campo de orden, excluyendo la opción "SIN ASIGNAR".

FormTipoMaquinaria
==================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``TipoMaquinaria`` dentro del sistema Django. Permite el ingreso del tipo de maquinaria.

Campos del Formulario
---------------------

1. ``tipo``

    - Tipo: CharField (definido en el modelo ``TipoMaquinaria``)

    - Etiqueta: "Tipo"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar el tipo de maquinaria.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``TipoMaquinaria`` y permite la gestión del campo ``tipo``.

FormMarcaMaquinaria
===================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``MarcaMaquinaria`` dentro del sistema Django. Permite la selección de un tipo de maquinaria y el ingreso de la marca o modelo correspondiente.

Campos del Formulario
---------------------

1. ``tipo``

    - Tipo: ForeignKey (definido en el modelo ``MarcaMaquinaria``)

    - Etiqueta: "Tipo de Maquinaria"

    - Widget: Select (alineado al centro mediante estilo CSS)

    - Descripción: Permite seleccionar un tipo de maquinaria de la lista de opciones disponibles.

    - Configuración especial:
        - El queryset se filtra utilizando la función ``get_filtered_queryset`` con el tipo de maquinaria actual y un campo de orden.

2. ``marca``

    - Tipo: CharField (definido en el modelo ``MarcaMaquinaria``)

    - Etiqueta: "Marca o Modelo de la Maquinaria"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar la marca o modelo de la maquinaria seleccionada.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación de los campos del formulario.

- Modelo: Este formulario está basado en el modelo ``MarcaMaquinaria`` y permite la gestión de los campos ``tipo`` y ``marca``.

- Filtrado de tipos de maquinaria: El campo ``tipo`` se filtra mediante la función ``get_filtered_queryset`` utilizando el tipo de maquinaria actual y un campo de orden.

FormKitReparacion
==================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``KitsMaquinaria`` dentro del sistema Django. Permite la selección de la marca (tipo de maquinaria), el ingreso del nombre del kit de reparación, y la gestión de los valores de stock mínimo y máximo.

Campos del Formulario
---------------------

1. ``marcaMaquina``

    - Tipo: ForeignKey (definido en el modelo ``KitsMaquinaria``)

    - Etiqueta: "Marca (Tipo)"

    - Widget: Select (alineado al centro mediante estilo CSS)

    - Descripción: Permite seleccionar la marca (tipo de maquinaria) de la lista de opciones disponibles.

    - Configuración especial:
  
        - El queryset se filtra utilizando la función ``get_filtered_queryset`` con la marca actual y un campo de orden.
        - Se define un conjunto de opciones dinámicas con formato ``tipo - marca``.

2. ``nombreKit``

    - Tipo: CharField (definido en el modelo ``KitsMaquinaria``)

    - Etiqueta: "Nombre del Kit de Reparación"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar el nombre del kit de reparación.

3. ``stockMinimo``

    - Tipo: IntegerField (definido en el modelo ``KitsMaquinaria``)

    - Etiqueta: "Stock Mínimo"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar el valor del stock mínimo disponible para el kit.

4. ``stockMaximo``

    - Tipo: IntegerField (definido en el modelo ``KitsMaquinaria``)

    - Etiqueta: "Stock Máximo"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar el valor del stock máximo disponible para el kit.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación de los campos del formulario.

- Modelo: Este formulario está basado en el modelo ``KitsMaquinaria`` y permite la gestión de los campos ``marcaMaquina``, ``nombreKit``, ``stockMinimo`` y ``stockMaximo``.

- Filtrado de marcas: El campo ``marcaMaquina`` se filtra mediante la función ``get_filtered_queryset`` utilizando la marca actual y un campo de orden, generando un conjunto de opciones dinámicas.

- Deshabilitar campos: Los campos ``marcaMaquina`` y ``nombreKit`` pueden ser deshabilitados a través de los parámetros ``marcaMaquina_disabled`` y ``nombreKit_disabled`` al inicializar el formulario.

FormFallaMaquinaria
===================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``FallaMaquinaria`` dentro del sistema Django. Permite la selección de un kit de maquinaria y el ingreso de la falla o incidente correspondiente.

Campos del Formulario
---------------------

1. ``kitMaquinaria``

    - Tipo: ForeignKey (definido en el modelo ``FallaMaquinaria``)

    - Etiqueta: "Kit de Maquinaria"

    - Widget: Select (alineado al centro mediante estilo CSS)

    - Descripción: Permite seleccionar un kit de maquinaria de la lista de opciones disponibles.

    - Configuración especial:
  
        - El queryset se filtra utilizando la función ``get_filtered_queryset`` con el kit actual y un campo de orden.

2. ``falla``

    - Tipo: CharField (definido en el modelo ``FallaMaquinaria``)

    - Etiqueta: "Falla o incidente"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar la descripción de la falla o incidente relacionado con el kit de maquinaria seleccionado.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación de los campos del formulario.

- Modelo: Este formulario está basado en el modelo ``FallaMaquinaria`` y permite la gestión de los campos ``kitMaquinaria`` y ``falla``.

- Filtrado de kits de maquinaria: El campo ``kitMaquinaria`` se filtra mediante la función ``get_filtered_queryset`` utilizando el kit actual y un campo de orden.

FormMarcaMaquinariaSelect
=========================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``KitsMaquinaria`` dentro del sistema Django. Permite la selección de la marca o modelo de maquinaria disponible.

Campos del Formulario
----------------------

1. ``marcaMaquina``

    - Tipo: ForeignKey (definido en el modelo ``KitsMaquinaria``)

    - Etiqueta: "Marca o Modelo"

    - Widget: Select (alineado al centro mediante estilo CSS)

    - Descripción: Permite seleccionar la marca o modelo de maquinaria de la lista de opciones disponibles.

    - Configuración especial:
  
        - El queryset se ordena por ``tipo`` de maquinaria de manera descendente y por ``marca`` de manera ascendente.
        - El campo es obligatorio.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``KitsMaquinaria`` y permite la gestión del campo ``marcaMaquina``.

- Ordenamiento de marcas: El campo ``marcaMaquina`` contiene un conjunto de opciones dinámicas basadas en el queryset de ``MarcaMaquinaria``, ordenado por tipo de maquinaria y marca.

- Requerimiento: El campo ``marcaMaquina`` es obligatorio.

FormNuevaFechasImportantes
===========================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``FechasImportantes`` dentro del sistema Django. Permite ingresar una fecha de vencimiento y una descripción asociada.

Campos del Formulario
----------------------

1. ``fechaVencimiento``

    - Tipo: DateField (definido en el modelo ``FechasImportantes``)

    - Etiqueta: "Fecha de Vencimiento"

    - Widget: DateInput (con formato adecuado para ingresar fechas)

    - Descripción: Permite ingresar la fecha de vencimiento correspondiente a la fecha importante.

2. ``descripcion``

    - Tipo: CharField (definido en el modelo ``FechasImportantes``)

    - Etiqueta: "Descripción"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar una breve descripción sobre la fecha importante.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo de descripción en el formulario.

- Modelo: Este formulario está basado en el modelo ``FechasImportantes`` y permite la gestión de los campos ``fechaVencimiento`` y ``descripcion``.

- Formato de fecha: El campo ``fechaVencimiento`` está diseñado para permitir la entrada de una fecha de vencimiento con el formato adecuado.

FormReporteError
================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``ReporteError`` dentro del sistema Django. Permite ingresar una descripción del error y detallar cómo se produjo el problema.

Campos del Formulario
---------------------

1. ``descripcion``

    - Tipo: CharField (definido en el modelo ``ReporteError``)

    - Etiqueta: "Descripción"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar una breve descripción sobre el error ocurrido.

2. ``detalle``

    - Tipo: CharField (definido en el modelo ``ReporteError``)

    - Etiqueta: "Detalla claramente como se produjo el problema (sección, hora aproximada, etc...)"

    - Widget: Textarea (con clase CSS ``textinput form-control``)

    - Descripción: Permite detallar cómo se produjo el error, especificando información adicional como la sección, hora aproximada, etc.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo de texto en el formulario.

- Modelo: Este formulario está basado en el modelo ``ReporteError`` y permite la gestión de los campos ``descripcion`` y ``detalle``.

- Etiqueta personalizada: La etiqueta del campo ``detalle`` se ajusta para pedir una descripción más detallada sobre el error.

FormAyudaManuales
=================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``AyudaManuales`` dentro del sistema Django. Permite seleccionar una sección y asignar un nombre de documento relacionado.

Campos del Formulario
---------------------

1. ``seccion``

    - Tipo: ForeignKey (definido en el modelo ``AyudaManuales``)

    - Etiqueta: "Sección"

    - Widget: Select (con las opciones disponibles en el modelo ``Seccion``)

    - Descripción: Permite seleccionar una sección de las opciones disponibles.

2. ``nombredocumento``

    - Tipo: CharField (definido en el modelo ``AyudaManuales``)

    - Etiqueta: "Nombre del Documento"

    - Widget: TextInput (con clase CSS ``textinput form-control``)

    - Descripción: Permite ingresar el nombre del documento asociado a la sección seleccionada.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación de los campos del formulario.

- Modelo: Este formulario está basado en el modelo ``AyudaManuales`` y permite la gestión de los campos ``seccion`` y ``nombredocumento``.

FormSeleccionSeccion
====================

Este formulario se utiliza para gestionar la selección de una sección en función de los permisos o configuraciones del usuario. Permite al usuario seleccionar una sección disponible según su perfil.

Campos del Formulario
---------------------

1. ``seccion_select``

    - Tipo: ChoiceField (definido en el formulario ``FormSeleccionSeccion``)

    - Etiqueta: "Opciones"

    - Widget: Select (con las opciones dinámicamente asignadas según el perfil del usuario)

    - Descripción: Permite al usuario seleccionar una de las opciones de sección disponibles, que se basan en los permisos del perfil.

    - Configuración especial:
        - Las opciones disponibles se filtran dependiendo de las configuraciones del perfil del usuario (por ejemplo, "Registro Vehicular", "Sondajes" y "Prevención de Riesgos").

Consideraciones Adicionales
---------------------------

- Diseño: El formulario utiliza el widget ``Select`` para ofrecer las opciones de forma visual.

- Modelo: Este formulario está basado en el modelo ``UsuarioProfile`` y permite la gestión del campo ``seccion_select`` de acuerdo con los permisos del usuario.

- Filtrado de opciones: Las opciones en el campo ``seccion_select`` se ajustan dinámicamente según las secciones activas del perfil del usuario (vehicular, sondaje, o prevención).

FormSondas
===========

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Sondas`` dentro del sistema Django. Permite seleccionar una sonda de las opciones disponibles.

Campos del Formulario
---------------------

1. ``sonda``

    - Tipo: ForeignKey (definido en el modelo ``Sondas``)

    - Etiqueta: "Sonda"

    - Widget: Select (con opciones disponibles en el modelo ``Sondas``)

    - Descripción: Permite seleccionar una sonda de la lista de opciones disponibles.

Consideraciones Adicionales
---------------------------

- Diseño: El formulario utiliza el widget ``Select`` para ofrecer las opciones de forma visual.

- Modelo: Este formulario está basado en el modelo ``Sondas`` y permite la gestión del campo ``sonda``.

- Filtrado de opciones: Las opciones disponibles para la selección de la sonda son las que se encuentran definidas en el modelo ``Sondas``.

FormSondajes
============

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Sondajes`` dentro del sistema Django. Permite seleccionar una faena y el ingreso de un sondaje asociado a ella.

Campos del Formulario
---------------------

1. ``faena``

    - Tipo: ForeignKey (definido en el modelo ``Sondajes``)

    - Etiqueta: "Faena"

    - Widget: Select (alineado al centro mediante estilo CSS)

    - Descripción: Permite seleccionar una faena de la lista de opciones disponibles.

    - Configuración especial:

        - Se filtra el queryset según el valor de ``faena_actual``.
        - Se excluye la opción "SIN ASIGNAR".

2. ``sondaje``

    - Tipo: CharField (definido en el modelo ``Sondajes``)

    - Etiqueta: "Sondaje"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre del sondaje asociado a la faena seleccionada.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan clases CSS para mejorar la presentación de los campos del formulario.

- Modelo: Este formulario está basado en el modelo ``Sondajes`` y permite la gestión de los campos ``faena`` y ``sondaje``.

- Filtrado de faenas: El campo ``faena`` se filtra mediante la función ``get_filtered_queryset`` utilizando el valor de ``faena_actual``, y se excluye la opción "SIN ASIGNAR".


FormDiametros
==============

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Diametros`` dentro del sistema Django. Permite ingresar el valor de un diámetro.

Campos del Formulario
----------------------

1. ``diametro``

    - Tipo: CharField (definido en el modelo ``Diametros``)

    - Etiqueta: "Diámetro"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el valor del diámetro.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``Diametros`` y permite la gestión del campo ``diametro``.

FormTipoTerreno
===============

Este formulario se utiliza para gestionar la información relacionada con el modelo ``TipoTerreno`` dentro del sistema Django. Permite ingresar el tipo de terreno.

Campos del Formulario
----------------------

1. ``tipoTerreno``

    - Tipo: CharField (definido en el modelo ``TipoTerreno``)

    - Etiqueta: "Tipo de Terreno"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el tipo de terreno.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``TipoTerreno`` y permite la gestión del campo ``tipoTerreno``.

FormOrientacion
===============

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Orientacion`` dentro del sistema Django. Permite ingresar la orientación.

Campos del Formulario
---------------------

1. ``orientacion``

    - Tipo: CharField (definido en el modelo ``Orientacion``)

    - Etiqueta: "Orientación"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar la orientación.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``Orientacion`` y permite la gestión del campo ``orientacion``.

FormDetalleControlHorario
=========================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``DetalleControlHorario`` dentro del sistema Django. Permite ingresar el detalle del control de horario.

Campos del Formulario
---------------------

1. ``detalle``

    - Tipo: CharField (definido en el modelo ``DetalleControlHorario``)

    - Etiqueta: "Detalle"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el detalle del control de horario.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``DetalleControlHorario`` y permite la gestión del campo ``detalle``.

FormCorona
==========

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Corona`` dentro del sistema Django. Permite ingresar el nombre de la corona.

Campos del Formulario
---------------------

1. ``corona``

    - Tipo: CharField (definido en el modelo ``Corona``)

    - Etiqueta: "Corona"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre de la corona.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``Corona`` y permite la gestión del campo ``corona``.

FormEscareador
==============

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Escareador`` dentro del sistema Django. Permite ingresar el nombre del escareador.

Campos del Formulario
---------------------

1. ``escareador``

    - Tipo: CharField (definido en el modelo ``Escareador``)

    - Etiqueta: "Escareador"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre del escareador.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``Escareador`` y permite la gestión del campo ``escareador``.

FormCantidadAgua
================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``CantidadAgua`` dentro del sistema Django. Permite ingresar la cantidad de agua.

Campos del Formulario
---------------------

1. ``cantidadAgua``

    - Tipo: IntegerField (definido en el modelo ``CantidadAgua``)

    - Etiqueta: "Cantidad de Agua"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar la cantidad de agua asociada.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``CantidadAgua`` y permite la gestión del campo ``cantidadAgua``.

FormAditivos
============

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Aditivos`` dentro del sistema Django. Permite ingresar el nombre del aditivo.

Campos del Formulario
---------------------

1. ``aditivo``

    - Tipo: CharField (definido en el modelo ``Aditivos``)

    - Etiqueta: "Aditivo"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre del aditivo.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``Aditivos`` y permite la gestión del campo ``aditivo``.

FormCasing
==========

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Casing`` dentro del sistema Django. Permite ingresar el nombre del casing.

Campos del Formulario
---------------------

1. ``casing``

    - Tipo: CharField (definido en el modelo ``Casing``)

    - Etiqueta: "Casing"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre del casing.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``Casing`` y permite la gestión del campo ``casing``.

FormZapata
==========

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Zapata`` dentro del sistema Django. Permite ingresar el nombre de la zapata.

Campos del Formulario
---------------------

1. ``zapata``

    - Tipo: CharField (definido en el modelo ``Zapata``)

    - Etiqueta: "Zapata"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre de la zapata.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``Zapata`` y permite la gestión del campo ``zapata``.

FormLargoBarra
==============

Este formulario se utiliza para gestionar la información relacionada con el modelo ``LargoBarra`` dentro del sistema Django. Permite ingresar el valor del largo de la barra.

Campos del Formulario
---------------------

1. ``largoBarra``

    - Tipo: CharField (definido en el modelo ``LargoBarra``)

    - Etiqueta: "Largo de Barra"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el valor del largo de la barra.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza una clase CSS para mejorar la presentación del campo del formulario.

- Modelo: Este formulario está basado en el modelo ``LargoBarra`` y permite la gestión del campo ``largoBarra``.

FormRecomendaciones
===================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Recomendacion`` dentro del sistema Django. Permite ingresar diversas recomendaciones con detalles sobre pozos, sondas, y parámetros geográficos.

Campos del Formulario
---------------------

1. ``recomendacion``

    - Tipo: CharField (definido en el modelo ``Recomendacion``)

    - Etiqueta: "Recomendación"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar una descripción de la recomendación.

2. ``pozo``

    - Tipo: ForeignKey (definido en el modelo ``Recomendacion``)

    - Etiqueta: "Pozo"

    - Widget: Select

    - Descripción: Permite seleccionar un pozo relacionado con la recomendación.

3. ``sonda``

    - Tipo: ForeignKey (definido en el modelo ``Recomendacion``)

    - Etiqueta: "Sonda"

    - Widget: Select

    - Descripción: Permite seleccionar una sonda relacionada con la recomendación.

4. ``fecha_inicio``

    - Tipo: DateTimeField (definido en el modelo ``Recomendacion``)

    - Etiqueta: "Fecha de Inicio"

    - Widget: DateTimeInput (con tipo de entrada 'date' y min="1920-01-01")

    - Descripción: Permite seleccionar la fecha de inicio de la recomendación.

5. ``sector``

    - Tipo: CharField (definido en el modelo ``Recomendacion``)

    - Etiqueta: "Sector"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el sector relacionado con la recomendación.

6. ``azimut``

    - Tipo: IntegerField (definido en el modelo ``Recomendacion``)

    - Etiqueta: "Azimut"

    - Widget: NumberInput (con min=0, max=360, step=1)

    - Descripción: Permite ingresar el valor de azimut asociado a la recomendación.

7. ``inclinacion``

    - Tipo: IntegerField (definido en el modelo ``Recomendacion``)

    - Etiqueta: "Inclinación"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el valor de inclinación de la recomendación.

8. ``largo_programado``

    - Tipo: IntegerField (definido en el modelo ``Recomendacion``)

    - Etiqueta: "Largo Programado"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el largo programado de la recomendación.

9. ``largo_real``

    - Tipo: IntegerField (definido en el modelo ``Recomendacion``)

    - Etiqueta: "Largo Real"

    - Widget: TextInput (con clase CSS textinput form-control, solo lectura)

    - Descripción: Permite ingresar el largo real de la recomendación. Este campo es solo lectura y su valor predeterminado es 0.

10. ``este``

     - Tipo: FloatField (definido en el modelo ``Recomendacion``)

     - Etiqueta: "Este"

     - Widget: TextInput (con clase CSS textinput form-control)

     - Descripción: Permite ingresar el valor del este de la recomendación.

11. ``norte``

     - Tipo: FloatField (definido en el modelo ``Recomendacion``)

     - Etiqueta: "Norte"

     - Widget: TextInput (con clase CSS textinput form-control)

     - Descripción: Permite ingresar el valor del norte de la recomendación.

12. ``cota``

     - Tipo: FloatField (definido en el modelo ``Recomendacion``)

     - Etiqueta: "Cota"

     - Widget: TextInput (con clase CSS textinput form-control)

     - Descripción: Permite ingresar el valor de la cota de la recomendación.

Consideraciones Adicionales
---------------------------

- Diseño: Se utilizan widgets personalizados para mejorar la presentación y la funcionalidad de los campos, como el widget ``DateTimeInput`` para ``fecha_inicio`` y el widget ``NumberInput`` para ``azimut``.

- Validación:
  
    - El campo ``azimut`` tiene una validación personalizada para asegurarse de que el valor esté entre 0 y 360.
    - Se realizan validaciones generales para asegurar que los campos obligatorios estén presentes y no vacíos.
    - El campo ``largo_real`` es solo lectura y tiene un valor predeterminado de 0.
    - Los campos ``azimut``, ``largo_programado``, ``largo_real``, ``este``, ``norte``, y ``cota`` no son obligatorios.

- Modelo: Este formulario está basado en el modelo ``Recomendacion`` y permite gestionar diversos parámetros relacionados con pozos, sondas, y características geográficas de la recomendación.

FormPerforista
==============

Este formulario se utiliza para gestionar la información relacionada con el modelo ``Perforistas`` dentro del sistema Django. Permite ingresar los detalles del perforista asignado.

Campos del Formulario
---------------------

1. ``perforista``

    - Tipo: CharField (definido en el modelo ``Perforistas``)

    - Etiqueta: "Perforista"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar el nombre o identificación del perforista.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza un widget de entrada de texto con la clase ``textinput form-control`` para una presentación clara y coherente con el resto de los formularios.

- Modelo: Este formulario está basado en el modelo ``Perforistas`` y se utiliza para gestionar los detalles del perforista.

FormMaterialesSonda
===================

Este formulario se utiliza para gestionar la información relacionada con el modelo ``MaterialesSonda`` dentro del sistema Django. Permite seleccionar o ingresar el material asociado a una sonda.

Campos del Formulario
----------------------

1. ``material``

    - Tipo: CharField (definido en el modelo ``MaterialesSonda``)

    - Etiqueta: "Material"

    - Widget: TextInput (con clase CSS textinput form-control)

    - Descripción: Permite ingresar o seleccionar el material asociado a la sonda.

Consideraciones Adicionales
---------------------------

- Diseño: Se utiliza un widget de entrada de texto con la clase ``textinput form-control`` para una presentación clara y coherente con el resto de los formularios.

- Modelo: Este formulario está basado en el modelo ``MaterialesSonda`` y se utiliza para gestionar los detalles del material utilizado en una sonda.

Vistas (views.py)
-----------------

Define la lógica para mostrar y procesar información en la interfaz.

select
======

Esta vista maneja la selección de la sección a la que un usuario debe ser redirigido, basándose en la configuración de su perfil. Dependiendo de las secciones asignadas al usuario (vehicular, sondaje, prevención o inventario), se redirige al dashboard correspondiente.

Decorador
---------

- ``@login_required``:  
   Este decorador asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
-------

La vista ``select`` realiza los siguientes pasos:

1. **Obtenemos el perfil del usuario**:  
   Se recupera el perfil del usuario actual desde el modelo ``UsuarioProfile`` mediante el usuario autenticado (`request.user`).

2. **Verificación de secciones asignadas**:  
   Dependiendo de las secciones que el usuario tiene habilitadas en su perfil (``seccionVehicular``, ``seccionSondaje``, ``seccionPrevencion`` y ``seccionInventario``), se ejecuta una de las siguientes acciones:
   
   - Si el usuario tiene habilitada la sección ``Vehicular`` (``seccionVehicular == 'Si'``), se guarda en la sesión que la sección activa es ``vehicular`` y se redirige al dashboard de vehículos mediante ``redirect('dashboard')``.
   
   - Si el usuario tiene habilitada la sección ``Sondaje`` (``seccionSondaje == 'Si'``), se guarda en la sesión que la sección activa es ``sondaje`` y se redirige al dashboard de sondajes mediante ``redirect('dashboardSondaje')``.
   
   - Si el usuario tiene habilitada la sección ``Prevención`` (``seccionPrevencion == 'Si'``), se guarda en la sesión que la sección activa es ``prevencion`` y se redirige al dashboard de prevención mediante ``redirect('dashboardPrevencion')``.

   - Si el usuario tiene habilitada la sección ``Inventario`` (``seccionInventario == 'Si'``), se guarda en la sesión que la sección activa es ``inventario`` y se redirige al dashboard de inventario mediante ``redirect('dashboardInventario')``.
   
3. **Caso sin secciones asignadas**:  
   Si el usuario no tiene ninguna sección asignada (todas las secciones tienen el valor ``'No'``), se muestra una página con un mensaje informando que no tiene secciones asignadas. Se recomienda que contacte al administrador para resolver el problema. El mensaje se pasa al template ``main/select.html`` con el siguiente contexto:
   
   - ``mensajeuno``: "Sin secciones asignadas".
   - ``mensajedos``: "Contacte al Administrador".
   - ``valor``: ``False`` para indicar que no hay secciones disponibles.
   
4. **Caso con secciones asignadas**:  
   Si el usuario tiene al menos una sección habilitada, se le muestra un formulario de selección de sección (``FormSeleccionSeccion``) junto con su perfil de usuario. El formulario se pasa al contexto junto con la variable ``valor`` establecida a ``True``.

5. **Renderización del template**:  
   Finalmente, se renderiza el template ``main/select.html`` con los datos apropiados, que permiten al usuario ver el mensaje de las secciones o el formulario de selección.

Retorno
-------

La vista retorna las siguientes respuestas dependiendo de la situación:

- Si el usuario tiene secciones asignadas, se redirige al dashboard correspondiente:
  
  - ``redirect('dashboard')`` para el dashboard vehicular.
  - ``redirect('dashboardSondaje')`` para el dashboard de sondajes.
  - ``redirect('dashboardPrevencion')`` para el dashboard de prevención.

- Si el usuario no tiene secciones asignadas, se renderiza el template ``main/select.html`` con un mensaje informativo:
  
  - Contexto: ``{'mensajeuno': "Sin secciones asignadas", 'mensajedos': "Contacte al Administrador", 'valor': False}``.
  
- Si el usuario tiene secciones asignadas y debe elegir una, se renderiza el template ``main/select.html`` con un formulario de selección de sección y el contexto:
  
  - ``{'valor': True, 'usuario': user, 'formseleccionar': FormSeleccionSeccion(usuario_profile=user)}``.

selectOption
=============

Esta vista maneja la selección de la sección activa por parte del usuario y redirige a la página correspondiente dependiendo de la sección elegida.

Decorador
----------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
-------

La vista ``selectOption`` realiza los siguientes pasos:

1. **Verificación del método de solicitud**:  
   Si la solicitud es de tipo ``POST``, se obtiene el valor de ``seccion_select`` desde los datos del formulario. Este valor indica la sección seleccionada por el usuario.

2. **Redirección según la sección seleccionada**:  
   Dependiendo del valor de ``seccion_select``, se realiza una de las siguientes acciones:
   
   - Si el valor es ``'vehicular'``, se guarda en la sesión que la sección activa es ``vehicular`` (`request.session['seccion'] = 'vehicular'`) y se redirige al dashboard vehicular mediante ``redirect('dashboard')``.
   
   - Si el valor es ``'sondaje'``, se guarda en la sesión que la sección activa es ``sondaje`` (`request.session['seccion'] = 'sondaje'`) y se redirige al dashboard de sondajes mediante ``redirect('dashboardSondaje')``.
   
   - Si el valor es ``'prevencion'``, se guarda en la sesión que la sección activa es ``prevencion`` (`request.session['seccion'] = 'prevencion'`) y se redirige al dashboard de prevención mediante ``redirect('dashboardPrevencion')``.

   - Si el valor es ``'inventario'``, se guarda en la sesión que la sección activa es ``inventario`` (`request.session['seccion'] = 'inventario'`) y se redirige al dashboard de inventario mediante ``redirect('dashboardInventario')``.

3. **Redirección en caso de solicitud no POST**:  
   Si la solicitud no es de tipo ``POST``, se redirige al usuario al formulario de selección de sección (``select``) mediante ``redirect('select')``.

Retorno
-------

La vista retorna las siguientes respuestas dependiendo de la solicitud:

- Si la solicitud es ``POST`` y se selecciona una sección válida (vehicular, sondaje, prevención o inventario), la vista redirige al dashboard correspondiente:
  
  - ``redirect('dashboard')`` para la sección vehicular.
  - ``redirect('dashboardSondaje')`` para la sección de sondaje.
  - ``redirect('dashboardPrevencion')`` para la sección de prevención.
  - ``redirect('dashboardInventario')`` para la sección de inventario.
  
- Si la solicitud no es ``POST``, se redirige al formulario de selección de sección:
  - ``redirect('select')`` para la vista de selección de sección.

dashboard
=========

Esta vista muestra el panel principal del área vehicular, proporcionando información sobre los vehículos, mantenimientos, y documentos relacionados, entre otros.

Decorador
---------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
-------

La vista ``dashboard`` realiza los siguientes pasos:

1. **Obtención de datos de vehículos**:  
   Se recopila información sobre los vehículos asignados que están activos. Se obtiene el detalle por tipo de vehículo y la cantidad de vehículos por faena.

2. **Ordenación de datos**:  
   Los datos obtenidos sobre los vehículos asignados, los vehículos con vencimientos próximos, y los usuarios son ordenados por la diferencia de días hasta su vencimiento.

3. **Recopilación de información de vehículos**:  
   Se obtiene información de los vehículos que tienen un vencimiento en los próximos 120 días, como su placa patente, tipo de vehículo, fecha de vencimiento y días restantes.

4. **Recopilación de información de arrendamientos de vehículos**:  
   Se obtiene información sobre los vehículos arrendados, calculando los días restantes hasta la fecha final de arriendo.

5. **Obtención de datos de usuarios**:  
   Se recopila información de los usuarios con fechas de vencimiento próximas (como la cédula de identidad o licencias) y se ordenan por la diferencia de días.

6. **Obtener el último kilómetro de cada vehículo y horómetro de maquinaria**:  
   Se obtiene el último registro de kilometraje de cada vehículo y el último horómetro de cada maquinaria.

7. **Obtención de solicitudes de mantenimiento**:  
   Se obtienen las solicitudes de mantenimiento pendientes, excluyendo aquellas con progreso '4' o '5' (es decir, completadas).

8. **Contexto para el template**:  
   Se pasan los siguientes datos al contexto para ser renderizados en el template:
   
   - ``detalle_por_faena_json``: Información sobre los vehículos por faena.
   - ``fechavencimientodocumentacionvehiculos``: Datos sobre los vehículos y sus fechas de vencimiento.
   - ``fechavencimientoarriendovehiculos``: Datos sobre los vehículos arrendados y sus fechas de vencimiento.
   - ``fechavencimientodocumentacionusuarios``: Información sobre los usuarios y sus fechas de vencimiento.
   - ``last_users``: Los últimos usuarios que han iniciado sesión.
   - ``ultimo_kilometraje_por_vehiculo``: El último registro de kilometraje de los vehículos.
   - ``ultimo_horometro_por_maquinaria``: El último registro de horómetro de las maquinarias.
   - ``fechas_importantes``: Fechas importantes ordenadas.
   - ``mantenimientos_vehiculos``: Solicitudes de mantenimiento pendientes.

Retorno
-------

La vista retorna el siguiente contexto para renderizar el template ``homevehicular.html``:

.. code-block:: bash

   {
       "detalle_por_faena_json": detalle_por_faena_dict,
       "sidebar": "dashboard",
       "fechavencimientodocumentacionvehiculos": data_vehiculos,
       "fechavencimientoarriendovehiculos": data_arriendo,
       "fechavencimientodocumentacionusuarios": data_usuarios,
       "last_users": last_users,
       "ultimo_kilometraje_por_vehiculo": ultimo_kilometraje_por_vehiculo,
       "ultimo_horometro_por_maquinaria": ultimo_horometro_por_maquinaria,
       "fechas_importantes": fechas_importantes_ordenadas,
       "mantenimientos_vehiculos": data_solicitudes
   }

dashboardSondaje
================

Esta vista muestra el panel principal para la sección de sondaje.

Decorador
---------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
-------

La vista ``dashboardSondaje`` realiza los siguientes pasos:

1. **Establecer sección en la sesión**:  
   Se guarda en la sesión la clave ``seccion`` con el valor ``sondaje`` para hacer un seguimiento de la sección seleccionada.

2. **Contexto para el template**:  
   Se pasa el valor ``sondaje`` al contexto con la clave ``seccion`` para ser utilizado en el template.

Retorno
-------

La vista retorna el siguiente contexto para renderizar el template ``homesondaje.html``:

.. code-block:: bash
   
   {
      'seccion': 'sondaje',
   }

dashboardPrevencion
===================

Esta vista maneja la carga del dashboard de la sección de prevención.

Decorador
---------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

Función
-------

La vista ``dashboardPrevencion`` realiza los siguientes pasos:

1. **Establecimiento de la sección activa**:  
   La vista establece en la sesión que la sección activa es ``'prevencion'`` (`request.session['seccion'] = 'prevencion'`).

2. **Contexto de la vista**:  
   Se crea un diccionario ``context`` con la clave ``'seccion'`` que tiene el valor ``'prevencion'``. Este contexto se pasa al template para su renderizado.

3. **Renderizado del template**:  
   La vista renderiza el template ``main/homeprevencion.html``, pasando el contexto con los datos relevantes para la sección de prevención.

Retorno
-------

La vista retorna una respuesta renderizada del template ``main/homeprevencion.html`` con el contexto establecido.

manage_genders
==============

Esta vista gestiona la visualización de los géneros registrados en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Garantiza que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador verifica que el usuario tenga uno de los roles permitidos para acceder a esta vista (administrador de sondaje, base de datos o supervisor).

Función
--------

La vista ``manage_genders`` realiza las siguientes acciones:

1. **Manejo de mensajes**:  
   La vista obtiene y marca como usados los mensajes almacenados en la solicitud (`storage = messages.get_messages(request)` y `storage.used = True`).

2. **Obtención de géneros**:  
   Se recuperan todos los registros de géneros de la base de datos, ordenados por ``id`` (`generos = list(Genero.objects.all().order_by('id'))`).

3. **Contexto para el template**:  
   Se crea un diccionario ``context`` que contiene los siguientes datos:
   
   - ``generos``: Lista de objetos de género.
   - ``sidebarsubmenu``: Valor ``'manage_genders'``, que se utiliza para resaltar la opción activa en la barra lateral.
   - ``sidebarmenu``: Valor ``'manage_users'``, que se utiliza para resaltar el submenú de usuarios en la barra lateral.
   - ``sidebarmain``: Valor ``'manage_system'``, que se utiliza para resaltar el menú principal de gestión del sistema.

4. **Renderizado del template**:  
   La vista renderiza el template ``pages/maintainer/manage_genders.html`` con el contexto creado.

Retorno
-------

La vista retorna una respuesta renderizada del template ``pages/maintainer/manage_genders.html``, pasando el contexto con los géneros y la información de la barra lateral.

new_gender
============

Esta vista permite la creación de nuevos géneros en el sistema.

Decoradores
------------

- ``@login_required``:  
   Garantiza que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador verifica que el usuario tenga uno de los roles permitidos para acceder a esta vista (administrador de sondaje, base de datos o supervisor).

Función
--------

La vista ``new_gender`` realiza las siguientes acciones:

1. **Creación del contexto**:  
   La vista crea un diccionario ``context`` con los siguientes datos:
   
   - ``formgenero``: La clase del formulario ``FormGenero`` que será utilizada en el template para mostrar el formulario de creación de género.
   - ``sidebarsubmenu``: Valor ``'manage_genders'``, que se utiliza para resaltar la opción activa en la barra lateral.
   - ``sidebarmenu``: Valor ``'manage_users'``, que se utiliza para resaltar el submenú de usuarios en la barra lateral.
   - ``sidebarmain``: Valor ``'manage_system'``, que se utiliza para resaltar el menú principal de gestión del sistema.

2. **Renderizado del template**:  
   La vista renderiza el template ``pages/maintainer/new_gender.html`` con el contexto creado, el cual incluye el formulario y los datos necesarios para la barra lateral.

Retorno
-------

La vista retorna una respuesta renderizada del template ``pages/maintainer/new_gender.html``, pasando el contexto con el formulario y la información de la barra lateral.

save_new_gender
=================

Esta vista maneja la creación de un nuevo género en el sistema, utilizando los datos enviados a través de un formulario.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``save_new_gender`` realiza las siguientes acciones:

1. **Procesamiento del formulario**:  
   Si la solicitud es de tipo ``POST``, la vista toma los datos enviados y los pasa al formulario ``FormGenero``.
   
2. **Validación del formulario**:  
   Si el formulario es válido, la vista:
   
   - Crea un nuevo objeto ``Genero`` con los valores proporcionados en el formulario (campo ``genero``) y marca el ``status`` como ``True``. 
   - Asigna el nombre del usuario que realizó la acción como ``creador``.
   - Guarda el nuevo objeto ``Genero`` en la base de datos.

3. **Notificación por correo**:  
   Tras guardar el nuevo género, se llama a la función ``notificacion_mantenedor_email`` para enviar una notificación por correo electrónico sobre el nuevo género creado.

4. **Respuesta exitosa**:  
   Si todo es correcto, la vista retorna una respuesta JSON indicando que la operación fue exitosa con el siguiente contenido:
   
   .. code-block:: json

      {
         "success": true
      }

status_gender
==============

Esta vista maneja el cambio de estado (habilitado/deshabilitado) de un género en el sistema, a través de una solicitud ``POST``.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``status_gender`` realiza las siguientes acciones:

1. **Obtener el género**:  
   Si la solicitud es de tipo ``POST``, la vista obtiene el género que corresponde al ``id`` proporcionado en los datos del formulario. Este ``id`` se usa para buscar el género en la base de datos.

2. **Verificación del estado**:  
   Se verifica si el ``status`` del género es ``True`` (habilitado). Dependiendo del estado actual, se realiza lo siguiente:
   - Si el género está habilitado (``status=True``), se deshabilita (``status=False``) y se envía una notificación por correo con el mensaje "Generos deshabilitado".
   - Si el género está deshabilitado (``status=False``), se habilita (``status=True``) y se envía una notificación por correo con el mensaje "Generos habilitado".

3. **Mensajes y redirección**:  
   Después de actualizar el estado, se muestra un mensaje de éxito usando ``messages.success`` indicando que el género fue habilitado o deshabilitado correctamente, dependiendo de la acción realizada.
   - Se redirige al usuario a la página ``manage_genders``.

Retorno
-------

- Si la operación se realiza correctamente, la vista redirige a la página de gestión de géneros (``manage_genders``).
- Los mensajes de éxito sobre la acción (habilitación o deshabilitación) se muestran al usuario.

manage_cities
==============

Esta vista maneja la visualización de las ciudades registradas en el sistema.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``manage_cities`` realiza lo siguiente:

1. **Obtener las ciudades**:  
   Se obtiene una lista de todas las ciudades de la base de datos, ordenadas por su ``id``. Los objetos ``Ciudad`` se recuperan a través de la consulta ``Ciudad.objects.all().order_by('id')``.

2. **Preparación del contexto**:  
   El contexto para el template se prepara con:
   - **``ciudades``**: La lista de todas las ciudades recuperadas de la base de datos.
   - **``sidebarsubmenu``**: Valor que indica que la opción actual seleccionada en el menú lateral es la gestión de ciudades.
   - **``sidebarmenu``**: Valor que indica que la opción principal del menú lateral es la gestión de usuarios.
   - **``sidebarmain``**: Valor que indica que la opción principal del menú es la gestión del sistema.

3. **Renderización de la vista**:  
   Finalmente, la vista se renderiza con el template ``pages/maintainer/manage_cities.html`` y el contexto preparado anteriormente.

Retorno
-------

- La vista renderiza el template ``manage_cities.html`` con la lista de ciudades y el contexto necesario para la página de gestión de ciudades.
- La vista incluye los elementos del menú de navegación adecuados para reflejar que el usuario está en la sección de "Gestión de Ciudades".

new_city
=========

Esta vista maneja la creación de una nueva ciudad en el sistema.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``new_city`` realiza lo siguiente:

1. **Preparación del formulario**:  
   Se prepara un formulario de tipo ``FormCiudad``, que es el formulario que el usuario deberá llenar para crear una nueva ciudad. Este formulario es pasado al contexto.

2. **Preparación del contexto**:  
   El contexto para el template se prepara con:
   - **``formciudad``**: El formulario de ``FormCiudad`` para la creación de una nueva ciudad.
   - **``sidebarsubmenu``**: Valor que indica que la opción actual seleccionada en el menú lateral es la gestión de ciudades.
   - **``sidebarmenu``**: Valor que indica que la opción principal del menú lateral es la gestión de usuarios.
   - **``sidebarmain``**: Valor que indica que la opción principal del menú es la gestión del sistema.

3. **Renderización de la vista**:  
   Finalmente, la vista se renderiza con el template ``pages/maintainer/new_city.html`` y el contexto preparado anteriormente.

Retorno
-------

- La vista renderiza el template ``new_city.html`` con el formulario y el contexto adecuado para la creación de una nueva ciudad.
- La vista incluye los elementos del menú de navegación necesarios para reflejar que el usuario está en la sección de "Gestión de Ciudades".

save_new_city
==============

Esta vista maneja el proceso de guardado de una nueva ciudad en el sistema.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``save_new_city`` realiza lo siguiente:

1. **Verificación del método POST**:  
   Si la solicitud es de tipo ``POST``, lo que indica que el usuario ha enviado un formulario, se procede a procesar los datos.

2. **Creación de una nueva ciudad**:  
   Si el formulario recibido es válido, se procede a crear un nuevo objeto de la clase ``Ciudad`` con los datos proporcionados en el formulario, que incluyen:
   
   - **``ciudad``**: El nombre de la ciudad.
   - **``status``**: Se establece como ``True`` para habilitar la ciudad de manera predeterminada.
   - **``creador``**: Se asigna el nombre completo del usuario que está creando la ciudad.

3. **Guardado de la ciudad**:  
   La ciudad recién creada se guarda en la base de datos.

4. **Notificación por correo electrónico**:  
   Después de guardar la ciudad, se envía una notificación por correo electrónico al mantenedor, indicando que se ha creado una nueva ciudad.

5. **Respuesta JSON**:  
   Si la ciudad se guarda correctamente, se devuelve una respuesta en formato JSON con el siguiente contenido:
   
   - ``{'success': True}``: Indica que el proceso se completó con éxito.

6. **Redirección en caso de error**:  
   Si la solicitud no es de tipo ``POST``, la vista redirige al usuario a la página para crear una nueva ciudad.

Retorno
-------

- La vista devuelve una respuesta en formato JSON con el estado de la operación. En caso de éxito, retorna ``{'success': True}``.
- Si la solicitud no es válida o no es de tipo ``POST``, se redirige al usuario a la vista ``new_city``.

status_city
============

Esta vista maneja el cambio de estado (habilitar/deshabilitar) de una ciudad existente en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``status_city`` realiza lo siguiente:

1. **Verificación del método POST**:  
   La vista maneja únicamente solicitudes de tipo ``POST``, lo que indica que el cambio de estado se solicita mediante un formulario o una acción.

2. **Obtención de la ciudad**:  
   Se obtiene el objeto de la ciudad que se desea modificar utilizando el ``id`` proporcionado en la solicitud POST.

3. **Cambio de estado**:
   
   - Si el estado actual de la ciudad es ``True`` (habilitada), la ciudad se deshabilita actualizando el campo ``status`` a ``False``.
   - Si el estado actual de la ciudad es ``False`` (deshabilitada), la ciudad se habilita actualizando el campo ``status`` a ``True``.

4. **Notificación por correo electrónico**:  
   Después de modificar el estado de la ciudad, se envía una notificación por correo electrónico al mantenedor para informar sobre el cambio de estado de la ciudad.

5. **Mensajes de éxito**:  
   Se muestra un mensaje de éxito al usuario que indica si la ciudad fue habilitada o deshabilitada correctamente, utilizando el sistema de mensajes de Django.

6. **Redirección**:  
   Después de completar la acción, se redirige al usuario a la vista ``manage_cities``, donde se muestran todas las ciudades gestionadas.

Retorno
-------

- La vista redirige al usuario a la página ``manage_cities`` después de realizar el cambio de estado de la ciudad.

manage_nationalities
====================

Esta vista maneja la visualización de todas las nacionalidades registradas en el sistema.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``manage_nationalities`` realiza lo siguiente:

1. **Obtención de las nacionalidades**:  
   Se obtienen todas las nacionalidades registradas en el sistema utilizando el modelo ``Nacionalidad``. Se ordenan por el campo ``id`` de manera ascendente.

2. **Limpieza de mensajes previos**:  
   Utiliza el sistema de mensajes de Django para limpiar cualquier mensaje anterior y permitir la visualización de nuevos mensajes (si corresponde).

3. **Contexto para la plantilla**:  
   Se crea un diccionario ``context`` con la siguiente información:
   - ``nacionalidades``: Una lista de todas las nacionalidades obtenidas.
   - ``sidebarsubmenu``: Valor que indica la sección activa en la barra lateral, en este caso, 'manage_nationalities'.
   - ``sidebarmenu``: Valor que indica el menú principal activo, en este caso, 'manage_users'.
   - ``sidebarmain``: Valor que indica la categoría principal del sistema, en este caso, 'manage_system'.

4. **Renderización de la plantilla**:  
   Se renderiza la plantilla ``manage_nationalities.html`` y se pasa el contexto para su visualización.

Retorno
-------

- La vista renderiza y muestra la página ``manage_nationalities.html`` con la lista de nacionalidades disponibles y otros datos relevantes.

new_nationality
================

Esta vista maneja la visualización del formulario para la creación de una nueva nacionalidad en el sistema.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``new_nationality`` realiza lo siguiente:

1. **Contexto para la plantilla**:  
   Se crea un diccionario ``context`` con la siguiente información:
   - ``formnacionalidad``: El formulario ``FormNacionalidad``, que se utiliza para crear una nueva nacionalidad.
   - ``sidebarsubmenu``: Valor que indica la sección activa en la barra lateral, en este caso, 'manage_nationalities'.
   - ``sidebarmenu``: Valor que indica el menú principal activo, en este caso, 'manage_users'.
   - ``sidebarmain``: Valor que indica la categoría principal del sistema, en este caso, 'manage_system'.

2. **Renderización de la plantilla**:  
   Se renderiza la plantilla ``new_nationality.html`` y se pasa el contexto para su visualización.

Retorno
-------

- La vista renderiza y muestra la página ``new_nationality.html`` con el formulario para la creación de una nueva nacionalidad y otros datos relevantes.

save_new_nationality
=====================

Esta vista maneja el guardado de una nueva nacionalidad en el sistema. El formulario se envía a través de una solicitud POST y, si es válido, se crea una nueva nacionalidad.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``save_new_nationality`` realiza lo siguiente:

1. **Verificación del método de solicitud**:  
   La vista solo responde a solicitudes ``POST``. Si la solicitud no es ``POST``, se redirige a la página de creación de una nueva nacionalidad.

2. **Procesamiento del formulario**:  
   
   - Si el formulario ``FormNacionalidad`` enviado con los datos es válido:
  
     - Se crea una nueva instancia del modelo ``Nacionalidad`` con los siguientes datos:
  
       - ``nacionalidad``: El nombre de la nacionalidad enviado en el formulario.
       - ``status``: Establece el estado como ``True`` (habilitado).
       - ``creador``: Nombre completo del usuario que crea la nacionalidad.
  
   - La nueva nacionalidad se guarda en la base de datos.

3. **Notificación por correo electrónico**:  
   Después de guardar la nacionalidad, se envía una notificación por correo electrónico al mantenedor, indicando que la nacionalidad ha sido creada.

Retorno
-------

- Si el formulario es válido y la nacionalidad se guarda correctamente, la vista devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, redirige al usuario a la página de creación de una nueva nacionalidad.

status_nationality
==================

Esta vista maneja el cambio de estado de una nacionalidad, habilitándola o deshabilitándola según su estado actual. La acción se realiza mediante una solicitud POST.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Este decorador garantiza que solo los usuarios con uno de los roles permitidos (administrador de sondaje, base de datos o supervisor) puedan acceder a la vista.

Función
--------

La vista ``status_nationality`` realiza lo siguiente:

1. **Verificación del método de solicitud**:  
   La vista solo responde a solicitudes ``POST``. Si la solicitud no es ``POST``, no realiza ninguna acción.

2. **Obtención de la nacionalidad y cambio de estado**:  
   - La vista obtiene la nacionalidad correspondiente al ID proporcionado en la solicitud POST.
   - Si la nacionalidad está habilitada (``status=True``), se deshabilita actualizándola a ``status=False``.
   - Si la nacionalidad está deshabilitada (``status=False``), se habilita actualizándola a ``status=True``.

3. **Notificación por correo electrónico**:  
   Después de cambiar el estado de la nacionalidad, se envía una notificación por correo electrónico al mantenedor, indicando que la nacionalidad ha sido habilitada o deshabilitada.

4. **Mensajes de éxito**:  
   - Si la nacionalidad se deshabilita, se muestra un mensaje de éxito indicando que la nacionalidad ha sido deshabilitada correctamente.
   - Si la nacionalidad se habilita, se muestra un mensaje de éxito indicando que la nacionalidad ha sido habilitada correctamente.

Retorno
-------

- Después de realizar la actualización, la vista redirige a la página de administración de nacionalidades, ``'manage_nationalities'``.

manage_years
=============

Esta vista permite la gestión de los años disponibles en el sistema, mostrando una lista de ellos y proporcionando una interfaz para su administración.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@admin_required``:  
   Este decorador garantiza que solo los usuarios con privilegios de administrador puedan acceder a la vista.

Función
--------

La vista ``manage_years`` realiza lo siguiente:

1. **Obtención de los años**:  
   Se obtienen todos los registros de años (``Ano``) desde la base de datos, ordenados por su identificador (ID).

2. **Almacenamiento de mensajes**:  
   - Se gestionan los mensajes del sistema mediante el objeto ``storage``. Esto permite mostrar mensajes relevantes en la interfaz de usuario, si es necesario.

3. **Preparación del contexto**:  
   El contexto se prepara con los años obtenidos y los parámetros necesarios para la plantilla:
   - ``anos``: Lista de los años disponibles.
   - ``sidebarsubmenu``: Establece el subtítulo del menú lateral como ``'manage_years'``.
   - ``sidebarmenu``: Establece el título del menú lateral principal como ``'manage_vehicles'``.
   - ``sidebarmain``: Establece el título principal del menú lateral como ``'manage_system'``.

4. **Renderizado de la plantilla**:  
   Se renderiza la plantilla ``'pages/maintainer/manage_years.html'`` con el contexto preparado, mostrando la lista de años.

Retorno
-------

- La vista retorna el renderizado de la plantilla con la información necesaria para gestionar los años disponibles en el sistema.

new_year
=========

Esta vista permite crear un nuevo año en el sistema mediante un formulario.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@admin_required``:  
   Este decorador garantiza que solo los usuarios con privilegios de administrador puedan acceder a la vista.

Función
--------

La vista ``new_year`` realiza lo siguiente:

1. **Preparación del formulario**:  
   Se prepara el formulario ``FormAno`` para ser mostrado en la interfaz, permitiendo al usuario ingresar un nuevo año.

2. **Preparación del contexto**:  
   El contexto se prepara con los siguientes datos:
   - ``formano``: El formulario para crear un nuevo año.
   - ``sidebarsubmenu``: Establece el subtítulo del menú lateral como ``'manage_years'``.
   - ``sidebarmenu``: Establece el título del menú lateral principal como ``'manage_vehicles'``.
   - ``sidebarmain``: Establece el título principal del menú lateral como ``'manage_system'``.

3. **Renderizado de la plantilla**:  
   Se renderiza la plantilla ``'pages/maintainer/new_year.html'`` con el contexto preparado, mostrando el formulario para la creación de un nuevo año.

Retorno
-------

- La vista retorna el renderizado de la plantilla con el formulario para crear un nuevo año en el sistema.

save_new_year
==============

Esta vista se encarga de guardar un nuevo año en el sistema mediante un formulario.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@admin_required``:  
   Este decorador garantiza que solo los usuarios con privilegios de administrador puedan acceder a la vista.

Función
--------

La vista ``save_new_year`` realiza lo siguiente:

1. **Validación del formulario**:  
   Si la solicitud es ``POST``, se crea una instancia del formulario ``FormAno`` con los datos recibidos. Si el formulario es válido:

2. **Creación de un nuevo año**:  
   Se crea un nuevo objeto de tipo ``Ano`` utilizando los datos del formulario, incluyendo el valor del año (`ano`), el estado activo (`status=True`), y el creador (`creador`), que es el nombre completo del usuario autenticado.

3. **Guardado en la base de datos**:  
   El nuevo objeto ``Ano`` se guarda en la base de datos.

4. **Envío de notificación**:  
   Se envía una notificación al mantenedor, utilizando la función ``notificacion_mantenedor_email``, informando que se ha creado un nuevo año.

5. **Respuesta JSON**:  
   Si el formulario es válido, la vista retorna una respuesta JSON con el valor ``{'success': True}`` para indicar que el proceso fue exitoso.

6. **Redirección si el formulario no es válido**:  
   Si la solicitud no es ``POST`` o si el formulario no es válido, se redirige al usuario de vuelta a la página de creación de un nuevo año.

Retorno
-------

- La vista retorna una respuesta JSON con el estado de éxito de la operación. Si no es ``POST``, redirige al usuario de vuelta a la vista de creación de un nuevo año.

status_year
============

Esta vista se encarga de habilitar o deshabilitar un año en el sistema según el estado actual del objeto.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@admin_required``:  
   Este decorador garantiza que solo los usuarios con privilegios de administrador puedan acceder a la vista.

Función
--------

La vista ``status_year`` realiza lo siguiente:

1. **Verificación de la solicitud POST**:  
   Si la solicitud es ``POST``, se obtiene el objeto ``Ano`` correspondiente al ``id`` enviado a través de ``request.POST['id']``.

2. **Cambio de estado**:  
   Se verifica si el año está habilitado (``status=True``). Si es así, se actualiza el estado a ``False``, deshabilitando el año. Si el estado es ``False``, se cambia a ``True``, habilitando el año.

3. **Envío de notificación**:  
   Después de realizar el cambio de estado, se envía una notificación utilizando la función ``notificacion_mantenedor_email``, indicando si el año ha sido habilitado o deshabilitado.

4. **Mensajes de éxito**:  
   Se muestran mensajes al usuario con la notificación correspondiente utilizando ``messages.success``. El mensaje varía según si el año ha sido habilitado o deshabilitado.

5. **Redirección**:  
   Finalmente, se redirige al usuario a la página de gestión de años (``manage_years``).

Retorno
-------

- La vista retorna una redirección a la página de gestión de años después de realizar la acción de habilitar o deshabilitar el año.

manage_brands
==============

Esta vista muestra una lista de todas las marcas disponibles en el sistema.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@admin_required``:  
   Este decorador garantiza que solo los usuarios con privilegios de administrador puedan acceder a la vista.

Función
--------

La vista ``manage_brands`` realiza lo siguiente:

1. **Obtención de las marcas**:  
   Se obtienen todas las marcas de la base de datos utilizando el modelo ``Marca`` y se ordenan por ``id``.

2. **Contexto de la vista**:  
   Se crea un contexto que contiene:
   - ``marcas``: La lista de marcas obtenida de la base de datos.
   - ``sidebarsubmenu``: Define el submenu actual de la barra lateral, en este caso, "manage_brands".
   - ``sidebarmenu``: Define el menú principal de la barra lateral, en este caso, "manage_vehicles".
   - ``sidebarmain``: Define el menú principal de la barra lateral, en este caso, "manage_system".

3. **Renderización de la plantilla**:  
   La vista renderiza la plantilla ``pages/maintainer/manage_brands.html``, pasando el contexto como datos para ser utilizados en la plantilla.

Retorno
-------

- La vista retorna una renderización de la plantilla ``manage_brands.html``, mostrando la lista de marcas y la estructura del sistema de navegación.

new_brand
==========

Esta vista se utiliza para mostrar el formulario de creación de una nueva marca.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@admin_required``:  
   Garantiza que solo los usuarios con privilegios de administrador puedan acceder a la vista.

Función
--------

La vista ``new_brand`` realiza lo siguiente:

1. **Contexto de la vista**:  
   Se crea un contexto que contiene:
   - ``formmarca``: El formulario ``FormMarca`` que se muestra para crear una nueva marca.
   - ``sidebarsubmenu``: Define el submenu actual de la barra lateral, en este caso, "manage_brands".
   - ``sidebarmenu``: Define el menú principal de la barra lateral, en este caso, "manage_vehicles".
   - ``sidebarmain``: Define el menú principal de la barra lateral, en este caso, "manage_system".

2. **Renderización de la plantilla**:  
   La vista renderiza la plantilla ``pages/maintainer/new_brand.html``, pasando el contexto con los datos necesarios para el formulario.

Retorno
-------

- La vista retorna una renderización de la plantilla ``new_brand.html``, mostrando el formulario para la creación de una nueva marca.

status_brand
============

Esta vista permite habilitar o deshabilitar el estado de una marca de vehículo.

Decoradores
------------

- ``@login_required``:  
   Asegura que solo los usuarios autenticados puedan acceder a esta vista.

- ``@admin_required``:  
   Garantiza que solo los usuarios con privilegios de administrador puedan acceder a la vista.

Función
--------

La vista ``status_brand`` realiza lo siguiente:

1. **Verifica que la solicitud sea POST**:  
   - Solo permite modificaciones si la solicitud se realiza mediante el método ``POST``.

2. **Obtiene la marca a modificar**:  
   - Se obtiene la instancia de ``Marca`` según el ``id`` recibido en la solicitud.

3. **Cambia el estado de la marca**:  
   - Si la marca está habilitada (``status=True``), se deshabilita (``status=False``).
   - Si la marca está deshabilitada (``status=False``), se habilita (``status=True``).

4. **Envía una notificación**:  
   - Se envía una notificación por correo utilizando ``notificacion_mantenedor_email``.

5. **Muestra un mensaje de éxito**:  
   - Se muestra un mensaje en la interfaz notificando si la marca fue habilitada o deshabilitada.

6. **Redirige a la gestión de marcas**:  
   - La vista redirige a ``manage_brands`` tras completar la acción.

Retorno
-------

- Redirige a la vista ``manage_brands`` luego de cambiar el estado de la marca.

manage_models
=============

Esta vista permite gestionar los modelos de vehículos registrados en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``manage_models`` realiza los siguientes pasos:

1. **Limpieza de mensajes previos**:  
   - Se obtiene la instancia de mensajes de Django y se marca como utilizada para evitar que se muestren mensajes antiguos.

2. **Obtención de modelos**:  
   - Se recuperan todos los registros del modelo ``Modelo`` ordenados por ``id``.

3. **Contexto para la plantilla**:  
   
   - Se prepara un diccionario ``context`` con:
  
     - ``modelos``: Lista de modelos de vehículos.
     - ``sidebarsubmenu``: Indica que se encuentra en la gestión de modelos.
     - ``sidebarmenu``: Categoriza la sección dentro de la gestión de vehículos.
     - ``sidebarmain``: Define la categoría principal de administración del sistema.

4. **Renderizado de la plantilla**:  
   - Se envía el contexto a la plantilla ``pages/maintainer/manage_models.html``.

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/manage_models.html`` con la lista de modelos disponibles.

new_model
=========

Esta vista permite acceder al formulario para registrar un nuevo modelo de vehículo.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``new_model`` realiza los siguientes pasos:

1. **Definición del contexto**:  
   
   - Se prepara un diccionario ``context`` con:
  
     - ``formmodelo``: Instancia del formulario ``FormModelo`` para la creación de un nuevo modelo.
     - ``sidebarsubmenu``: Indica que se encuentra en la gestión de modelos.
     - ``sidebarmenu``: Categoriza la sección dentro de la gestión de vehículos.
     - ``sidebarmain``: Define la categoría principal de administración del sistema.

2. **Renderizado de la plantilla**:  
   - Se envía el contexto a la plantilla ``pages/maintainer/new_model.html``.

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/new_model.html`` con el formulario para crear un nuevo modelo de vehículo.

save_new_model
==============

Esta vista permite registrar un nuevo modelo de vehículo en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``save_new_model`` realiza los siguientes pasos:

1. **Verificación del método HTTP**:  
   
   - Si la solicitud es ``POST``, se procesa el formulario de creación.

2. **Validación del formulario**:  
   
   - Se instancia el formulario ``FormModelo`` con los datos enviados.
   - Si el formulario es válido:
  
     - Se crea un nuevo objeto ``Modelo`` con los datos ingresados.
     - Se asigna el estado ``True`` por defecto.
     - Se registra el usuario que lo creó.
     - Se guarda el nuevo modelo en la base de datos.
     - Se envía una notificación mediante ``notificacion_mantenedor_email``.
     - Se retorna un ``JsonResponse`` con ``{'success': True}``.

3. **Redirección en caso de solicitud GET**: 
    
   - Si la solicitud no es ``POST``, se redirige a la vista ``new_model``.

Retorno
-------

- ``JsonResponse({'success': True})`` si el modelo se crea correctamente.
- Redirección a ``new_model`` si la solicitud no es ``POST`` o el formulario no es válido.

status_model
============

Esta vista permite cambiar el estado de un modelo de vehículo (habilitar o deshabilitar) en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``status_model`` realiza los siguientes pasos:

1. **Verificación del método HTTP**:  

   - Solo procesa solicitudes de tipo ``POST``.

2. **Cambio de estado del modelo**:  
   
   - Se obtiene el modelo de vehículo a partir del ``id`` recibido en la solicitud.
   - Si el modelo está habilitado (``status=True``):
  
     - Se deshabilita (``status=False``).
     - Se envía una notificación indicando que fue deshabilitado.
     - Se muestra un mensaje de éxito.
  
   - Si el modelo está deshabilitado (``status=False``):
  
     - Se habilita (``status=True``).
     - Se envía una notificación indicando que fue habilitado.
     - Se muestra un mensaje de éxito.

3. **Redirección**:  
   
   - Después de cambiar el estado, se redirige a la vista ``manage_models``.

Retorno
-------

- Redirección a ``manage_models`` después de actualizar el estado.

manage_colours
==============

Esta vista permite administrar los colores disponibles en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``manage_colours`` realiza los siguientes pasos:

1. **Gestión de mensajes**:  
   
   - Se obtiene la lista de mensajes almacenados en la sesión y se marca como utilizada.

2. **Obtención de colores**:  
   
   - Se recupera la lista de todos los colores registrados en la base de datos, ordenados por ``id``.

3. **Contexto**:  
   
   - Se crea un diccionario de contexto con:
  
     - ``colores``: Lista de colores obtenida.
     - ``sidebarsubmenu``: Indica la sección activa en la barra lateral.
     - ``sidebarmenu``: Categoría del menú lateral.
     - ``sidebarmain``: Sección principal en el sistema.

4. **Renderizado de la plantilla**:  
   - Se renderiza la plantilla ``pages/maintainer/manage_colours.html`` con el contexto definido.

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/manage_colours.html`` con la lista de colores disponibles.

new_colour
==========

Esta vista permite acceder al formulario para agregar un nuevo color al sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``new_colour`` realiza los siguientes pasos:

1. **Definición del contexto**:  
   
   - Se crea un diccionario de contexto con:
  
     - ``formcolor``: Instancia del formulario ``FormColor`` para la creación de un nuevo color.
     - ``sidebarsubmenu``: Indica la sección activa en la barra lateral.
     - ``sidebarmenu``: Categoría del menú lateral.
     - ``sidebarmain``: Sección principal en el sistema.

2. **Renderizado de la plantilla**:  
   - Se renderiza la plantilla ``pages/maintainer/new_colour.html`` con el contexto definido.

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/new_colour.html`` con el formulario para agregar un nuevo color.

save_new_colour
===============

Esta vista permite guardar un nuevo color en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``save_new_colour`` realiza los siguientes pasos:

1. **Verificación del método HTTP**:  
   - Solo permite solicitudes ``POST``. Si la solicitud es ``GET``, redirige a ``new_colour``.

2. **Validación del formulario**:  

   - Se instancia el formulario ``FormColor`` con los datos recibidos.
   - Si el formulario es válido:
  
     - Se crea un nuevo objeto ``Color`` con:
  
       - ``color``: Valor ingresado en el formulario.
       - ``status``: Se establece en ``True`` por defecto.
       - ``creador``: Nombre completo del usuario autenticado.
  
     - Se guarda el nuevo color en la base de datos.
     - Se envía una notificación mediante ``notificacion_mantenedor_email``.
     - Se retorna una respuesta JSON con ``success: True``.

Retorno
-------

- Si la creación es exitosa, devuelve una respuesta JSON con ``success: True``.
- Si la solicitud no es ``POST``, redirige a ``new_colour``.

status_colour
=============

Esta vista permite habilitar o deshabilitar un color en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``status_colour`` realiza los siguientes pasos:

1. **Verificación del método HTTP**:  
   
   - Solo permite solicitudes ``POST``.

2. **Obtención del color**:  
   
   - Se obtiene el objeto ``Color`` correspondiente al ``id`` enviado en la solicitud.

3. **Cambio de estado**: 
    
   - Si el color está habilitado (``status=True``), se deshabilita (``status=False``).
   - Si el color está deshabilitado (``status=False``), se habilita (``status=True``).
   - Se actualiza la base de datos con el nuevo estado.

4. **Notificación y mensaje de éxito**:  
   
   - Se envía una notificación mediante ``notificacion_mantenedor_email``.
   - Se muestra un mensaje de éxito en la interfaz.

Retorno
-------

- Redirige a la vista ``manage_colours`` tras actualizar el estado del color.

manage_types
=============

Esta vista muestra la lista de tipos de vehículos registrados en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``manage_types`` realiza los siguientes pasos:

1. **Obtención de tipos**:  
   - Se obtienen todos los objetos ``Tipo`` ordenados por ``id``.

2. **Contexto**:  
   - Se pasa la lista de tipos al contexto para ser renderizada en la plantilla.

3. **Renderización**:  
   - La vista renderiza la plantilla ``pages/maintainer/manage_types.html`` con el contexto generado.

Retorno
-------

- Devuelve una respuesta con la plantilla ``manage_types.html`` y el contexto que contiene la lista de tipos.
  
new_type
=========

Esta vista permite a los administradores crear un nuevo tipo de vehículo en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``new_type`` realiza los siguientes pasos:

1. **Contexto**:  
   - Se crea un diccionario de contexto que incluye el formulario ``FormTipo`` para ser utilizado en la plantilla.
   - También se incluyen valores para los menús y submenús de la barra lateral.

2. **Renderización**:  
   - La vista renderiza la plantilla ``pages/maintainer/new_type.html`` con el contexto generado.

Retorno
-------

- Devuelve una respuesta con la plantilla ``new_type.html`` y el contexto que incluye el formulario para crear un nuevo tipo de vehículo.

save_new_type
==============

Esta vista maneja la creación de un nuevo tipo de vehículo y su almacenamiento en la base de datos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``save_new_type`` realiza los siguientes pasos:

1. **Verificación del método de la solicitud**:  
   Si la solicitud es de tipo ``POST``, se procesa el formulario enviado con los datos.

2. **Formulario de validación**:  
   Se valida el formulario ``FormTipo`` con los datos recibidos. Si el formulario es válido:

   - Se crea una nueva instancia de ``Tipo`` con los datos proporcionados por el usuario.
   - Se asigna el estado de ``True`` al nuevo tipo y se guarda el creador (nombre y apellido del usuario actual).
   - El tipo creado se guarda en la base de datos.

3. **Notificación**:  
   Después de guardar el tipo, se envía una notificación por correo electrónico al mantenedor con la información del tipo creado.

4. **Respuesta**:  
   - Si el formulario es válido y el tipo se crea con éxito, se devuelve una respuesta JSON con el valor ``{'success': True}``.
   - Si el formulario no es válido o la solicitud no es ``POST``, se redirige al usuario a la vista ``new_type``.

Retorno
-------

- Devuelve una respuesta JSON con ``{'success': True}`` si el tipo se creó correctamente.
- Si no es una solicitud ``POST`` válida, redirige al usuario a la vista ``new_type``.

status_type
============

Esta vista maneja la habilitación o deshabilitación de un tipo de vehículo en la base de datos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``status_type`` realiza las siguientes acciones:

1. **Verificación del método de la solicitud**:  
   La vista solo responde a solicitudes ``POST``.

2. **Obtención del tipo de vehículo**:  
   Se obtiene el objeto ``Tipo`` de la base de datos usando el ``id`` proporcionado en la solicitud ``POST``.

3. **Verificación del estado del tipo**:  
   Si el estado del tipo es ``True`` (habilitado):

   - El estado del tipo se actualiza a ``False`` (deshabilitado).
   - Se envía una notificación por correo electrónico al mantenedor con el cambio de estado.
   - Se muestra un mensaje de éxito indicando que el tipo de vehículo fue deshabilitado correctamente.

   Si el estado del tipo es ``False`` (deshabilitado):

   - El estado del tipo se actualiza a ``True`` (habilitado).
   - Se envía una notificación por correo electrónico al mantenedor con el cambio de estado.
   - Se muestra un mensaje de éxito indicando que el tipo de vehículo fue habilitado correctamente.

4. **Redirección**:  
   Después de cambiar el estado del tipo, se redirige al usuario a la vista ``manage_types``.

Retorno
-------

- Redirige a la vista ``manage_types`` después de actualizar el estado del tipo de vehículo.
- Se muestra un mensaje de éxito al usuario indicando si el tipo de vehículo fue habilitado o deshabilitado correctamente.

edit_type
==========

Esta vista permite la edición de las opciones de un tipo de vehículo, incluyendo opciones adicionales, técnicas, de documentación, interiores y exteriores.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``edit_type`` realiza las siguientes acciones:

1. **Manejo de la sesión**:  
   La vista intenta recuperar el ``tipo_id`` de la solicitud ``POST``. Si no está presente, utiliza el ``tipo_id`` almacenado previamente en la sesión. Este ``tipo_id`` corresponde al ID del tipo de vehículo a editar.

2. **Obtención del tipo de vehículo**:  
   Se obtiene el objeto ``Tipo`` de la base de datos usando el ``tipo_id`` almacenado en la sesión.

3. **Obtención de opciones relacionadas con el tipo**:  
   Se obtiene el objeto ``OcultarOpcionesVehiculo`` asociado al tipo de vehículo, que contiene las opciones relacionadas con el vehículo.

4. **Formularios de edición**:  
   Se crean instancias de formularios para editar las diferentes opciones relacionadas con el vehículo:

   - ``formocultaropcionesadicional``: Para opciones adicionales del vehículo.
   - ``formocultaropcionestecnica``: Para opciones técnicas del vehículo.
   - ``formocultaropcionesdocumentacion``: Para opciones relacionadas con la documentación del vehículo.
   - ``formocultaropcionesinterior``: Para opciones del interior del vehículo.
   - ``formocultaropcionesexterior``: Para opciones del exterior del vehículo.

   Estos formularios se inicializan con los datos actuales de las opciones de vehículo.

5. **Contexto**:  
   Se prepara el contexto para renderizar la plantilla ``edit_type.html``, incluyendo los formularios, las opciones del vehículo y los valores para el menú lateral de la página.

Retorno
-------

- Renderiza la plantilla ``edit_type.html`` con los formularios para editar las opciones del tipo de vehículo.
- Muestra los datos actuales de las opciones relacionadas con el vehículo en los formularios.

save_edit_type
===============

Esta vista guarda los cambios realizados en las opciones de un tipo de vehículo.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``save_edit_type`` realiza las siguientes acciones:

1. **Verificación del método de solicitud**:  
   Solo se procesa la solicitud si es un ``POST``. Si el método es diferente, redirige a la vista ``edit_type``.

2. **Obtención de la instancia de opciones**:  
   Se obtiene la instancia de ``OcultarOpcionesVehiculo`` asociada al tipo de vehículo que se está editando. Esto se hace usando el ``tipo_vehiculo`` enviado en la solicitud ``POST``. Si no se encuentra la instancia, se lanza un error 404.

3. **Formularios de edición**:  
   Se crean instancias de los formularios para editar las opciones del vehículo con los datos enviados en la solicitud:
   
   - ``formadicional``: Para opciones adicionales del vehículo.
   - ``formtecnica``: Para opciones técnicas del vehículo.
   - ``formdocumentacion``: Para opciones relacionadas con la documentación del vehículo.
   - ``forminterior``: Para opciones del interior del vehículo.
   - ``formexterior``: Para opciones del exterior del vehículo.

   Los formularios se inicializan con la instancia de ``OcultarOpcionesVehiculo`` correspondiente al tipo de vehículo.

4. **Validación y guardado**:  
   Si todos los formularios son válidos, se guardan las modificaciones en la base de datos para cada sección de opciones (adicional, técnica, documentación, interior y exterior).

5. **Notificación**:  
   Después de guardar los cambios, se envía una notificación por correo al mantenedor informando que las opciones del vehículo han sido actualizadas.

6. **Respuesta**:  
   Si los formularios son válidos y se guardan correctamente, la vista devuelve un ``JsonResponse`` con un ``success`` igual a ``True``. Si algún formulario no es válido, se devuelve un ``JsonResponse`` con ``error`` igual a ``True``.

Retorno
-------

- Si todos los formularios son válidos y se guardan correctamente, se devuelve un ``JsonResponse`` con el valor ``{'success': True}``.
- Si alguno de los formularios es inválido, se devuelve un ``JsonResponse`` con el valor ``{'error': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_type``.

manage_mining
==============

Esta vista gestiona las faenas mineras. Muestra una lista de todas las faenas registradas en la base de datos y las organiza para su visualización.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Limita el acceso a usuarios con privilegios de administrador, base de datos o supervisor.

Función
-------

La vista ``manage_mining`` realiza las siguientes acciones:

1. **Obtención de las faenas**:  
   Recupera todas las faenas registradas en la base de datos, ordenadas por su ID.

2. **Contexto**:  
   Se prepara el contexto para renderizar la plantilla ``manage_mining.html``, pasando la lista de faenas y los valores para el menú lateral de la página.

Retorno
-------

- Renderiza la plantilla ``manage_mining.html`` con los datos de las faenas para su visualización.
- Incluye las configuraciones del menú lateral para navegar a otras secciones relacionadas con la administración del sistema.

new_mining
==========

Esta vista permite a los usuarios crear una nueva faena minera. Proporciona un formulario para ingresar los datos relacionados con una nueva faena.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Limita el acceso a usuarios con privilegios de administrador, base de datos o supervisor.

Función
-------

La vista ``new_mining`` realiza las siguientes acciones:

1. **Contexto**:  
   Se prepara el contexto para renderizar la plantilla ``new_mining.html``, pasando el formulario de la nueva faena y los valores para el menú lateral de la página.

Retorno
-------

- Renderiza la plantilla ``new_mining.html``, que contiene el formulario para la creación de una nueva faena minera.
- Incluye las configuraciones del menú lateral para navegar a otras secciones relacionadas con la administración del sistema.

save_new_mining
===============

Esta vista maneja la creación de una nueva faena minera. Valida el formulario enviado a través de una solicitud POST y, si es válido, guarda la nueva faena en la base de datos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Limita el acceso a usuarios con privilegios de administrador, base de datos o supervisor.

Función
-------

La vista ``save_new_mining`` realiza las siguientes acciones:

1. **Validación del Formulario**:  
   Si la solicitud es ``POST``, crea un objeto de formulario ``FormNuevaFaena`` utilizando los datos de la solicitud.
   
2. **Creación de Faena**:  
   Si el formulario es válido, se crea un objeto ``Faena`` con los datos proporcionados: nombre de la faena, descripción, y creador. La faena se guarda en la base de datos.

3. **Notificación**:  
   Después de guardar la faena, se envía una notificación por correo electrónico relacionada con la creación de la faena.

4. **Respuesta JSON**:  
   Si la operación fue exitosa, la vista devuelve un objeto ``JsonResponse`` indicando el éxito de la operación.

Retorno
-------

- Si la solicitud es válida y la faena se guarda correctamente, devuelve un ``JsonResponse`` con el estado de éxito.
- Si la solicitud no es ``POST`` o el formulario no es válido, redirige a la vista ``new_mining``.

status_mining
===============

Esta vista gestiona el cambio de estado (habilitar/deshabilitar) de una faena minera existente. Dependiendo del estado actual de la faena, la vista alterna entre habilitarla o deshabilitarla.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Limita el acceso a usuarios con privilegios de administrador, base de datos o supervisor.

Función
-------

La vista ``status_mining`` realiza las siguientes acciones:

1. **Obtención de Faena**:  
   Si la solicitud es ``POST``, se obtiene el objeto ``Faena`` correspondiente al ``id`` proporcionado en la solicitud.

2. **Cambio de Estado**:  
   
   - Si la faena está habilitada (``status=True``), se deshabilita (se establece ``status=False``) y se envía una notificación por correo electrónico indicando que la faena fue deshabilitada.
   - Si la faena está deshabilitada (``status=False``), se habilita (se establece ``status=True``) y se envía una notificación por correo electrónico indicando que la faena fue habilitada.

3. **Mensajes**:  
   Después de cambiar el estado de la faena, se muestra un mensaje de éxito, indicando si la faena fue habilitada o deshabilitada correctamente.

4. **Redirección**:  
   Después de completar la acción, la vista redirige al usuario a la página de administración de faenas.

Retorno
-------

- La vista redirige a la página de gestión de faenas, ``manage_mining``, después de realizar el cambio de estado.
- Se muestran mensajes de éxito según el cambio realizado (habilitar o deshabilitar).

edit_mining
============

Esta vista permite editar los detalles de una faena minera existente. Los datos de la faena se cargan en un formulario pre-llenado para que el usuario pueda realizar modificaciones.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Limita el acceso a usuarios con privilegios de administrador, base de datos o supervisor.

Función
-------

La vista ``edit_mining`` realiza las siguientes acciones:

1. **Obtención del ID de Faena**:  
   Si la solicitud contiene el ``faena_id`` en los datos ``POST``, se guarda este ``id`` en la sesión para ser usado en la edición. Si no se encuentra en los datos ``POST``, se usa el ``id`` almacenado previamente en la sesión.

2. **Carga de Datos de la Faena**:  
   Se recupera la faena correspondiente al ``id`` almacenado en la sesión. Los datos de esta faena (nombre y descripción) se cargan en un formulario de edición.

3. **Renderización del Formulario**:  
   El formulario ``FormNuevaFaena`` se inicializa con los datos de la faena y se pasa al contexto para renderizarse en la plantilla. El campo ``faena_disabled`` se establece en ``True`` para evitar que el nombre de la faena sea editado.

4. **Contexto**:  
   Además del formulario, se pasan otros valores al contexto:
   
   - ``faena_id``: El ID de la faena que está siendo editada.
   - ``sidebarsubmenu``, ``sidebarmenu``, ``sidebarmain``: Valores de navegación para el menú de la aplicación.

Retorno
-------

- La vista renderiza la plantilla ``pages/maintainer/edit_mining.html`` con el formulario pre-llenado y el contexto adecuado.

save_edit_mining
=================

Esta vista guarda las modificaciones realizadas a una faena minera existente. Se actualiza la descripción de la faena en la base de datos y se notifica al mantenedor de la actualización.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Limita el acceso a usuarios con privilegios de administrador, base de datos o supervisor.

Función
-------

La vista ``save_edit_mining`` realiza las siguientes acciones:

1. **Verificación del Método de Solicitud**:  
   La vista solo procesa solicitudes ``POST``. Si la solicitud no es ``POST``, redirige al usuario a la vista ``edit_mining``.

2. **Obtención de la Faena**:  
   Se obtiene la faena a partir del ``faena_id`` enviado en los datos ``POST`` de la solicitud.

3. **Actualización de la Descripción**:  
   La descripción de la faena se actualiza en la base de datos con el valor enviado en el campo ``descripcion`` del formulario.

4. **Notificación**:  
   Se envía una notificación por correo electrónico al mantenedor indicando que la faena ha sido actualizada.

Retorno
-------

- Si la solicitud es procesada correctamente, se retorna un ``JsonResponse`` con el mensaje ``{'success': True}`` indicando que la operación fue exitosa.
- Si la solicitud no es ``POST``, el usuario es redirigido a la vista ``edit_mining``.

manage_mining_documents
=======================

Esta vista permite visualizar la lista de tipos de documentos asociados a las faenas mineras. Los documentos se presentan ordenados por la fecha de creación.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``manage_mining_documents`` realiza las siguientes acciones:

1. **Obtención de Documentos**:  
   Se recuperan todos los tipos de documentos asociados a las faenas mineras desde la base de datos. Estos documentos se ordenan por la fecha de creación (``fechacreacion``).

2. **Preparación del Contexto**:  
   Se prepara el contexto que será enviado a la plantilla. El contexto contiene los documentos obtenidos, además de las variables para gestionar los menús y submenús en la interfaz de usuario.

Retorno
-------

- La vista retorna la respuesta con el template ``pages/maintainer/manage_mining_documents.html`` junto con el contexto preparado, permitiendo al usuario ver la lista de tipos de documentos mineros.

new_mining_document
====================

Esta vista permite la creación de un nuevo tipo de documento asociado a una faena minera.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Función
-------

La vista ``new_mining_document`` realiza las siguientes acciones:

1. **Preparación del Contexto**:  
   Se prepara el contexto para renderizar la plantilla. Este contexto incluye el formulario para la creación de un nuevo tipo de documento de faena (``FormTipoDocumentoFaena``), junto con las variables para gestionar los menús y submenús en la interfaz de usuario.

Retorno
-------

- La vista retorna la respuesta con el template ``pages/maintainer/new_mining_document.html`` junto con el contexto preparado, mostrando el formulario para crear un nuevo documento de faena minera.

save_new_mining_document
=========================

Esta vista se encarga de guardar un nuevo tipo de documento para una faena minera, verificando si el tipo de documento ya existe para la faena, y si no, lo crea.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Verificación de Existencia**:  
   La vista verifica si el tipo de documento para la faena ya existe mediante el documento y la faena recibidos en la solicitud. Si ya existe, retorna el objeto ``tipo_documento_faena``.

2. **Creación de Tipo de Documento**:  
   Si el tipo de documento no existe, obtiene la faena correspondiente, valida el formulario recibido, y en caso de ser válido, crea el nuevo tipo de documento asociado a la faena. 

3. **Notificación**:  
   Una vez creado el tipo de documento, se envía una notificación sobre su creación.

Retorno
-------

- Si el formulario es válido, se guarda el tipo de documento y se retorna una respuesta JSON indicando el éxito de la operación.
- Si el formulario no es válido, se retorna una respuesta JSON con un mensaje de error.
- Si la solicitud no es un ``POST``, redirige a la vista ``manage_mining_documents``.

status_mining_document
=======================

Esta vista permite habilitar o deshabilitar un tipo de documento asociado a una faena minera.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Verificación del Método**:  
   La vista solo procesa solicitudes ``POST``.  

2. **Obtención del Documento**:  
   Se obtiene el tipo de documento de faena a partir del ``id`` recibido en la solicitud.

3. **Cambio de Estado**:  
   
   - Si el documento está habilitado, se deshabilita.  
   - Si el documento está deshabilitado, se habilita.  

4. **Notificación y Mensaje**:  
   
   - Se envía una notificación sobre el cambio de estado.  
   - Se muestra un mensaje de éxito con la acción realizada.  

Retorno
-------

- Redirige a la vista ``manage_mining_documents`` después de cambiar el estado del documento.  

manage_maintenance_companies
============================

Esta vista permite administrar las empresas de mantenimiento registradas en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Limpieza de Mensajes**:  
   
   - Se obtienen los mensajes almacenados en el sistema.  
   - Se marca como usados para evitar su repetición.  

2. **Obtención de Empresas**:  
   
   - Se consulta la lista de empresas de servicios de mantenimiento ordenadas por ``id``.  

3. **Contexto**:  
   Se envía la información al template con las siguientes variables:  
   
   - ``empresas``: Lista de empresas de mantenimiento.  
   - ``sidebarsubmenu``: Indica la sección activa en el menú lateral.  
   - ``sidebarmenu``: Define la categoría del menú de mantenimiento.  
   - ``sidebarmain``: Sección principal del sistema.  

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/manage_maintenance_companies.html`` con el contexto definido.  

new_maintenance_companie
========================

Esta vista permite acceder al formulario para registrar una nueva empresa de mantenimiento en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Contexto**:  
   Se prepara la información a enviar a la plantilla con las siguientes variables:  
   
   - ``formnuevaempresa``: Instancia del formulario ``FormNuevaEmpresaServicios``.  
   - ``sidebarsubmenu``: Indica la sección activa en el menú lateral.  
   - ``sidebarmenu``: Define la categoría del menú de mantenimiento.  
   - ``sidebarmain``: Sección principal del sistema.  

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/new_maintenance_companie.html`` con el contexto definido.  

save_new_maintenance_companie
=============================

Esta vista permite registrar una nueva empresa de mantenimiento en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Recepción de datos**:  
   
   - Se verifica que la solicitud sea de tipo ``POST``.  
   - Se instancia el formulario ``FormNuevaEmpresaServicios`` con los datos enviados.  

2. **Validación y almacenamiento**:  
   
   - Si el formulario es válido, se crea una nueva instancia del modelo ``EmpresaServicios`` con los datos ingresados:  
     
     - ``empresa``: Nombre de la empresa.  
     - ``rut``: Número de identificación tributaria.  
     - ``direccion``: Dirección de la empresa.  
     - ``telefono``: Número de contacto.  
     - ``descripcion``: Información adicional sobre la empresa.  
     - ``status``: Estado activo por defecto.  
     - ``creador``: Nombre completo del usuario que registra la empresa. 
   
   - Se guarda la instancia en la base de datos.  
   - Se envía una notificación por correo mediante la función ``notificacion_mantenedor_email``.  
   - Se retorna una respuesta JSON con ``success: True``.  

3. **Redirección en caso de error**:  
   
   - Si la solicitud no es ``POST``, se redirige a la vista ``new_maintenance_companie``.  

Retorno
-------

- Si el registro es exitoso, devuelve una respuesta JSON con ``success: True``.  
- Si hay un error, redirige a ``new_maintenance_companie``.  

status_maintenance_companie
===========================

Esta vista permite habilitar o deshabilitar una empresa de mantenimiento.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Recepción de datos**:  
   
   - Se verifica que la solicitud sea de tipo ``POST``.  
   - Se obtiene la empresa de mantenimiento a modificar a partir del ``id`` recibido en la solicitud.  

2. **Cambio de estado**:  
   
   - Si la empresa está habilitada (``status=True``), se actualiza a ``False``.  
   - Si está deshabilitada (``status=False``), se actualiza a ``True``.  
   - Se actualiza el estado de la empresa en la base de datos mediante ``update(status=...)``.  

3. **Notificación y mensaje de éxito**: 
    
   - Se envía una notificación por correo mediante la función ``notificacion_mantenedor_email``.  
   - Se muestra un mensaje de éxito con ``messages.success`` indicando si la empresa fue habilitada o deshabilitada.  

4. **Redirección**:  
   
   - Se redirige a la vista ``manage_maintenance_companies`` tras actualizar el estado.  

Retorno
-------

- Redirige a ``manage_maintenance_companies`` después de actualizar el estado de la empresa.  


edit_maintenance_companie
=========================

Esta vista permite acceder al formulario de edición de una empresa de mantenimiento.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Gestión de sesión**:
  
   - Intenta obtener el ``empresa_id`` desde la solicitud ``POST`` y almacenarlo en la sesión.  
   - Si no se encuentra en ``POST``, se usa el valor previamente almacenado en la sesión.  

2. **Obtención de la empresa**:  
   - Se recupera la instancia de ``EmpresaServicios`` correspondiente al ``id`` almacenado en la sesión.  

3. **Carga del formulario**:  
   
   - Se crea una instancia de ``FormNuevaEmpresaServicios`` con los datos de la empresa.  
   - Los campos ``empresa`` y ``rut`` están deshabilitados para evitar modificaciones.  

4. **Contexto y renderizado**:
     
   - Se pasa el formulario y el ``empresa_id`` al contexto.  
   - Se envían las variables necesarias para la barra lateral.  
   - Se renderiza la plantilla ``edit_maintenance_companie.html`` con el contexto.  

Retorno
-------

- Renderiza la plantilla ``edit_maintenance_companie.html`` con el formulario precargado.  

edit_maintenance_companie
==========================

Esta vista permite acceder al formulario de edición de una empresa de mantenimiento.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Gestión de sesión**:  
   
   - Intenta obtener el ``empresa_id`` desde la solicitud ``POST`` y almacenarlo en la sesión.  
   - Si no se encuentra en ``POST``, se usa el valor previamente almacenado en la sesión.  

2. **Obtención de la empresa**: 
    
   - Se recupera la instancia de ``EmpresaServicios`` correspondiente al ``id`` almacenado en la sesión.  

3. **Carga del formulario**: 
    
   - Se crea una instancia de ``FormNuevaEmpresaServicios`` con los datos de la empresa.  
   - Los campos ``empresa`` y ``rut`` están deshabilitados para evitar modificaciones.  

4. **Contexto y renderizado**: 
    
   - Se pasa el formulario y el ``empresa_id`` al contexto.  
   - Se envían las variables necesarias para la barra lateral.  
   - Se renderiza la plantilla ``edit_maintenance_companie.html`` con el contexto.  

Retorno
-------

- Renderiza la plantilla ``edit_maintenance_companie.html`` con el formulario precargado.  

save_edit_maintenance_companie
===============================

Esta vista permite guardar los cambios realizados en una empresa de mantenimiento.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Verificación del método**:  
   
   - Solo permite solicitudes ``POST``.  

2. **Obtención de la empresa**: 
    
   - Recupera la instancia de ``EmpresaServicios`` utilizando el ``empresa_id`` enviado en la solicitud.  

3. **Actualización de datos**: 
    
   - Modifica los campos ``telefono``, ``direccion`` y ``descripcion`` en la base de datos.  

4. **Notificación y respuesta**:  
   
   - Envía una notificación de actualización.  
   - Retorna una respuesta ``JSON`` con ``success: True``.  

5. **Redirección en caso de error**: 
    
   - Si la solicitud no es ``POST``, redirige a la vista ``edit_maintenance_companie``.  

Retorno
-------

- ``JsonResponse({'success': True})`` si la actualización es exitosa.  
- Redirección a ``edit_maintenance_companie`` en caso de error.  

manage_maintenance_services
============================

Esta vista permite gestionar los servicios de mantenimiento registrados en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Gestión de mensajes**:
     
   - Recupera los mensajes almacenados en el sistema de notificaciones de Django.  
   - Marca los mensajes como utilizados para evitar que se repitan.  

2. **Obtención de servicios**: 
    
   - Recupera una lista de todos los registros de ``EmpresaTipoServicios``.  
   - Ordena la lista por ``fechacreacion``.  

3. **Contexto**:  
   
   - ``servicios``: Lista de servicios obtenidos.  
   - ``sidebarsubmenu``: Define la opción de submenú activo.  
   - ``sidebarmenu``: Define la opción de menú activo.  
   - ``sidebarmain``: Define la categoría principal del sistema.  

4. **Renderizado de plantilla**: 
    
   - Muestra la página ``manage_maintenance_services.html`` con el contexto definido.  

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/manage_maintenance_services.html`` con los datos de los servicios.  

new_maintenance_service
========================

Esta vista permite la creación de un nuevo servicio de mantenimiento en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Contexto**: 
    
   - ``formnuevoservicio``: Instancia del formulario ``FormEmpresaTipoServicios`` para la creación de un nuevo servicio.  
   - ``sidebarsubmenu``: Define la opción de submenú activo.  
   - ``sidebarmenu``: Define la opción de menú activo.  
   - ``sidebarmain``: Define la categoría principal del sistema.  

2. **Renderizado de plantilla**: 
    
   - Muestra la página ``new_maintenance_service.html`` con el formulario correspondiente.  

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/new_maintenance_service.html`` con el formulario para ingresar un nuevo servicio de mantenimiento.  

save_new_maintenance_service
=============================

Esta vista permite guardar un nuevo servicio de mantenimiento en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Verificación de método**: 
    
   - Solo acepta solicitudes ``POST``.  

2. **Validación de existencia**: 
    
   - Verifica si ya existe un servicio de mantenimiento con el mismo nombre asociado a la empresa.  
   - Si existe, retorna el objeto encontrado.  

3. **Creación del servicio**:  
   
   - Obtiene la empresa asociada al servicio.  
   - Valida el formulario ``FormEmpresaTipoServicios`` con los datos proporcionados.  
   - Si es válido, crea un nuevo servicio con los siguientes atributos:  
     - ``empresa``: Empresa a la que pertenece el servicio.  
     - ``servicio``: Nombre del servicio.  
     - ``status``: Estado activo por defecto.  
     - ``creador``: Usuario que registra el servicio.  
   - Guarda el servicio en la base de datos.  

4. **Notificación y respuesta**:  
   - Envía una notificación mediante ``notificacion_mantenedor_email``.  
   - Retorna un ``JsonResponse`` con éxito o error según el resultado.  

Retorno
-------

- ``JsonResponse({'success': True})`` si el servicio se crea correctamente.  
- ``JsonResponse({'success': False, 'message': 'El formulario no es válido.'})`` si hay errores de validación.  
- Redirige a ``manage_maintenance_services`` si la solicitud no es ``POST``.  

status_maintenance_service
==========================

Esta vista permite habilitar o deshabilitar un servicio de mantenimiento.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Verificación de método**: 
    
   - Solo acepta solicitudes ``POST``.

2. **Obtención del servicio**:  
   
   - Se obtiene el objeto ``servicio`` de la base de datos mediante el ``id`` recibido en la solicitud ``POST``.  
   - Si el ``id`` no corresponde a un servicio existente, se genera una excepción.

3. **Cambio de estado**:  
   
   - Si el estado del servicio está activo (``status=True``), se actualiza a deshabilitado (``status=False``).  
   - Si el estado del servicio está deshabilitado (``status=False``), se actualiza a habilitado (``status=True``).  

4. **Notificación y mensajes**: 
    
   - Se envía una notificación por correo mediante ``notificacion_mantenedor_email`` informando el cambio de estado.  
   - Se muestra un mensaje de éxito mediante ``messages.success`` indicando que el servicio fue habilitado o deshabilitado correctamente.  

5. **Redirección**:  
   
   - Redirige a la vista ``manage_maintenance_services`` luego de completar la acción.

Retorno
-------

- Redirige a ``manage_maintenance_services`` luego de realizar el cambio de estado.

manage_failures
===============

Esta vista permite gestionar las fallas de los vehículos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Obtención de fallas**:  
   
   - Se recuperan todas las instancias de ``TipoFallaVehiculo`` de la base de datos, ordenadas por ``id``.

2. **Contexto**:  
   
   - Se pasa la lista de fallas obtenidas al contexto, junto con las configuraciones del menú lateral:
  
     - ``sidebarsubsubmenu``: Identifica la subsección activa del menú.
     - ``sidebarsubmenu``: Define la subsección en la que el usuario está trabajando.
     - ``sidebarmenu``: Identifica la sección principal del menú.
     - ``sidebarmain``: Define la categoría principal en el menú.

3. **Renderizado de la plantilla**:  
   
   - Se renderiza la plantilla ``pages/maintainer/manage_failures.html`` pasando el contexto que contiene la lista de fallas y las configuraciones del menú.

Retorno
-------

- Se retorna la renderización de la plantilla ``manage_failures.html`` con la lista de fallas y el contexto necesario para mostrar la interfaz correctamente.

new_failure
===========

Esta vista permite la creación de nuevas fallas de vehículos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Contexto**:  

   - Se define el formulario ``FormTipoFallaVehiculo`` para la creación de una nueva falla.
   - Se configuran las claves del menú lateral para asegurar la navegación en la interfaz:
  
     - ``sidebarsubsubmenu``: Identifica la subsección activa del menú.
     - ``sidebarsubmenu``: Define la subsección en la que el usuario está trabajando.
     - ``sidebarmenu``: Identifica la sección principal del menú.
     - ``sidebarmain``: Define la categoría principal en el menú.

2. **Renderizado de la plantilla**:
     
   - Se renderiza la plantilla ``pages/maintainer/new_failure.html`` con el formulario y las configuraciones del menú.

Retorno
-------

- Se retorna la renderización de la plantilla ``new_failure.html`` con el formulario y el contexto necesario para la interfaz de usuario.

save_new_failure
================

Esta vista permite el registro de una nueva falla de vehículo en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Verificación del método HTTP**: 
    
   - Se verifica que la solicitud sea de tipo ``POST`` antes de procesar los datos.

2. **Procesamiento del formulario**:  
   
   - Se instancia el formulario ``FormTipoFallaVehiculo`` con los datos enviados.  
   - Se obtiene la categoría de la falla utilizando su identificador.  

3. **Validación y almacenamiento**:  
   
   - Si el formulario es válido:
  
     - Se crea un objeto ``TipoFallaVehiculo`` con los datos proporcionados, estableciendo:
  
       - ``categoria``: Categoría de la falla.
       - ``falla``: Nombre de la falla.
       - ``status``: Activo por defecto (``True``).
       - ``creador``: Nombre completo del usuario que realiza el registro.
  
     - Se guarda la falla en la base de datos.
     - Se envía una notificación por correo electrónico.  
     - Se retorna una respuesta en formato ``JSON`` indicando éxito.

4. **Redirección en caso de error**:  
   
   - Si la solicitud no es ``POST``, se redirige a la vista ``new_failure``.

Retorno
-------

- Si el registro es exitoso, retorna una respuesta ``JSON`` con ``{'success': True}``.
- Si la solicitud no es ``POST``, redirige a ``new_failure``.

status_failure
==============

Esta vista permite habilitar o deshabilitar una falla de vehículo en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Verificación del método HTTP**:  
   
   - Se verifica que la solicitud sea de tipo ``POST`` antes de continuar.

2. **Obtención de la falla**: 
    
   - Se busca la falla de vehículo en la base de datos utilizando el ``id`` proporcionado en la solicitud.

3. **Cambio de estado**:  
   
   - Si la falla está habilitada (``status=True``), se deshabilita (``status=False``).
   - Si la falla está deshabilitada (``status=False``), se habilita (``status=True``).

4. **Notificación y mensaje de confirmación**:  
   
   - Se envía una notificación por correo electrónico informando el cambio de estado.
   - Se muestra un mensaje de éxito indicando la acción realizada.

5. **Redirección**:  
   
   - Se redirige a la vista ``manage_failures`` después de actualizar el estado.

Retorno
-------

- Redirige a ``manage_failures`` tras cambiar el estado de la falla.

manage_categories_failures
==========================

Esta vista permite gestionar las categorías de fallas de vehículos en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Limpieza de mensajes previos**:
     
   - Se obtiene la lista de mensajes almacenados en ``messages`` y se marcan como usados para evitar que se muestren repetidamente.

2. **Obtención de categorías de fallas**: 
    
   - Se consulta la base de datos para obtener todas las categorías de fallas de vehículos, ordenadas por ``id``.

3. **Definición del contexto**:  
   
   - Se almacenan las categorías obtenidas en el contexto para ser utilizadas en la plantilla.

4. **Renderización de la plantilla**: 
    
   - Se devuelve la página ``manage_categories_failures.html`` con el contexto definido.

Retorno
-------

- Renderiza la plantilla ``manage_categories_failures.html`` con la lista de categorías de fallas de vehículos.

new_categories_failure
======================

Esta vista permite la creación de nuevas categorías de fallas de vehículos en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Definición del contexto**: 
    
   - Se inicializa el formulario ``FormCategoriaFallaVehiculo`` para la creación de una nueva categoría de falla.
   - Se configuran las variables de navegación de la interfaz.

2. **Renderización de la plantilla**:
     
   - Se devuelve la página ``new_categorie_failure.html`` con el formulario disponible para la creación de una nueva categoría de falla.

Retorno
-------

- Renderiza la plantilla ``new_categorie_failure.html`` con el formulario para ingresar una nueva categoría de falla de vehículo.

save_new_categories_failure
===========================

Esta vista maneja la creación de nuevas categorías de fallas de vehículos en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Verificación del método HTTP**: 
    
   - Solo permite solicitudes ``POST``.

2. **Validación del formulario**:  
   
   - Se inicializa el formulario ``FormCategoriaFallaVehiculo`` con los datos enviados.
   - Si el formulario es válido:
  
     - Se crea una nueva instancia de ``CategoriaFallaVehiculo`` con los datos proporcionados.
     - Se asigna el estado ``status = True`` por defecto.
     - Se guarda la nueva categoría en la base de datos.
     - Se envía una notificación por correo electrónico informando la creación.
     - Se retorna una respuesta ``JsonResponse`` indicando éxito.

3. **Redirección en caso de solicitud no válida**:  
   
   - Si la solicitud no es ``POST``, se redirige a la vista ``new_categories_failure``.

Retorno
-------

- Si la creación es exitosa, se devuelve una ``JsonResponse`` con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a ``new_categories_failure``.

status_categories_failure
=========================

Esta vista permite habilitar o deshabilitar categorías de fallas de vehículos en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Limita el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Verificación del método HTTP**:  
   
   - Solo permite solicitudes ``POST``.

2. **Cambio de estado de la categoría**: 
    
   - Se obtiene la categoría de falla de vehículo a partir del ``id`` enviado en la solicitud.
   - Si la categoría está habilitada (``status=True``):
  
     - Se actualiza su estado a ``False`` (deshabilitada).
     - Se envía una notificación por correo electrónico informando la deshabilitación.
     - Se muestra un mensaje de éxito con ``messages.success``.
  
   - Si la categoría está deshabilitada (``status=False``):
  
     - Se actualiza su estado a ``True`` (habilitada).
     - Se envía una notificación por correo electrónico informando la habilitación.
     - Se muestra un mensaje de éxito con ``messages.success``.

3. **Redirección**:  
   
   - Luego de actualizar el estado, se redirige a ``manage_categories_failures``.

Retorno
-------

- Siempre redirige a ``manage_categories_failures`` después de cambiar el estado.

manage_mining_documents_general
===============================

Esta vista permite gestionar los documentos generales de faenas en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles específicos (administrador de sondajes, base de datos o supervisor).

Funcionamiento
--------------

1. **Gestión de mensajes**:
     
   - Se obtiene el almacenamiento de mensajes con ``messages.get_messages(request)`` y se marca como utilizado (``storage.used = True``).

2. **Obtención de documentos**:  
   
   - Se consultan todos los registros de ``TipoDocumentoFaenaGeneral`` y se ordenan por ``fechacreacion``.

3. **Contexto**:  
   
   - Se define un diccionario con los siguientes datos:
  
     - ``tipo_documentos``: Lista de documentos generales de faena.
     - ``sidebarsubmenu``: Identificador de la opción de menú seleccionada.
     - ``sidebarmenu``: Categoría principal en la barra lateral.
     - ``sidebarmain``: Sección principal del sistema.

4. **Renderizado de la plantilla**:  
   
   - Se renderiza la vista ``manage_mining_documents_general.html`` con el contexto preparado.

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/manage_mining_documents_general.html`` con los datos obtenidos.

new_mining_document_general
============================

Esta vista permite la creación de un nuevo documento general de faena en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles específicos (administrador de sondajes, base de datos o supervisor).

Funcionamiento
--------------

1. **Contexto**:  
   
   - Se define un diccionario con los siguientes datos:
  
     - ``formnuevodocumentogeneral``: Instancia del formulario ``FormTipoDocumentoFaenaGeneral`` para la creación de un nuevo documento general de faena.
     - ``sidebarsubmenu``: Identificador de la opción de menú seleccionada.
     - ``sidebarmenu``: Categoría principal en la barra lateral.
     - ``sidebarmain``: Sección principal del sistema.

2. **Renderizado de la plantilla**:  
   
   - Se renderiza la vista ``new_mining_document_general.html`` con el contexto preparado.

Retorno
-------

- Renderiza la plantilla ``pages/maintainer/new_mining_document_general.html`` con el formulario de creación de un nuevo documento general de faena.

save_new_mining_document_general
=================================

Esta vista permite guardar un nuevo documento general de faena en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles específicos (administrador de sondajes, base de datos o supervisor).

Funcionamiento
--------------

1. **Verificación del método HTTP**:
     
   - Se ejecuta solo si la solicitud es de tipo ``POST``.
   - En caso contrario, se muestra un mensaje de error y se redirige a la vista ``manage_mining_documents_general``.

2. **Procesamiento del archivo**:  
   
   - Se obtiene el valor del campo ``toggle-archivoDocumento`` del formulario.
   - Se procesa el archivo utilizando la función ``procesar_fotografia_dos``.

3. **Validación de existencia previa**:
     
   - Se verifica si ya existe un documento con el mismo ``nombredocumento`` y ``faena`` en la base de datos.
   - Si existe, se devuelve el documento encontrado.

4. **Creación del nuevo documento**:  
   
   - Se obtiene la instancia de ``Faena`` correspondiente al ``faena`` seleccionado.
   - Se valida el formulario ``FormTipoDocumentoFaenaGeneral`` con los datos enviados.
   - Si el formulario es válido:
  
     - Se crea una instancia de ``TipoDocumentoFaenaGeneral`` con los datos ingresados y el archivo procesado.
     - Se asigna el estado ``status=True``.
     - Se guarda en la base de datos.
     - Se envía una notificación mediante ``notificacion_admin_jefe_mantencion_email``.
     - Se retorna una respuesta JSON con ``{'success': True}``.
  
   - Si el formulario no es válido, se retorna un JSON con ``{'success': False, 'message': 'El formulario no es válido.'}``.

Retorno
-------

- Si la creación es exitosa, retorna una respuesta JSON con ``{'success': True}``.
- Si el formulario no es válido, retorna ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si la solicitud no es ``POST``, muestra un mensaje de error y redirige a ``manage_mining_documents_general``.

status_mining_document_general
===============================

Esta vista permite cambiar el estado de un documento general de faena (habilitar o deshabilitar).

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles específicos (administrador de sondajes, base de datos o supervisor).

Funcionamiento
--------------

1. **Verificación del método HTTP**:  

   - Se ejecuta solo si la solicitud es de tipo ``POST``.
   - En caso contrario, se muestra un mensaje de error y se redirige a la vista ``manage_mining_documents_general``.

2. **Obtención del documento**:  
   
   - Se obtiene el documento ``TipoDocumentoFaenaGeneral`` correspondiente al ``id`` enviado en la solicitud ``POST``.

3. **Cambio de estado**:  
   
   - Si el estado del documento es ``True`` (habilitado), se actualiza a ``False`` (deshabilitado), y se envía una notificación de deshabilitación mediante ``notificacion_admin_jefe_mantencion_email``.
   - Si el estado es ``False`` (deshabilitado), se actualiza a ``True`` (habilitado), y se envía una notificación de habilitación mediante ``notificacion_admin_jefe_mantencion_email``.
   - Se muestra un mensaje de éxito al usuario con ``messages.success``.

4. **Retorno**:  
   
   - Después de cambiar el estado, la vista redirige a ``manage_mining_documents_general``.

5. **Manejo de errores**: 
    
   - Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a ``manage_mining_documents_general``.

Retorno
-------

- Si la acción es exitosa, redirige a ``manage_mining_documents_general`` con un mensaje de éxito.
- Si la solicitud no es ``POST``, muestra un mensaje de error y redirige a ``manage_mining_documents_general``.

edit_mining_document_general
=============================

Esta vista permite editar un documento general de faena, cargando sus datos en un formulario para que el usuario pueda modificarlos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles específicos (administrador de sondajes, base de datos o supervisor).

Funcionamiento
--------------

1. **Gestión de la sesión**:  
   
   - Se guarda el ``id`` del documento general de faena en la sesión, si no existe un valor previamente, se mantiene el valor actual.
   
2. **Obtención del documento**: 
    
   - Se obtiene el documento ``TipoDocumentoFaenaGeneral`` correspondiente al ``id`` almacenado en la sesión.

3. **Determinación del tipo de archivo**:  
   
   - Se verifica la extensión del archivo asociado al documento:
  
     - Si es una imagen (``.jpg``, ``.jpeg``, ``.png``), se asigna la extensión ``imagen``.
     - Si es un archivo PDF (``.pdf``), se asigna la extensión ``pdf``.
     - Si es otro tipo de archivo, se asigna la extensión ``otro``.

4. **Formulario de edición**:  
   
   - Se renderiza un formulario de edición con los datos del documento cargados inicialmente.
   - Los campos de ``faena`` y ``nombredocumento`` se configuran como deshabilitados para evitar su modificación.

5. **Retorno**:  
   
   - El formulario se muestra al usuario en la plantilla ``edit_mining_document_general.html`` con el archivo y su extensión correspondiente.

Retorno
-------

- La vista devuelve el formulario de edición cargado con los datos actuales del documento y su archivo.

save_edit_mining_document_general
=================================

Esta vista permite guardar los cambios realizados en un documento general de faena, incluyendo la actualización de su archivo adjunto.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@sondaje_admin_or_base_datos_or_supervisor_required``:  
   Restringe el acceso a usuarios con roles específicos (administrador de sondajes, base de datos o supervisor).

Funcionamiento
--------------

1. **Verificación de método**:  
   
   - Se comprueba que la solicitud sea de tipo ``POST``, lo cual indica que el usuario está enviando los datos del formulario.

2. **Obtención del documento**:  

   - Se obtiene el documento ``TipoDocumentoFaenaGeneral`` correspondiente al ``id`` proporcionado en los datos del formulario.

3. **Procesamiento del archivo**: 
    
   - Se maneja el archivo adjunto mediante la función ``procesar_fotografia_dos``:
  
     - Si el archivo no ha sido proporcionado, se utiliza una imagen predeterminada: ``base/no-imagen.png``.
     - Si se ha proporcionado un archivo, se procesa adecuadamente.

4. **Actualización del documento**:
     
   - Se actualiza el campo ``archivodocumento`` del documento con el nuevo archivo procesado.

5. **Notificación**:  
   
   - Se envía una notificación por correo al administrador o jefe de mantención indicando que el documento ha sido actualizado.

6. **Retorno**:  
   
   - Si el documento se guarda correctamente, se retorna un ``JsonResponse`` con un estado de éxito.

7. **Redirección en caso de error**: 
    
   - Si no se cumple el método ``POST``, se redirige al usuario a la vista de edición del documento general de faena.

Retorno
-------

- La vista devuelve un ``JsonResponse`` con el valor ``success: True`` si la actualización fue exitosa.
- Si no es una solicitud ``POST``, se redirige a la vista de edición.

manage_types_machines
======================

Esta vista permite gestionar los diferentes tipos de maquinaria. Muestra una lista de los tipos registrados en el sistema.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Obtención de datos**: 
    
   - Se consulta la base de datos para obtener todos los objetos de tipo ``TipoMaquinaria``, ordenados por su ``id``.

2. **Contexto**: 
    
   - Se prepara un diccionario ``context`` con los siguientes elementos:
  
     - ``tiposmaquinas``: Lista de tipos de maquinaria obtenida de la base de datos.
     - ``sidebarsubmenu``: Valor para indicar la opción seleccionada en el menú lateral.
     - ``sidebarmenu``: Valor para indicar la opción principal del menú lateral.
     - ``sidebarmain``: Valor para indicar el menú principal.

3. **Renderización**:  
   
   - Se renderiza la plantilla ``manage_types_machine.html`` pasando el contexto preparado.

Retorno
-------

- La vista devuelve una página HTML con la lista de los tipos de maquinaria, utilizando los valores proporcionados en el contexto.

new_type_machine
================

Esta vista permite crear un nuevo tipo de maquinaria. Muestra un formulario para ingresar los datos necesarios.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Contexto**:  
   
   - Se prepara un diccionario ``context`` con los siguientes elementos:
  
     - ``formnuevotipomaquinaria``: El formulario para crear un nuevo tipo de maquinaria.
     - ``sidebarsubmenu``: Valor para indicar la opción seleccionada en el menú lateral.
     - ``sidebarmenu``: Valor para indicar la opción principal del menú lateral.
     - ``sidebarmain``: Valor para indicar el menú principal.

2. **Renderización**:  
   
   - Se renderiza la plantilla ``new_type_machine.html`` pasando el contexto preparado.

Retorno
-------

- La vista devuelve un formulario HTML para ingresar un nuevo tipo de maquinaria, utilizando los valores proporcionados en el contexto.

save_new_type_machine
=====================

Esta vista guarda un nuevo tipo de maquinaria. Recibe los datos del formulario y, si son válidos, crea y guarda un nuevo tipo de maquinaria en la base de datos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Método POST**:  
   
   - Si la solicitud es de tipo ``POST``, se procesa el formulario ``FormTipoMaquinaria`` con los datos recibidos.
   - Si el formulario es válido, se crea un nuevo objeto ``TipoMaquinaria`` con los siguientes datos:
  
     - ``tipo``: Valor del campo ``tipo`` del formulario.
     - ``status``: Se establece como ``True``.
     - ``creador``: Nombre completo del usuario autenticado (``request.user.first_name + " " + request.user.last_name``).
   
   - Se guarda el nuevo tipo de maquinaria en la base de datos.
   - Se envía una notificación por correo sobre la creación del nuevo tipo de maquinaria.
   - Se devuelve un ``JsonResponse`` indicando que la operación fue exitosa.

2. **Método GET**: 
    
   - Si la solicitud no es de tipo ``POST``, se redirige al usuario a la vista ``new_type_machine`` para que complete el formulario.

Retorno
-------

- Si el formulario es válido, se devuelve una respuesta JSON con el campo ``success: True``.
- Si la solicitud no es ``POST``, se redirige al usuario a la vista ``new_type_machine``.

status_type_machine
====================

Esta vista cambia el estado de un tipo de maquinaria entre habilitado y deshabilitado. Si el tipo de maquinaria está habilitado, se deshabilita, y viceversa.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

1. **Método POST**:  
   
   - Si la solicitud es de tipo ``POST``, se obtiene el tipo de maquinaria con el ``id`` recibido en la solicitud.
   - Si el estado del tipo de maquinaria es ``True`` (habilitado), se cambia a ``False`` (deshabilitado).
  
     - Se actualiza el estado del tipo de maquinaria en la base de datos.
     - Se envía una notificación por correo indicando que el tipo de maquinaria fue deshabilitado.
     - Se muestra un mensaje de éxito.
  
   - Si el estado del tipo de maquinaria es ``False`` (deshabilitado), se cambia a ``True`` (habilitado).
  
     - Se actualiza el estado del tipo de maquinaria en la base de datos.
     - Se envía una notificación por correo indicando que el tipo de maquinaria fue habilitado.
     - Se muestra un mensaje de éxito.

2. **Método GET**:  

   - Si la solicitud no es de tipo ``POST``, se muestra un mensaje de error indicando que hubo un problema al deshabilitar el tipo de maquinaria.

Retorno
-------

- Si el tipo de maquinaria se habilita o deshabilita correctamente, se redirige al usuario a la vista ``manage_types_machines``.
- Si ocurre un error (no es una solicitud ``POST``), se muestra un mensaje de error y se redirige al usuario a la vista ``manage_types_machines``.

manage_brands_machines
========================

Esta vista permite visualizar una lista de las marcas de maquinaria registradas en el sistema. Se muestra en una tabla donde se pueden ver todas las marcas ordenadas por su identificador.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- Se obtienen todas las marcas de maquinaria desde la base de datos y se ordenan por su ``id``.
- Los resultados se pasan al contexto de la plantilla para su renderizado.

Retorno
-------

- Se renderiza la plantilla ``manage_brands_machine.html`` y se pasa al contexto la lista de marcas de maquinaria junto con información de la estructura del menú y la barra lateral.

manage_kits_repairs
====================

Esta vista permite visualizar una lista de los kits de reparación de maquinaria registrados en el sistema. Se muestra en una tabla donde se pueden ver todos los kits ordenados por su identificador.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- Se obtienen todos los kits de reparación desde la base de datos y se ordenan por su ``id``.
- Los resultados se pasan al contexto de la plantilla para su renderizado.

Retorno
-------

- Se renderiza la plantilla ``manage_kits_repair.html`` y se pasa al contexto la lista de kits de reparación junto con información de la estructura del menú y la barra lateral.

new_kit_repair
===============

Esta vista permite mostrar el formulario para crear un nuevo kit de reparación para maquinaria. El formulario es proporcionado a través del contexto para ser renderizado en la plantilla correspondiente.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- Se crea el contexto con el formulario ``FormKitReparacion`` para que sea procesado y renderizado en la plantilla.
- Además, se configura la estructura del menú y la barra lateral.

Retorno
-------

- Se renderiza la plantilla ``new_kit_repair.html`` con el formulario de creación del kit de reparación junto con la configuración del menú y barra lateral.


save_new_kit_repair
====================

Esta vista maneja la lógica para guardar un nuevo kit de reparación para maquinaria. Recibe los datos del formulario, valida los campos y guarda el kit en la base de datos si la validación es exitosa.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- Si la solicitud es de tipo ``POST``, se obtiene la marca de maquinaria seleccionada.
- Luego, se valida el formulario ``FormKitReparacion`` con los datos proporcionados.
- Si el formulario es válido:

  - Se crea un nuevo objeto ``KitsMaquinaria`` con los datos del formulario.
  - El kit se guarda en la base de datos.
  - Se envía una notificación por correo electrónico para informar que el kit de reparación ha sido creado.

- Si el formulario no es válido, la vista redirige al formulario de creación de un nuevo kit de reparación.

Retorno
-------

- Si el formulario es válido y el kit se guarda correctamente, se devuelve una respuesta JSON indicando que la operación fue exitosa.
- Si no es ``POST``, o el formulario no es válido, se redirige a la página de creación de un nuevo kit de reparación.

status_kit_repair
=================

Esta vista permite habilitar o deshabilitar un kit de reparación de maquinaria. Se actualiza el estado del kit y se envía una notificación al usuario sobre el cambio.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- Si la solicitud es de tipo ``POST``:
  
  - Se obtiene el kit de reparación a partir del ``id`` proporcionado.
  - Si el kit está habilitado (``status=True``), se deshabilita (``status=False``), se guarda el cambio en la base de datos, se envía una notificación por correo electrónico sobre el cambio y se muestra un mensaje de éxito.
  - Si el kit está deshabilitado (``status=False``), se habilita (``status=True``), se guarda el cambio en la base de datos, se envía una notificación por correo electrónico sobre el cambio y se muestra un mensaje de éxito.
  
Retorno
-------

- Si el cambio se realiza con éxito, se redirige a la página de gestión de kits de reparación.
- Si la solicitud no es ``POST`` o ocurre un error, se redirige a la misma página con un mensaje de error.

edit_kit_repair
================

Esta vista permite editar los detalles de un kit de reparación existente. La información del kit es cargada y presentada en un formulario para su actualización.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- Se intenta obtener el ``id`` del kit a editar a partir de la solicitud ``POST``.
- Si el ``id`` no está presente, se recupera desde la sesión del usuario.
- Se obtiene el kit de reparación a partir del ``id`` almacenado en la sesión y se pasa a un formulario con los datos prellenados.
- En el formulario:
  
  - Los campos ``marcaMaquina`` y ``nombreKit`` están deshabilitados, ya que no pueden ser modificados directamente.
  
Retorno
-------

- Se renderiza un formulario con los detalles del kit de reparación, permitiendo al usuario editar otros campos como ``stockMinimo`` y ``stockMaximo``.

save_edit_kit_repair
====================

Esta vista procesa la edición de un kit de reparación. Permite actualizar los valores de ``stockMinimo`` y ``stockMaximo`` de un kit existente, validando que los valores ingresados sean correctos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- Si la solicitud es ``POST``:
  
  - Se obtiene el kit de reparación basado en el ``id`` enviado en el formulario.
  - Se recuperan los valores de ``stockMinimo`` y ``stockMaximo``.
  - Si alguno de los valores es menor a 1, se retorna un error.
  - Si el ``stockMinimo`` es mayor o igual que ``stockMaximo``, también se retorna un error.
  - Si los valores son válidos, se actualizan los campos de ``stockMinimo`` y ``stockMaximo`` para el kit de reparación.

Retorno
-------

- Si la validación es exitosa, se devuelve una respuesta JSON con ``success: True``.
- Si la validación falla (por ejemplo, los valores son menores a 1 o ``stockMinimo`` es mayor que ``stockMaximo``), se retorna un error en formato JSON.
- Si la solicitud no es ``POST``, se redirige al formulario de edición del kit de reparación.

manage_failures_machines
=========================

Esta vista muestra la lista de fallas de maquinaria registradas en el sistema. Se obtienen todas las instancias de ``FallaMaquinaria`` y se muestran en una página de administración.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- La vista obtiene todas las fallas de maquinaria desde el modelo ``FallaMaquinaria``.
- Se ordenan por el campo ``id`` en orden ascendente.
- Se renderiza la página ``manage_failures_machine.html`` con el contexto necesario, que incluye:

  - ``fallasmaquinas``: Lista de fallas de maquinaria.
  - Variables de configuración de barra lateral para la navegación dentro del panel de administración.

Retorno
-------

- Se retorna un renderizado de la página ``manage_failures_machine.html`` con el contexto cargado.

new_failure_machine
===================

Esta vista muestra un formulario para crear una nueva falla de maquinaria. Permite seleccionar la marca de la maquinaria y especificar los detalles de la falla.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- La vista renderiza un formulario compuesto por dos formularios:
  
  - ``formmarcasmaquinaria``: Un formulario para seleccionar la marca de la maquinaria utilizando ``FormMarcaMaquinariaSelect``.
  - ``formfallamaquinaria``: Un formulario para ingresar los detalles de la falla utilizando ``FormFallaMaquinaria``.

- Además, se configuran las variables de la barra lateral para la navegación dentro del panel de administración.

Retorno
-------

- Se retorna un renderizado de la página ``new_failure_machine.html`` con el contexto cargado, que incluye los formularios y las variables de configuración de barra lateral.

save_new_failure_machine
=========================

Esta vista maneja la creación y almacenamiento de una nueva falla de maquinaria. Los usuarios envían un formulario con los detalles de la falla y la maquinaria asociada. Si el formulario es válido, la falla se guarda en la base de datos.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.

Funcionamiento
--------------

- La vista procesa una solicitud POST, donde el formulario contiene la información de la falla y el kit de maquinaria asociado.
- Primero, obtiene el objeto ``kit`` de la base de datos usando el ``id`` del kit de maquinaria que se envía a través de la solicitud POST.
- Luego, valida el formulario ``FormFallaMaquinaria`` con los datos de la solicitud.
- Si el formulario es válido:
  
  - Crea un nuevo objeto ``FallaMaquinaria`` con la maquinaria seleccionada, la descripción de la falla, y marca el estado como ``True``.
  - Guarda el nuevo objeto ``FallaMaquinaria`` en la base de datos.
  - Envía una notificación por correo electrónico sobre la creación de la nueva falla.
  - Retorna una respuesta JSON con ``success: True``.
  
- Si no se realiza una solicitud POST, la vista redirige al usuario a la vista ``new_failure_machine``.

Retorno
-------

- Si el formulario es válido, se retorna una respuesta JSON con un valor de éxito: ``{'success': True}``.
- Si no se realiza un POST, se redirige a la vista ``new_failure_machine``.

status_failure_machine
========================

Esta vista se encarga de cambiar el estado de una falla de maquinaria. Si la falla está habilitada, la deshabilita, y si está deshabilitada, la habilita.

Decoradores
-----------

- ``@login_required``:  
   Restringe el acceso a usuarios autenticados.
- ``@admin_required``:  
   Restringe el acceso a usuarios con privilegios de administrador.

Funcionamiento
--------------

- La vista maneja una solicitud POST, en la que se pasa el ``id`` de la falla que se desea modificar.
- Primero, se obtiene el objeto ``FallaMaquinaria`` correspondiente al ``id`` pasado en la solicitud.
- Si el estado de la falla es ``True`` (habilitado), se cambia a ``False`` (deshabilitado) y se envía una notificación por correo electrónico indicando que la falla ha sido deshabilitada. Además, se muestra un mensaje de éxito en la interfaz.
- Si el estado de la falla es ``False`` (deshabilitado), se cambia a ``True`` (habilitado) y se envía una notificación por correo electrónico indicando que la falla ha sido habilitada. También se muestra un mensaje de éxito en la interfaz.
- Después de realizar la actualización, se redirige al usuario a la vista ``manage_failures_machines``.
- Si no se realiza una solicitud POST, se muestra un mensaje de error y se redirige a la vista ``manage_failures_machines``.

Retorno
-------

- Si el estado se actualiza correctamente, se redirige a la vista ``manage_failures_machines`` y muestra un mensaje de éxito.
- Si ocurre un error al intentar deshabilitar la falla, se redirige a la vista ``manage_failures_machines`` y se muestra un mensaje de error.

cargar_kits_por_marca
======================

Esta vista se encarga de cargar los kits de maquinaria según la marca proporcionada. Los kits que se devuelven son aquellos que están habilitados (con ``status=True``).

Decoradores
-----------

No se utilizan decoradores específicos en esta vista, lo que implica que no hay restricciones de acceso o validaciones previas.

Funcionamiento
--------------

- La vista maneja una solicitud GET, donde se espera recibir el parámetro ``marca_id`` que especifica la marca de maquinaria cuyos kits se desean obtener.
- Si el parámetro ``marca_id`` está presente, se filtran los kits de maquinaria correspondientes a esa marca que tengan ``status=True``.
- Los resultados son devueltos en formato JSON, donde cada kit tiene dos campos:
  
  - ``id``: El identificador del kit.
  - ``nombre``: El nombre del kit.
  
- Si el parámetro ``marca_id`` no está presente en la solicitud GET, la vista devuelve un error con código de estado 400 (solicitud incorrecta).

Retorno
-------

- Si ``marca_id`` es proporcionado y válido, la vista devuelve una respuesta JSON con los kits correspondientes.
- Si no se proporciona el parámetro ``marca_id``, la vista devuelve un error con el código de estado HTTP 400.

new_important_dates
===================

Esta vista permite al administrador crear nuevas fechas importantes. Se muestra un formulario para ingresar los detalles de las fechas importantes que se desean agregar.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@admin_required``: Limita el acceso a la vista solo a los usuarios con privilegios de administrador.

Funcionamiento
--------------

- La vista renderiza un formulario utilizando el formulario ``FormNuevaFechasImportantes``.
- El contexto proporcionado incluye:
  
  - ``formnuevafecha``: El formulario para agregar nuevas fechas importantes.
  - ``sidebarsubmenu``: Valor que define la sección activa del menú lateral.
  - ``sidebarmenu``: Valor que define la sección principal del menú lateral.
  - ``sidebarmain``: Valor que define la sección principal del menú superior.
  
La vista no maneja ninguna acción de procesamiento de datos, simplemente muestra el formulario.

Retorno
-------

La vista devuelve la plantilla ``new_important_dates.html`` con el contexto mencionado.

save_new_important_dates
=========================

Esta vista maneja la creación de nuevas fechas importantes. Procesa los datos enviados a través de un formulario y guarda un nuevo registro de fecha importante en la base de datos.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.

Funcionamiento
--------------

- Si la solicitud es de tipo ``POST``, se valida el formulario ``FormNuevaFechasImportantes`` con los datos proporcionados.
- Si el formulario es válido, se crea un nuevo registro en la base de datos:
  
  - ``descripcion``: Descripción de la fecha importante.
  - ``fechaVencimiento``: Fecha de vencimiento de la fecha importante.
  - ``creador``: El nombre del usuario que creó el registro.
  - ``status``: Estado de la fecha importante, establecido como ``True`` por defecto.
  
- Tras guardar el registro, se envía una notificación por correo electrónico utilizando ``notificacion_mantenedor_email``.
- Finalmente, la vista devuelve un ``JsonResponse`` indicando el éxito de la operación.

Si la solicitud no es ``POST``, se redirige al usuario a la vista ``new_important_dates``.

Retorno
-------

La vista devuelve:

- ``JsonResponse({'success': True})`` si el registro se crea correctamente.
- Si no es una solicitud ``POST``, redirige a ``new_important_dates``.

manage_important_dates
=======================

Esta vista se encarga de mostrar la lista de fechas importantes almacenadas en el sistema.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@admin_required``: Solo los administradores pueden acceder a esta vista.

Funcionamiento
--------------

- La vista recupera todas las fechas importantes de la base de datos y las ordena por su ``id``.
- Los datos obtenidos son pasados al contexto para ser utilizados en el template.
- En el contexto se incluyen:
  
  - ``fechasimportantes``: Lista de objetos ``FechasImportantes``.
  - ``sidebarsubmenu``: Indica la sección del menú lateral en la que se encuentra el usuario, en este caso, ``manage_important_dates``.
  - ``sidebarmenu``: Indica la categoría principal del menú lateral, ``manage_vehicles``.
  - ``sidebarmain``: Indica la categoría principal de la barra lateral, ``manage_system``.
  
- Luego, se renderiza el template ``pages/maintainer/manage_important_dates.html`` con el contexto proporcionado.

Retorno
-------

La vista devuelve el renderizado de la página ``manage_important_dates.html`` con las fechas importantes disponibles en el sistema.

status_important_dates
=======================

Esta vista permite cambiar el estado de una fecha importante, habilitándola o deshabilitándola.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@admin_required``: Solo los administradores pueden acceder a esta vista.

Funcionamiento
--------------

- La vista recibe una solicitud ``POST`` con un ``id`` de la fecha importante a modificar.
- Se recupera el objeto ``FechasImportantes`` correspondiente utilizando el ``id`` proporcionado.
- Dependiendo del estado actual de la fecha (habilitada o deshabilitada):
  
  - Si la fecha está habilitada, se cambia su estado a deshabilitado y se envía una notificación por correo.
  - Si la fecha está deshabilitada, se cambia su estado a habilitado y se envía una notificación por correo.
  
- Tras realizar la actualización, se muestra un mensaje de éxito.
- Finalmente, se redirige al usuario a la página de gestión de fechas importantes.

Retorno
-------

La vista devuelve una redirección a la página ``manage_important_dates``, donde se muestra el estado actualizado de las fechas importantes.

edit_important_dates
======================

Esta vista permite editar una fecha importante existente en el sistema.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@admin_required``: Solo los administradores pueden acceder a esta vista.

Funcionamiento
--------------

- La vista intenta obtener el ``id`` de la fecha importante a editar desde la solicitud ``POST``. Si no se encuentra, se usa el ``id`` previamente almacenado en la sesión del usuario.
- Se recupera la fecha importante correspondiente mediante el ``id`` almacenado.
- Se carga un formulario de edición utilizando la instancia de la fecha obtenida.
- El formulario se pasa al contexto para que el usuario pueda editar la fecha.
- La vista renderiza la plantilla ``edit_important_dates.html``, que contiene el formulario de edición.

Retorno
-------

La vista devuelve una respuesta de renderizado con el formulario de edición de la fecha importante.

save_edit_important_dates
==========================

Esta vista permite guardar los cambios realizados en una fecha importante en el sistema.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@admin_required``: Solo los administradores pueden acceder a esta vista.

Funcionamiento
--------------

- La vista recupera el ``id`` de la fecha importante que se desea editar desde la solicitud ``POST``.
- Se utiliza ``get_object_or_404`` para obtener la instancia de la fecha importante correspondiente. Si no se encuentra, se devuelve un error 404.
- Se crea una instancia del formulario ``FormNuevaFechasImportantes`` con los datos recibidos en la solicitud, utilizando la instancia de la fecha importante para la edición.
- Si el formulario es válido, se guarda la instancia y se envía una notificación por correo electrónico indicando que la fecha importante ha sido actualizada.
- Si el formulario no es válido, se retorna un mensaje de error en formato JSON.
- Si la solicitud no es ``POST``, la vista redirige al usuario al formulario de edición de la fecha.

Retorno
-------

- Si el formulario es válido, se retorna una respuesta JSON con ``success: True``.
- Si el formulario no es válido, se retorna una respuesta JSON con ``error: True``.
- En caso de una solicitud diferente a ``POST``, se redirige a la vista de edición de la fecha.

manage_report_error
====================

Esta vista permite gestionar los reportes de error en el sistema.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@admin_required``: Solo los administradores pueden acceder a esta vista.

Funcionamiento
--------------

- La vista recupera todos los reportes de error registrados en el sistema, ordenados por la fecha de creación.
- Los reportes de error se almacenan en una lista llamada ``report_errors``.
- Se envía al contexto de la plantilla la lista de reportes, que se utilizará para mostrar los errores reportados.
- También se incluye el valor ``sidebarmain`` en el contexto para determinar qué opción del menú lateral estará activa.
  
Retorno
-------

- La vista renderiza la plantilla ``manage_report_errors.html``, pasando los reportes de error al contexto para su visualización.

new_report_error
=================

Esta vista permite al usuario crear un nuevo reporte de error.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.

Funcionamiento
--------------

- La vista presenta un formulario vacío de reporte de error para que el usuario lo complete y lo envíe.
- Se incluye el formulario ``FormReporteError`` en el contexto de la plantilla, el cual permitirá a los usuarios ingresar los detalles del error.
- También se incluye el valor ``sidebar`` en el contexto para determinar qué opción del menú lateral estará activa.

Retorno
-------

- La vista renderiza la plantilla ``new_report_error.html``, pasando el formulario al contexto para su visualización.

save_new_report_error
=====================

Esta vista se encarga de guardar un nuevo reporte de error en la base de datos.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.

Funcionamiento
--------------

- Cuando el usuario envía un formulario con los datos del reporte de error, la vista procesa la solicitud ``POST``.
- Se crea un nuevo objeto ``ReporteError`` con la descripción y el detalle proporcionados por el usuario.
- Se asigna el creador del reporte como el nombre completo del usuario autenticado.
- El reporte se guarda en la base de datos con el campo ``status`` establecido en ``True``.

Retorno
-------

- Si la solicitud es válida y el reporte se guarda correctamente, se devuelve una respuesta JSON con ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la página de creación de reporte de error ``new_report_error``.

mostrar_reporte_error
======================

Esta vista se encarga de mostrar los detalles de un reporte de error específico.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@admin_required``: Asegura que solo los usuarios con privilegios de administrador puedan acceder a esta vista.

Funcionamiento
--------------

- La vista recibe un parámetro ``id`` que corresponde al identificador del reporte de error que se desea mostrar.
- Se obtiene el objeto ``ReporteError`` correspondiente al ``id`` proporcionado mediante el método ``get()``.
- Se pasa el objeto ``ReporteError`` al contexto para que esté disponible en la plantilla.

Retorno
-------

- La vista devuelve la plantilla ``mostrarregistro.html`` que muestra los detalles del reporte de error con el contexto adecuado.

manage_help_manuals
====================

Esta vista permite gestionar los manuales de ayuda cargados en el sistema.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------

- Se recuperan todos los documentos de tipo ``AyudaManuales`` ordenados por la fecha de creación en orden descendente.
- Los documentos recuperados se pasan al contexto para su visualización en la plantilla.

Retorno
-------

- La vista devuelve la plantilla ``manage_help_manuals.html`` con el contexto adecuado para mostrar los documentos de ayuda.

new_help_manuals
=================

Esta vista permite mostrar el formulario para crear un nuevo manual de ayuda.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------

- Se presenta un formulario en blanco de tipo ``FormAyudaManuales`` para crear un nuevo documento de ayuda.
- El contexto contiene el formulario y la configuración del menú lateral para una experiencia de navegación coherente.

Retorno
-------

- La vista devuelve la plantilla ``new_help_manuals.html`` con el formulario para que el usuario pueda agregar un nuevo manual de ayuda.

save_new_help_manuals
======================

Esta vista guarda un nuevo manual de ayuda en el sistema. Si ya existe un documento con el mismo nombre y sección, no se crea uno nuevo.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Cuando se recibe una solicitud POST, se verifica si ya existe un documento con el mismo nombre y sección. Si ya existe, se retorna ese documento.
- Si no existe, se valida el formulario y se guarda el nuevo documento de ayuda en la base de datos.
- El archivo relacionado con el manual se procesa mediante la función ``procesar_fotografia_dos``.
- Si el formulario es válido, se guarda el nuevo manual de ayuda.

Retorno
-------

- Si el formulario es válido, se retorna una respuesta JSON con ``{'success': True}``.
- Si el formulario no es válido, se retorna una respuesta JSON con ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si la solicitud no es POST, se redirige a la vista ``manage_help_manuals`` con un mensaje de error.

status_help_manuals
===================

Esta vista habilita o deshabilita un manual de ayuda, cambiando su estado en la base de datos.

Decoradores
-----------

- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se recibe una solicitud POST con el ID del documento y se cambia su estado entre habilitado y deshabilitado.
- Si el documento está habilitado, se deshabilita. Si está deshabilitado, se habilita.

Retorno
-------
- Se redirige al usuario a la vista ``manage_help_manuals`` con un mensaje de éxito o error dependiendo de la acción realizada.

---

edit_help_manuals
=================

Esta vista permite editar los detalles de un manual de ayuda previamente creado.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Cuando se recibe una solicitud POST con el ID del documento, se carga el documento de ayuda correspondiente.
- Se determina el tipo de archivo del documento (imagen, PDF, u otro) en función de su extensión.
- Se muestra el formulario pre-llenado con los detalles del documento.

Retorno
-------
- La vista devuelve el formulario de edición de manual de ayuda con los datos del documento cargados en el contexto.

save_edit_help_manuals
======================

Esta vista permite guardar los cambios realizados a un manual de ayuda existente.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se recibe una solicitud POST con los datos del documento a editar (sección y nombre del documento).
- Si el formulario es válido, se actualizan los campos correspondientes del manual de ayuda en la base de datos.
- También se procesa un nuevo archivo asociado al manual utilizando la función ``procesar_fotografia_dos``.
- Finalmente, se guarda el documento actualizado.

Retorno
-------
- Si la operación es exitosa, se retorna una respuesta JSON con ``{'success': True}``.
- Si no se recibe una solicitud POST, se redirige a la vista ``edit_help_manuals``.

---

view_help_manuals
=================

Esta vista permite mostrar los manuales de ayuda existentes.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.

Funcionamiento
--------------
- Se obtiene la lista de documentos de ayuda existentes y se ordenan por la fecha de creación.
- Los documentos se pasan al contexto para ser mostrados en la plantilla correspondiente.

Retorno
-------
- La vista retorna la plantilla ``manage_help_manuals.html`` con los documentos de ayuda cargados.

---

manage_probe
=============

Esta vista permite gestionar las sondas (probes) en el sistema.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se obtiene la lista de sondas existentes en el sistema y se ordenan por el nombre de la sonda.
- Los datos se pasan al contexto para ser mostrados en la plantilla correspondiente.

Retorno
-------
- La vista retorna la plantilla ``manage_probe.html`` con la lista de sondas cargadas.

---

new_probe
==========

Esta vista permite crear una nueva sonda (probe) en el sistema.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se muestra un formulario para crear una nueva sonda. El formulario se encuentra en el contexto para ser renderizado.

Retorno
-------
- La vista retorna la plantilla ``new_probe.html`` con el formulario para crear una nueva sonda.

save_new_probe
===============

Esta vista permite guardar una nueva sonda (probe) en el sistema.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es POST, se intenta obtener una sonda existente con el nombre proporcionado. Si ya existe, se retorna el objeto de la sonda.
- Si la sonda no existe, se valida el formulario con los datos proporcionados. Si el formulario es válido, se crea una nueva sonda en la base de datos con el nombre y el estado activo.
- Si el formulario no es válido, se retorna una respuesta JSON con un mensaje de error.

Retorno
-------
- Si la operación es exitosa, se retorna una respuesta JSON con ``{'success': True}``.
- Si no se recibe una solicitud POST o hay un error, se redirige a la vista ``manage_probe`` con un mensaje de error.

---

status_probe
=============

Esta vista permite cambiar el estado de una sonda entre habilitada y deshabilitada.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es POST, se obtiene la sonda correspondiente mediante su ID.
- Si la sonda está habilitada, se deshabilita; si está deshabilitada, se habilita.
- Se muestra un mensaje de éxito después de realizar la operación.

Retorno
-------
- Después de modificar el estado de la sonda, se redirige a la vista ``manage_probe`` con un mensaje de éxito o error.

---

edit_probe
===========

Esta vista permite editar una sonda existente.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se intenta obtener el ID de la sonda a editar desde la solicitud POST o la sesión.
- Se obtiene el objeto de la sonda y se carga en un formulario para ser editado.
- El formulario se presenta al usuario para editar los detalles de la sonda.

Retorno
-------
- La vista retorna la plantilla ``edit_probe.html`` con el formulario de edición de la sonda y su información cargada.

save_edit_probe
================

Esta vista permite guardar los cambios realizados a una sonda existente.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es POST, se actualiza el nombre de la sonda con el valor proporcionado en el formulario.
- Si la operación es exitosa, se retorna una respuesta JSON con ``{'success': True}``.
- Si no se recibe una solicitud POST, se redirige a la vista ``edit_probe``.

Retorno
-------
- Una respuesta JSON con ``{'success': True}`` si la actualización fue exitosa.
- Si no se recibe una solicitud POST, se redirige a la vista ``edit_probe``.

---

manage_aditivos
===============

Esta vista muestra la lista de aditivos disponibles.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se obtiene la lista de aditivos de la base de datos y se ordena alfabéticamente.
- Los aditivos se pasan al contexto para ser mostrados en la plantilla ``manage_aditivos.html``.

Retorno
-------
- La vista retorna la plantilla ``manage_aditivos.html`` con la lista de aditivos ordenados.

---

new_aditivos
=============

Esta vista permite crear un nuevo aditivo.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se renderiza el formulario para agregar un nuevo aditivo. 
- El formulario es pasado al contexto para ser mostrado en la plantilla ``new_aditivos.html``.

Retorno
-------
- La vista retorna la plantilla ``new_aditivos.html`` con el formulario para crear un nuevo aditivo.

save_new_aditivos
==================

Esta vista permite guardar un nuevo aditivo en el sistema.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es POST, se verifica si ya existe un aditivo con el mismo nombre.
  - Si ya existe, retorna el objeto ``aditivo``.
  - Si no existe, se valida el formulario y se guarda el nuevo aditivo en la base de datos.
  - Si el formulario es válido, se guarda el aditivo y se retorna una respuesta JSON con ``{'success': True}``.
  - Si el formulario no es válido, se retorna una respuesta JSON con ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si no se recibe una solicitud POST, se muestra un mensaje de error y se redirige a ``manage_aditivos``.

Retorno
-------
- Una respuesta JSON con ``{'success': True}`` si el aditivo fue guardado correctamente.
- Si el formulario no es válido, retorna ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si no se recibe una solicitud POST, se redirige a ``manage_aditivos``.

---

status_aditivos
===============

Esta vista permite habilitar o deshabilitar un aditivo.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es POST, se obtiene el aditivo con el ID proporcionado.
- Si el aditivo está habilitado, se deshabilita, y se muestra un mensaje de éxito.
- Si el aditivo está deshabilitado, se habilita, y también se muestra un mensaje de éxito.
- Si no se recibe una solicitud POST, se muestra un mensaje de error y se redirige a ``manage_aditivos``.

Retorno
-------
- Una redirección a ``manage_aditivos`` con un mensaje de éxito dependiendo de si el aditivo fue habilitado o deshabilitado.
- Si no se recibe una solicitud POST, se redirige con un mensaje de error.

---

edit_aditivos
==============

Esta vista permite editar un aditivo existente en el sistema.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se intenta obtener el ``id`` del aditivo a editar desde la solicitud POST. Si no está presente, se recupera desde la sesión.
- Luego, se obtiene el aditivo correspondiente a ese ``id`` desde la base de datos.
- Se crea un formulario de edición pre-poblado con el valor del aditivo seleccionado.
- Finalmente, se pasa el formulario y el aditivo a la plantilla ``edit_aditivos.html`` para que el usuario pueda realizar cambios.

Retorno
-------
- Se renderiza la plantilla ``edit_aditivos.html`` con el formulario pre-poblado y la información necesaria para editar el aditivo.

save_edit_aditivos
==================

Esta vista permite guardar los cambios realizados en un aditivo existente.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se actualiza el aditivo correspondiente en la base de datos con el nuevo valor recibido desde el formulario.
- El proceso de actualización se realiza mediante el método ``update`` en el modelo ``Aditivos``.
- Si la operación es exitosa, se devuelve un ``JsonResponse`` con un valor ``{'success': True}``.

Retorno
-------
- Si la solicitud no es ``POST``, el usuario será redirigido a la vista ``edit_aditivos``.
- Si la operación es exitosa, se devuelve una respuesta JSON con el resultado de la acción.

---

manage_cantidadAgua
===================

Esta vista muestra una lista de todas las cantidades de agua registradas en el sistema.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los registros en el modelo ``CantidadAgua`` ordenada por la cantidad de agua.
- Se renderiza la plantilla ``manage_cantidadAgua.html`` con la lista de registros.

Retorno
-------
- Se renderiza la plantilla ``manage_cantidadAgua.html`` con la lista de registros de cantidad de agua.

---

new_cantidadAgua
================

Esta vista permite mostrar un formulario para agregar una nueva cantidad de agua.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Se crea un formulario vacío de tipo ``FormCantidadAgua`` para agregar una nueva cantidad de agua.
- Se renderiza la plantilla ``new_cantidadAgua.html`` con el formulario.

Retorno
-------
- Se renderiza la plantilla ``new_cantidadAgua.html`` con el formulario para agregar una nueva cantidad de agua.

save_new_cantidadAgua
======================

Esta vista permite guardar una nueva cantidad de agua en el sistema.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se verifica si ya existe una cantidad de agua con el mismo nombre.
  - Si existe, se devuelve el objeto existente.
  - Si no existe, se valida el formulario ``FormCantidadAgua``.
- Si el formulario es válido, se crea una nueva entrada de ``CantidadAgua`` con el valor proporcionado, marcándola como activa (status = True), y se guarda en la base de datos.
- Si el formulario no es válido, se devuelve un mensaje indicando que el formulario no es válido.

Retorno
-------
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_cantidadAgua``.
- Si la operación es exitosa, se devuelve una respuesta JSON con el resultado de la acción.

---

status_cantidadAgua
===================

Esta vista permite habilitar o deshabilitar una cantidad de agua.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se obtiene el registro de la cantidad de agua correspondiente al ``id`` proporcionado.
- Si la cantidad de agua está habilitada, se deshabilita y se muestra un mensaje de éxito.
- Si la cantidad de agua está deshabilitada, se habilita y se muestra un mensaje de éxito.

Retorno
-------
- Si la operación es exitosa, se redirige a la vista ``manage_cantidadAgua``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_cantidadAgua``.

---

edit_cantidadAgua
=================

Esta vista permite editar los datos de una cantidad de agua existente.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si el ``id`` de la cantidad de agua está presente en el ``POST``, se guarda en la sesión para usarlo en la búsqueda del objeto correspondiente.
- Luego se obtiene el objeto ``CantidadAgua`` utilizando el ``id`` almacenado en la sesión.
- Se carga un formulario de edición ``FormCantidadAgua`` con los valores actuales de la cantidad de agua y se presenta en el contexto de la plantilla.

Retorno
-------
- Se renderiza la plantilla ``edit_cantidadAgua.html`` con el formulario de edición de la cantidad de agua.

save_new_cantidadAgua
======================

Esta vista permite guardar una nueva cantidad de agua en el sistema.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se verifica si ya existe una cantidad de agua con el mismo nombre.
  - Si existe, se devuelve el objeto existente.
  - Si no existe, se valida el formulario ``FormCantidadAgua``.
- Si el formulario es válido, se crea una nueva entrada de ``CantidadAgua`` con el valor proporcionado, marcándola como activa (status = True), y se guarda en la base de datos.
- Si el formulario no es válido, se devuelve un mensaje indicando que el formulario no es válido.

Retorno
-------
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_cantidadAgua``.
- Si la operación es exitosa, se devuelve una respuesta JSON con el resultado de la acción.

---

status_cantidadAgua
===================

Esta vista permite habilitar o deshabilitar una cantidad de agua.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se obtiene el registro de la cantidad de agua correspondiente al ``id`` proporcionado.
- Si la cantidad de agua está habilitada, se deshabilita y se muestra un mensaje de éxito.
- Si la cantidad de agua está deshabilitada, se habilita y se muestra un mensaje de éxito.

Retorno
-------
- Si la operación es exitosa, se redirige a la vista ``manage_cantidadAgua``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_cantidadAgua``.

---

edit_cantidadAgua
=================

Esta vista permite editar los datos de una cantidad de agua existente.

Decoradores
-----------
- ``@login_required``: Asegura que solo los usuarios autenticados puedan acceder a esta vista.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Permite el acceso solo a usuarios con privilegios de administrador, base de datos o supervisor en el contexto de sondajes.

Funcionamiento
--------------
- Si el ``id`` de la cantidad de agua está presente en el ``POST``, se guarda en la sesión para usarlo en la búsqueda del objeto correspondiente.
- Luego se obtiene el objeto ``CantidadAgua`` utilizando el ``id`` almacenado en la sesión.
- Se carga un formulario de edición ``FormCantidadAgua`` con los valores actuales de la cantidad de agua y se presenta en el contexto de la plantilla.

Retorno
-------
- Se renderiza la plantilla ``edit_cantidadAgua.html`` con el formulario de edición de la cantidad de agua.

save_edit_cantidadAgua
=======================

Esta vista permite guardar los cambios realizados en una cantidad de agua existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se busca la cantidad de agua por su ``id`` y se actualiza el valor del campo ``cantidadAgua`` con la nueva información proporcionada en el formulario.
- Si la actualización es exitosa, se devuelve una respuesta JSON indicando el éxito de la operación.

Retorno
-------
- Si la operación es exitosa, se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_cantidadAgua``.

---

manage_casing
=============

Esta vista muestra la lista de registros de casing almacenados en el sistema.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los registros de ``Casing`` ordenados por el campo ``casing``.
- Se pasa esta lista al contexto de la plantilla para su visualización.

Retorno
-------
- Se renderiza la plantilla ``manage_casing.html`` con la lista de registros de casing.

---

new_casing
==========

Esta vista permite acceder al formulario para registrar un nuevo casing.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se carga el formulario ``FormCasing`` en el contexto de la plantilla.

Retorno
-------
- Se renderiza la plantilla ``new_casing.html`` con el formulario para la creación de un nuevo casing.

save_new_casing
===============

Esta vista permite registrar un nuevo casing en el sistema.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se verifica si el casing ya existe en la base de datos.
- Si el casing existe, se retorna sin registrar un nuevo documento.
- Si no existe, se valida el formulario ``FormCasing`` y, si es válido, se crea un nuevo registro con el nombre del usuario como creador.
- Si el formulario es válido, se devuelve una respuesta JSON indicando el éxito de la operación.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_casing``.

Retorno
-------
- Si la operación es exitosa, se devuelve una respuesta JSON con ``{'success': True}``.
- Si el formulario no es válido, se devuelve una respuesta JSON con ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si la solicitud no es ``POST``, se redirige a ``manage_casing`` con un mensaje de error.

---

status_casing
=============

Esta vista permite cambiar el estado de un casing (habilitar o deshabilitar).

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se obtiene el casing por su ``id``.
- Se cambia el estado del casing:
  - Si estaba habilitado, se deshabilita.
  - Si estaba deshabilitado, se habilita.
- Se muestra un mensaje de éxito indicando el cambio de estado.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a ``manage_casing``.

Retorno
-------
- Se redirige a ``manage_casing`` con un mensaje de éxito o error según corresponda.

---

edit_casing
===========

Esta vista permite acceder al formulario de edición de un casing.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene el ``id`` del casing desde la solicitud ``POST`` y se almacena en la sesión.
- Se busca el casing correspondiente en la base de datos.
- Se crea un formulario ``FormCasing`` con los datos actuales del casing.
- Se pasa el formulario y el ``id`` del documento al contexto de la plantilla.

Retorno
-------
- Se renderiza la plantilla ``edit_casing.html`` con el formulario de edición del casing.

save_edit_casing
=================

Esta vista permite guardar las ediciones realizadas en un casing.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se actualiza el casing con el nuevo nombre proporcionado en el formulario.
- Se utiliza ``filter`` y ``update`` para modificar el casing correspondiente en la base de datos utilizando el ``id`` proporcionado en la solicitud.
- Se devuelve una respuesta JSON indicando el éxito de la operación.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_casing``.

Retorno
-------
- Si la operación es exitosa, se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_casing``.

---

manage_corona
=============

Esta vista muestra la lista de coronas registradas en el sistema.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todas las coronas registradas en la base de datos, ordenadas por nombre.
- El contexto incluye la lista de coronas y algunos datos de navegación para la plantilla.

Retorno
-------
- Se renderiza la plantilla ``manage_corona.html`` con el listado de coronas.

---

new_corona
==========

Esta vista permite mostrar el formulario para crear una nueva corona.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se muestra un formulario vacío de tipo ``FormCorona`` para registrar una nueva corona.
- Se pasan datos de navegación al contexto para la plantilla.

Retorno
-------
- Se renderiza la plantilla ``new_corona.html`` con el formulario para la creación de una nueva corona.

save_new_corona
================

Esta vista permite guardar una nueva corona en el sistema.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, intenta obtener una corona existente con el nombre proporcionado.
- Si no existe, se crea una nueva corona utilizando los datos proporcionados en el formulario.
- El formulario es validado antes de guardar la nueva corona en la base de datos.
- Si la corona se guarda correctamente, se devuelve una respuesta JSON indicando que la operación fue exitosa.
- Si el formulario no es válido, se devuelve un mensaje de error.

Retorno
-------
- Si la operación es exitosa, se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST`` o si el formulario es inválido, se redirige a la vista ``manage_corona`` con un mensaje de error.

---

status_corona
==============

Esta vista permite habilitar o deshabilitar una corona.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se obtiene la corona correspondiente al ``id`` enviado.
- Si la corona está habilitada, se deshabilita y se muestra un mensaje de éxito.
- Si la corona está deshabilitada, se habilita y se muestra un mensaje de éxito.
- Se redirige a la vista ``manage_corona`` después de realizar el cambio.

Retorno
-------
- Se redirige a la vista ``manage_corona`` con un mensaje de éxito si el cambio fue exitoso.
- Si la solicitud no es ``POST``, se redirige a la vista ``manage_corona`` con un mensaje de error.

---

edit_corona
============

Esta vista permite editar los detalles de una corona existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud contiene un ``id``, se guarda en la sesión el ``id`` del documento a editar.
- Se obtiene el objeto ``Corona`` correspondiente a ese ``id`` y se pre-carga el formulario con los datos actuales.
- Se pasa el formulario de edición y el ``id`` del documento al contexto de la plantilla.

Retorno
-------
- Se renderiza la plantilla ``edit_corona.html`` con el formulario de edición de la corona.

save_edit_corona
=================

Esta vista permite guardar las modificaciones de una corona existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, actualiza el nombre de la corona correspondiente al ``id`` proporcionado.
- La corona es actualizada utilizando el campo ``corona`` recibido desde el formulario.

Retorno
-------
- Si la operación es exitosa, se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_corona``.

---

manage_details
==============

Esta vista gestiona los detalles del control horario en el sistema.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Obtiene todos los registros de ``DetalleControlHorario`` ordenados por el campo ``detalle``.
- Pasa la lista de detalles y la información de la barra lateral (menú) al contexto de la plantilla.

Retorno
-------
- Se renderiza la plantilla ``manage_details.html`` con la lista de detalles del control horario.

---

new_details
============

Esta vista permite crear un nuevo detalle de control horario.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se pasa un formulario vacío (``FormDetalleControlHorario``) al contexto de la plantilla para crear un nuevo detalle.

Retorno
-------
- Se renderiza la plantilla ``new_details.html`` con el formulario para crear un nuevo detalle de control horario.

save_new_details
=================

Esta vista permite crear un nuevo detalle de control horario.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se verifica si ya existe un detalle con el mismo nombre, utilizando el campo ``detalle``.
    - Si no existe, se crea un nuevo registro de ``DetalleControlHorario`` con los datos del formulario y se guarda en la base de datos.
    - Si el formulario no es válido, se devuelve una respuesta JSON con el estado ``success: False``.
  
Retorno
-------
- Si la operación es exitosa, se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``manage_details``.

---

status_details
==============

Esta vista permite habilitar o deshabilitar un detalle de control horario.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se obtiene el detalle de control horario correspondiente al ``id`` proporcionado.
    - Si el estado del detalle es ``True``, se cambia a ``False`` (deshabilitado).
    - Si el estado es ``False``, se cambia a ``True`` (habilitado).
    - Se muestra un mensaje de éxito indicando si se habilitó o deshabilitó el detalle correctamente.

Retorno
-------
- Después de actualizar el estado, se redirige a la vista ``manage_details``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la misma vista.

---

edit_details
=============

Esta vista permite editar un detalle de control horario existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene el ``id`` del detalle de control horario que se desea editar. El ``id`` se guarda en la sesión.
- Si no existe el ``id`` en la sesión, se captura un error y se utiliza el ``id`` de la sesión anterior.
- Se pasa el detalle a un formulario de edición con los datos existentes.

Retorno
-------
- Se renderiza la plantilla ``edit_details.html`` con el formulario para editar el detalle de control horario.

save_edit_details
==================

Esta vista permite guardar la edición de un detalle de control horario.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se actualiza el campo ``detalle`` del ``DetalleControlHorario`` correspondiente al ``id`` proporcionado en el formulario.
  
Retorno
-------
- Si la operación es exitosa, se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_details``.

---

manage_diameter
================

Esta vista muestra la lista de los diámetros disponibles en la base de datos.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de los objetos ``Diametros`` ordenados por el campo ``diametro``.
- Esta lista se pasa a la plantilla ``manage_diameter.html`` para ser visualizada por el usuario.

Retorno
-------
- Se renderiza la plantilla ``manage_diameter.html`` con los diámetros disponibles.

---

new_diameter
=============

Esta vista muestra el formulario para crear un nuevo diámetro.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se pasa un formulario vacío de tipo ``FormDiametros`` a la plantilla ``new_diameter.html``.

Retorno
-------
- Se renderiza la plantilla ``new_diameter.html`` con el formulario para crear un nuevo diámetro.

save_new_diameter
==================

Esta vista permite guardar un nuevo diámetro.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se comprueba si ya existe un ``Diametros`` con el valor del campo ``diametro`` proporcionado en el formulario.
    - Si el diámetro ya existe, se devuelve el objeto.
    - Si el diámetro no existe, se valida el formulario, y si es válido, se crea un nuevo objeto ``Diametros`` con el valor proporcionado y se guarda en la base de datos.
  
Retorno
-------
- Si la operación es exitosa, se devuelve una respuesta JSON con ``{'success': True}``.
- Si el formulario no es válido, se devuelve una respuesta JSON con ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``manage_diameter``.

---

status_diameter
================

Esta vista permite cambiar el estado de un diámetro (habilitar o deshabilitar).

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se obtiene el objeto ``Diametros`` correspondiente al ``id`` proporcionado en el formulario.
    - Si el estado del diámetro es ``True`` (habilitado), se cambia a ``False`` (deshabilitado), y se muestra un mensaje de éxito.
    - Si el estado del diámetro es ``False`` (deshabilitado), se cambia a ``True`` (habilitado), y se muestra un mensaje de éxito.

Retorno
-------
- Si la operación es exitosa, se redirige a la vista ``manage_diameter``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_diameter``.

---

edit_diameter
==============

Esta vista permite editar un diámetro existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud contiene el parámetro ``id`` en el ``POST``, se guarda ese valor en la sesión.
- Se obtiene el objeto ``Diametros`` correspondiente al ``id`` guardado en la sesión.
- Se pasa un formulario prellenado con los datos del diámetro al contexto de la plantilla ``edit_diameter.html``.
  
Retorno
-------
- Se renderiza la plantilla ``edit_diameter.html`` con el formulario para editar el diámetro.

save_edit_diameter
===================

Esta vista permite editar un diámetro existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se actualiza el objeto ``Diametros`` correspondiente al ``id`` proporcionado, cambiando su valor de ``diametro`` por el nuevo valor enviado.
  
Retorno
-------
- Si la operación es exitosa, se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_diameter``.

---

manage_drilling
================

Esta vista permite gestionar los sondajes existentes.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los objetos ``Sondajes`` ordenados por el campo ``sondaje``.
- La lista de sondajes se pasa al contexto de la plantilla ``manage_drilling.html``.

Retorno
-------
- Se renderiza la plantilla ``manage_drilling.html`` con la lista de sondajes y la configuración del menú lateral.

---

new_drilling
=============

Esta vista permite crear un nuevo sondaje.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se pasa al contexto un formulario vacío de tipo ``FormSondajes`` para crear un nuevo sondaje.
  
Retorno
-------
- Se renderiza la plantilla ``new_drilling.html`` con el formulario vacío para crear un nuevo sondaje.

save_new_drilling
==================

Esta vista permite crear un nuevo sondaje.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se obtiene el objeto ``Faena`` correspondiente al ``id`` enviado.
    - Se verifica si ya existe un objeto ``Sondajes`` con el ``sondaje`` proporcionado. Si existe, se devuelve dicho objeto.
    - Si no existe, se crea un nuevo ``Sondajes`` utilizando los datos del formulario, asignando como ``faena`` el objeto previamente obtenido y el resto de los campos desde el formulario.
    - Si el formulario es válido, se guarda el nuevo sondaje y se devuelve una respuesta JSON con ``{'success': True}``.
    - Si el formulario no es válido, se devuelve una respuesta JSON con el mensaje de error.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``manage_drilling`` con un mensaje de error.

---

status_drilling
================

Esta vista permite cambiar el estado (habilitado/deshabilitado) de un sondaje.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se obtiene el objeto ``Sondajes`` correspondiente al ``id`` enviado.
    - Se cambia el estado del sondaje:
        - Si el estado es ``True`` (habilitado), se cambia a ``False`` (deshabilitado).
        - Si el estado es ``False`` (deshabilitado), se cambia a ``True`` (habilitado).
    - Se muestra un mensaje de éxito dependiendo del cambio realizado.

Retorno
-------
- Se redirige a la vista ``manage_drilling`` después de cambiar el estado.

---

edit_drilling
==============

Esta vista permite editar un sondaje existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Intenta obtener el ``id`` del sondaje a editar desde el ``POST`` o desde la sesión.
- Se obtiene el objeto ``Sondajes`` correspondiente al ``id`` obtenido.
- Se pasa un formulario de edición inicializado con los datos del sondaje para editarlo.
  
Retorno
-------
- Se renderiza la plantilla ``edit_drilling.html`` con el formulario de edición y los datos del sondaje.

save_edit_drilling
===================

Esta vista permite editar un sondaje existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se actualiza el objeto ``Sondajes`` correspondiente al ``id`` enviado, modificando los campos ``faena`` y ``sondaje`` con los valores proporcionados en el formulario.
    - Se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_drilling``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_drilling``.

---

manage_escareador
=================

Esta vista muestra una lista de todos los escareadores disponibles.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los objetos ``Escareador``, ordenados por el campo ``escareador``.
- Se pasa la lista obtenida a la plantilla para su renderización, junto con otros datos necesarios para la navegación en el sistema.

Retorno
-------
- Se renderiza la plantilla ``manage_escareador.html`` con la lista de escareadores.

---

new_escareador
===============

Esta vista muestra un formulario para crear un nuevo escareador.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se renderiza un formulario vacío de ``FormEscareador`` para la creación de un nuevo escareador.
- Se pasan otros datos al contexto para la navegación en el sistema.

Retorno
-------
- Se renderiza la plantilla ``new_escareador.html`` con el formulario para crear un nuevo escareador.

save_new_escareador
===================

Esta vista permite crear un nuevo escareador.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se verifica si ya existe un escareador con el mismo nombre.
    - Si el escareador ya existe, se devuelve el objeto.
    - Si el escareador no existe, se valida el formulario ``FormEscareador``:
        - Si el formulario es válido, se crea un nuevo escareador y se guarda en la base de datos.
        - Se devuelve una respuesta JSON con ``{'success': True}`` si la operación es exitosa.
        - Si el formulario no es válido, se devuelve una respuesta JSON con ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``manage_escareador``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si el formulario no es válido, se devuelve ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``manage_escareador``.

---

status_escareador
=================

Esta vista permite habilitar o deshabilitar un escareador.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se obtiene el objeto ``Escareador`` correspondiente al ``id`` enviado.
    - Si el escareador está habilitado (``status=True``), se deshabilita (``status=False``).
    - Si el escareador está deshabilitado (``status=False``), se habilita (``status=True``).
    - Se muestra un mensaje de éxito indicando si el escareador fue habilitado o deshabilitado correctamente.
    - Se redirige a la vista ``manage_escareador``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_escareador``.

Retorno
-------
- Si la operación es exitosa, se redirige a la vista ``manage_escareador`` con un mensaje de éxito.
- Si no es una solicitud ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_escareador``.

---

edit_escareador
================

Esta vista permite editar un escareador existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se guarda el ``id`` del escareador a editar en la sesión.
    - Se obtiene el objeto ``Escareador`` correspondiente al ``id`` de la sesión.
    - Se renderiza un formulario de edición pre-rellenado con los datos del escareador.
    - Se muestra la vista ``edit_escareador.html`` con el formulario para editar el escareador.

Retorno
-------
- Se renderiza la plantilla ``edit_escareador.html`` con el formulario de edición del escareador.

save_edit_escareador
====================

Esta vista permite editar un escareador existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se actualiza el campo ``escareador`` del objeto ``Escareador`` correspondiente al ``id`` enviado.
    - Se devuelve una respuesta JSON con ``{'success': True}`` si la operación es exitosa.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_escareador``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``edit_escareador``.

---

manage_largoBarra
=================

Esta vista permite gestionar los objetos de tipo ``LargoBarra``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtienen todos los objetos de tipo ``LargoBarra`` y se ordenan por el campo ``largoBarra``.
- Se pasa la lista de objetos ``LargoBarra`` a la plantilla ``manage_largoBarra.html`` junto con información sobre el menú y submenú activos.

Retorno
-------
- Se renderiza la plantilla ``manage_largoBarra.html`` con la lista de objetos ``LargoBarra`` y las configuraciones del menú.

---

new_largoBarra
================

Esta vista permite crear un nuevo objeto ``LargoBarra``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se renderiza la plantilla ``new_largoBarra.html`` con un formulario vacío para crear un nuevo objeto ``LargoBarra``.
- Se pasa el formulario ``FormLargoBarra`` a la plantilla, junto con información sobre el menú y submenú activos.

Retorno
-------
- Se renderiza la plantilla ``new_largoBarra.html`` con el formulario para crear un nuevo ``LargoBarra``.

save_new_largoBarra
====================

Esta vista permite guardar un nuevo objeto ``LargoBarra``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se verifica si ya existe un objeto ``LargoBarra`` con el nombre recibido en el formulario.
    - Si el objeto ya existe, se devuelve el objeto.
    - Si el objeto no existe, se crea uno nuevo con los datos del formulario.
    - Si el formulario es válido, se guarda el nuevo objeto y se devuelve una respuesta JSON con ``{'success': True}``.
    - Si el formulario no es válido, se devuelve una respuesta JSON con un mensaje de error.
- Si la solicitud no es ``POST``, se redirige a la vista ``manage_largoBarra``.

Retorno
-------
- Si el formulario es válido y el objeto se guarda, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``manage_largoBarra``.
- Si el formulario no es válido, se devuelve ``{'success': False, 'message': 'El formulario no es válido.'}``.

---

status_largoBarra
=================

Esta vista permite cambiar el estado de un objeto ``LargoBarra`` (habilitar o deshabilitar).

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se obtiene el objeto ``LargoBarra`` correspondiente al ``id`` recibido en el formulario.
    - Si el objeto está habilitado, se deshabilita (cambia su ``status`` a ``False``).
    - Si el objeto está deshabilitado, se habilita (cambia su ``status`` a ``True``).
    - Se muestra un mensaje de éxito con la acción realizada (habilitado o deshabilitado).
- Si la solicitud no es ``POST``, se redirige a la vista ``manage_largoBarra``.

Retorno
-------
- Si la operación es exitosa, se redirige a la vista ``manage_largoBarra`` con un mensaje de éxito.

---

edit_largoBarra
================

Esta vista permite editar un objeto ``LargoBarra``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si no existe una sesión con el ``id`` de la edición, se toma el ``id`` de la solicitud ``POST``.
- Se obtiene el objeto ``LargoBarra`` correspondiente al ``id`` almacenado en la sesión.
- Se pasa el objeto ``LargoBarra`` a la plantilla de edición con el formulario ``FormLargoBarra`` que se rellena con los datos actuales del objeto.
- Se renderiza la plantilla ``edit_largoBarra.html`` con el formulario y la información sobre el menú y submenú activos.

Retorno
-------
- Se renderiza la plantilla ``edit_largoBarra.html`` con el formulario para editar el objeto ``LargoBarra``.

save_edit_largoBarra
=====================

Esta vista permite editar un objeto ``LargoBarra``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se actualiza el objeto ``LargoBarra`` con el nuevo valor recibido para el campo ``largoBarra``.
    - Se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_largoBarra``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``edit_largoBarra``.

---

manage_orientation
==================

Esta vista muestra una lista de todos los objetos ``Orientacion`` ordenados por el campo ``orientacion``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los objetos ``Orientacion`` ordenados por el campo ``orientacion``.
- Se renderiza la plantilla ``manage_orientation.html`` y se pasa la lista de objetos y la información sobre el menú y submenú activos.

Retorno
-------
- Se renderiza la plantilla ``manage_orientation.html`` con la lista de objetos ``Orientacion``.

---

new_orientation
================

Esta vista permite crear un nuevo objeto ``Orientacion`` a través de un formulario.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se renderiza la plantilla ``new_orientation.html`` y se pasa el formulario ``FormOrientacion`` y la información sobre el menú y submenú activos.

Retorno
-------
- Se renderiza la plantilla ``new_orientation.html`` con el formulario para crear un nuevo objeto ``Orientacion``.

save_new_orientation
=====================

Esta vista permite crear un nuevo objeto ``Orientacion``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se verifica si el objeto ``Orientacion`` ya existe con el valor proporcionado para el campo ``orientacion``.
    - Si no existe, se valida el formulario y se crea un nuevo objeto ``Orientacion`` con los datos recibidos.
    - Se guarda el nuevo objeto en la base de datos.
    - Se devuelve una respuesta JSON con ``{'success': True}``.
- Si el formulario no es válido, se devuelve una respuesta JSON con ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_orientation``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``manage_orientation``.

---

status_orientation
==================

Esta vista permite cambiar el estado de un objeto ``Orientacion`` (habilitar/deshabilitar).

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se obtiene el objeto ``Orientacion`` con el ID proporcionado.
    - Si el estado actual es ``True``, se cambia a ``False`` y se muestra un mensaje de éxito.
    - Si el estado actual es ``False``, se cambia a ``True`` y se muestra un mensaje de éxito.
- Se redirige a la vista ``manage_orientation``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_orientation``.

Retorno
-------
- Se redirige a la vista ``manage_orientation`` con un mensaje de éxito o error.

---

edit_orientation
=================

Esta vista permite editar un objeto ``Orientacion``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene el objeto ``Orientacion`` a editar utilizando el ID almacenado en la sesión.
- Se renderiza la plantilla ``edit_orientation.html`` con el formulario de edición, prellenado con los datos del objeto ``Orientacion``.
- Se pasan datos adicionales sobre el menú y submenú activos.

Retorno
-------
- Se renderiza la plantilla ``edit_orientation.html`` con el formulario de edición.

---

save_edit_orientation
======================

Esta vista guarda los cambios realizados en un objeto ``Orientacion``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se actualiza el objeto ``Orientacion`` con los nuevos valores recibidos.
    - Se devuelve una respuesta JSON con ``{'success': True}``.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_orientation``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``edit_orientation``.

manage_tipoTerreno
===================

Esta vista muestra una lista de objetos ``TipoTerreno``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los objetos ``TipoTerreno`` ordenados por el campo ``tipoTerreno``.
- Se renderiza la plantilla ``manage_tipoTerreno.html`` con los objetos listados.

Retorno
-------
- Se renderiza la plantilla ``manage_tipoTerreno.html`` con los objetos ``TipoTerreno``.

---

new_tipoTerreno
================

Esta vista muestra un formulario para crear un nuevo objeto ``TipoTerreno``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se muestra un formulario para crear un nuevo ``TipoTerreno``.
- Se pasa el formulario vacío a la plantilla ``new_tipoTerreno.html``.

Retorno
-------
- Se renderiza la plantilla ``new_tipoTerreno.html`` con el formulario de creación.

---

save_new_tipoTerreno
=====================

Esta vista guarda un nuevo objeto ``TipoTerreno``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se verifica si el objeto ``TipoTerreno`` ya existe con el valor proporcionado para el campo ``tipoTerreno``.
    - Si no existe, se valida el formulario y se crea un nuevo objeto ``TipoTerreno`` con los datos recibidos.
    - Se guarda el nuevo objeto en la base de datos.
    - Se devuelve una respuesta JSON con ``{'success': True}``.
- Si el formulario no es válido, se devuelve una respuesta JSON con ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_tipoTerreno``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``manage_tipoTerreno``.

---

status_tipoTerreno
===================

Esta vista permite cambiar el estado de un objeto ``TipoTerreno`` (habilitar/deshabilitar).

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se obtiene el objeto ``TipoTerreno`` con el ID proporcionado.
    - Si el estado actual es ``True``, se cambia a ``False`` y se muestra un mensaje de éxito.
    - Si el estado actual es ``False``, se cambia a ``True`` y se muestra un mensaje de éxito.
- Se redirige a la vista ``manage_tipoTerreno``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_tipoTerreno``.

Retorno
-------
- Se redirige a la vista ``manage_tipoTerreno`` con un mensaje de éxito o error.

edit_tipoTerreno
=================

Esta vista permite editar un objeto ``TipoTerreno``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se intenta obtener el ID del ``TipoTerreno`` desde la solicitud ``POST`` y almacenarlo en la sesión.
- Si el ID no está presente, se usa el valor almacenado previamente en la sesión.
- Se obtiene el objeto ``TipoTerreno`` correspondiente al ID de la sesión.
- Se pasa un formulario para editar el campo ``tipoTerreno`` del objeto a la plantilla ``edit_tipoTerreno.html``.

Retorno
-------
- Se renderiza la plantilla ``edit_tipoTerreno.html`` con el formulario de edición y el objeto ``TipoTerreno``.

---

save_edit_tipoTerreno
======================

Esta vista guarda los cambios realizados en un objeto ``TipoTerreno``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se actualiza el campo ``tipoTerreno`` del objeto con el ID proporcionado.
- Se devuelve una respuesta JSON indicando el éxito de la operación.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_tipoTerreno``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``edit_tipoTerreno``.

---

manage_zapata
==============

Esta vista muestra una lista de objetos ``Zapata``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los objetos ``Zapata`` ordenados por el campo ``zapata``.
- Se renderiza la plantilla ``manage_zapata.html`` con los objetos listados.

Retorno
-------
- Se renderiza la plantilla ``manage_zapata.html`` con los objetos ``Zapata``.

---

new_zapata
============

Esta vista muestra un formulario para crear un nuevo objeto ``Zapata``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se muestra un formulario para crear un nuevo ``Zapata``.
- Se pasa el formulario vacío a la plantilla ``new_zapata.html``.

Retorno
-------
- Se renderiza la plantilla ``new_zapata.html`` con el formulario de creación.

---

save_new_zapata
================

Esta vista guarda un nuevo objeto ``Zapata``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``:
    - Se verifica si el objeto ``Zapata`` ya existe con el valor proporcionado para el campo ``zapata``.
    - Si no existe, se valida el formulario y se crea un nuevo objeto ``Zapata`` con los datos recibidos.
    - Se guarda el nuevo objeto en la base de datos.
    - Se devuelve una respuesta JSON con ``{'success': True}``.
- Si el formulario no es válido, se devuelve una respuesta JSON con ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_zapata``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``manage_zapata``.

status_zapata
===============

Esta vista permite habilitar o deshabilitar un objeto ``Zapata``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se obtiene el objeto ``Zapata`` con el ID proporcionado.
- Si el campo ``status`` de la ``Zapata`` es ``True``, se cambia a ``False`` y se muestra un mensaje indicando que la zapata ha sido deshabilitada correctamente.
- Si el campo ``status`` de la ``Zapata`` es ``False``, se cambia a ``True`` y se muestra un mensaje indicando que la zapata ha sido habilitada correctamente.
- Se redirige a la vista ``manage_zapata``.
- Si la solicitud no es de tipo ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_zapata``.

Retorno
-------
- Redirige a la vista ``manage_zapata`` después de realizar la acción correspondiente.

---

edit_zapata
============

Esta vista permite editar un objeto ``Zapata``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se intenta obtener el ID de la ``Zapata`` desde la solicitud ``POST`` y almacenarlo en la sesión.
- Si el ID no está presente, se usa el valor almacenado previamente en la sesión.
- Se obtiene el objeto ``Zapata`` correspondiente al ID de la sesión.
- Se pasa un formulario para editar el campo ``zapata`` del objeto a la plantilla ``edit_zapata.html``.

Retorno
-------
- Se renderiza la plantilla ``edit_zapata.html`` con el formulario de edición y el objeto ``Zapata``.

---

save_edit_zapata
=================

Esta vista guarda los cambios realizados en un objeto ``Zapata``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se actualiza el campo ``zapata`` del objeto con el ID proporcionado.
- Se devuelve una respuesta JSON indicando el éxito de la operación.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_zapata``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``edit_zapata``.

---

manage_perforista
==================

Esta vista muestra una lista de objetos ``Perforistas``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los objetos ``Perforistas`` ordenados por el campo ``perforista``.
- Se renderiza la plantilla ``manage_perforista.html`` con los objetos listados.

Retorno
-------
- Se renderiza la plantilla ``manage_perforista.html`` con los objetos ``Perforistas``.

new_perforista
================

Esta vista muestra un formulario para crear un nuevo objeto ``Perforista``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se renderiza un formulario vacío para crear un nuevo objeto ``Perforista``.
- Se pasa a la plantilla ``new_perforista.html`` con el formulario.

Retorno
-------
- Se renderiza la plantilla ``new_perforista.html`` con el formulario.

---

save_new_perforista
====================

Esta vista guarda un nuevo objeto ``Perforista`` en la base de datos.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se intenta obtener un objeto ``Perforista`` con el nombre proporcionado en el formulario.
- Si el objeto ya existe, no se crea uno nuevo y se retorna el objeto encontrado.
- Si el objeto no existe, se valida el formulario y si es válido, se crea un nuevo ``Perforista`` y se guarda en la base de datos.
- Se devuelve una respuesta JSON indicando el éxito o el fracaso de la operación.

Retorno
-------
- Si el formulario es válido y el ``Perforista`` se guarda correctamente, se devuelve ``{'success': True}``.
- Si el formulario no es válido, se devuelve ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si la solicitud no es ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_perforista``.

---

status_perforista
==================

Esta vista permite habilitar o deshabilitar un objeto ``Perforista``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se obtiene el objeto ``Perforista`` con el ID proporcionado.
- Si el campo ``status`` de la ``Perforista`` es ``True``, se cambia a ``False`` y se muestra un mensaje indicando que el perforista ha sido deshabilitado correctamente.
- Si el campo ``status`` de la ``Perforista`` es ``False``, se cambia a ``True`` y se muestra un mensaje indicando que el perforista ha sido habilitado correctamente.
- Se redirige a la vista ``manage_perforista``.
- Si la solicitud no es de tipo ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_perforista``.

Retorno
-------
- Redirige a la vista ``manage_perforista`` después de realizar la acción correspondiente.

---

edit_perforista
================

Esta vista permite editar un objeto ``Perforista``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se intenta obtener el ID del ``Perforista`` desde la solicitud ``POST`` y almacenarlo en la sesión.
- Si el ID no está presente, se usa el valor almacenado previamente en la sesión.
- Se obtiene el objeto ``Perforista`` correspondiente al ID de la sesión.
- Se pasa un formulario para editar el campo ``perforista`` del objeto a la plantilla ``edit_perforista.html``.

Retorno
-------
- Se renderiza la plantilla ``edit_perforista.html`` con el formulario de edición y el objeto ``Perforista``.

---

save_edit_perforista
====================

Esta vista guarda los cambios realizados en un objeto ``Perforista``.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se actualiza el campo ``perforista`` del objeto con el ID proporcionado.
- Se devuelve una respuesta JSON indicando el éxito de la operación.
- Si la solicitud no es ``POST``, se redirige a la vista ``edit_perforista``.

Retorno
-------
- Si la operación es exitosa, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``edit_perforista``.

manage_recomendaciones
=======================

Esta vista maneja la visualización de todas las recomendaciones existentes.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene la lista de todas las recomendaciones ordenadas por el campo ``recomendacion``.
- Se procesan los campos ``este``, ``norte`` y ``cota`` para eliminar ceros innecesarios al final de los valores.
- Se ajusta el campo ``largo_real`` para que solo sea modificado si su valor es igual a cero.
- Se pasa la lista de recomendaciones a la plantilla ``manage_recomendacion.html``.

Retorno
-------
- Se renderiza la plantilla ``manage_recomendacion.html`` con la lista de recomendaciones.

---

new_recomendacion
==================

Esta vista muestra un formulario para crear una nueva recomendación.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se renderiza un formulario vacío para crear una nueva recomendación.
- Se pasa el formulario a la plantilla ``new_recomendacion.html``.

Retorno
-------
- Se renderiza la plantilla ``new_recomendacion.html`` con el formulario vacío.

---

save_new_recomendacion
=======================

Esta vista guarda una nueva recomendación en la base de datos.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se valida que la recomendación no exista previamente en la base de datos.
- Se valida el formulario y si es válido, se crea una nueva recomendación con los datos proporcionados.
- Si el valor de ``azimut`` es válido (entre 0 y 360), se guarda la recomendación con los valores proporcionados.
- Si la sonda seleccionada no existe o si hay errores en los datos, se retorna un mensaje JSON de error.

Retorno
-------
- Si el formulario es válido y la recomendación se guarda correctamente, se devuelve ``{'success': True, 'message': 'Recomendación creada con éxito.'}``.
- Si la recomendación ya existe, se devuelve ``{'success': False, 'message': 'La recomendación ya existe.'}``.
- Si el formulario no es válido, se devuelve ``{'success': False, 'message': 'El formulario no es válido.', 'errors': formulario.errors}``.
- En caso de un error de conversión o un problema con los datos, se devuelve un mensaje de error específico.

---

status_recomendacion
====================

Esta vista permite habilitar o deshabilitar una recomendación.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es de tipo ``POST``, se obtiene el objeto ``Recomendacion`` con el ID proporcionado.
- Si el campo ``status`` de la recomendación es ``True``, se cambia a ``False`` y se muestra un mensaje indicando que la recomendación ha sido terminada correctamente.
- Si el campo ``status`` de la recomendación es ``False``, se cambia a ``True`` y se muestra un mensaje indicando que la recomendación ha sido activada correctamente.
- Se redirige a la vista ``manage_recomendacion``.
- Si la solicitud no es de tipo ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_recomendacion``.

Retorno
-------
- Redirige a la vista ``manage_recomendacion`` después de realizar la acción correspondiente.

edit_recomendacion
===================

Esta vista permite editar una recomendación existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se intenta obtener el ID de la recomendación a editar y se guarda en la sesión. Si no se encuentra un ID válido, se muestra un mensaje de error.
- Se obtiene la recomendación correspondiente desde la base de datos.
- Los valores opcionales, como ``este``, ``norte`` y ``cota``, se formatean para evitar errores si están vacíos o nulos.
- La fecha de inicio se ajusta para asegurar que esté en formato correcto.
- Se pasa un formulario prellenado a la plantilla ``edit_recomendacion.html`` con los datos de la recomendación.

Retorno
-------
- Se renderiza la plantilla ``edit_recomendacion.html`` con el formulario prellenado y los datos de la recomendación.

---

save_edit_recomendacion
========================

Esta vista guarda los cambios realizados a una recomendación.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se intenta obtener el ID de la recomendación a editar.
- Se realiza una validación de la fecha de inicio para asegurar que esté en el formato correcto.
- Se valida y convierte el valor del ``azimut`` asegurando que esté entre 0 y 360.
- Se validan otros valores numéricos como ``inclinacion``, ``largo_programado``, ``largo_real``, ``este``, ``norte`` y ``cota``.
- Se actualiza la recomendación con los nuevos valores proporcionados.
- Si algún dato es incorrecto o hay un error en la base de datos, se devuelve un mensaje JSON con el error.

Retorno
-------
- Si la recomendación se actualiza correctamente, se devuelve ``{'success': True, 'message': 'Recomendación actualizada con éxito.'}``.
- Si no se encuentra la recomendación o ocurre un error, se devuelve un mensaje de error específico.

---

manage_materiales_sonda
=======================

Esta vista muestra todos los materiales de la sonda existentes.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los materiales de la sonda ordenados por el campo ``material``.
- Se pasan los materiales a la plantilla ``manage_materiales_sonda.html``.

Retorno
-------
- Se renderiza la plantilla ``manage_materiales_sonda.html`` con la lista de materiales.

---

new_materiales_sonda
====================

Esta vista muestra un formulario para crear un nuevo material de sonda.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se renderiza un formulario vacío para crear un nuevo material de sonda.
- Se pasa el formulario a la plantilla ``new_materiales_sonda.html``.

Retorno
-------
- Se renderiza la plantilla ``new_materiales_sonda.html`` con el formulario vacío.

---

save_new_materiales_sonda
==========================

Esta vista guarda un nuevo material de sonda en la base de datos.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se valida que el material no exista previamente en la base de datos.
- Se valida el formulario y si es válido, se crea un nuevo material de sonda con los datos proporcionados.
- Si el material ya existe o el formulario no es válido, se retorna un mensaje JSON con un error.

Retorno
-------
- Si el material se guarda correctamente, se devuelve ``{'success': True}``.
- Si el material ya existe o el formulario no es válido, se devuelve ``{'success': False, 'message': 'El formulario no es válido.'}``.

status_materiales_sonda
========================

Esta vista cambia el estado de un material de sonda, habilitándolo o deshabilitándolo.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se obtiene el material de sonda correspondiente utilizando el ID proporcionado en la solicitud.
- Si el material está habilitado, se deshabilita (``status=False``) y se muestra un mensaje de éxito.
- Si el material está deshabilitado, se habilita (``status=True``) y se muestra un mensaje de éxito.
- Se redirige a la vista ``manage_materiales_sonda`` después de realizar el cambio.

Retorno
-------
- Se redirige a la vista ``manage_materiales_sonda`` después de realizar el cambio.
- Si no es una solicitud ``POST``, se muestra un mensaje de error y se redirige a ``manage_perforista``.

---

edit_materiales_sonda
======================

Esta vista permite editar un material de sonda existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se guarda el ID del material en la sesión para permitir la edición de un material específico.
- Se obtiene el material correspondiente desde la base de datos utilizando el ID almacenado en la sesión.
- Se renderiza un formulario prellenado con los datos del material.

Retorno
-------
- Se renderiza la plantilla ``edit_materiales_sonda.html`` con el formulario para editar el material de sonda.

---

save_edit_materiales_sonda
===========================

Esta vista guarda los cambios realizados en un material de sonda.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se actualiza el material de sonda con los nuevos valores proporcionados en el formulario.
- Se devuelve una respuesta JSON indicando el éxito de la operación.

Retorno
-------
- Si el material se actualiza correctamente, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``edit_materiales_sonda``.

---

manage_materiales_caseta
=========================

Esta vista muestra todos los materiales de caseta existentes.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se obtiene una lista de todos los materiales de caseta ordenados por el campo ``material``.
- Se pasan los materiales a la plantilla ``manage_materiales_caseta.html``.

Retorno
-------
- Se renderiza la plantilla ``manage_materiales_caseta.html`` con la lista de materiales.

new_materiales_caseta
======================

Esta vista permite mostrar un formulario para crear un nuevo material de caseta.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Se crea un contexto que incluye un formulario vacío para la creación de un nuevo material de caseta.
- Se renderiza el formulario en la plantilla ``new_materiales_caseta.html``.

Retorno
-------
- Se renderiza la plantilla ``new_materiales_caseta.html`` con el formulario para crear un nuevo material.

---

save_new_materiales_caseta
===========================

Esta vista guarda un nuevo material de caseta.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se verifica si el material ya existe en la base de datos.
- Si el material existe, se devuelve ese objeto.
- Si el material no existe, se valida el formulario, se crea un nuevo material de caseta y se guarda en la base de datos.
- Si el formulario no es válido, se devuelve un mensaje de error.
- Se devuelve una respuesta JSON con el resultado de la operación.

Retorno
-------
- Si el material se guarda correctamente, se devuelve ``{'success': True}``.
- Si el formulario no es válido, se devuelve ``{'success': False, 'message': 'El formulario no es válido.'}``.
- Si no es una solicitud ``POST``, se muestra un mensaje de error y se redirige a la vista ``manage_materiales_caseta``.

---

status_materiales_caseta
=========================

Esta vista cambia el estado de un material de caseta, habilitándolo o deshabilitándolo.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se obtiene el material de caseta correspondiente utilizando el ID proporcionado en la solicitud.
- Si el material está habilitado, se deshabilita (``status=False``) y se muestra un mensaje de éxito.
- Si el material está deshabilitado, se habilita (``status=True``) y se muestra un mensaje de éxito.
- Se redirige a la vista ``manage_materiales_caseta`` después de realizar el cambio.

Retorno
-------
- Se redirige a la vista ``manage_materiales_caseta`` después de realizar el cambio.
- Si no es una solicitud ``POST``, se muestra un mensaje de error y se redirige a ``manage_materiales_caseta``.

---

edit_materiales_caseta
=======================

Esta vista permite editar un material de caseta existente.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se guarda el ID del material en la sesión para permitir la edición de un material específico.
- Se obtiene el material correspondiente desde la base de datos utilizando el ID almacenado en la sesión.
- Se renderiza un formulario prellenado con los datos del material.

Retorno
-------
- Se renderiza la plantilla ``edit_materiales_caseta.html`` con el formulario para editar el material de caseta.

---

save_edit_materiales_caseta
============================

Esta vista guarda los cambios realizados en un material de caseta.

Decoradores
-----------
- ``@login_required``: Restringe el acceso a usuarios autenticados.
- ``@sondaje_admin_or_base_datos_or_supervisor_required``: Restringe el acceso a usuarios con permisos administrativos, de base de datos o supervisores en el módulo de sondajes.

Funcionamiento
--------------
- Si la solicitud es ``POST``, se actualiza el material de caseta con los nuevos valores proporcionados en el formulario.
- Se devuelve una respuesta JSON indicando el éxito de la operación.

Retorno
-------
- Si el material se actualiza correctamente, se devuelve ``{'success': True}``.
- Si no es una solicitud ``POST``, se redirige a la vista ``edit_materiales_caseta``.

Utilidades (utils.py)
*********************

Funciones auxiliares reutilizables dentro del sistema.

procesar_fotografia
========================

Reemplaza la fotografía actual de un campo en un objeto de documentación de usuario con una fotografía base o con una nueva imagen proporcionada en la solicitud.

Parámetros
----------

- ``documentacionUsuario``: El objeto que contiene la documentación del usuario.
- ``toggle``: Un valor que indica si se debe utilizar la fotografía base ("si") o una imagen proporcionada por el usuario.
- ``fotografia_tipo``: El tipo de campo de fotografía que se está procesando (por ejemplo, "fotografiaLicenciaInterna").
- ``archivo_base``: La ruta de la fotografía base que reemplazará la actual si ``toggle`` es "si".
- ``request``: La solicitud HTTP que contiene los archivos subidos por el usuario.

Proceso
-------

Si ``toggle`` es igual a "si", la función asigna la fotografía base al campo correspondiente. Si no es "si", intenta asignar el archivo cargado por el usuario desde la solicitud. Si no se encuentra un archivo, mantiene la imagen actual.

---

procesar_fotografia_dos
========================

Reemplaza la fotografía actual de un campo con una fotografía base si no se ha proporcionado una nueva imagen. Si se proporciona una nueva imagen, la utiliza en lugar de la fotografía base.

Parámetros
----------

- ``toggle``: Un valor que indica si se debe utilizar la fotografía base ("si") o una imagen proporcionada por el usuario.
- ``fotografia_tipo``: El tipo de campo de fotografía que se está procesando.
- ``archivo_base``: La ruta de la fotografía base que reemplazará la actual si ``toggle`` es "si".
- ``request``: La solicitud HTTP que contiene los archivos subidos por el usuario.

Resultado
---------

Devuelve la fotografía base o el archivo proporcionado por el usuario, dependiendo del valor de ``toggle`` y de si se ha cargado un archivo.

---

validar_campo_vacio
========================

Verifica si un campo de texto en la solicitud está vacío y devuelve ``None`` si lo está, o el valor del campo si no lo está.

Parámetros
----------

- ``campo_tipo``: El nombre del campo de texto que se va a validar.
- ``request``: La solicitud HTTP que contiene los valores de los campos enviados por el usuario.

Resultado
---------

Devuelve ``None`` si el campo está vacío, de lo contrario, devuelve el valor del campo.

---

validar_archivo_vacio
========================

Verifica si un campo de tipo archivo en la solicitud está vacío y devuelve ``None`` si lo está, o el archivo proporcionado si no lo está.

Parámetros
----------

- ``campo_tipo``: El nombre del campo de archivo que se va a validar.
- ``request``: La solicitud HTTP que contiene los archivos subidos por el usuario.

Resultado
---------

Devuelve ``None`` si el campo de archivo está vacío, de lo contrario, devuelve el archivo cargado.

---

get_filtered_queryset
========================

Genera un listado de objetos filtrados por estado. Si el campo ``objeto_actual`` no está vacío, incluye el objeto actual en el listado.

Parámetros
----------

- ``model``: El modelo de los objetos a filtrar.
- ``objeto_actual``: Un objeto que se incluirá en el listado, incluso si su estado es ``False``.
- ``orden``: Una lista de campos por los cuales se ordenará el resultado.

Resultado
---------

Devuelve un queryset de objetos filtrados y ordenados, mostrando solo los objetos habilitados a menos que se incluya un objeto actual con estado ``False``.

---

formatear_fecha
========================

Formatea una fecha a un formato de año-mes-día (``YYYY-MM-DD``). Si la fecha es nula, devuelve una cadena vacía.

Parámetros
----------

- ``fecha``: La fecha que se desea formatear.

Resultado
---------

Devuelve la fecha en formato ``YYYY-MM-DD`` si la fecha no es nula, de lo contrario, devuelve una cadena vacía.

---

extension_archivo
========================

Reconoce el tipo de extensión de un archivo y devuelve el tipo de archivo (imagen, PDF o otro).

Parámetros
----------

- ``archivo``: Un objeto de archivo cuya extensión se desea identificar.

Resultado
---------

Devuelve una cadena que indica el tipo de archivo: "imagen" si la extensión es una de las imágenes soportadas, "pdf" si es un archivo PDF, o "otro" si no corresponde a ninguno de estos tipos.

---

extension_archivo_pdfs
========================

Obtiene la extensión del archivo y la devuelve en formato minúscula.

Parámetros
----------

- ``file_path``: La ruta del archivo cuya extensión se va a obtener.

Resultado
---------

Devuelve la extensión del archivo (en minúsculas), o una cadena vacía si el archivo no tiene extensión reconocida.

---

convert_pdf_to_images
========================

Convierte un archivo PDF a una serie de imágenes JPEG, utilizando el software Poppler. Los archivos resultantes se guardan en un directorio temporal.

Parámetros
----------

- ``pdf_path``: La ruta del archivo PDF que se desea convertir.
- ``poppler_path``: La ruta de instalación de Poppler (dependiendo del sistema operativo).
- ``quality``: La calidad de la imagen JPEG generada.

Resultado
---------

Devuelve una lista de rutas de archivo de las imágenes generadas.

---

check_and_convert_pdf
========================

Verifica si un archivo es un PDF y lo convierte en imágenes si es el caso. Si no es un PDF, simplemente devuelve la ruta del archivo.

Parámetros
----------

- ``file_path``: La ruta del archivo que se desea convertir.

Resultado
---------

Devuelve una lista de rutas de imágenes si el archivo es un PDF, o una lista que contiene la ruta del archivo original si no es un PDF.

---

ordenar_por_mes_inicial
========================

Ordena los objetos ``FechasImportantes`` por el mes de vencimiento, considerando un mes inicial para el orden.

Parámetros
----------

- ``mes_inicial``: El mes de referencia desde el cual se ordenarán las fechas.

Resultado
---------

Devuelve un queryset de objetos ``FechasImportantes`` ordenados por el mes de vencimiento, ajustado en relación con el mes inicial proporcionado.



Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.

select
======

Ruta para seleccionar una opción.

URL
---

- ``/select``

Vista asociada
--------------

- ``select``

selectOption
=============

Ruta para seleccionar una opción de una lista.

URL
---

- ``/selectOption``

Vista asociada
--------------

- ``selectOption``

dashboard
==========

Ruta para mostrar el panel de control.

URL
---

- ``/dashboard``

Vista asociada
--------------

- ``dashboard``

dashboardSondaje
=================

Ruta para mostrar el panel de control de sondajes.

URL
---

- ``/dashboardSondaje``

Vista asociada
--------------

- ``dashboardSondaje``

dashboardPrevencion
====================

Ruta para mostrar el panel de control de prevención.

URL
---

- ``/dashboardPrevencion``

Vista asociada
--------------

- ``dashboardPrevencion``


manage_genders
===============

Ruta para gestionar géneros.

URL
---

- ``/manage_genders``

Vista asociada
--------------

- ``manage_genders``

new_gender
===========

Ruta para crear un nuevo género.

URL
---

- ``/new_gender``

Vista asociada
--------------

- ``new_gender``

save_new_gender
================

Ruta para guardar un nuevo género.

URL
---

- ``/save_new_gender``

Vista asociada
--------------

- ``save_new_gender``

status_gender
==============

Ruta para cambiar el estado de un género.

URL
---

- ``/status_gender``

Vista asociada
--------------

- ``status_gender``

manage_cities
==============

Ruta para gestionar las ciudades.

URL
---

- ``/manage_cities``

Vista asociada
--------------

- ``manage_cities``

new_city
=========

Ruta para crear una nueva ciudad.

URL
---

- ``/new_city``

Vista asociada
--------------

- ``new_city``

save_new_city
=============

Ruta para guardar una nueva ciudad.

URL
---

- ``/save_new_cities``

Vista asociada
--------------

- ``save_new_city``
  
status_city
===========

Ruta para cambiar el estado de una ciudad.

URL
---

- ``/status_city``

Vista asociada
--------------

- ``status_city``

manage_nationalities
====================

Ruta para gestionar las nacionalidades.

URL
---

- ``/manage_nationalities``

Vista asociada
--------------

- ``manage_nationalities``

new_nationality
===============

Ruta para crear una nueva nacionalidad.

URL
---

- ``/new_nationality``

Vista asociada
--------------

- ``new_nationality``

save_new_nationality
====================

Ruta para guardar una nueva nacionalidad.

URL
---

- ``/save_new_nationality``

Vista asociada
--------------

- ``save_new_nationality``

status_nationality
===================

Ruta para cambiar el estado de una nacionalidad.

URL
---

- ``/status_nationality``

Vista asociada
--------------

- ``status_nationality``

manage_years
=============

Ruta para gestionar los años.

URL
---

- ``/manage_years``

Vista asociada
--------------

- ``manage_years``

new_year
=========

Ruta para crear un nuevo año.

URL
---

- ``/new_year``

Vista asociada
--------------

- ``new_year``

save_new_year
===============

Ruta para guardar un nuevo año.

URL
---

- ``/save_new_yearr``

Vista asociada
--------------

- ``save_new_year``

status_year
============

Ruta para cambiar el estado de un año.

URL
---

- ``/status_year``

Vista asociada
--------------

- ``status_year``

manage_brands
==============

Ruta para gestionar las marcas.

URL
---

- ``/manage_brands``

Vista asociada
--------------

- ``manage_brands``

new_brand
==========

Ruta para crear una nueva marca.

URL
---

- ``/new_brand``

Vista asociada
--------------

- ``new_brand``

save_new_brand
===============

Ruta para guardar una nueva marca.

URL
---

- ``/save_new_brand``

Vista asociada
--------------

- ``save_new_brand``

status_brand
=============

Ruta para cambiar el estado de una marca.

URL
---

- ``/status_brand``

Vista asociada
--------------

- ``status_brand``

manage_models
==============

Ruta para gestionar los modelos.

URL
---

- ``/manage_models``

Vista asociada
--------------

- ``manage_models``

new_model
==========

Ruta para crear un nuevo modelo.

URL
---

- ``/new_model``

Vista asociada
--------------

- ``new_model``

save_new_model
===============

Ruta para guardar un nuevo modelo.

URL
---

- ``/save_new_model``

Vista asociada
--------------

- ``save_new_model``

status_model
=============

Ruta para cambiar el estado de un modelo.

URL
---

- ``/status_model``

Vista asociada
--------------

- ``status_model``

manage_colours
===============

Ruta para gestionar los colores.

URL
---

- ``/manage_colours``

Vista asociada
--------------

- ``manage_colours``

new_colour
===========

Ruta para crear un nuevo color.

URL
---

- ``/new_colour``

Vista asociada
--------------

- ``new_colour``

save_new_colour
================

Ruta para guardar un nuevo color.

URL
---

- ``/save_new_colour``

Vista asociada
--------------

- ``save_new_colour``

status_colour
==============

Ruta para cambiar el estado de un color.

URL
---

- ``/status_colour``

Vista asociada
--------------

- ``status_colour``

manage_types
=============

Ruta para gestionar los tipos.

URL
---

- ``/manage_types``

Vista asociada
--------------

- ``manage_types``

new_type
=========

Ruta para crear un nuevo tipo.

URL
---

- ``/new_type``

Vista asociada
--------------

- ``new_type``

save_new_type
===============

Ruta para guardar un nuevo tipo.

URL
---

- ``/save_new_type``

Vista asociada
--------------

- ``save_new_type``

status_type
============

Ruta para cambiar el estado de un tipo.

URL
---

- ``/status_type``

Vista asociada
--------------

- ``status_type``

edit_type
==========

Ruta para editar un tipo.

URL
---

- ``/edit_type``

Vista asociada
--------------

- ``edit_type``

save_edit_type
===============

Ruta para guardar la edición de un tipo.

URL
---

- ``/save_edit_type``

Vista asociada
--------------

- ``save_edit_type``


Señales (signals.py)
--------------------

Ejecuta acciones automáticamente cuando ocurren eventos en los modelos.
