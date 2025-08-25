from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from django.http import FileResponse, Http404
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView

from company_reports.models.company import CompanyData
from company_reports.serialiazers.company_serializers import CompanyDataSerializer, UploadImageRequest
from company_reports.services.companay_services import CompanyService, LogoValidationService


class LogoFileView(APIView):
    """Responsable exclusivamente del manejo de archivos de logos."""
    
    def get_logo_file_response(self, company):
        """Genera la respuesta del archivo de logo."""
        if not company.company_logo:
            raise Http404("La empresa no tiene logo")
        
        # Usar el storage de Django en lugar de os.path
        try:
            return FileResponse(company.company_logo.open('rb'))
        except Exception:
            raise Http404("Archivo de logo no encontrado")
    
    def delete_logo_file(self, company):
        """Elimina el archivo de logo de una empresa."""
        CompanyService.clear_company_logo(company)
        return {"message": "Logo eliminado correctamente"}


class CompanyBusinessView(APIView):
    """Responsable exclusivamente de la lógica de negocio de empresas."""
    
    def preserve_logo_on_update(self, instance, current_logo):
        """Preserva el logo existente si no se envía uno nuevo."""
        if current_logo and not instance.company_logo:
            instance.company_logo = current_logo
            instance.save()
    
    def handle_logo_update(self, instance, request):
        """Maneja la actualización de logos en el update."""
        if 'logo' in request.FILES or 'company_logo' in request.FILES:
            return True  # Indicar que se debe usar el store method
        return False


class CompanyDataViewSet(viewsets.ModelViewSet):
    """API REST pura para empresas. Delega responsabilidades específicas."""
    
    queryset = CompanyData.objects.all()
    serializer_class = CompanyDataSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logo_view = LogoFileView()
        self.business_view = CompanyBusinessView()

    @action(detail=True, methods=['post', 'put'], parser_classes=[MultiPartParser, FormParser])
    def upload_logo(self, request, pk=None):
        """
        POST: Sube un logo solo si la empresa no tiene uno
        PUT: Actualiza el logo existente
        """
        company = self.get_object()
        serializer = UploadImageRequest(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Si es POST y ya tiene logo, no permitir la subida
        if request.method == 'POST' and company.company_logo:
            return Response(
                {"error": "La empresa ya tiene un logo. Use PUT para actualizar."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            CompanyService.process_logo(company, serializer.validated_data['logo'])
            message = "Logo actualizado correctamente" if request.method == 'PUT' else "Logo subido correctamente"
            return Response({"message": message}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def show_logo(self, request, pk=None):
        """Muestra el logo de la empresa."""
        try:
            company = self.get_object()
        except Http404:
            raise Http404("Empresa no encontrada")

        return self.logo_view.get_logo_file_response(company)

    @action(detail=True, methods=['delete'])
    def delete_logo(self, request, pk=None):
        """Elimina el logo de la empresa."""
        company = self.get_object()
        result = self.logo_view.delete_logo_file(company)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser, JSONParser])
    def store(self, request):
        """Crea o actualiza datos de la empresa y procesa el logo si se envía."""
        data = request.data
        file = request.FILES.get('logo') or request.FILES.get('company_logo')
    
        try:
            company = CompanyService.store(data, file)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        if not company:
            return Response({"error": "No se pudo crear/actualizar la empresa"}, 
                    status=status.HTTP_400_BAD_REQUEST)

        serializer = CompanyDataSerializer(company, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def show(self, request, pk=None):
        try:
            company = self.get_object()
            serializer = self.get_serializer(company)
            return Response({
                'status': 'success',
                'data': serializer.data
            })
        except Http404:
            return Response({
                'status': 'error',
                'message': 'Empresa no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    def update(self, request, *args, **kwargs):
        """Actualiza los datos de la empresa, incluyendo el logo si se proporciona"""
        instance = self.get_object()
        data = request.data.copy()  # Hacer una copia para poder modificar
        data['id'] = kwargs.get('pk')  # Añadir el ID para que store sepa que es una actualización
        file = request.FILES.get('logo') or request.FILES.get('company_logo')

        try:
            # Usar CompanyService para manejar la actualización
            company = CompanyService.store(data, file)
            serializer = self.get_serializer(company)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def destroy(self, request, *args, **kwargs):
        """Sobrescribe el método destroy para retornar un mensaje de éxito"""
        try:
            instance = self.get_object()
            company_name = instance.company_name
            self.perform_destroy(instance)
            return Response({
                'status': 'success',
                'message': f'Empresa "{company_name}" eliminada correctamente'
            }, status=status.HTTP_200_OK)
        except Http404:
            return Response({
                'status': 'error',
                'message': 'Empresa no encontrada'
            }, status=status.HTTP_404_NOT_FOUND)

'''
def company_form_view(request):
    """Vista para el formulario de gestión de empresas"""
    return render(request, 'company/company_form.html')
    '''