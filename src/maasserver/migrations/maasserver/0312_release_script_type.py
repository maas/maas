# Generated by Django 3.2.12 on 2023-10-18 09:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0311_image_sync_tracking"),
    ]

    operations = [
        migrations.AlterField(
            model_name="script",
            name="script_type",
            field=models.IntegerField(
                choices=[
                    (0, "Commissioning script"),
                    (2, "Testing script"),
                    (3, "Release script"),
                ],
                default=2,
            ),
        ),
        migrations.AlterField(
            model_name="scriptset",
            name="result_type",
            field=models.IntegerField(
                choices=[
                    (0, "Commissioning"),
                    (1, "Installation"),
                    (2, "Testing"),
                    (3, "Release"),
                ],
                default=0,
                editable=False,
            ),
        ),
    ]
