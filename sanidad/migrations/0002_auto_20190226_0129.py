# Generated by Django 2.1 on 2019-02-26 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanidad', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='company',
            name='type_company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sanidad.TypeCompany', verbose_name='Tipo De Compañia'),
        ),
        migrations.AlterField(
            model_name='typecompany',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]