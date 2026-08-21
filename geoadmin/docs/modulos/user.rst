####
User
####

Descripción General
*******************

El módulo user gestiona los perfiles de los usuarios en la aplicación, incluyendo la creación y modificación de información personal, roles de usuario, y funcionalidades relacionadas con la autenticación y autorización.

.. code-block:: bash   

    user/
    │── admin.py         = Configuración para la interfaz de administración de Django
    │── apps.py          = Configuración de la aplicación dentro del proyecto Django
    │── forms.py         = Formularios para la entrada de datos relacionados con los usuarios
    │── __init__.py      = Marca el directorio como un paquete de Python
    │── migrations/      = Archivos de migración para la base de datos
    │── models.py        = Definición de modelos de datos relacionados con los usuarios
    │── urls.py          = Configuración de rutas del módulo
    │── views.py         = Lógica para las vistas relacionadas con los usuarios

Modelos de Datos (models.py)
*****************************

Este archivo define los modelos de datos que gestionan la información del usuario, como el perfil y roles asociados.

User
====

Este modelo extiende la clase AbstractUser de Django, y se utiliza para gestionar los usuarios del sistema, con un enfoque en los roles y permisos específicos para cada tipo de usuario.

- Campos:
    - ``role``: (CharField) Define el rol del usuario en el sistema, con opciones que corresponden a distintos niveles de acceso o permisos. Los valores posibles son:
        - ``ADMINISTRADOR``: Administrador, tiene acceso a todo.
        - ``JEFE_MANTENCION``: Jefe de Mantención.
        - ``SUPERVISOR``: Supervisor.
        - ``CONTROLADOR``: Controlador.
        - ``BASE_DATOS``: Usuario con acceso a la base de datos.
        - ``CONDUCTOR``: Conductor.
        - ``TRABAJADOR``: Trabajador.
        - ``SIN_ASIGNAR``: Sin asignar, no tiene acceso a nada más allá de su perfil.
        - ``phone``: (IntegerField) Número de teléfono del usuario. Puede ser nulo.
- Metadatos:
    - ``Role Enum (Role)``: Define los diferentes roles disponibles en el sistema, utilizando la opción TextChoices de Django para crear una lista de opciones. Estos roles permiten asignar permisos específicos y restringir el acceso a las distintas funcionalidades del sistema.

UsuarioManager
==============

Este es un administrador personalizado para el modelo Usuario. Un administrador personalizado permite modificar la lógica de consulta para obtener resultados específicos, adaptados a las necesidades de la aplicación.

- Métodos:
    - ``get_queryset(self, *args, **kwargs)``: Este método sobrescribe el método get_queryset del BaseUserManager para filtrar los resultados de la consulta y devolver solo aquellos usuarios cuyo role sea SIN_ASIGNAR. Utiliza el super() para obtener el conjunto de resultados de la consulta base y luego aplica un filtro específico que selecciona solo aquellos registros donde el campo role tiene el valor User.Role.SIN_ASIGNAR. Esto se utiliza para obtener los usuarios sin un rol asignado.

Usuario
=======

Este modelo extiende el modelo User y está diseñado para gestionar usuarios con roles personalizados, añadiendo una capa adicional de lógica o funcionalidad a los usuarios de la aplicación.

- Campos:
    - ``base_role``: (Atributo de clase) Asigna un rol base al usuario, en este caso, el valor es User.Role.SIN_ASIGNAR. Este valor parece ser un rol por defecto o sin asignar, dependiendo de la estructura del sistema de roles.
    - ``Usuario``: (Manager) Asocia un UsuarioManager a este modelo, lo que sugiere que se pueden realizar consultas personalizadas o funciones adicionales sobre los usuarios a través de este manager.
- Metadatos:
    - ``proxy``: True indica que este modelo no crea una nueva tabla en la base de datos, sino que es un modelo proxy para extender el modelo User existente sin modificar la estructura de la tabla original. Esto significa que puedes agregar métodos adicionales o comportamientos sin alterar la base de datos directamente.

UsuarioProfile
==============

Este modelo extiende el modelo de usuario (User) para incluir información adicional sobre un usuario, como detalles sobre su faena, ciudad, nacionalidad, género, fecha de nacimiento, vencimiento de la cédula de identidad, y más.

- Campos:
    - ``user``: (OneToOneField) Relacionado con el modelo User, establece una relación uno a uno con el usuario de Django, es decir, cada perfil de usuario está vinculado a un usuario único.
    - ``faena``: (ForeignKey) Relacionado con el modelo Faena, indica la faena en la que trabaja el usuario. Puede ser nulo o en blanco.
    - ``ciudad``: (ForeignKey) Relacionado con el modelo Ciudad, indica la ciudad de residencia del usuario. Puede ser nulo o en blanco.
    - ``nacionalidad``: (ForeignKey) Relacionado con el modelo Nacionalidad, representa la nacionalidad del usuario. Puede ser nulo o en blanco.
    - ``genero``: (ForeignKey) Relacionado con el modelo Genero, representa el género del usuario. Puede ser nulo o en blanco.
    - ``fechaNacimiento``: (DateTimeField) La fecha de nacimiento del usuario. Puede ser nula.
    - ``fechaCedulaVencimiento``: (DateTimeField) La fecha de vencimiento de la cédula de identidad del usuario. Puede ser nula.
    - ``seccionVehicular``: (CharField) Define la sección en la que el usuario trabaja en el área vehicular, usando opciones predefinidas. Puede ser nulo o en blanco.
    - ``seccionSondaje``: (CharField) Define la sección en la que el usuario trabaja en el área de sondaje, usando opciones predefinidas. Puede ser nulo o en blanco.
    - ``seccionPrevencion``: (CharField) Define la sección en la que el usuario trabaja en el área de prevención de riesgos, usando opciones predefinidas. Puede ser nulo o en blanco.
