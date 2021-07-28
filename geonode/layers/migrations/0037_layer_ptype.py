# Generated by Django 3.2.4 on 2021-07-20 17:09

from django.db import migrations, models
from geonode.services.enumerations import GXP_PTYPES


def update_remotes_attributes(apps, schema_editor):
    """Updating Remote Services related attributes

     - For the time being we need to iterate over the layers since the remote service properties
       are built at runtime and therefore we cannot benefit of an optimized Subquery.
    """
    MyModel = apps.get_model('layers', 'Layer')
    FkModel = apps.get_model('services', 'Service')

    for _m in MyModel.objects.filter(models.Q(remote_service__isnull=False)):
        service = FkModel.objects.get(pk=_m.remote_service)
        MyModel.objects.filter(pk=_m).update(
            sourcetype='REMOTE',
            remote_typename=service.name,
            ptype=GXP_PTYPES.get(service.type, None))


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0036_remove_layer_storetype'),
        ('base', '0070_auto_20210720_1709')
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='ptype',
            field=models.CharField(default='gxp_wmscsource', max_length=80, verbose_name='P-Type'),
        ),
        migrations.RunPython(update_remotes_attributes, migrations.RunPython.noop)
    ]