# Generated by Django 2.1 on 2019-01-27 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_securityquestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSecurityQuestion',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Pregunta')),
                ('answer', models.TextField(verbose_name='Respuesta')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Pregunta De Seguridad',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('ci', models.CharField(max_length=8, verbose_name='Cedula')),
                ('name', models.CharField(max_length=50, verbose_name='Nombres')),
                ('last_name', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('email', models.EmailField(db_index=True, max_length=254, verbose_name='Correo Electronico')),
                ('uuid', models.CharField(blank=True, max_length=50, null=True, verbose_name='Uuid')),
                ('change_pass', models.BooleanField(default=False, verbose_name='Cambio La Contraseña')),
                ('question', models.BooleanField(default=False, verbose_name='Completo Sus Preguntas')),
                ('is_active', models.BooleanField(default=True, verbose_name='Es Activo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Es Staff')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Es Super Usuario')),
                ('is_delete', models.BooleanField(default=False, verbose_name='Eliminado')),
                ('role', models.CharField(blank=True, choices=[('is_coordinator', 'Coordinador'), ('is_worker', 'Trabajador')], max_length=500, null=True, verbose_name='Rol')),
                ('level', models.CharField(blank=True, choices=[('is_ord_pesque', 'Ordenación Pesquera'), ('is_acuicul', 'Acuicultura')], max_length=50, null=True, verbose_name='Level')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Unido Desde')),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical User',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
