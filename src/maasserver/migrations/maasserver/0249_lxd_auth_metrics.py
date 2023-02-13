# Generated by Django 2.2.12 on 2021-09-23 13:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0248_auto_20211006_1829"),
    ]

    operations = [
        migrations.AddField(
            model_name="bmc",
            name="created_with_cert_expiration_days",
            field=models.IntegerField(default=None, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="bmc",
            name="created_with_maas_generated_cert",
            field=models.BooleanField(default=None, editable=False, null=True),
        ),
        migrations.AddField(
            model_name="bmc",
            name="created_with_trust_password",
            field=models.BooleanField(default=None, editable=False, null=True),
        ),
    ]
