# Generated by Django 2.1 on 2019-06-04 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanidad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='type_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sanidad.TypeCompany', verbose_name='Tipo De Compañia'),
        ),
    ]
