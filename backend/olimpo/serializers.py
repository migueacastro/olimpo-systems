from django.contrib.auth.models import User
from olimpo.models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'cedula', 'nombres', 'apellidos', 'telefono']

class TipoDispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDispositivo
        fields = ['id', 'nombre']

class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = ['id', 'cedula', 'nombres', 'apellidos', 'telefono']

class DispositivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispositivo
        fields = ['id', 'marca', 'modelo', 'serial', 'imeis', 'tipo']

class ServicioSerializer(serializers.ModelSerializer):
    nombre_tecnico = serializers.SerializerMethodField()
    nombre_cliente = serializers.SerializerMethodField()
    cedula = serializers.SerializerMethodField()
    nombre_dispositivo = serializers.SerializerMethodField()
    class Meta:
        model = Servicio
        fields = ['id','fecha', 'falla_reportada', 'reparacion_efectuada', 'tecnico', 'cliente', 'cedula', 'dispositivo', 'nombre_tecnico', 'nombre_cliente', 'nombre_dispositivo']
    
    def get_nombre_tecnico(self, obj):
        return obj.tecnico.nombres + ' ' + obj.tecnico.apellidos
    
    def get_nombre_cliente(self, obj):
        return obj.cliente.nombres + ' ' + obj.cliente.apellidos
    
    def get_cedula(self, obj):
        return obj.cliente.cedula
    
    def get_nombre_dispositivo(self, obj):
        return obj.dispositivo.marca + obj.dispositivo.modelo
