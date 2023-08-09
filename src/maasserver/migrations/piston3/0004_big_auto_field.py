# Generated by Django 3.2.12 on 2023-05-02 07:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("piston3", "0003_piston_nonce_index"),
    ]

    operations = [
        migrations.AlterField(
            model_name="consumer",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="nonce",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="token",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
    ]