- Método:
    - ``__str__(self)``: Devuelve una representación del objeto que incluye la nacionalidad y la ciudad del usuario, para mostrar una visión rápida de la información de ubicación del usuario.
- Metadatos:
    - ``verbose_name``: "Usuario Información Adicional".
    - ``verbose_name_plural``: "Usuarios Información Adicional".

LicenciasUsuario
================

Este modelo se utiliza para gestionar las licencias de conducir de los usuarios en el sistema. Se almacena información relacionada con las fechas de vencimiento de diversas licencias de conducir y tipos de licencias que un usuario puede poseer.

- Campos:
    - ``user``: (OneToOneField) Relacionado con el modelo User, establece una relación uno a uno con el usuario de Django. Cada registro de licencia está vinculado a un único usuario.
    - ``fechaLicenciaVencimiento``: (DateTimeField) La fecha de vencimiento de la licencia de conducir estándar del usuario. Puede ser nula.
    - ``fechaLicenciaInternaVencimiento``: (DateTimeField) La fecha de vencimiento de la licencia interna del usuario. Puede ser nula.
    - ``licenciaClaseB``: (CharField) Representa si el usuario tiene la licencia de Clase B. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseC``: (CharField) Representa si el usuario tiene la licencia de Clase C. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseD``: (CharField) Representa si el usuario tiene la licencia de Clase D. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseE``: (CharField) Representa si el usuario tiene la licencia de Clase E. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseF``: (CharField) Representa si el usuario tiene la licencia de Clase F. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseA1``: (CharField) Representa si el usuario tiene la licencia de Clase A1. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseA2``: (CharField) Representa si el usuario tiene la licencia de Clase A2. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseA3``: (CharField) Representa si el usuario tiene la licencia de Clase A3. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseA4``: (CharField) Representa si el usuario tiene la licencia de Clase A4. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseA5``: (CharField) Representa si el usuario tiene la licencia de Clase A5. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseA1Antigua``: (CharField) Representa si el usuario tiene la licencia de Clase A1 Antigua. Las opciones son predefinidas mediante el campo opcion.
    - ``licenciaClaseA2Antigua``: (CharField) Representa si el usuario tiene la licencia de Clase A2 Antigua. Las opciones son predefinidas mediante el campo opcion.
- Método:
    - ``__str__(self)``: Devuelve una representación del objeto que incluye el id_usuario.
- Metadatos:
    - ``verbose_name``: "Licencia de Conducir".
    - ``verbose_name_plural``: "Licencias de Conducir".
    - ``db_table``: 'user_licencia_conducir'.

DocumentacionUsuario
====================

Este modelo gestiona la documentación relacionada con el usuario, en particular las imágenes que representan las credenciales del usuario, como la fotografía de identificación, cédula de identidad y licencias.

- Campos:
    - ``user``: (OneToOneField) Relacionado con el modelo User (usuario de Django), cada registro de documentación está vinculado a un único usuario.
    - ``fotografiaUsuario``: (ImageField) Permite cargar una imagen de la fotografía del usuario. Si no se proporciona, se usa una imagen predeterminada ('documentacion_usuario/no-avatar.png').
    - ``fotografiaCedula``: (ImageField) Permite cargar una imagen de la cédula de identidad del usuario. Si no se proporciona, se usa una imagen predeterminada ('documentacion_usuario/no-imagen.png').
    - ``fotografiaLicencia``: (ImageField) Permite cargar una imagen de la licencia de conducir del usuario. Si no se proporciona, se usa una imagen predeterminada ('documentacion_usuario/no-imagen.png').
    - ``fotografiaLicenciaInterna``: (ImageField) Permite cargar una imagen de la licencia interna del usuario. Si no se proporciona, se usa una imagen predeterminada ('documentacion_usuario/no-imagen.png').
- Método:
    - ``generaNombre(instance, filename)``: Método utilizado para generar un nombre único para cada archivo cargado. La ruta incluye el username del usuario y la fecha/hora actual para asegurar que el nombre del archivo sea único.
    - ``__str__(self)``: Devuelve una representación del objeto que incluye el id_usuario.
- Metadatos:
    - ``verbose_name``: "Documentación Usuario".
    - ``verbose_name_plural``: "Documentación Usuarios".
    - ``db_table``: 'user_documentacion'.

Signal: create_usuario_profile
==============================

Esta es una señal de Django que se ejecuta automáticamente después de que un objeto Usuario se guarda en la base de datos, específicamente después de la creación de un nuevo usuario.

