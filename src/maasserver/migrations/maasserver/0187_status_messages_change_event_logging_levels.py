# Generated by Django 1.11.11 on 2019-04-16 16:24

from logging import DEBUG

from django.db import migrations

CHANGED_EVENTS_INFO_TO_DEBUG = [
    "NODE_POWERED_ON",
    "NODE_POWERED_OFF",
    "NODE_POWER_QUERIED",
    "NODE_PXE_REQUEST",
    "NODE_INSTALLATION_FINISHED",
    "NODE_CHANGED_STATUS",
    "REQUEST_NODE_START_COMMISSIONING",
    "REQUEST_NODE_ABORT_COMMISSIONING",
    "REQUEST_NODE_START_TESTING",
    "REQUEST_NODE_ABORT_TESTING",
    "REQUEST_NODE_OVERRIDE_FAILED_TESTING",
    "REQUEST_NODE_ABORT_DEPLOYMENT",
    "REQUEST_NODE_ACQUIRE",
    "REQUEST_NODE_ERASE_DISK",
    "REQUEST_NODE_ABORT_ERASE_DISK",
    "REQUEST_NODE_RELEASE",
    "REQUEST_NODE_MARK_FAILED",
    "REQUEST_NODE_MARK_BROKEN",
    "REQUEST_NODE_MARK_FIXED",
    "REQUEST_NODE_LOCK",
    "REQUEST_NODE_UNLOCK",
    "REQUEST_NODE_START_DEPLOYMENT",
    "REQUEST_NODE_START",
    "REQUEST_NODE_STOP",
    "REQUEST_NODE_START_RESCUE_MODE",
    "REQUEST_NODE_STOP_RESCUE_MODE",
    "REQUEST_CONTROLLER_REFRESH",
    "REQUEST_RACK_CONTROLLER_ADD_CHASSIS",
    "RACK_IMPORT_INFO",
    "REGION_IMPORT_INFO",
]


def change_event_levels_from_info_to_debug(apps, schema_editor):
    EventType = apps.get_model("maasserver", "EventType")
    for event_type in EventType.objects.filter(
        name__in=CHANGED_EVENTS_INFO_TO_DEBUG
    ):
        event_type.level = DEBUG
        event_type.save()


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0186_node_description")]

    operations = [migrations.RunPython(change_event_levels_from_info_to_debug)]
