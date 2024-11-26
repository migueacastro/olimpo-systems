# Generated by Django 5.1.3 on 2024-11-18 01:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olimpo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispositivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('CELULAR', 'Celular'), ('COMPUTADORA', 'Computadora'), ('LAPTOP', 'Laptop')], max_length=50)),
                ('marca', models.CharField(blank=True, max_length=50, null=True)),
                ('modelo', models.CharField(blank=True, max_length=50, null=True)),
                ('serial', models.CharField(blank=True, max_length=50, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='servicio',
            name='dispositivo',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='olimpo.dispositivo'),
        ),
        migrations.CreateModel(
            name='Imei',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
                ('dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='olimpo.dispositivo')),
            ],
        ),
    ]
