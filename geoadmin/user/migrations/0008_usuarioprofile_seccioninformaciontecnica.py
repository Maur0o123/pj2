from django.db import migrations, models

import core.choices


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0007_usuarioprofile_seccioninventario"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuarioprofile",
            name="seccionInformacionTecnica",
            field=models.CharField(
                blank=True,
                choices=core.choices.opcion,
                default="No",
                max_length=10,
                null=True,
                verbose_name="Sección Información Técnica",
            ),
        ),
    ]
