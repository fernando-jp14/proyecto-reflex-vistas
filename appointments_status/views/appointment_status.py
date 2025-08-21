from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models import AppointmentStatus
from ..serializers import AppointmentStatusSerializer


class AppointmentStatusViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los estados de citas.
    Basado en la estructura del módulo Laravel 05_appointments_status.
    """
    
    queryset = AppointmentStatus.objects.all()
    serializer_class = AppointmentStatusSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['name']
    
    def get_queryset(self):
        """
        Filtra el queryset según los parámetros de la request.
        """
        queryset = AppointmentStatus.objects.all()
        
        # Filtro por estado activo
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Obtiene solo los estados activos.
        """
        queryset = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activa un estado de cita.
        """
        status_obj = self.get_object()
        status_obj.is_active = True
        status_obj.save()
        serializer = self.get_serializer(status_obj)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """
        Desactiva un estado de cita.
        """
        status_obj = self.get_object()
        status_obj.is_active = False
        status_obj.save()
        serializer = self.get_serializer(status_obj)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def appointments(self, request, pk=None):
        """
        Obtiene las citas asociadas a un estado específico.
        """
        status_obj = self.get_object()
        appointments = status_obj.appointment_set.all()
        
        # TODO: (Dependencia externa) - Usar el serializer de Appointment cuando esté disponible
        from ..serializers import AppointmentSerializer
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