- Funcionalidad:
    - Evento: 
        - ``post_save``: Esta señal se activa después de que un modelo se guarda en la base de datos.
    - ``Emisor``: 
        - ``Usuario``: La señal se dispara cada vez que un objeto Usuario es creado o actualizado.
    - Condición:
        - Si el usuario recién creado tiene el rol "SIN ASIGNAR" (comprobado en minúsculas usando .upper() para asegurarse de que sea insensible a mayúsculas/minúsculas), se crea un nuevo perfil para ese usuario (UsuarioProfile).
        - El perfil de usuario (UsuarioProfile) se asigna con una faena que corresponde al valor "SIN ASIGNAR" dentro de la tabla Faena.
    - Detalles del Código:
        - ``create_usuario_profile(sender, instance, created, **kwargs)``: Esta es la función que se ejecuta al activarse la señal. Recibe varios parámetros, entre ellos:
            - ``sender``: El modelo que envió la señal (en este caso, Usuario).
            - ``instance``: La instancia del modelo que se está guardando (el usuario).
            - ``created``: Un valor booleano que indica si la instancia fue creada (True) o actualizada (False).
            - ``**kwargs``: Argumentos adicionales que pueden ser pasados a la función.
    - Lógica interna:
        - if created and instance.role.upper() == "SIN ASIGNAR":: Verifica si el usuario ha sido creado (created == True) y si su rol es "SIN ASIGNAR".
        - faena = Faena.objects.get(faena="SIN ASIGNAR"): Obtiene la faena correspondiente con el nombre "SIN ASIGNAR" de la tabla Faena.
        - ``UsuarioProfile.objects.create(user=instance, faena=faena)``: Crea un nuevo perfil de usuario (UsuarioProfile) y lo vincula con el usuario recién creado y la faena que se ha obtenido.

Signal: create_licencias_usuario
================================

Esta señal que se activa después de que un objeto Usuario se guarda en la base de datos, específicamente después de la creación de un nuevo usuario.

- Funcionalidad:
    - Evento: 
        - ``post_save``: Esta señal se ejecuta después de que un objeto modelo se guarda.
    - Emisor: 
        - ``Usuario``: La señal se dispara cuando se crea o se guarda un objeto del modelo Usuario.
    - Acción: Cuando un nuevo objeto Usuario es creado, automáticamente se crea una entrada asociada en el modelo LicenciasUsuario para ese usuario.
    - Detalles del Código:
        - ``create_licencias_usuario(sender, instance, created, **kwargs)``: Esta función se ejecuta cuando la señal es activada. Los parámetros son:
        - ``sender``: El modelo que envió la señal, en este caso, Usuario.
        - ``instance``: La instancia del modelo que se está guardando (el usuario).
        - ``created``: Un valor booleano que indica si la instancia fue creada (True) o actualizada (False).
        - ``kwargs**``: Argumentos adicionales.
    - Lógica interna:
        - ``LicenciasUsuario.objects.create(user=instance)``: Después de que un usuario es creado, esta línea crea automáticamente un nuevo objeto LicenciasUsuario que se asocia con el usuario recién creado. No se especifican otros campos, por lo que los campos de LicenciasUsuario se establecerán con sus valores predeterminados o nulos.

Signal: create_documentacion_usuario
====================================

Esta señal se ejecuta cuando se guarda una instancia del modelo Usuario, y su propósito es crear un objeto asociado en el modelo DocumentacionUsuario cada vez que se crea un nuevo usuario.

- Funcionalidad:
    - Evento: 
        - ``post_save``: La señal se dispara después de que se guarda un objeto de tipo Usuario.
    - Emisor: 
        - ``Usuario``: La señal se activa cuando un objeto Usuario es guardado.
    - Acción: Cuando se crea un nuevo Usuario, automáticamente se crea una entrada asociada en el modelo DocumentacionUsuario para ese usuario.
    - Detalles del Código:
        - ``create_documentacion_usuario(sender, instance, created, **kwargs)``: Esta función se ejecuta cuando la señal es activada. Los parámetros son:

        - ``sender``: El modelo que envió la señal, en este caso Usuario.
        - ``instance``: La instancia del objeto que se está guardando (el usuario).
        - ``created``: Un valor booleano que indica si la instancia fue creada (True) o actualizada (False).
        - ``**kwargs``: Argumentos adicionales.
    - Lógica interna:
        ``DocumentacionUsuario.objects.create(user=instance)``: Una vez que se crea un objeto Usuario, se crea automáticamente una entrada asociada en el modelo DocumentacionUsuario. El campo user en DocumentacionUsuario se llena con la instancia del Usuario recién creado, lo que vincula ambas tablas.

Formularios (forms.py)
**********************

Los formularios permiten que los usuarios creen o editen su información personal.

get_filtered_queryset
======================

Esta función filtra los objetos de un modelo específico según el estado y el objeto actual proporcionado.

Parámetros
-----------

1. ``model``  
    - Tipo: Clase de modelo  
    - Descripción: El modelo sobre el que se realizará el filtrado.  
    - Ejemplo: ``Vehiculo``, ``Maquinaria``  

2. ``objeto_actual``  
    - Tipo: QuerySet  
    - Descripción: El conjunto de objetos actuales a considerar.  
    - Ejemplo: ``Vehiculo.objects.filter(id=1)``  

3. ``orden``  
    - Tipo: Lista de cadenas  
    - Descripción: El campo o los campos por los cuales se ordenarán los resultados.  
    - Ejemplo: ``['nombre', 'fecha']``  

Retorno
-------

- Tipo: QuerySet  
- Descripción: Un conjunto de objetos filtrados y ordenados según el estado y el objeto actual. Si ``objeto_actual`` tiene elementos, se agrega el objeto actual a la lista filtrada si su ``status`` es ``True``; de lo contrario, solo se devuelven los objetos con estado ``True``.

Comportamiento
--------------

1. Filtra los objetos del modelo con el estado ``True``.
2. Si se pasa un ``objeto_actual`` y su ``status`` es ``True``, se incluye ese objeto en el conjunto filtrado.
3. Ordena los resultados según los campos especificados en ``orden``.

FormRegistro
============

Este formulario permite el registro de un nuevo usuario en el sistema, basándose en el modelo ``Usuario``.

Campos del Formulario
----------------------

