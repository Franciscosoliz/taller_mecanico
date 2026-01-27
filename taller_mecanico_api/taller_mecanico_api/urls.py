from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic.base import RedirectView
from django.views.decorators.csrf import csrf_exempt

from taller.views import (
    ClienteViewSet,
    VehiculoViewSet,
    MecanicoViewSet,
    ServicioViewSet,
    OrdenReparacionViewSet,
    DetalleServicioViewSet,
    CustomAuthToken,
)

router = DefaultRouter()
router.register(r"clientes", ClienteViewSet, basename="cliente")
router.register(r"vehiculos", VehiculoViewSet, basename="vehiculo")
router.register(r"mecanicos", MecanicoViewSet, basename="mecanico")
router.register(r"servicios", ServicioViewSet, basename="servicio")
router.register(r"ordenes", OrdenReparacionViewSet, basename="orden")
router.register(r"detalles", DetalleServicioViewSet, basename="detalle")
    
urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/login/", csrf_exempt(CustomAuthToken.as_view()), name="api_login"),
]
