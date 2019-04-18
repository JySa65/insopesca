# Generated by Django 2.1 on 2019-04-18 05:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('type_document', models.CharField(choices=[('V', 'V'), ('E', 'E')], max_length=2, verbose_name='Tipo De Documento')),
                ('document', models.CharField(max_length=15, unique=True, verbose_name='Documento')),
                ('name', models.CharField(max_length=50, verbose_name='Nombres')),
                ('last_name', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('sex', models.CharField(choices=[('is_male', 'Masculino'), ('is_female', 'Femenino')], max_length=15, verbose_name='Sexo')),
                ('tlf', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefono')),
                ('tlf_house', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefono Casa')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('address', models.TextField(verbose_name='Dirección')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('type_document', models.CharField(choices=[('V', 'V'), ('E', 'E'), ('G', 'G'), ('J', 'J'), ('C', 'C'), ('P', 'P')], max_length=2, verbose_name='Tipo De Documento')),
                ('document', models.CharField(max_length=15, unique=True, verbose_name='Documento')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('tlf', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefono')),
                ('tlf_house', models.CharField(blank=True, max_length=15, null=True, verbose_name='Telefono Casa')),
                ('address', models.TextField(verbose_name='Direccion')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_id', models.UUIDField()),
                ('is_active', models.BooleanField(default=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notification_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Parish',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Municipality')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='municipality',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.State'),
        ),
        migrations.AddField(
            model_name='company',
            name='municipality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Municipality', verbose_name='Municipio'),
        ),
        migrations.AddField(
            model_name='company',
            name='parish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Parish', verbose_name='Parroquia'),
        ),
        migrations.AddField(
            model_name='company',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.State', verbose_name='Estado'),
        ),
    ]
