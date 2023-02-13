# Generated by Django 2.2.12 on 2020-07-15 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0211_jsonfield_default_callable")]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="admins",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name="notification",
            name="dismissable",
            field=models.BooleanField(blank=True, default=True),
        ),
        migrations.AlterField(
            model_name="notification",
            name="users",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
