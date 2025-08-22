from rest_framework import serializers
from therapists.models import Region


class RegionSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Region"""
    
    class Meta:
        model = Region
        fields = ['id', 'name', 'ubigeo_code']
        read_only_fields = ['id']
    
    def validate_name(self, value):
        """Validar que el nombre no esté vacío"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre de la región no puede estar vacío")
        return value.strip()
    
    def validate_ubigeo_code(self, value):
        """Validar el código de la región"""
        if not value or not value.strip():
            raise serializers.ValidationError("El código de la región no puede estar vacío")
        return value.strip().upper()
