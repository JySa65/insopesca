# Generated by Django 2.1 on 2019-02-12 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanidad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountHasCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='company',
        ),
        migrations.RemoveField(
            model_name='account',
            name='is_delete',
        ),
        migrations.AddField(
            model_name='accounthascompany',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sanidad.Account'),
        ),
        migrations.AddField(
            model_name='accounthascompany',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sanidad.Company'),
        ),
        migrations.AddField(
            model_name='company',
            name='account',
            field=models.ManyToManyField(through='sanidad.AccountHasCompany', to='sanidad.Account'),
        ),
    ]
