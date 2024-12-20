# Generated by Django 4.2.16 on 2024-12-02 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olimpo', '0006_remove_servicio_falla_reportada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispositivoservicio',
            name='dispositivo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='olimpo.dispositivo'),
        ),
        migrations.AlterField(
            model_name='dispositivoservicio',
            name='servicio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='olimpo.servicio'),
        ),
    ]
