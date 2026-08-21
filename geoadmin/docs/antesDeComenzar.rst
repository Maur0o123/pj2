
Antes de Comenzar
=================

Aquí encontraremos los principales consejos y requisitos necesarios para ejecutar todos los procesos sin problemas.

    - Siempre trabaja en un entorno virtual.
    - Todas las variables de entorno deben estar correctamente configuradas en el archivo ``.env``.

.. important::

    La configuración exacta puede variar entre ambientes. En el repositorio actual se validó un entorno local con ``Python 3.12`` y ``Django 4.2.11``. Los datos de producción deben verificarse directamente en el servidor antes de desplegar.

Servidor
--------

Actualmente, contamos con un servidor disponible con las siguientes credenciales de acceso:

.. table:: Información del Servidor

   +-------------------+---------+------------+-------------------------------------+---------------------+------------------------+
   | IP                | Usuario | Contraseña | Ruta del Repositorio                | Usuario del Sistema | Contraseña del Sistema |
   +===================+=========+============+=====================================+=====================+========================+
   | ``152.70.140.40`` | XXXX    |   XXXX     | /home/app                           |   ubuntu            |       XXXX             |
   +-------------------+---------+------------+-------------------------------------+---------------------+------------------------+

El servidor y el entorno de ejecución deben revisar al menos los siguientes componentes:

.. list-table:: Tecnologías y Configuración del Servidor
   :header-rows: 1

   * - Tecnología
     - Versión
     - Usuario
     - Contraseña
     - Usuario BD
     - Contraseña BD
     - Base de Datos
   * - Python
     - 3.12.x
     - 
     - 
     - 
     - 
     - 
   * - Django
     - 4.2.11
     - 
     - 
     - 
     - 
     - 
   * - Mysql
     - 8.x
     - 
     - 
     - 
     - 
     - Definida en ``SQL_NAME``

.. important::

    Para tener acceso a las credenciales comuniquese con el departamento de Informatica.

Conección al Servidor
---------------------

Antes de establecer la conexión con el servidor, es necesario solicitar al departamento de informática los siguientes elementos:

- Archivo de clave privada ``.ppk``.
- Credenciales de acceso al servidor:
    1. ``usuario``
    2. ``contraseña``
    3. ``dirección IP``

.. Note::

    Asegúrese de tener instalado ``OpenSSH`` en su equipo local antes de continuar.

1.  Instalación de herramientas necesarias. 

    Abra una terminal y ejecute el siguiente comando para instalar ``putty-tools``:

    .. code-block:: bash

        sudo apt update && sudo apt install putty-tools -y

2.  Conversión de clave privada ``.ppk`` → ``.pem``.

    Si la clave proporcionada está en formato ``.ppk``, conviértala a ``.pem`` con el siguiente comando:

    .. code-block:: bash    

        puttygen key.ppk -O private-openssh -o key.pem

    .. Note::

        Reemplace ``key.ppk`` con el nombre exacto del archivo recibido.

3.  Configuración de Permisos del Archivo ``.pem``

    Para evitar problemas de seguridad, ajuste los permisos del archivo ``.pem``:

    .. code-block:: bash  

        chmod 600 key.pem

4.  Establecer Conexión con el Servidor

    Ubíquese en el directorio donde se encuentra el archivo ``.pem`` y ejecute el siguiente comando:

    .. code-block:: bash  

        ssh -i key.pem root@152.70.140.40

    .. Note::

        - Reemplace key.pem con el nombre del archivo recibido.
        - Asegúrese de que el nombre del archivo no contenga espacios.
        - En caso de que el usuario no sea root, cámbielo por el usuario correspondiente (por ejemplo, ubuntu).

5.  Acceso al Directorio del Repositorio


    Una vez dentro del servidor, diríjase al directorio donde se alojará el repositorio:

    .. code-block:: bash  

        cd /home/app

    Si el directorio no existe, créelo con los siguientes comandos:    

    .. code-block:: bash  

        mkdir -p /home/app

    Para acceder al directorio:

    .. code-block:: bash  

        cd /home/app

    Aquí es donde debe clonar o descargar el repositorio del proyecto.

Instalación del Repositorio 
---------------------------

