from rest_framework import serializers
from ..models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Appointment.
    Basado en la estructura del módulo Laravel 05_appointments_status.
    """
    
    # Campos calculados
    is_completed = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    
    # Campos de relación (solo lectura por ahora)
    appointment_status_name = serializers.CharField(
        source='appointment_status.name', 
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = Appointment
        fields = [
            'id',
            'appointment_date',
            'appointment_hour',
            'ailments',
            'diagnosis',
            'surgeries',
            'reflexology_diagnostics',
            'medications',
            'observation',
            'initial_date',
            'final_date',
            'appointment_type',
            'room',
            'social_benefit',
            'payment_detail',
            'payment',
            'ticket_number',
            'appointment_status',
            'appointment_status_name',
            'is_completed',
            'is_pending',
            'created_at',
            'updated_at',
            'is_active',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        
        # TODO: (Dependencia externa) - Agregar campos cuando estén disponibles:
        # 'patient', 'patient_name', 'therapist', 'therapist_name', 'payment_type', 'payment_type_name'
    
    def validate_appointment_date(self, value):
        """Validación personalizada para la fecha de la cita"""
        from django.utils import timezone
        today = timezone.now().date()
        
        if value < today:
            raise serializers.ValidationError(
                "La fecha de la cita no puede ser anterior a hoy."
            )
        return value
    
    def validate(self, data):
        """Validación a nivel de objeto"""
        appointment_date = data.get('appointment_date')
        appointment_hour = data.get('appointment_hour')
        
        if appointment_date and appointment_hour:
            # Aquí se podría agregar validación para evitar solapamientos
            # cuando estén disponibles los modelos Patient y Therapist
            pass
        
        return data