1. ``username``  
    - Tipo: CharField  
    - Etiqueta: Rut (Usuario)  
    - Requerido: Sí  
    - Widget: TextInput  
    - Descripción: Identificador único del usuario.  
    - Restricciones: Formato sin puntos ni guión, máximo de 12 caracteres.

2. ``password1``  
    - Tipo: CharField  
    - Etiqueta: Contraseña  
    - Requerido: Sí  
    - Widget: PasswordInput  
    - Descripción: Contraseña del usuario.  
    - Restricciones: Mínimo de 8 caracteres.

3. ``password2``  
    - Tipo: CharField  
    - Etiqueta: Confirmar Contraseña  
    - Requerido: Sí  
    - Widget: PasswordInput  
    - Descripción: Confirmación de la contraseña.

4. ``first_name``  
    - Tipo: CharField  
    - Etiqueta: Nombres  
    - Requerido: Sí  
    - Widget: TextInput  
    - Descripción: Primer nombre del usuario.

5. ``last_name``  
    - Tipo: CharField  
    - Etiqueta: Apellidos  
    - Requerido: Sí  
    - Widget: TextInput  
    - Descripción: Apellidos del usuario.

6. ``phone``  
    - Tipo: CharField  
    - Etiqueta: Número Celular  
    - Requerido: Sí  
    - Widget: TextInput  
    - Descripción: Número celular del usuario.  
    - Restricciones: Solo números, máximo de 9 caracteres.

7. ``email``  
    - Tipo: EmailField  
    - Etiqueta: Correo Electrónico  
    - Requerido: Sí  
    - Widget: EmailInput  
    - Descripción: Correo electrónico del usuario.

8. ``role``  
    - Tipo: ForeignKey  
    - Etiqueta: Rol  
    - Requerido: Sí  
    - Widget: Select  
    - Descripción: Rol asignado al usuario.  
    - Valor inicial: ``Usuario.base_role``

Consideraciones Adicionales
---------------------------

- El campo ``role`` se oculta si el parámetro ``ocultar_role`` es ``True``.
- Los campos ``password1`` y ``password2`` se ocultan si el parámetro ``ocultar_password`` es ``True``.
- Los campos ``username``, ``first_name``, ``last_name``, ``phone``, ``email``, y ``role`` pueden ser deshabilitados según los parámetros de inicialización.

FormRegistroExtra
=================

Este formulario permite el registro adicional de información extra del usuario, basándose en el modelo ``UsuarioProfile``.

Campos del Formulario
----------------------

1. ``ciudad``  
    - Tipo: ForeignKey  
    - Requerido: No  
    - Widget: Select  
    - Descripción: Ciudad del usuario.  
    - Restricciones: Se filtra con un conjunto de datos basado en la ciudad actual proporcionada.

2. ``nacionalidad``  
    - Tipo: ForeignKey  
    - Requerido: No  
    - Widget: Select  
    - Descripción: Nacionalidad del usuario.  
    - Restricciones: Se filtra con un conjunto de datos basado en la nacionalidad actual proporcionada.

3. ``genero``  
    - Tipo: ForeignKey  
    - Requerido: No  
    - Widget: Select  
    - Descripción: Género del usuario.  
    - Restricciones: Se filtra con un conjunto de datos basado en el género actual proporcionado.

4. ``fechaNacimiento``  
    - Tipo: DateField  
    - Requerido: No  
    - Widget: DateTimeInput  
    - Descripción: Fecha de nacimiento del usuario.  
    - Restricciones: Mínimo 1920-01-01.

5. ``fechaCedulaVencimiento``  
    - Tipo: DateField  
    - Requerido: No  
    - Widget: DateTimeInput  
    - Descripción: Fecha de vencimiento de la cédula de identidad del usuario.  
    - Restricciones: Mínimo 1920-01-01.

6. ``faena``  
    - Tipo: ForeignKey  
    - Requerido: Sí  
    - Widget: Select  
    - Descripción: Faena asignada al usuario.  
    - Restricciones: Se filtra con un conjunto de datos basado en la faena actual proporcionada.

Consideraciones Adicionales
---------------------------

- Los campos ``ciudad``, ``nacionalidad``, ``genero``, ``fechaNacimiento`` y ``fechaCedulaVencimiento`` son opcionales y pueden ser deshabilitados según los parámetros proporcionados.
- El campo ``faena`` es obligatorio y se puede deshabilitar también.
- Se filtra la información de los campos ``ciudad``, ``nacionalidad``, ``genero`` y ``faena`` según los valores actuales proporcionados en los parámetros.

FormRegistroSeccion
===================

Este formulario permite la asignación de secciones dentro del perfil del usuario, basándose en el modelo ``UsuarioProfile``.

Campos del Formulario
----------------------

1. ``seccionVehicular``  
    - Tipo: ForeignKey  
    - Requerido: Sí  
    - Widget: Select  
    - Descripción: Sección vehicular asignada al usuario.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``seccionVehicular_disabled``.

2. ``seccionSondaje``  
    - Tipo: ForeignKey  
    - Requerido: Sí  
    - Widget: Select  
    - Descripción: Sección de sondaje asignada al usuario.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``seccionSondaje_disabled``.

3. ``seccionPrevencion``  
    - Tipo: ForeignKey  
    - Requerido: Sí  
    - Widget: Select  
    - Descripción: Sección de prevención asignada al usuario.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``seccionPrevencion_disabled``.

Consideraciones Adicionales
---------------------------

- Todos los campos de secciones son obligatorios.
- Los campos de las secciones pueden ser deshabilitados según los parámetros ``seccionVehicular_disabled``, ``seccionSondaje_disabled`` y ``seccionPrevencion_disabled``.

