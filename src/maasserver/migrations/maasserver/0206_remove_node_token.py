# Generated by Django 1.11.11 on 2020-04-08 03:28

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0205_pod_nodes")]

    operations = [migrations.RemoveField(model_name="node", name="token")]
