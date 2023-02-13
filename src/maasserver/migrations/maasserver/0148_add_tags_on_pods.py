# Generated by Django 1.11.9 on 2018-03-01 01:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0147_pod_zones")]

    operations = [
        migrations.AddField(
            model_name="bmc",
            name="tags",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TextField(),
                size=None,
                default=list,
                blank=True,
                null=True,
            ),
        )
    ]
