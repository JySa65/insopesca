# Generated by Django 2.1 on 2019-04-24 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acuicultura', '0003_lagoontracing_sistem_cultivate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lagoontracing',
            name='sistem_cultivate',
        ),
    ]
