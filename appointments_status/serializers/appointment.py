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
    
    # Campos de relación
    appointment_status_name = serializers.CharField(
        source='appointment_status.name', 
        read_only=True,
        allow_null=True
    )
    patient_name = serializers.CharField(
        source='patient.get_full_name', 
        read_only=True
    )
    therapist_name = serializers.CharField(
        source='therapist.get_full_name', 
        read_only=True
    )
    payment_type_name = serializers.CharField(
        source='payment_type.name', 
        read_only=True,
        allow_null=True
    )
    
    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient',
            'patient_name',
            'therapist',
            'therapist_name',
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
            'payment_type',
            'payment_type_name',
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
        
        # Campos de relación integrados
    
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
