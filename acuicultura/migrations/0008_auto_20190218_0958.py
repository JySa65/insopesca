# Generated by Django 2.1 on 2019-02-18 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acuicultura', '0007_auto_20190211_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lagoon',
            name='total_area_mirror_guater',
            field=models.IntegerField(blank=True, null=True, verbose_name='Area total de Terreno'),
        ),
    ]