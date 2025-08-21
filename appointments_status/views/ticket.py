from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from ..models import Ticket
from ..serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar los tickets.
    Basado en la estructura del módulo Laravel 05_appointments_status.
    """
    
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        'ticket_number', 
        'payment_method', 
        'status', 
        'is_active'
    ]
    search_fields = [
        'ticket_number', 
        'description'
    ]
    ordering_fields = [
        'payment_date', 
        'amount', 
        'created_at', 
        'updated_at'
    ]
    ordering = ['-payment_date']
    
    def get_queryset(self):
        """
        Filtra el queryset según los parámetros de la request.
        """
        queryset = Ticket.objects.all()
        
        # Filtros adicionales
        payment_date = self.request.query_params.get('payment_date', None)
        if payment_date:
            queryset = queryset.filter(payment_date__date=payment_date)
        
        # TODO: (Dependencia externa) - Agregar filtros cuando estén disponibles:
        # appointment_id = self.request.query_params.get('appointment_id', None)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def paid(self, request):
        """
        Obtiene los tickets pagados.
        """
        queryset = self.get_queryset().filter(status='paid')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Obtiene los tickets pendientes.
        """
        queryset = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def cancelled(self, request):
        """
        Obtiene los tickets cancelados.
        """
        queryset = self.get_queryset().filter(status='cancelled')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """
        Marca un ticket como pagado.
        """
        ticket = self.get_object()
        ticket.mark_as_paid()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_cancelled(self, request, pk=None):
        """
        Marca un ticket como cancelado.
        """
        ticket = self.get_object()
        ticket.mark_as_cancelled()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_payment_method(self, request):
        """
        Obtiene tickets agrupados por método de pago.
        """
        payment_method = request.query_params.get('payment_method')
        if not payment_method:
            return Response(
                {'error': 'Se requiere payment_method'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset().filter(payment_method=payment_method)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Obtiene estadísticas de tickets.
        """
        total_tickets = Ticket.objects.count()
        paid_tickets = Ticket.objects.filter(status='paid').count()
        pending_tickets = Ticket.objects.filter(status='pending').count()
        cancelled_tickets = Ticket.objects.filter(status='cancelled').count()
        
        # TODO: (Dependencia externa) - Agregar cálculos de montos cuando esté disponible
        # total_amount = Ticket.objects.filter(status='paid').aggregate(Sum('amount'))
        
        stats = {
            'total_tickets': total_tickets,
            'paid_tickets': paid_tickets,
            'pending_tickets': pending_tickets,
            'cancelled_tickets': cancelled_tickets,
            'paid_percentage': (paid_tickets / total_tickets * 100) if total_tickets > 0 else 0,
        }
        
        return Response(stats)
