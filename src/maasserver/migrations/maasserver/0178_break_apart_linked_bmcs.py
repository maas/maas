# Generated by Django 1.11.11 on 2018-09-18 12:28

import re

from django.db import migrations
import petname


def get_none_chassis_power_types():
    """Return the power_types that are not chassis."""
    return ["amt", "ipmi", "manual", "openbmc", "webhook", "wedge"]


def generate_bmc_name(existing_names):
    while True:
        name = petname.Generate(2, "-")
        if name not in existing_names:
            existing_names.append(name)
            return name


def break_apart_linked_bmcs(apps, schema_editor):
    BMC = apps.get_model("maasserver", "BMC")
    existing_names = list(BMC.objects.values_list("name", flat=True))
    power_types = get_none_chassis_power_types()
    for bmc in BMC.objects.filter(power_type__in=power_types).prefetch_related(
        "node_set"
    ):
        nodes = list(bmc.node_set.all())
        for node in nodes[1:]:
            bmc.id = None
            bmc._state.adding = True
            bmc.name = generate_bmc_name(existing_names)
            bmc.save()
            node.bmc = bmc
            node.save()


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0177_remove_unique_together_on_bmc")]

    operations = [migrations.RunPython(break_apart_linked_bmcs)]
