# Generated by Django 2.1 on 2019-02-11 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acuicultura', '0002_auto_20190210_2329'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cardinal_point',
            new_name='CardinalPoint',
        ),
        migrations.RenameModel(
            old_name='Lagoon_tracing',
            new_name='LagoonTracing',
        ),
        migrations.RenameModel(
            old_name='Well_tracing',
            new_name='WellTracing',
        ),
    ]