# Generated by Django 3.2.12 on 2024-05-28 07:32

from email.policy import default

from django.db import migrations, models
import django.db.models.deletion

restore_fk_maasserver_dnsresource_ip_addresses = """\
ALTER TABLE ONLY public.maasserver_dnsresource_ip_addresses
    ADD CONSTRAINT maasserver_dnsresour_dnsresource_id_fk_maasserve FOREIGN KEY (dnsresource_id) REFERENCES public.maasserver_dnsresource(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.maasserver_dnsresource_ip_addresses
    ADD CONSTRAINT maasserver_dnsresour_staticipaddress_id_fk_maasserve FOREIGN KEY (staticipaddress_id) REFERENCES public.maasserver_staticipaddress(id) DEFERRABLE INITIALLY DEFERRED;
"""

restore_fk_maasserver_forwarddnsserver_domains = """\
ALTER TABLE ONLY public.maasserver_forwarddnsserver_domains
    ADD CONSTRAINT maasserver_forwarddn_forwarddnsserver_id_fk_maasserve FOREIGN KEY (forwarddnsserver_id) REFERENCES public.maasserver_forwarddnsserver(id) DEFERRABLE INITIALLY DEFERRED;
"""

restore_fk_maasserver_interface_ip_addresses = """\
ALTER TABLE ONLY public.maasserver_interface_ip_addresses
    ADD CONSTRAINT maasserver_interface_interface_id_fk_maasserve FOREIGN KEY (interface_id) REFERENCES public.maasserver_interface(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.maasserver_interface_ip_addresses
    ADD CONSTRAINT maasserver_interface_staticipaddress_id_fk_maasserve FOREIGN KEY (staticipaddress_id) REFERENCES public.maasserver_staticipaddress(id) DEFERRABLE INITIALLY DEFERRED;
"""

restore_fk_maasserver_podhints_nodes = """\
ALTER TABLE ONLY public.maasserver_podhints_nodes
    ADD CONSTRAINT maasserver_podhints__node_id_fk_maasserve FOREIGN KEY (node_id) REFERENCES public.maasserver_node(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.maasserver_podhints_nodes
    ADD CONSTRAINT maasserver_podhints__podhints_id_fk_maasserve FOREIGN KEY (podhints_id) REFERENCES public.maasserver_podhints(id) DEFERRABLE INITIALLY DEFERRED;
"""

restore_fk_maasserver_node_tags = """\
ALTER TABLE ONLY public.maasserver_node_tags
    ADD CONSTRAINT maasserver_node_tags_node_id_fk_maasserver_node_id FOREIGN KEY (node_id) REFERENCES public.maasserver_node(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY public.maasserver_node_tags
    ADD CONSTRAINT maasserver_node_tags_tag_id_fk_maasserver_tag_id FOREIGN KEY (tag_id) REFERENCES public.maasserver_tag(id) DEFERRABLE INITIALLY DEFERRED;
"""


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0326_foreign_key_cleanup"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bmc",
            name="default_storage_pool",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="maasserver.podstoragepool",
            ),
        ),
        migrations.AlterField(
            model_name="staticroute",
            name="destination",
            field=models.ForeignKey(
                blank=False,
                null=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="maasserver.subnet",
            ),
        ),
        migrations.AlterField(
            model_name="staticroute",
            name="source",
            field=models.ForeignKey(
                blank=False,
                null=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="maasserver.subnet",
            ),
        ),
        migrations.AlterField(
            model_name="virtualmachinedisk",
            name="backing_pool",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="maasserver.podstoragepool",
            ),
        ),
        migrations.AlterField(
            model_name="virtualmachinedisk",
            name="vm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="maasserver.virtualmachine",
            ),
        ),
        migrations.AlterField(
            model_name="virtualmachineinterface",
            name="vm",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="maasserver.virtualmachine",
            ),
        ),
        migrations.AlterField(
            model_name="vlan",
            name="primary_rack",
            field=models.ForeignKey(
                null=True,
                blank=True,
                editable=True,
                related_name="+",
                on_delete=django.db.models.deletion.PROTECT,
                to="maasserver.rackcontroller",
            ),
        ),
        migrations.AlterField(
            model_name="vlan",
            name="secondary_rack",
            field=models.ForeignKey(
                null=True,
                blank=True,
                editable=True,
                related_name="+",
                on_delete=django.db.models.deletion.PROTECT,
                to="maasserver.rackcontroller",
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="boot_interface",
            field=models.ForeignKey(
                default=None,
                blank=True,
                null=True,
                editable=False,
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                to="maasserver.interface",
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="current_config",
            field=models.ForeignKey(
                null=True,
                related_name="+",
                on_delete=django.db.models.deletion.CASCADE,
                to="maasserver.nodeconfig",
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="gateway_link_ipv4",
            field=models.ForeignKey(
                default=None,
                blank=True,
                null=True,
                editable=False,
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                to="maasserver.staticipaddress",
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="gateway_link_ipv6",
            field=models.ForeignKey(
                default=None,
                blank=True,
                null=True,
                editable=False,
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                to="maasserver.staticipaddress",
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="managing_process",
            field=models.ForeignKey(
                null=True,
                editable=False,
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                to="maasserver.regioncontrollerprocess",
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="dns_process",
            field=models.OneToOneField(
                null=True,
                editable=False,
                unique=True,
                related_name="+",
                on_delete=django.db.models.deletion.SET_NULL,
                to="maasserver.regioncontrollerprocess",
            ),
        ),
        migrations.RunSQL(restore_fk_maasserver_dnsresource_ip_addresses),
        migrations.RunSQL(restore_fk_maasserver_forwarddnsserver_domains),
        migrations.RunSQL(restore_fk_maasserver_interface_ip_addresses),
        migrations.RunSQL(restore_fk_maasserver_podhints_nodes),
        migrations.RunSQL(restore_fk_maasserver_node_tags),
    ]