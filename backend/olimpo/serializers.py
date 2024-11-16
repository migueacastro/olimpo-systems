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

class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = ['id', 'cedula', 'nombres', 'apellidos', 'telefono']

class ServicioSerializer(serializers.ModelSerializer):
    tecnico = serializers.SerializerMethodField()
    cliente = serializers.SerializerMethodField()
    class Meta:
        model = Servicio
        fields = ['id','fecha', 'falla_reportada', 'reparacion_efectuada', 'tecnico', 'cliente']
    
    def get_tecnico(self, obj):
        return obj.tecnico.nombres + ' ' + obj.tecnico.apellidos
    
    def get_cliente(self, obj):
        return obj.cliente.nombres + ' ' + obj.cliente.apellidos
    
