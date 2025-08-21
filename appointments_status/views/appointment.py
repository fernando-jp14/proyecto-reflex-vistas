from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models import Appointment
from ..serializers import AppointmentSerializer
from django.utils import timezone


# Create your models here.


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar las citas médicas.
    Basado en la estructura del módulo Laravel 05_appointments_status.
    """
    
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'appointment_date', 
        'appointment_status', 
        'appointment_type', 
        'room',
        'is_active'
    ]
    search_fields = [
        'ailments', 
        'diagnosis', 
        'observation', 
        'ticket_number'
    ]
    ordering_fields = [
        'appointment_date', 
        'appointment_hour', 
        'created_at', 
        'updated_at'
    ]
    ordering = ['-appointment_date', '-appointment_hour']
    
    def get_queryset(self):
        """
        Filtra el queryset según los parámetros de la request.
        """
        queryset = Appointment.objects.all()
        
        # Filtros adicionales
        appointment_date = self.request.query_params.get('appointment_date', None)
        if appointment_date:
            queryset = queryset.filter(appointment_date=appointment_date)
        
        # TODO: (Dependencia externa) - Agregar filtros cuando estén disponibles:
        # patient_id = self.request.query_params.get('patient_id', None)
        # therapist_id = self.request.query_params.get('therapist_id', None)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Obtiene las citas completadas.
        """
        queryset = self.get_queryset().filter(
            appointment_date__lt=timezone.now().date()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Obtiene las citas pendientes.
        """
        queryset = self.get_queryset().filter(
            appointment_date__gte=timezone.now().date()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        """
        Obtiene citas dentro de un rango de fechas.
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'Se requieren start_date y end_date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(
            appointment_date__range=[start_date, end_date]
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancela una cita específica.
        """
        appointment = self.get_object()
        # TODO: Implementar lógica de cancelación
        return Response({'message': 'Cita cancelada'})
    
    @action(detail=True, methods=['post'])
    def reschedule(self, request, pk=None):
        """
        Reprograma una cita específica.
        """
        appointment = self.get_object()
        # TODO: Implementar lógica de reprogramación
        return Response({'message': 'Cita reprogramada'})
