from django.contrib.auth.models import User
from olimpo.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin, NestedUpdateMixin
from rest_framework.validators import UniqueValidator
from django.db.models import Count
import json




class UserRegistrationSerializer(serializers.ModelSerializer):
    # Prepare the type of field for passwords in order to validate them
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8, max_length=100)
    confirmPassword = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=8, max_length=100)
    class Meta:
        model = get_user_model()
        # Fields that will be received
        fields = ['email', 'nombres', 'apellidos', 'cedula', 'telefono', 'password', 'confirmPassword']

    def create(self, validated_data):
        # Create the user
        user_password = validated_data.get('password', None)
        user_instance = self.Meta.model(email = validated_data.get('email'), nombres = validated_data.get('nombres'), apellidos = validated_data.get('apellidos'), cedula = validated_data.get('cedula'), telefono = validated_data.get('telefono'))
        user_instance.set_password(user_password)
        user_instance.save()
        return user_instance
    

class UserLoginSerializer(serializers.ModelSerializer):
    # Prepare the type of field for passwords in order to validate them
    password = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)
    email = serializers.CharField(max_length=100, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)
    confirmPassword = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)
    dispositivos_reparados = serializers.SerializerMethodField(read_only=True)
    rol = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = get_user_model()
        fields = ['id', 'nombres','apellidos','cedula','telefono', 'email','is_superuser', 'dispositivos_reparados', 'password', 'confirmPassword', 'rol']

    def create(self, validated_data):
        # Create the user
        user_password = validated_data.get('password', None)
        user_instance = self.Meta.model(email = validated_data.get('email'), nombres = validated_data.get('nombres'), apellidos = validated_data.get('apellidos'), cedula = validated_data.get('cedula'), telefono = validated_data.get('telefono'))
        user_instance.set_password(user_password)
        user_instance.is_staff = validated_data.get('is_staff', False)
        user_instance.is_superuser = validated_data.get('is_superuser', False)
        user_instance.save()

        return user_instance
    
    def update(self, user_instance, validated_data):
        user_password = validated_data.get('password', None)
        user_instance.set_password(user_password) if user_password else None
        user_instance.email = validated_data.get('email', user_instance.email)
        user_instance.nombres = validated_data.get('nombres', user_instance.nombres)
        user_instance.apellidos = validated_data.get('apellidos', user_instance.apellidos)
        user_instance.cedula = validated_data.get('cedula', user_instance.cedula)
        user_instance.telefono = validated_data.get('telefono', user_instance.telefono)
        user_instance.is_superuser = validated_data.get('is_superuser', user_instance.is_superuser)
        user_instance.save()
        return user_instance
    
    def get_dispositivos_reparados(self, obj):
        return Servicio.objects.filter(tecnico=obj.id).annotate(
            dispositivoservicio_count=Count('dispositivoservicio')
        ).count()

    def get_rol(self, obj):
        return "Administrador" if obj.is_superuser else "Tecnico"

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, style={'input_type': 'password'}, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields=['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id=force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)


class ClienteSerializer(serializers.ModelSerializer):
    servicios = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Cliente
        fields = ['id', 'cedula', 'nombres', 'apellidos', 'telefono', 'servicios']
    
    def create(self, validated_data):
        cliente, created = Cliente.objects.update_or_create(cedula=validated_data['cedula'], defaults=validated_data)
        return cliente
    
    def get_servicios(self, obj):
        return Servicio.objects.filter(cliente=obj.id).all().values()

    
class MarcaSerializer(serializers.ModelSerializer):
    modelos = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Marca
        fields = ['id', 'nombre', 'modelos']

    def get_modelos(self, obj):
        return obj.modelo_set.all().values()


class ModeloSerializer(serializers.ModelSerializer):
    nombre_marca = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Modelo
        fields = ['id', 'marca', 'nombre', 'nombre_marca']

    def get_nombre_marca(self, obj):
        return obj.marca.nombre

class TipoDispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDispositivo
        fields = ['id', 'nombre']


class DispositivoSerializer(WritableNestedModelSerializer):
    marca = serializers.SerializerMethodField(read_only=True)
    modelos_marca = serializers.SerializerMethodField(read_only=True)
    nombre_marca = serializers.SerializerMethodField(read_only=True)
    nombre_modelo = serializers.SerializerMethodField(read_only=True)
    nombre_tipo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Dispositivo
        fields = ['id', 'marca', 'modelo', 'serial', 'imeis', 'tipo', 'modelos_marca', 'nombre_marca', 'nombre_modelo', 'nombre_tipo']

    def get_marca(self, obj):
        return obj.modelo.marca.id
    
    def get_modelos_marca(self, obj):
        return obj.modelo.marca.modelo_set.all().values()

    def get_nombre_marca(self, obj):
        return obj.modelo.marca.nombre

    def get_nombre_modelo(self, obj):
        return obj.modelo.nombre
    
    def get_nombre_tipo(self, obj):
        return obj.tipo.nombre
    

class ReparacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reparacion
        fields = ['id', 'nombre', 'dispositivo', 'activo']
        read_only_fields = ['dispositivo']


class DispositivoServicioSerializer(WritableNestedModelSerializer):
    reparaciones = ReparacionSerializer(many=True, source='reparacion_set', partial=True)
    dispositivo = DispositivoSerializer(partial=True)
    class Meta:
        model = DispositivoServicio
        fields = ['id', 'reparaciones', 'costo', 'status', 'dispositivo']
    
    def __str__(self):
        return self.dispositivo.marca + ' ' + self.dispositivo.modelo
    
    

class ServicioSerializer(WritableNestedModelSerializer):
    costo_total = serializers.SerializerMethodField(read_only=True)
    cliente = ClienteSerializer(partial = True)
    cedula = serializers.SerializerMethodField(read_only=True)
    nombre_tecnico = serializers.SerializerMethodField(read_only=True)
    nombre_cliente = serializers.SerializerMethodField(read_only=True)
    dispositivos = DispositivoServicioSerializer(many=True, source='dispositivoservicio_set', partial=True)
    status = serializers.SerializerMethodField(read_only=True)
    fecha_salida = serializers.DateField(format='%d/%m/%Y')
    fecha_entrega = serializers.DateField(format='%d/%m/%Y')
    class Meta:
        model = Servicio
        fields = ['id','fecha_entrega','fecha_salida', 'nombre_tecnico',  'nombre_cliente', 'cedula', 'dispositivos', 'observaciones', 'costo_total', 'status', 'tecnico', 'cliente']
    
    def get_nombre_tecnico(self, obj):
        return obj.tecnico.nombres + ' ' + obj.tecnico.apellidos
    
    def get_nombre_cliente(self, obj):
        return obj.cliente.nombres + ' ' + obj.cliente.apellidos
    
    def get_cedula(self, obj):
        return obj.cliente.cedula
    
    def get_costo_total(self, obj):
        return str(sum(dispositivo.costo for dispositivo in obj.dispositivoservicio_set.all())) + "$"

    def get_nombre_dispositivo(self, obj):
        return obj.dispositivo.marca + obj.dispositivo.modelo
    
    def get_status(self, obj):
        for dispositivo in obj.dispositivoservicio_set.all():
            if dispositivo.status != 'REPARADO':
                return 'EN REPARACIÓN'
        return 'REPARADO'
    
