# Generated by Django 4.2.16 on 2024-12-05 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('olimpo', '0011_alter_dispositivo_tipo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='dispositivo',
            name='marca',
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olimpo.marca')),
            ],
        ),
        migrations.AlterField(
            model_name='dispositivo',
            name='modelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='olimpo.modelo'),
        ),
    ]
