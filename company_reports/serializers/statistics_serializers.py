from rest_framework import serializers

class TerapeutaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    terapeuta = serializers.CharField()  # Cambié 'nombre' por 'terapeuta'
    sesiones = serializers.IntegerField()
    ingresos = serializers.FloatField()
    raiting = serializers.FloatField()  # 

class MetricasSerializer(serializers.Serializer):
    ttlpacientes = serializers.IntegerField()
    ttlsesiones = serializers.IntegerField()
    ttlganancias = serializers.FloatField(allow_null=True)

class TiposPacientesSerializer(serializers.Serializer):
    c = serializers.IntegerField()
    cc = serializers.IntegerField()

class StatisticsResource(serializers.Serializer):
    terapeutas = serializers.ListField(
        child=TerapeutaSerializer(), 
        required=False
    )
    tipos_pago = serializers.DictField(
        child=serializers.IntegerField(), 
        required=False
    )
    metricas = MetricasSerializer(required=False)
    ingresos = serializers.DictField(
        child=serializers.FloatField(), 
        required=False
    )
    sesiones = serializers.DictField(
        child=serializers.IntegerField(), 
        required=False
    )
    tipos_pacientes = TiposPacientesSerializer(required=False)