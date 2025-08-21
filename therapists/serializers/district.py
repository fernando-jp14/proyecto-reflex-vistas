from rest_framework import serializers
from therapists.models import District, Province


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer para el modelo District"""
    
    province_name = serializers.CharField(source='province.name', read_only=True)
    region_name = serializers.CharField(source='province.region.name', read_only=True)
    
    class Meta:
        model = District
        fields = ['id', 'name', 'code', 'province', 'province_name', 'region_name']
        read_only_fields = ['id', 'province_name', 'region_name']
    
    def validate_name(self, value):
        """Validar que el nombre no esté vacío"""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del distrito no puede estar vacío")
        return value.strip()
    
    def validate_code(self, value):
        """Validar el código del distrito"""
        if not value or not value.strip():
            raise serializers.ValidationError("El código del distrito no puede estar vacío")
        return value.strip().upper()
    
    def validate_province(self, value):
        """Validar que la provincia exista"""
        if not value:
            raise serializers.ValidationError("Debe seleccionar una provincia")
        return value
