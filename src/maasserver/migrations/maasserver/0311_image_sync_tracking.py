# Generated by Django 3.2.12 on 2023-09-27 14:21

from django.db import migrations, models
import django.db.models.deletion

import maasserver.models.cleansave


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0310_rootfs_image_extensions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bootresourceset",
            name="sync",
        ),
        migrations.CreateModel(
            name="BootResourceFileSync",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("updated", models.DateTimeField(editable=False)),
                ("size", models.BigIntegerField(default=0)),
                (
                    "file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="maasserver.bootresourcefile",
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="maasserver.regioncontroller",
                    ),
                ),
            ],
            options={
                "unique_together": {("file", "region")},
            },
            bases=(maasserver.models.cleansave.CleanSave, models.Model),
        ),
    ]