FormRegistroLicenciasUsuarioFecha
=================================

Este formulario permite registrar y gestionar las fechas de vencimiento de las licencias del usuario, basándose en el modelo ``LicenciasUsuario``.

Campos del Formulario
----------------------

1. ``fechaLicenciaVencimiento``  
    - Tipo: DateTimeField  
    - Requerido: No  
    - Widget: DateTimeInput  
    - Descripción: Fecha de vencimiento de la licencia.  
    - Restricciones: Puede ser deshabilitado según el parámetro ``fechalicenciavencimiento_disabled``.

2. ``fechaLicenciaInternaVencimiento``  
    - Tipo: DateTimeField  
    - Requerido: No  
    - Widget: DateTimeInput  
    - Descripción: Fecha de vencimiento de la licencia interna.  
    - Restricciones: Puede ser deshabilitado según el parámetro ``fechalicenciainternavencimiento_disabled``.

Consideraciones Adicionales
---------------------------

- Ambos campos no son obligatorios.
- Los campos de fecha pueden ser deshabilitados utilizando los parámetros ``fechalicenciavencimiento_disabled`` y ``fechalicenciainternavencimiento_disabled``.


FormRegistroLicenciasUsuarioNoProfesionales
===========================================

Este formulario permite registrar y gestionar las licencias de usuario no profesionales, basándose en el modelo ``LicenciasUsuario``.

Campos del Formulario
----------------------

1. ``licenciaClaseB``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase B.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclaseb_disabled``.

2. ``licenciaClaseC``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase C.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasec_disabled``.

3. ``licenciaClaseD``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase D.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclased_disabled``.

4. ``licenciaClaseE``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase E.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasee_disabled``.

5. ``licenciaClaseF``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase F.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasef_disabled``.

Consideraciones Adicionales
---------------------------

- Todos los campos de licencia son opcionales.
- Los campos de licencia pueden ser deshabilitados utilizando los parámetros ``licenciaclaseb_disabled``, ``licenciaclasec_disabled``, ``licenciaclased_disabled``, ``licenciaclasee_disabled`` y ``licenciaclasef_disabled``.

FormRegistroLicenciasUsuarioProfesionales
===========================================

Este formulario permite registrar y gestionar las licencias de usuario profesionales, basándose en el modelo ``LicenciasUsuario``.

Campos del Formulario
----------------------

1. ``licenciaClaseA1``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase A1.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasea1_disabled``.

2. ``licenciaClaseA2``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase A2.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasea2_disabled``.

3. ``licenciaClaseA3``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase A3.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasea3_disabled``.

4. ``licenciaClaseA4``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase A4.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasea4_disabled``.

5. ``licenciaClaseA5``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase A5.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasea5_disabled``.

Consideraciones Adicionales
---------------------------

- Todos los campos de licencia son opcionales.
- Los campos de licencia pueden ser deshabilitados utilizando los parámetros ``licenciaclasea1_disabled``, ``licenciaclasea2_disabled``, ``licenciaclasea3_disabled``, ``licenciaclasea4_disabled`` y ``licenciaclasea5_disabled``.

FormRegistroLicenciasUsuarioProfesionalesAntiguas
===================================================

Este formulario permite registrar y gestionar las licencias de usuario profesionales antiguas, basándose en el modelo ``LicenciasUsuario``.

Campos del Formulario
----------------------

1. ``licenciaClaseA1Antigua``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase A1 Antigua.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasea1antigua_disabled``.

2. ``licenciaClaseA2Antigua``  
    - Tipo: BooleanField  
    - Requerido: No  
    - Descripción: Licencia Clase A2 Antigua.  
    - Restricciones: Puede ser deshabilitada según el parámetro ``licenciaclasea2antigua_disabled``.

Consideraciones Adicionales
---------------------------

- Los campos de licencia son opcionales.
- Los campos de licencia pueden ser deshabilitados utilizando los parámetros ``licenciaclasea1antigua_disabled`` y ``licenciaclasea2antigua_disabled``.

FormDocumentacionUsuario
=========================

Este formulario permite registrar la documentación del usuario, basándose en el modelo ``DocumentacionUsuario``.

Campos del Formulario
----------------------

1. ``fotografiaUsuario``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía del usuario.

2. ``fotografiaCedula``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía de la cédula del usuario.

3. ``fotografiaLicencia``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía de la licencia del usuario.

4. ``fotografiaLicenciaInterna``  
    - Tipo: ImageField  
    - Requerido: Sí  
    - Descripción: Fotografía de la licencia interna del usuario.

Consideraciones Adicionales
---------------------------

- Todos los campos son obligatorios para asegurar que la documentación esté completa.

Vistas (views.py)
*****************

Las vistas contienen la lógica para manejar las interacciones relacionadas con los usuarios, como la visualización y edición de perfiles.

CustomLoginView
=================

Vista personalizada de inicio de sesión que extiende ``LoginView``.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Utilizado para gestionar la solicitud de inicio de sesión.

Funcionamiento
--------------

- La clase ``CustomLoginView`` hereda de ``LoginView`` y sobrescribe el método ``get_context_data`` para personalizar el contexto de la vista.
- La plantilla utilizada para el inicio de sesión es ``registration/login.html``.

Retorno
-------

- Retorna el contexto de la vista con los datos adicionales o modificados definidos en el método ``get_context_data``.
  
---

CustomLogoutView
==================

