# Generated by Django 1.11.11 on 2018-06-01 13:13

from django.db import migrations

from maasserver.enum import NODE_TYPE


def unset_resource_pools_nodes_not_machines(apps, schema_editor):
    """Unset resource pools for nodes that are not machines."""
    Node = apps.get_model("maasserver", "Node")
    Node.objects.exclude(node_type=NODE_TYPE.MACHINE).update(pool=None)


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0159_userprofile_auth_last_check_no_now_default")
    ]

    operations = [
        migrations.RunPython(unset_resource_pools_nodes_not_machines)
    ]
