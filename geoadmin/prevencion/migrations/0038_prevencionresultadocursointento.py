from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prevencion', '0037_prevencionnotificaciondocumento_fecha_inicio_lectura'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrevencionResultadoCursoIntento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_intento', models.PositiveSmallIntegerField(default=1, verbose_name='Nro Intento')),
                ('total_preguntas', models.PositiveIntegerField(default=0, verbose_name='Total Preguntas')),
                ('total_correctas', models.PositiveIntegerField(default=0, verbose_name='Total Correctas')),
                ('porcentaje_aprobacion', models.FloatField(default=0, verbose_name='Porcentaje Aprobación')),
                ('aprobado', models.BooleanField(default=False, verbose_name='Aprobado')),
                ('detalle_respuestas', models.JSONField(blank=True, default=list, verbose_name='Detalle Respuestas')),
                ('fechacreacion', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha Intento')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentos_curso', to='prevencion.prevenciondocumento', verbose_name='Documento')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentos_curso_prevencion', to=settings.AUTH_USER_MODEL, verbose_name='Trabajador')),
            ],
            options={
                'verbose_name': 'Intento Resultado Curso',
                'verbose_name_plural': 'Intentos Resultado Curso',
                'db_table': 'prevencion_resultado_curso_intento',
                'ordering': ['trabajador_id', 'numero_intento', 'id'],
            },
        ),
        migrations.AddConstraint(
            model_name='prevencionresultadocursointento',
            constraint=models.UniqueConstraint(fields=('documento', 'trabajador', 'numero_intento'), name='uq_prev_resultado_curso_intento_documento_trabajador_numero'),
        ),
        migrations.AddIndex(
            model_name='prevencionresultadocursointento',
            index=models.Index(fields=['documento', 'trabajador', 'numero_intento'], name='prevencion__documen_7fbad0_idx'),
        ),
        migrations.AddIndex(
            model_name='prevencionresultadocursointento',
            index=models.Index(fields=['trabajador', 'fechacreacion'], name='prevencion__trabaja_937969_idx'),
        ),
    ]