Vista personalizada de cierre de sesión que extiende ``LogoutView``.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Utilizado para gestionar la solicitud de cierre de sesión.

Funcionamiento
--------------

- La clase ``CustomLogoutView`` hereda de ``LogoutView`` y especifica que, después de cerrar sesión, se debe redirigir al usuario a la página de inicio de sesión personalizada (definida por ``reverse_lazy('logincustom')``).

Retorno
-------

- Redirige al usuario a la URL de inicio de sesión personalizada después de cerrar sesión.

---

register
=========

Función para gestionar el registro de nuevos usuarios.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Utilizado para gestionar la solicitud de registro.

Funcionamiento
--------------

- La función renderiza la página de registro y pasa el formulario de registro ``FormRegistro`` al contexto de la plantilla.
- La plantilla utilizada para la página de registro es ``registration/register.html``.

Retorno
-------

- Retorna la respuesta renderizada con la plantilla de registro, pasando el formulario de registro y el contexto necesario.

new_user
=========

Vista que permite crear un nuevo usuario, solo accesible por usuarios autenticados con permisos específicos.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Utilizado para gestionar la solicitud de creación de usuario.

Funcionamiento
--------------

- La función se asegura de que el usuario esté autenticado y tenga permisos adecuados para crear nuevos usuarios. La validación de permisos se realiza mediante los decoradores ``@login_required`` y ``@sondaje_admin_or_base_datos_or_supervisor_required``.
- Si el usuario tiene acceso, se renderiza el formulario de registro (``FormRegistro``) en la plantilla ``pages/users/new_user.html``.

Retorno
-------

- Retorna la página con el formulario de registro de usuario, pasando el formulario y el contexto necesario para la vista.

---

save_new_user
==============

Vista para guardar un nuevo usuario después de validar el formulario.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Utilizado para obtener los datos del formulario y realizar la creación del usuario.

Funcionamiento
--------------

- Se obtiene la ubicación de origen del formulario, que puede ser ``inside`` (interno) o de otro tipo.
- Se valida el formulario ``FormRegistro`` y se verifica si el RUT ingresado es válido utilizando la función ``rut_chile.is_valid_rut``.
- Si el formulario es válido, se crea el usuario y se envía una notificación por correo electrónico. Dependiendo de la ubicación de origen, el usuario puede ser redirigido a la página de gestión de usuarios o a la página de inicio de sesión.
- Si el formulario no es válido, se retornan mensajes de error correspondientes.

Retorno
-------

- Retorna una redirección a la página de gestión de usuarios o al inicio de sesión según el caso. Si hay errores en el formulario, se muestra el formulario nuevamente con los errores.

---

error_rut_origen
=================

Función para manejar errores relacionados con un RUT inválido.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``).
  
- ``origen``:  
  La ubicación de origen, que puede ser ``inside`` o de otro tipo.

- ``formulario``:  
  El formulario con los datos ingresados por el usuario.

Funcionamiento
--------------

- Si el RUT ingresado es inválido, se muestra un mensaje de error.
- Dependiendo del origen, se renderiza la página correspondiente, ya sea la de gestión de usuarios o la de registro.

Retorno
-------

- Retorna la página correspondiente con el mensaje de error y el formulario de nuevo usuario o registro.

---

error_campos_origen
====================

Función para manejar errores relacionados con campos incorrectos en el formulario.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``).
  
- ``origen``:  
  La ubicación de origen, que puede ser ``inside`` o de otro tipo.

- ``formulario``:  
  El formulario con los datos ingresados por el usuario.

Funcionamiento
--------------

- Si hay campos incorrectos en el formulario, se muestra un mensaje de error.
- Dependiendo del origen, se renderiza la página correspondiente, ya sea la de gestión de usuarios o la de registro.

Retorno
-------

- Retorna la página correspondiente con el mensaje de error y el formulario de nuevo usuario o registro.

manage_users
=============

Vista para gestionar los usuarios del sistema, accesible solo para usuarios con permisos adecuados.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la sesión y obtener la lista de usuarios y sus perfiles.

Funcionamiento
--------------

- Se elimina cualquier dato previo relacionado con el campo ``edit_username`` en la sesión del usuario.
- Se obtiene una lista de usuarios excluyendo al usuario con el RUT ``15.053.475-5`` y se ordena por fecha de creación en orden descendente.
- También se obtiene una lista de perfiles de usuarios (``UsuarioProfile``) excluyendo el usuario con ID 2.
- Se pasa la lista de usuarios y perfiles al contexto y se renderiza la plantilla ``pages/users/manage_users.html``.

Retorno
-------

- Retorna la página con la lista de usuarios y sus perfiles en el contexto, mostrando la vista de gestión de usuarios.

---

status_user
============

Vista para cambiar el estado de un usuario (habilitar/deshabilitar).

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener el nombre de usuario y actualizar su estado.

Funcionamiento
--------------

- Cuando se recibe una solicitud ``POST``, se obtiene el usuario cuyo estado se desea cambiar.
- Si el usuario está habilitado (``is_active=True``), se deshabilita (``is_active=False``) y se envía una notificación por correo electrónico.
- Si el usuario ya está deshabilitado, se habilita de nuevo y se envía otra notificación.
- Se muestra un mensaje de éxito después de realizar el cambio.

Retorno
-------

- Retorna una redirección a la vista de gestión de usuarios después de cambiar el estado del usuario.

---

edit_user_profile
==================

Vista para editar el perfil de un usuario, accesible solo para usuarios con permisos adecuados.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para obtener y modificar los datos del perfil del usuario.

Funcionamiento
--------------

