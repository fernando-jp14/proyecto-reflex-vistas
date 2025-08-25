from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TherapistViewSet,
    RegionViewSet,
    ProvinceViewSet,
    DistrictViewSet,
    index
)

router = DefaultRouter()
router.register(r'therapists', TherapistViewSet, basename='therapist')
router.register(r"regions", RegionViewSet, basename="region")
router.register(r"provinces", ProvinceViewSet, basename="province")
router.register(r"districts", DistrictViewSet, basename="district")

urlpatterns = [
    path('', index, name='therapists_index'),  # Página principal en /
    path('', include(router.urls)),  # APIs disponibles en la raíz
]