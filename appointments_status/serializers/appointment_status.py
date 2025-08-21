from rest_framework import serializers
from ..models import AppointmentStatus


class AppointmentStatusSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo AppointmentStatus.
    Basado en la estructura del módulo Laravel 05_appointments_status.
    """
    
    # Campo calculado
    appointments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = AppointmentStatus
        fields = [
            'id',
            'name',
            'description',
            'appointments_count',
            'created_at',
            'updated_at',
            'is_active',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'appointments_count']
    
    def validate_name(self, value):
        """Validación personalizada para el nombre del estado"""
        # Verificar que el nombre no esté vacío
        if not value.strip():
            raise serializers.ValidationError(
                "El nombre del estado no puede estar vacío."
            )
        
        # Verificar que no exista otro estado con el mismo nombre
        instance = self.instance
        if AppointmentStatus.objects.filter(name=value).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError(
                "Ya existe un estado de cita con este nombre."
            )
        
        return value.strip()
    
    def validate(self, data):
        """Validación a nivel de objeto"""
        name = data.get('name', '')
        description = data.get('description', '')
        
        # Si no hay descripción, usar el nombre como descripción
        if not description and name:
            data['description'] = name
        
        return data
