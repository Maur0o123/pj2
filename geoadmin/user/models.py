import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Ciudad, Nacionalidad, Genero, Faena
from datetime import datetime
from core.choices import opcion

from administration.managers import AuditableQuerySet

class AuditableUserManager(UserManager):
    def get_queryset(self):
        return AuditableQuerySet(self.model, using=self._db)

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador" # lo ve todo
        JEFE_MANTENCION = "JEFE MANTENCION", "Jefe Mantencion"
        SUPERVISOR = "SUPERVISOR", "Supervisor" 
        CONTROLADOR = "CONTROLADOR", "Controlador" 
        PERFORISTA = "PERFORISTA", "Perforista"
        BASE_DATOS = "BASE DATOS", "Base de Datos"
        CONDUCTOR = "CONDUCTOR", "Conductor" 
        TRABAJADOR = "TRABAJADOR", "Trabajador" 
        PREVENCIONISTA = "PREVENCIONISTA", "Prevencionista"
        SIN_ASIGNAR = "SIN ASIGNAR", "Sin Asignar" # no ve nada, solo su perfil

    base_role = "ADMIN"
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.SIN_ASIGNAR, verbose_name='Rol')
    phone = models.IntegerField(null=True, verbose_name='Telefono')

    objects = AuditableUserManager()

    @property
    def nombre_con_detalles(self):
        nombre = self.get_full_name() or self.username
        cargo = self.get_role_display() if self.role else "Sin Cargo"
        try:
            faena = self.usuarioprofile.faena.faena if self.usuarioprofile.faena else "Sin Faena"
        except Exception:
            faena = "Sin Faena"
        return f"{nombre} ({cargo}) - {faena}"


class UsuarioManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return AuditableQuerySet(self.model, using=self._db)

class Usuario(User):
    base_role = User.Role.SIN_ASIGNAR
    Usuario = UsuarioManager()
    class Meta:
        proxy = True

