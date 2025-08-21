from rest_framework import serializers
from ..models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Ticket.
    Basado en la estructura del módulo Laravel 05_appointments_status.
    """
    
    # Campos calculados
    is_paid = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    
    # Campos de relación
    appointment_details = serializers.CharField(
        source='appointment.__str__', 
        read_only=True
    )
    
    class Meta:
        model = Ticket
        fields = [
            'id',
            'appointment',
            'appointment_details',
            'ticket_number',
            'payment_date',
            'amount',
            'payment_method',
            'description',
            'status',
            'is_paid',
            'is_pending',
            'created_at',
            'updated_at',
            'is_active',
        ]
        read_only_fields = ['id', 'payment_date', 'created_at', 'updated_at']
        
        # Campo de relación integrado
    
    def validate_ticket_number(self, value):
        """Validación personalizada para el número de ticket"""
        # Verificar que el número de ticket no esté vacío
        if not value.strip():
            raise serializers.ValidationError(
                "El número de ticket no puede estar vacío."
            )
        
        # Verificar que no exista otro ticket con el mismo número
        instance = self.instance
        if Ticket.objects.filter(ticket_number=value).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError(
                "Ya existe un ticket con este número."
            )
        
        return value.strip()
    
    def validate_amount(self, value):
        """Validación personalizada para el monto"""
        if value <= 0:
            raise serializers.ValidationError(
                "El monto debe ser mayor a cero."
            )
        return value
    
    def validate_payment_method(self, value):
        """Validación personalizada para el método de pago"""
        valid_methods = ['efectivo', 'tarjeta', 'transferencia', 'cheque', 'otro']
        if value.lower() not in valid_methods:
            raise serializers.ValidationError(
                f"Método de pago no válido. Opciones válidas: {', '.join(valid_methods)}"
            )
        return value.lower()
    
    def validate(self, data):
        """Validación a nivel de objeto"""
        status = data.get('status')
        amount = data.get('amount')
        
        # Si el ticket está marcado como pagado, debe tener un monto
        if status == 'paid' and (not amount or amount <= 0):
            raise serializers.ValidationError(
                "Un ticket pagado debe tener un monto válido."
            )
        
        return data