- Se guarda el nombre de usuario que se va a editar en la sesión de usuario (campo ``edit_username``).
- Se obtiene el usuario y su perfil, junto con su documentación y licencias asociadas.
- Se verifica la extensión de las imágenes y documentos asociados al usuario.
- Se formatean las fechas de nacimiento, vencimiento de cédula y licencias a un formato específico.
- Dependiendo del rol del usuario, algunos campos del formulario serán deshabilitados.
- Se renderizan varios formularios relacionados con el perfil del usuario, incluyendo los campos de usuario, perfil, licencias y documentación.

Retorno
-------

- Retorna la página de edición del perfil de usuario con todos los datos cargados en el contexto para ser editados en la plantilla ``pages/users/edit_user_profile.html``.

save_edit_user_profile
=======================

Vista para guardar la edición del perfil de un usuario.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar los datos del formulario enviados en una solicitud POST.

Requisitos
----------

- Requiere que el usuario esté autenticado, como se indica con el decorador ``@login_required``.
- El usuario debe tener permisos de administrador, base de datos o supervisor, como se indica con el decorador ``@sondaje_admin_or_base_datos_or_supervisor_required``.

Funcionamiento
--------------

- La función permite la edición de los datos del perfil de un usuario en varios campos (nombre, apellido, teléfono, correo, rol, etc.) utilizando datos enviados en una solicitud POST.
- Los datos se actualizan en las tablas relacionadas con el usuario, como ``Usuario``, ``UsuarioProfile`` y ``LicenciasUsuario``.
- Para cada campo, se verifican posibles errores (como la existencia duplicada de teléfono o correo) y, en caso de error, se retorna un mensaje de error con el código de estado 400.
- La función también gestiona la actualización de los documentos del usuario, como la fotografía, cédula y licencias, dependiendo de los valores enviados en la solicitud.
- Al final de la ejecución, se envían notificaciones por correo electrónico sobre la actualización del perfil y se redirige al usuario a la página de gestión de usuarios.

Retorno
-------

- Si todo se procesa correctamente, la función redirige al usuario a la página de gestión de usuarios (``redirect('manage_users')``).
- En caso de error, se retornan respuestas JSON con los mensajes de error apropiados y el código de estado 400.

edit_my_profile
================

Vista para editar el perfil de un usuario.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar los datos y proporcionar la vista de edición del perfil.

Requisitos
----------

- Requiere que el usuario esté autenticado, como se indica con el decorador ``@login_required``.

Funcionamiento
--------------

- La función obtiene la información del usuario actualmente autenticado, incluyendo datos de su perfil, licencias y documentación.
- Se consultan los datos relacionados con el usuario, como la ciudad, nacionalidad, género, faena, y la documentación de la faena general (fotografías y licencias).
- Se formatean las fechas de nacimiento, vencimiento de cédula y licencias.
- La función construye un contexto para la vista con datos iniciales para los formularios de edición del perfil, incluyendo campos de nombre, correo, teléfono, rol, ciudad, nacionalidad, faena, y licencias.
- El contexto también incluye las URLs de las fotografías del usuario y las extensiones de los archivos asociados (imagen, PDF, etc.), y la documentación relacionada con la faena general.
- Finalmente, se devuelve la vista de perfil del usuario con el contexto generado, lo que permite al usuario editar sus datos en el formulario.

Retorno
-------

- La función devuelve una vista renderizada con el contexto de edición de perfil del usuario, utilizando el template ``pages/users/my_profile.html``.

save_edit_my_profile
====================

Vista para guardar los cambios realizados en el perfil del usuario.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar los datos del formulario de edición del perfil y actualizar la información del usuario.

Requisitos
----------

- Requiere que el usuario esté autenticado, como se indica con el decorador ``@login_required``.

Funcionamiento
--------------

- La función maneja las solicitudes de tipo ``POST`` para guardar los cambios en el perfil del usuario.
- Se actualizan los datos del usuario, incluyendo:
  - ``first_name``, ``last_name``, ``phone``, y ``email``.
  - Los campos adicionales de su perfil (ciudad, nacionalidad, género, fecha de nacimiento, fecha de vencimiento de la cédula).
  - Las fechas de vencimiento de las licencias del usuario.
  - Se actualizan los permisos de licencias profesionales (A1, A2, etc.).
- Si los datos de teléfono o correo electrónico ya existen, se devuelve un error con un mensaje de advertencia.
- Si alguna actualización de perfil falla, se captura la excepción y no se realiza la actualización.
- Las fotografías asociadas al perfil, cédula, y licencias se actualizan si el usuario activa los campos correspondientes.
- Finalmente, se guardan los cambios en la documentación del usuario y se envía una notificación por correo electrónico al usuario informando que su perfil ha sido actualizado.
  
Retorno
-------

- La función redirige al usuario a la vista ``edit_my_profile`` con un mensaje de éxito una vez que los datos han sido guardados correctamente.

save_password_change
=====================

Vista para cambiar la contraseña del usuario.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud del formulario de cambio de contraseña.

Requisitos
----------

- Requiere que el usuario esté autenticado, como se indica con el decorador ``@login_required``.

Funcionamiento
--------------

- La función maneja las solicitudes de tipo ``POST`` para cambiar la contraseña del usuario.
- Se utiliza el formulario ``PasswordChangeForm`` para validar y procesar la nueva contraseña.
- Si el formulario es válido, se guarda la nueva contraseña, se actualiza la sesión del usuario con la nueva autenticación y se muestra un mensaje de éxito.
- Si el formulario no es válido, se muestra un mensaje de error indicando que las contraseñas no coinciden o son incorrectas, y se redirige al usuario a la página de cambio de contraseña.
- Si la solicitud no es de tipo ``POST``, se muestra un mensaje de error y se redirige al usuario a la página de cambio de contraseña.

