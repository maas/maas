# Generated by Django 1.11.11 on 2018-04-12 20:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("metadataserver", "0017_store_requested_scripts")]

    operations = [
        migrations.AlterField(
            model_name="scriptresult",
            name="status",
            field=models.IntegerField(
                choices=[
                    (0, "Pending"),
                    (1, "Running"),
                    (2, "Passed"),
                    (3, "Failed"),
                    (4, "Timed out"),
                    (5, "Aborted"),
                    (6, "Degraded"),
                    (7, "Installing dependencies"),
                    (8, "Failed installing dependencies"),
                    (9, "Skipped"),
                ],
                default=0,
            ),
        )
    ]
