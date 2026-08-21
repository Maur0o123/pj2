from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prevencion', '0036_prevencionresultadocurso_intentos_aprobado'),
    ]

    operations = [
        migrations.AddField(
            model_name='prevencionnotificaciondocumento',
            name='fecha_inicio_lectura',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha Inicio Lectura'),
        ),
    ]
