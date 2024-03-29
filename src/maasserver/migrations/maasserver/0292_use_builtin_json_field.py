# Generated by Django 3.2.12 on 2023-01-18 16:17

from django.db import migrations, models

# See https://bugs.launchpad.net/maas/+bug/2048519
# At the time of 1.x the migrations were applied by South and we were setting default values
# at db level. We have to remove them in order to make the migrations contained in this file.
MIGRATE_DEFAULT_VALUES_QUERIES = (
    "ALTER TABLE maasserver_bootresourcefile ALTER COLUMN extra SET DEFAULT NULL",
    "ALTER TABLE maasserver_bootresource ALTER COLUMN extra SET DEFAULT NULL",
    "ALTER TABLE maasserver_interface ALTER COLUMN ipv4_params SET DEFAULT NULL",
    "ALTER TABLE maasserver_interface ALTER COLUMN ipv6_params SET DEFAULT NULL",
    "ALTER TABLE maasserver_interface ALTER COLUMN params SET DEFAULT NULL",
)


class Migration(migrations.Migration):
    dependencies = [
        ("maasserver", "0291_rdns_hostnames_as_array"),
    ]

    operations = [
        *(
            migrations.RunSQL(query)
            for query in MIGRATE_DEFAULT_VALUES_QUERIES
        ),
        migrations.AlterField(
            model_name="bootresource",
            name="extra",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="bootresourcefile",
            name="extra",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="bootsourcecache",
            name="extra",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="config",
            name="value",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="interface",
            name="ipv4_params",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="interface",
            name="ipv6_params",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="interface",
            name="params",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name="notification",
            name="context",
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
