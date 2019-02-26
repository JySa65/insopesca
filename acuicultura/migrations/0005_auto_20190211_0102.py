# Generated by Django 2.1 on 2019-02-11 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acuicultura', '0004_auto_20190211_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specie',
            name='ordinary_name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre Ordinario'),
        ),
        migrations.AlterField(
            model_name='specie',
            name='scientific_name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre Cientifico'),
        ),
    ]