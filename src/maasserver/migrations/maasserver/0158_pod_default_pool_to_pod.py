# Generated by Django 1.11.11 on 2018-05-25 12:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0157_drop_usergroup_and_role")]

    operations = [
        migrations.RenameField(
            model_name="bmc", old_name="default_pool", new_name="pool"
        )
    ]
