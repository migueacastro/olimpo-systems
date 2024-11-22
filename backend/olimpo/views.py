from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from olimpo.serializers import UserSerializer
from olimpo.models import *
from olimpo.serializers import *

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.filter(activo=True)
    serializer_class = ClienteSerializer



class TecnicoViewSet(viewsets.ModelViewSet):
    queryset = Tecnico.objects.filter(activo=True)
    serializer_class = TecnicoSerializer

class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.filter(activo=True)
    serializer_class = DispositivoSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.filter(activo=True)
    serializer_class = ServicioSerializer


class TipoDispositivoViewSet(viewsets.ModelViewSet):
    queryset = TipoDispositivo.objects.filter(activo=True)
    serializer_class = TipoDispositivoSerializer
