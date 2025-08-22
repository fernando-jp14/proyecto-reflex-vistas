from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from company_reports.services.statistics_services import StatisticsService
from company_reports.serializers.statistics_serializers import StatisticsResource
from django.shortcuts import render

class GetMetricsView(APIView):
    def get(self, request):
        start = request.query_params.get("start")
        end = request.query_params.get("end")

        if not start or not end:
            return Response(
                {"error": "Parámetros 'start' y 'end' son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar formato de fechas
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            end_date = datetime.strptime(end, '%Y-%m-%d').date()
            
            if start_date > end_date:
                return Response(
                    {"error": "La fecha de inicio no puede ser mayor que la fecha de fin."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except ValueError:
            return Response(
                {"error": "Formato de fecha inválido. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            service = StatisticsService()
            data = service.get_statistics(start_date, end_date)
            
            serializer = StatisticsResource(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Error interno del servidor: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StatisticsViewSet(viewsets.ViewSet):
    @action(detail=False, methods=["get"], url_path="metricas")
    def get_statistics(self, request):
        view = GetMetricsView()
        return view.get(request)
        
def dashboard_view(request):
    return render(request, 'dashboard.html')   