# Generated by Django 4.2.16 on 2024-12-02 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olimpo', '0007_alter_dispositivoservicio_dispositivo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cedula',
            field=models.CharField(max_length=16),
        ),
    ]
