# Generated by Django 2.1 on 2019-05-12 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_backuprestorebd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='level',
            field=models.CharField(blank=True, choices=[('is_acuicul', 'Acuicultura'), ('is_sanid', 'Sanidad')], max_length=50, null=True, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.CharField(blank=True, choices=[('is_acuicul', 'Acuicultura'), ('is_sanid', 'Sanidad')], max_length=50, null=True, verbose_name='Level'),
        ),
    ]
