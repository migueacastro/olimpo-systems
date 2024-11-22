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


class TipoDispositivo(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
    

class Dispositivo(models.Model):
    tipo = models.ForeignKey(TipoDispositivo, on_delete=models.DO_NOTHING, related_name='dispositivos')
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    serial = models.CharField(max_length=50, blank=True, null=True)
    imeis = models.JSONField(null=True, blank=True)
    activo = models.BooleanField(default=True)




class Servicio(models.Model):
    fecha = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.DO_NOTHING)
    activo = models.BooleanField(default=True)
    falla_reportada = models.TextField()
    reparacion_efectuada = models.TextField()
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.DO_NOTHING, default=None, null=True)

    def __unicode__(self):
        return self.falla_reportada
    