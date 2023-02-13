# Generated by Django 2.2.12 on 2022-02-01 09:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0260_drop_maas_support_views"),
    ]

    operations = [
        migrations.RunSQL(
            """
            UPDATE maasserver_interface
            SET node_config_id = maasserver_node.current_config_id
            FROM maasserver_node
            WHERE maasserver_interface.node_id = maasserver_node.id
            """
        ),
    ]
