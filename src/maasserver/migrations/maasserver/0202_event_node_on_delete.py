# Generated by Django 1.11.11 on 2020-02-07 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("maasserver", "0201_merge_20191008_1426")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="node",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="maasserver.Node",
            ),
        )
    ]
