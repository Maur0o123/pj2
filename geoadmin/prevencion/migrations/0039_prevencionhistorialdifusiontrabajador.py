from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('prevencion', '0038_prevencionresultadocursointento'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrevencionHistorialDifusionTrabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trabajador_rut', models.CharField(blank=True, default='', max_length=20, verbose_name='RUT Trabajador')),
                ('trabajador_nombre', models.CharField(blank=True, default='', max_length=200, verbose_name='Nombre Trabajador')),
                ('actor_nombre', models.CharField(blank=True, default='', max_length=200, verbose_name='Nombre Actor')),
                ('accion', models.CharField(choices=[('agregado', 'Agregado'), ('quitado', 'Eliminado')], max_length=20, verbose_name='Accion')),
                ('fechacreacion', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha Creacion')),
                ('actor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='historial_difusion_trabajador_realizado', to=settings.AUTH_USER_MODEL, verbose_name='Realizado por')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_difusion_trabajadores', to='prevencion.prevenciondocumento', verbose_name='Documento')),
                ('trabajador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='historial_difusion_trabajador_afectado', to=settings.AUTH_USER_MODEL, verbose_name='Trabajador afectado')),
            ],
            options={
                'verbose_name': 'Historial Difusion Trabajador',
                'verbose_name_plural': 'Historiales Difusion Trabajadores',
                'db_table': 'prevencion_historial_difusion_trabajador',
                'ordering': ['-fechacreacion', '-id'],
            },
        ),
        migrations.AddIndex(
            model_name='prevencionhistorialdifusiontrabajador',
            index=models.Index(fields=['documento', 'fechacreacion'], name='prevencion__documen_2ea83b_idx'),
        ),
        migrations.AddIndex(
            model_name='prevencionhistorialdifusiontrabajador',
            index=models.Index(fields=['accion'], name='prevencion__accion_94d0f8_idx'),
        ),
        migrations.AddIndex(
            model_name='prevencionhistorialdifusiontrabajador',
            index=models.Index(fields=['trabajador'], name='prevencion__trabaja_ea531e_idx'),
        ),
    ]
