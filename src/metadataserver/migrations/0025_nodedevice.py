# Generated by Django 2.2.12 on 2020-12-15 00:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("metadataserver", "0024_reorder_commissioning_scripts"),
    ]

    operations = [
        migrations.AlterField(
            model_name="script",
            name="hardware_type",
            field=models.IntegerField(
                choices=[
                    (0, "Node"),
                    (1, "CPU"),
                    (2, "Memory"),
                    (3, "Storage"),
                    (4, "Network"),
                    (5, "GPU"),
                ],
                default=0,
            ),
        ),
    ]
