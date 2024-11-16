from django.urls import path, include
from rest_framework import routers # type: ignore

from olimpo.views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tecnicos', TecnicoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'servicios', ServicioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]