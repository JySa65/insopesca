# Generated by Django 2.1 on 2019-01-20 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acuicultura', '0003_tracing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Well_tracing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tracing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acuicultura.Tracing')),
                ('well', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acuicultura.Well')),
            ],
        ),
    ]
