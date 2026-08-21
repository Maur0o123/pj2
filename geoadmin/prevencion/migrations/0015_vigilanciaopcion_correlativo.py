from django.db import migrations, models


def poblar_correlativo_por_tipo(apps, schema_editor):
    VigilanciaOpcion = apps.get_model('prevencion', 'VigilanciaOpcion')

    tipos = (
        VigilanciaOpcion.objects
        .values_list('tipo', flat=True)
        .distinct()
    )

    for tipo in tipos:
        opciones = VigilanciaOpcion.objects.filter(tipo=tipo).order_by('id')
        for correlativo, opcion in enumerate(opciones, start=1):
            VigilanciaOpcion.objects.filter(pk=opcion.pk).update(correlativo=correlativo)


def revertir_correlativo_por_tipo(apps, schema_editor):
    VigilanciaOpcion = apps.get_model('prevencion', 'VigilanciaOpcion')
    VigilanciaOpcion.objects.all().update(correlativo=None)


class Migration(migrations.Migration):

    dependencies = [
        ('prevencion', '0014_vigilanciaopcion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vigilanciaopcion',
            name='correlativo',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='ID Tipo'),
        ),
        migrations.RunPython(
            poblar_correlativo_por_tipo,
            reverse_code=revertir_correlativo_por_tipo,
        ),
        migrations.AlterField(
            model_name='vigilanciaopcion',
            name='correlativo',
            field=models.PositiveIntegerField(verbose_name='ID Tipo'),
        ),
        migrations.AddConstraint(
            model_name='vigilanciaopcion',
            constraint=models.UniqueConstraint(fields=('tipo', 'correlativo'), name='uq_prevencion_vigilancia_tipo_correlativo'),
        ),
    ]
