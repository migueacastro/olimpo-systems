# Generated by Django 4.2.16 on 2024-12-02 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olimpo', '0009_remove_dispositivo_imeis_dispositivo_imei1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispositivo',
            name='imei1',
        ),
        migrations.RemoveField(
            model_name='dispositivo',
            name='imei2',
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='imeis',
            field=models.JSONField(blank=True, null=True),
        ),
    ]