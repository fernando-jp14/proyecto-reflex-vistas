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
            return value.strftime('%Y-%m-%d')
        return localtime().date().strftime('%Y-%m-%d')
    
    def validate(self, data):
        """Validaciones cruzadas entre fechas."""
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("start_date no puede ser mayor que end_date")
        return data


class TherapistAppointmentSerializer(serializers.Serializer):
    """Serializa datos de citas por terapeuta."""
    
    id = serializers.IntegerField()
    name = serializers.CharField()
    paternal_lastname = serializers.CharField()
    maternal_lastname = serializers.CharField()
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
    """Serializa datos de caja diaria."""
    
    payment_type = serializers.CharField()
    total_payment = serializers.FloatField()
    
    def to_representation(self, instance):
        """Formatea el total de pago."""
        data = super().to_representation(instance)
        data['total_payment'] = float(data['total_payment'])
        return data


class AppointmentRangeSerializer(serializers.Serializer):
    """Serializa citas entre fechas."""
    
    appointment_id = serializers.IntegerField()
    appointment_date = serializers.DateField(format='%Y-%m-%d')
    appointment_hour = serializers.TimeField(format='%H:%M')
    therapist = serializers.CharField()
    patient = serializers.CharField()
    payment = serializers.FloatField()
    payment_type = serializers.CharField()


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