Retorno
-------

- Si el formulario es válido, redirige al usuario a la vista ``edit_my_profile`` con un mensaje de éxito.
- Si hay errores en el formulario, redirige al usuario a la vista ``password_change`` con un mensaje de error.

password_reset_send
===================

Vista para enviar un correo electrónico de restablecimiento de contraseña.

Parámetros
----------

- ``request``:  
  El objeto de solicitud HTTP (``HttpRequest``). Se utiliza para gestionar la solicitud de restablecimiento de contraseña.

Requisitos
----------

- El formulario ``PasswordResetForm`` es utilizado para validar la dirección de correo electrónico proporcionada.
- Si el correo electrónico es válido, se envía un correo de restablecimiento de contraseña a la dirección correspondiente.
- La función requiere que el correo electrónico ingresado esté registrado en el sistema. Si no se encuentra un usuario asociado, se muestra un mensaje de error.

Funcionamiento
--------------

- La función maneja las solicitudes de tipo ``POST`` para el envío del correo de restablecimiento de contraseña.
- Si el formulario es válido, se obtiene la dirección de correo electrónico ingresada.
- Se verifica si hay usuarios registrados con esa dirección de correo electrónico.
  - Si hay usuarios asociados, se envía el correo de restablecimiento de contraseña utilizando el método ``form.save``.
  - Si el envío del correo es exitoso, se muestra un mensaje de éxito y se redirige al usuario a la vista ``logincustom``.
  - Si ocurre un error durante el envío del correo (por ejemplo, un error en el encabezado del correo), se muestra un mensaje de error indicando "Solicitud Invalida".
- Si no se encuentran usuarios asociados con el correo ingresado, se muestra un mensaje de error que indica que no hay usuarios registrados con esa dirección de correo electrónico.
- Si el formulario no es válido, se muestra un mensaje de error indicando que el correo ingresado es incorrecto.

Retorno
-------

- Si el correo es enviado con éxito, redirige al usuario a la vista ``logincustom`` con un mensaje de éxito.
- Si hay un error al procesar el formulario o si no se encuentra un usuario asociado con el correo ingresado, redirige al usuario a la vista ``password_reset`` con un mensaje de error.


Rutas (urls.py)
***************

Define las rutas de acceso a las vistas del módulo.

logincustom
============

Ruta para la vista de inicio de sesión personalizada.

URL
---

- ``/``

Vista asociada
--------------

- ``CustomLoginView.as_view()``

---

logoutcustom
============

Ruta para la vista de cierre de sesión personalizada.

URL
---

- ``/logout/``

Vista asociada
--------------

- ``CustomLogoutView.as_view()``

---

register
=========

Ruta para registrarse en la aplicación.

URL
---

- ``/register``

Vista asociada
--------------

- ``register``

---

new_user
==========

Ruta para crear un nuevo usuario.

URL
---

- ``/new_user``

Vista asociada
--------------

- ``new_user``

---

save_new_user
===============

Ruta para guardar un nuevo usuario.

URL
---

- ``/save_new_user``

Vista asociada
--------------

- ``save_new_user``

---

manage_users
=============

Ruta para gestionar usuarios.

URL
---

- ``/manage_users``

Vista asociada
--------------

- ``manage_users``

---

status_user
============

Ruta para ver el estado de un usuario.

URL
---

- ``/status_user``

Vista asociada
--------------

- ``status_user``

---

edit_user_profile
==================

Ruta para editar el perfil de un usuario.

URL
---

- ``/edit_user_profile``

Vista asociada
--------------

- ``edit_user_profile``

---

save_edit_user_profile
========================

Ruta para guardar los cambios en el perfil de un usuario.

URL
---

- ``/save_edit_user_profile``

Vista asociada
--------------

- ``save_edit_user_profile``

---

edit_my_profile
================

Ruta para editar el perfil del usuario actual.

URL
---

- ``/edit_my_profile``

Vista asociada
--------------

- ``edit_my_profile``

---

save_edit_my_profile
======================

Ruta para guardar los cambios en el perfil del usuario actual.

URL
---

- ``/save_edit_my_profile``

Vista asociada
--------------

- ``save_edit_my_profile``

---

password_change
================

Ruta para cambiar la contraseña del usuario.

URL
---

- ``/password_change/``

Vista asociada
--------------

- ``auth_views.PasswordChangeView.as_view(template_name="registration/password_change.html")``

---

save_password_change
======================

Ruta para guardar el cambio de contraseña.

URL
---

- ``/save_password_change``

Vista asociada
--------------

- ``save_password_change``

---

password_reset
===============

Ruta para restablecer la contraseña del usuario.

URL
---

- ``/pasword_reset/``

Vista asociada
--------------

- ``auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html")``

---

password_reset_send
====================

Ruta para enviar la solicitud de restablecimiento de contraseña.

URL
---

- ``/pasword_reset_send``

Vista asociada
--------------

- ``password_reset_send``

---

password_reset_confirm
========================

Ruta para confirmar el restablecimiento de la contraseña.

URL
---

- ``/reset/<uidb64>/<token>``

Vista asociada
--------------

- ``auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html")``

---

password_reset_complete
========================

Ruta para completar el restablecimiento de la contraseña.

URL
---

- ``/password_reset_complete/``

Vista asociada
--------------

- ``auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html")``

