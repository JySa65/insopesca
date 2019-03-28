# Generated by Django 2.1 on 2019-03-28 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('sanidad', '0003_driver_is_inspection'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantIce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_ice', models.CharField(choices=[('is_iceplant', 'Platas de Hielo'), ('is_refrigeratedcavas', 'Cavas Refrigeradas')], max_length=20)),
                ('name', models.CharField(max_length=500)),
                ('capacity_ton', models.DecimalField(decimal_places=2, max_digits=5)),
                ('capacity_ton_mes', models.DecimalField(decimal_places=2, max_digits=5)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.State')),
            ],
        ),
        migrations.AddField(
            model_name='inspection',
            name='pass_inspection',
            field=models.BooleanField(default=False),
        ),
    ]
