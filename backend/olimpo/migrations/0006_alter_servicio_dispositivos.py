# Generated by Django 4.2.16 on 2024-11-22 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olimpo', '0005_remove_servicio_dispositivos_servicio_dispositivos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='dispositivos',
            field=models.ManyToManyField(to='olimpo.dispositivo'),
        ),
    ]