class UsuarioProfile(models.Model):
    class RolVehicular(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        JEFE_MANTENCION = "JEFE MANTENCION", "Jefe Mantencion"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        BASE_DATOS = "BASE DATOS", "Base de Datos"
        CONDUCTOR = "CONDUCTOR", "Conductor"
        TRABAJADOR = "TRABAJADOR", "Trabajador"
        SIN_ASIGNAR = "SIN ASIGNAR", "Sin Asignar"

    class RolSondaje(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        JEFE_MANTENCION = "JEFE MANTENCION", "Jefe Mantencion"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        CONTROLADOR = "CONTROLADOR", "Controlador"
        PERFORISTA = "PERFORISTA", "Perforista"
        BASE_DATOS = "BASE DATOS", "Base de Datos"
        CONDUCTOR = "CONDUCTOR", "Conductor"
        TRABAJADOR = "TRABAJADOR", "Trabajador"
        SIN_ASIGNAR = "SIN ASIGNAR", "Sin Asignar"

    class RolPrevencion(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        BASE_DATOS = "BASE DATOS", "Base de Datos"
        CONDUCTOR = "CONDUCTOR", "Conductor"
        TRABAJADOR = "TRABAJADOR", "Trabajador"
        PREVENCIONISTA = "PREVENCIONISTA", "Prevencionista"
        SIN_ASIGNAR = "SIN ASIGNAR", "Sin Asignar"

    class RolInventarioAdministracion(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        BASE_DATOS = "BASE DATOS", "Base de Datos"
        SIN_ASIGNAR = "SIN ASIGNAR", "Sin Asignar"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faena = models.ForeignKey(Faena, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Faena')
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ciudad')
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Nacionalidad')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Genero')
    fechaNacimiento = models.DateTimeField(auto_now=False, null=True, verbose_name='Fecha Nacimiento')
    fechaCedulaVencimiento = models.DateTimeField(auto_now=False, null=True, verbose_name='Cédula Identidad (Vencimiento)')
    
    seccionVehicular = models.CharField(
        max_length=50, choices=RolVehicular.choices, default=RolVehicular.SIN_ASIGNAR, null=True, blank=True, verbose_name='Rol Sección Vehicular'
    )
    seccionSondaje = models.CharField(
        max_length=50, choices=RolSondaje.choices, default=RolSondaje.SIN_ASIGNAR, null=True, blank=True, verbose_name='Rol Sección Sondaje'
    )
    seccionPrevencion = models.CharField(
        max_length=50, choices=RolPrevencion.choices, default=RolPrevencion.SIN_ASIGNAR, null=True, blank=True, verbose_name='Rol Sección Prevención de Riesgos'
    )
    seccionInventario = models.CharField(
        max_length=50, choices=RolInventarioAdministracion.choices, default=RolInventarioAdministracion.SIN_ASIGNAR, null=True, blank=True, verbose_name='Rol Sección Inventario'
    )
    seccionAdministracion = models.CharField(
        max_length=50, choices=RolInventarioAdministracion.choices, default=RolInventarioAdministracion.SIN_ASIGNAR, null=True, blank=True, verbose_name='Rol Sección Administración'
    )

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return "{} {}".format(self.nacionalidad, self.ciudad)

    class Meta:
        verbose_name = 'Usuario Información Adicional'
        verbose_name_plural = 'Usuarios Información Adicional'

class UserInformacionLaboral(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='informacion_laboral')
    area = models.ForeignKey(
        'prevencion.VigilanciaArea',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_informacion_laboral_area',
    )
    ges = models.ForeignKey(
        'prevencion.VigilanciaGes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_informacion_laboral_ges',
    )
    cargo = models.ForeignKey(
        'prevencion.VigilanciaCargo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_informacion_laboral_cargo',
    )
    tipo_contrato = models.ForeignKey(
        'prevencion.VigilanciaTipoContrato',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_informacion_laboral_tipo_contrato',
    )
    contrato = models.ForeignKey(
        'prevencion.VigilanciaContrato',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios_informacion_laboral_contrato',
    )
    fechaIngreso = models.DateField(null=True, blank=True, verbose_name='Fecha Ingreso')
    fechaDesvinculacion = models.DateField(null=True, blank=True, verbose_name='Fecha Desvinculación')

    objects = AuditableQuerySet.as_manager()

    def __str__(self):
        return f"Info laboral {self.user.username}"

    class Meta:
        verbose_name = 'Información Laboral'
        verbose_name_plural = 'Información Laboral'
        db_table = 'user_informacion_laboral'

class LicenciasUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fechaLicenciaVencimiento = models.DateTimeField(auto_now=False,null=True,verbose_name='Licencia Conducir (Vencimiento)')
    fechaLicenciaInternaVencimiento = models.DateTimeField(auto_now=False,null=True,verbose_name='Licencia Interna (Vencimiento)')
    licenciaClaseB = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase B')
    licenciaClaseC = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase C')
    licenciaClaseD = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase D')
    licenciaClaseE = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase E')
    licenciaClaseF = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase F')
    licenciaClaseA1 = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase A1')
    licenciaClaseA2 = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase A2')
    licenciaClaseA3 = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase A3')
    licenciaClaseA4 = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase A4')
    licenciaClaseA5 = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase A5')
    licenciaClaseA1Antigua = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase A1 Antigua')
    licenciaClaseA2Antigua = models.CharField(max_length=10,null=True,choices=opcion,verbose_name='Clase A2 Antigua')
    
    objects = AuditableQuerySet.as_manager()

    def __str__(self) :
        return "{}".format(self.user.username)
    class Meta:
        verbose_name = 'Licencia de Conducir'
        verbose_name_plural = 'Licencia de Conducir'
        db_table = 'user_licencia_conducir' 
    
class DocumentacionUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def generaNombre(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        user_id = instance.user.username
        ruta = f'documentacion_usuario/{user_id}' 
        fecha =datetime.now().strftime("%Y%m%d_%H%M%S") 
        nombre = "{}.{}".format(fecha,extension)
        return os.path.join(ruta,nombre)            
    fotografiaUsuario = models.ImageField(upload_to=generaNombre,null=True,blank=True,default='documentacion_usuario/no-avatar.png')
    fotografiaCedula = models.ImageField(upload_to=generaNombre,null=True,blank=True,default='documentacion_usuario/no-imagen.png')
    fotografiaLicencia = models.ImageField(upload_to=generaNombre,null=True,blank=True,default='documentacion_usuario/no-imagen.png')
    fotografiaLicenciaInterna = models.ImageField(upload_to=generaNombre,null=True,blank=True,default='documentacion_usuario/no-imagen.png')
    
    objects = AuditableQuerySet.as_manager()

    def __str__(self) :
        return "{}".format(self.user.username)
    class Meta:
        verbose_name = 'Documentacion Usuario'
        verbose_name_plural = 'Documentacion Usuarios'
        db_table = 'user_documentacion' 


@receiver(post_save, sender=Usuario)
def create_usuario_profile(sender, instance, created, **kwargs):
    if created:
        faena, _ = Faena.objects.get_or_create(faena="SIN ASIGNAR")
        UsuarioProfile.objects.get_or_create(
            user=instance, 
            defaults={'faena': faena}
        )

@receiver(post_save, sender=Usuario)
def create_licencias_usuario(sender, instance, created, **kwargs):
    if created:
        LicenciasUsuario.objects.create(user=instance)
        
@receiver(post_save, sender=Usuario)
def create_documentacion_usuario(sender, instance, created, **kwargs):
    if created:
        DocumentacionUsuario.objects.create(user=instance)

@receiver(post_save, sender=Usuario)
def create_informacion_laboral_usuario(sender, instance, created, **kwargs):
    if created:
        UserInformacionLaboral.objects.get_or_create(user=instance)