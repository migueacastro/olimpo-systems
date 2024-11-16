from django.db import models

# Create your models here.
class Cliente(models.Model):
    cedula = models.CharField(max_length=16, unique=True, blank=False, null=False)
    nombres = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=50, blank=False, null=False)
    activo = models.BooleanField(default=True)
    telefono = models.CharField(max_length=25, blank=False, null=False)

    def __unicode__(self):
        return self.nombres + ' ' + self.apellidos

class Tecnico(models.Model):
    cedula = models.CharField(max_length=16, unique=True, blank=False, null=False)
    nombres = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=50, blank=False, null=False)
    activo = models.BooleanField(default=True)
    telefono = models.CharField(max_length=25, blank=False, null=False)

    def __unicode__(self):
        return self.nombres + ' ' + self.apellidos


class Servicio(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.DO_NOTHING)
    activo = models.BooleanField(default=True)
    falla_reportada = models.TextField()
    reparacion_efectuada = models.TextField()

    def __unicode__(self):
        return self.falla_reportada
    