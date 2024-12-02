from django.utils import timezone
from django.utils.translation import gettext as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)
    cedula = models.CharField(max_length=16, unique=True, blank=False, null=False)
    telefono = models.CharField(max_length=25, blank=True, null=False)
    nombres = models.CharField(max_length=50, blank=True, null=False)
    apellidos = models.CharField(max_length=50, blank=True, null=False)
    activo = models.BooleanField(default=True)
    

    # Para mantener propiedades de la clase "AbstractUser"
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cedula', 'telefono', 'nombres', 'apellidos']

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.nombres, self.apellidos)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.nombres
    

class Cliente(models.Model):
    cedula = models.CharField(max_length=16, blank=False, null=False)
    nombres = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=50, blank=True, null=False)
    activo = models.BooleanField(default=True)
    telefono = models.CharField(max_length=25, blank=False, null=False)

    def __unicode__(self):
        return self.nombres + " " + self.apellidos


class TipoDispositivo(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
    
    def __str__(self):
        return self.nombre
    

class Dispositivo(models.Model):
    tipo = models.ForeignKey(
        TipoDispositivo, on_delete=models.DO_NOTHING, related_name="dispositivos"
    )
    marca = models.CharField(max_length=50, blank=True, null=True)
    modelo = models.CharField(max_length=50, blank=True, null=True)
    serial = models.CharField(max_length=50, blank=True, null=True)
    imeis = models.JSONField(null=True, blank=True)
    activo = models.BooleanField(default=True)


class Servicio(models.Model):
    fecha_salida = models.DateField(blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    tecnico = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    activo = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.falla_reportada
    

class DispositivoServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING, blank=True, null=True)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.DO_NOTHING, blank=True, null=True)
    activo = models.BooleanField(default=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('EN REPARACIÓN', 'En reparación'), ('REPARADO', 'Reparado')], blank=False, null=False, default='EN REPARACIÓN')

    def __unicode__(self):
        return self.dispositivo.nombre


class Reparacion(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    dispositivo = models.ForeignKey(DispositivoServicio, on_delete=models.DO_NOTHING)
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
    



