# Generated by Django 4.2.16 on 2024-12-02 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olimpo', '0008_alter_cliente_cedula'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispositivo',
            name='imeis',
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='imei1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='imei2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
