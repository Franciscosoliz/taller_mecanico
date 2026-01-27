from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions as drf_permissions

from .models import (
    Cliente,
    Vehiculo,
    Mecanico,
    Servicio,
    OrdenReparacion,
    DetalleServicio,
)
from .serializers import (
    ClienteSerializer,
    VehiculoSerializer,
    MecanicoSerializer,
    ServicioSerializer,
    OrdenReparacionSerializer,
    DetalleServicioSerializer,
)
from .permissions import IsAdminOrReadOnly
from . import permissions

class BaseViewSet(viewsets.ModelViewSet):
    """
    Configuración base: paginación, search y ordering ya vienen del settings.py
    """
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = [IsAdminOrReadOnly]


class ClienteViewSet(BaseViewSet):
    queryset = Cliente.objects.all().order_by("id_cliente")
    serializer_class = ClienteSerializer
    search_fields = ["nombre", "telefono", "correo"]


class VehiculoViewSet(BaseViewSet):
    queryset = Vehiculo.objects.select_related("cliente").all().order_by("id_vehiculo")
    serializer_class = VehiculoSerializer
    search_fields = ["placa", "marca", "modelo", "cliente__nombre"]


class MecanicoViewSet(BaseViewSet):
    queryset = Mecanico.objects.all().order_by("id_mecanico")
    serializer_class = MecanicoSerializer
    search_fields = ["nombre", "especialidad", "estado"]


class ServicioViewSet(BaseViewSet):
    queryset = Servicio.objects.all().order_by("id_servicio")
    serializer_class = ServicioSerializer
    search_fields = ["nombre", "descripcion"]

@method_decorator(csrf_exempt, name='dispatch')
class OrdenReparacionViewSet(BaseViewSet):
    queryset = (
        OrdenReparacion.objects
        .select_related("vehiculo", "mecanico")
        .all()
        .order_by("-fecha_ingreso")
    )
    serializer_class = OrdenReparacionSerializer
    search_fields = ["vehiculo__placa", "estado", "mecanico__nombre"]
    
    authentication_classes = [] 
    permission_classes = [drf_permissions.AllowAny] 

    # Agregamos esto para estar 100% seguros de que DRF no pida nada
    def get_permissions(self):
        return [drf_permissions.AllowAny()]


class DetalleServicioViewSet(BaseViewSet):
    queryset = (
        DetalleServicio.objects
        .select_related("orden", "servicio")
        .all()
        .order_by("id_detalle")
    )
    serializer_class = DetalleServicioSerializer
    search_fields = ["orden__id_orden", "servicio__nombre"]

class CustomAuthToken(ObtainAuthToken):
    """
    POST /api/auth/login/
    body: { "username": "admin", "password": "1234" }
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "is_staff": user.is_staff,
        })