from rest_framework import serializers
from datetime import datetime
from django.utils.timezone import localtime


class DateParameterSerializer(serializers.Serializer):
    """Valida parámetros de fecha para reportes."""
    
    date = serializers.DateField(required=False, input_formats=['%Y-%m-%d'])
    start_date = serializers.DateField(required=False, input_formats=['%Y-%m-%d'])
    end_date = serializers.DateField(required=False, input_formats=['%Y-%m-%d'])
    
    def validate_date(self, value):
        """Valida formato de fecha."""
        if value:
            return value  # Retornar el objeto date, no string
        return localtime().date()
    
    def validate(self, data):
        """Validaciones cruzadas entre fechas."""
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("start_date no puede ser mayor que end_date")
        
        # Asegurar que date tenga un valor por defecto si no se proporciona
        if 'date' not in data:
            data['date'] = localtime().date()
            
        return data


class TherapistAppointmentSerializer(serializers.Serializer):
    """Serializa datos de citas por terapeuta."""
    
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name_paternal = serializers.CharField()
    last_name_maternal = serializers.CharField()
    appointments_count = serializers.IntegerField()
    percentage = serializers.FloatField(required=False)
    
    def to_representation(self, instance):
        """Calcula porcentajes automáticamente."""
        data = super().to_representation(instance)
        if 'percentage' not in data:
            # Calcular porcentaje si no viene
            total = self.context.get('total_appointments', 1)
            data['percentage'] = (data['appointments_count'] / total) * 100 if total > 0 else 0
        return data


class PatientByTherapistSerializer(serializers.Serializer):
    """Serializa datos de pacientes por terapeuta."""
    
    therapist_id = serializers.CharField()
    therapist = serializers.CharField()
    patients = serializers.ListField(child=serializers.DictField())


class DailyCashSerializer(serializers.Serializer):
    """Serializa datos de caja diaria por cita."""
    
    id_cita = serializers.IntegerField()
    payment = serializers.CharField()
    payment_type = serializers.IntegerField()
    payment_type_name = serializers.CharField()
    
    def to_representation(self, instance):
        """Formatea el pago."""
        data = super().to_representation(instance)
        if isinstance(data['payment'], (int, float)):
            data['payment'] = f"{float(data['payment']):.2f}"
        return data


class AppointmentRangeSerializer(serializers.Serializer):
    """Serializa citas entre fechas."""
    
    appointment_id = serializers.IntegerField()
    patient_id = serializers.IntegerField()
    document_number_patient = serializers.CharField()
    patient = serializers.CharField()
    primary_phone_patient = serializers.CharField()
    appointment_date = serializers.DateField(format='%Y-%m-%d')
    appointment_hour = serializers.TimeField(format='%H:%M')


class ReportResponseSerializer(serializers.Serializer):
    """Serializa respuestas de reportes con manejo de errores."""
    
    def to_representation(self, instance):
        """Maneja errores y datos exitosos."""
        if isinstance(instance, dict) and "error" in instance:
            return {"error": instance["error"]}
        return instance


class PDFContextSerializer(serializers.Serializer):
    """Serializa contexto para templates PDF."""
    
    date = serializers.CharField()
    data = serializers.DictField(required=False)
    title = serializers.CharField()
    total = serializers.FloatField(required=False)
    total_appointments = serializers.IntegerField(required=False)
    
    def to_representation(self, instance):
        """Formatea contexto para PDF."""
        data = super().to_representation(instance)
        # Asegurar que date esté en formato string
        if hasattr(data['date'], 'strftime'):
            data['date'] = data['date'].strftime('%Y-%m-%d')
        return data