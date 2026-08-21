from django.db import models
from user.models import User

class NotificationGroup(models.Model):
    class Category(models.TextChoices):
        VEHICULAR = 'VEHICULAR', 'Gestión Vehicular'
        SONDAJE = 'SONDAJE', 'Sondaje (Drilling)'
        PREVENCION = 'PREVENCION', 'Prevención de Riesgos'
        SISTEMA = 'SISTEMA', 'Mantenimiento del Sistema'

    name = models.CharField(max_length=100, verbose_name="Nombre del Grupo")
    slug = models.SlugField(unique=True, verbose_name="Identificador Único")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.VEHICULAR, verbose_name="Categoría")
    users = models.ManyToManyField(User, related_name='notification_groups', blank=True, verbose_name="Usuarios del Sistema")
    external_emails = models.JSONField(default=list, blank=True, verbose_name="Emails Externos")

    class Meta:
        verbose_name = "Grupo de Notificación"
        verbose_name_plural = "Grupos de Notificaciones"

    def __str__(self):
        return self.name
