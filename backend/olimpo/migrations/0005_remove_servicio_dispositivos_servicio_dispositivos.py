# Generated by Django 4.2.16 on 2024-11-22 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olimpo', '0004_remove_servicio_dispositivo_remove_servicio_fecha_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicio',
            name='dispositivos',
        ),
        migrations.AddField(
            model_name='servicio',
            name='dispositivos',
            field=models.ManyToManyField(blank=True, null=True, to='olimpo.dispositivo'),
        ),
    ]
