# Generated by Django 2.2.12 on 2021-06-14 23:05

from django.db import migrations, models

import maasserver.models.cleansave


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0241_physical_interface_default_node_numanode"),
    ]

    operations = [
        migrations.CreateModel(
            name="ForwardDNSServer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(editable=False)),
                ("updated", models.DateTimeField(editable=False)),
                (
                    "ip_address",
                    models.GenericIPAddressField(
                        default=None, editable=False, unique=True
                    ),
                ),
                ("domains", models.ManyToManyField(to="maasserver.Domain")),
            ],
            options={
                "abstract": False,
            },
            bases=(maasserver.models.cleansave.CleanSave, models.Model),
        ),
    ]
