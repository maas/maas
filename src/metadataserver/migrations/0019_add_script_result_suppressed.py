# Generated by Django 1.11.11 on 2019-03-13 19:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("metadataserver", "0018_script_result_skipped")]

    operations = [
        migrations.AddField(
            model_name="scriptresult",
            name="suppressed",
            field=models.BooleanField(default=False),
        )
    ]