Lo primero que debemos realizar es lo siguiente:
    - Debemos solicitar acceso al repositorio, que se encuentra en GitHub.
    - Debemos clonar el repositorio en el servidor, en la ruta /home/app.
    - Al ingresar al directorio, debemos inicializar el entorno virtual.

Asegurate de estar dentro del Servidor, en caso de no tener las credenciales de acceso solicitalos al departamento de informatica.

1.  Ingresa al PATH del repositorio:

    .. code-block:: bash

        cd /home/app

.. note::

    - En caso de no tener creado el entorno virtual, debes crearlo, de lo contrario omite este paso:
    
    .. code-block:: bash

        python3 -m venv .venv

2.  Activar entorno virtual:

    .. code-block:: bash

        source .venv/bin/activate

3.  Instalar dependecias desde el archivo **requirements.txt**:

    .. code-block:: bash

        pip install -r requirements.txt

4.  En caso de  actualizar dependencias o agregar una nueva, debe actualizar **requirements.txt**:
 
    .. code-block:: bash

        pip freeze > requirements.txt

5.  Para salir del entorno virtual ejecuta:

    .. code-block:: bash

        deactivate

.. important::

    Es fundamental garantizar que se está trabajando con la versión más reciente del repositorio. Como parte de las buenas prácticas de desarrollo, se recomienda realizar las modificaciones en un entorno local en lugar de directamente en el servidor.  
    A continuación, se detallan los parámetros necesarios para la correcta configuración del archivo ``.env``.  

Configuración archivo ``.env``
------------------------------

Antes de proceder, es imprescindible verificar la existencia del archivo ``.env``, ya que, por razones de seguridad y buenas prácticas, este no se incluye en el repositorio de código.  

Si el archivo no está presente, deberá crearlo manualmente ejecutando el siguiente comando:  

1.  Asegurese de estar en el ``PATH`` correcto antes de continuar, ejecute:

    .. code-block:: bash

        cd /home/app

2.  Cree el archivo he ingrese los valores de las variables, para esto ejecute:

    .. code-block:: bash

        vim .env

    .. table:: Detalle archivo .env 

        +--------------------------+------------------------------------------------------------+
        | Variable                 | Descripción                                                |
        +==========================+============================================================+
        | TWILIO_ACCOUNT_SID       | ID de cuenta de Twilio, necesario para autenticarse.       |
        +--------------------------+------------------------------------------------------------+
        | TWILIO_AUTH_TOKEN        | Token de autenticación de Twilio para realizar solicitudes.|
        +--------------------------+------------------------------------------------------------+
        | TWILIO_WHATSAPP_NUMBER   | Número de WhatsApp proporcionado por Twilio.               |
        +--------------------------+------------------------------------------------------------+
        | TWILIO_PHONE_NUMBER      | Número de teléfono de Twilio para enviar SMS y llamadas.   |
        +--------------------------+------------------------------------------------------------+
        | DEFAULT_FROM_EMAIL       | Correo electrónico predeterminado para el envío de emails. |
        +--------------------------+------------------------------------------------------------+
        | EMAIL_HOST_USER          | Usuario del servicio SMTP (correo saliente).               |
        +--------------------------+------------------------------------------------------------+
        | EMAIL_HOST_PASSWORD      | Contraseña o token para autenticarse en el servicio SMTP.  |
        +--------------------------+------------------------------------------------------------+
        | SQL_NAME                 | Nombre de la base de datos del proyecto.                   |
        +--------------------------+------------------------------------------------------------+
        | SQL_USER                 | Usuario de la base de datos.                               |
        +--------------------------+------------------------------------------------------------+
        | SQL_PASSWORD             | Contraseña del usuario de la base de datos.                |
        +--------------------------+------------------------------------------------------------+
        | SQL_PORT                 | Puerto en el que corre la base de datos.                   |
        +--------------------------+------------------------------------------------------------+
        | DB_OPTIONS_INIT_COMMAND  | Comando de inicialización para la base de datos, como el   |
        |                          | modo SQL (ejemplo: `sql_mode=STRICT_TRANS_TABLES`).        |
        +--------------------------+------------------------------------------------------------+
        | DB_OPTIONS_CHARSET       | Configuración de codificación de caracteres de la BD.      |
        +--------------------------+------------------------------------------------------------+

.. important::

    Para tener acceso a estas variables de entono comuniquese con el departamento de Informatica.
