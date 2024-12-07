from django.urls import path, include
from rest_framework import routers # type: ignore
from olimpo.views import *

router = routers.DefaultRouter()
router.register(r'tecnicos', UserViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'tipos_dispositivos', TipoDispositivoViewSet)
router.register(r'dispositivos', DispositivoViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'modelos', ModeloViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('user/', UserProfileView.as_view()),
    path('export/<int:id>/', service_to_pdf),

]