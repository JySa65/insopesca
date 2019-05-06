# Generated by Django 2.1 on 2019-05-04 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicaluser',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Usuario'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-created_at',), 'verbose_name': 'Usuario'},
        ),
    ]