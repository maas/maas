# Generated by Django 3.2.12 on 2022-11-15 15:12

from collections import defaultdict
from datetime import datetime

from django.db import migrations


def move_secrets(apps, schema_editor):
    BMC = apps.get_model("maasserver", "BMC")
    Secret = apps.get_model("maasserver", "Secret")

    now = datetime.utcnow()

    bmc_secrets = {}

    power_driver_secrets = defaultdict(
        set,
        {
            "amt": {"power_pass"},
            "dli": {"power_pass"},
            "hmc": {"power_pass"},
            "hmcz": {"power_pass"},
            "ipmi": {"power_pass": "k_g"},
            "moonshot": {"power_pass"},
            "mscm": {"power_pass"},
            "msftocs": {"power_pass"},
            "nova": {"os_password"},
            "openbmc": {"power_pass"},
            "proxmox": {"power_pass": "power_token_secret"},
            "recs_box": {"power_pass"},
            "redfish": {"power_pass"},
            "sm15k": {"power_pass"},
            "ucsm": {"power_pass"},
            "vmware": {"power_pass"},
            "webhook": {"power_pass": "power_token"},
            "wedge": {"power_pass"},
            "lxd": {"password": "key"},
            "virsh": {"power_pass"},
        },
    )

    for bmc_id, power_type, power_parameters in BMC.objects.values_list(
        "id", "power_type", "power_parameters"
    ):
        # LP:2002109 - Manual power driver has empty power parameters
        if not power_parameters:
            continue
        secrets = {}
        parameters = {}
        for name, value in power_parameters.items():
            if name in power_driver_secrets[power_type]:
                secrets[name] = value
            else:
                parameters[name] = value

        bmc_secrets[bmc_id] = secrets
        BMC.objects.filter(id=bmc_id).update(power_parameters=parameters)

    Secret.objects.bulk_create(
        Secret(
            path=f"bmc/{bmc_id}/power-parameters",
            value=secret,
            created=now,
            updated=now,
        )
        for bmc_id, secret in bmc_secrets.items()
    )


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0289_vault_secret"),
    ]

    operations = [migrations.RunPython(move_secrets)]
