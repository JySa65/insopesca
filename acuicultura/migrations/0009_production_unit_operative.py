# Generated by Django 2.1 on 2019-01-28 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acuicultura', '0008_auto_20190128_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='production_unit',
            name='operative',
            field=models.BooleanField(default=False, verbose_name='Activa'),
        ),
    ]
