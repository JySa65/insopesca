# Generated by Django 2.1 on 2019-03-23 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanidad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='is_inspection',
            field=models.BooleanField(default=False),
        ),
    ]
