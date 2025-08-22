from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from company_reports.serializers.emails_serializers import EmailRequest, VerifyCodeRequest
from company_reports.services.emails_services import EmailService
from django.shortcuts import render

class EmailController(APIView):
    """
    Controlador para manejar las operaciones relacionadas con emails de verificación
    """
    
    def send_verify_code(self, request):
        """
        Envía un código de verificación por email
        """
        # 1. Validar los datos de entrada usando el serializer
        serializer = EmailRequest(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'message': 'Datos de entrada inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # 2. Extraer datos validados
        validated_data = serializer.validated_data
        email = validated_data.get('email')
        type_email = validated_data.get('type', 'password_recovery')

        # 3. Usar el servicio para enviar el email
        result = EmailService.send_verification_email(email, type_email)

        # 4. Retornar respuesta según el resultado del servicio
        if result['success']:
            return Response({
                'message': result['message'],
                'email': result['data']['email'],
                'username': result['data']['username'],
                'verification_type': result['data']['verification_type'],
                'code': result['data']['code'],  # Solo para desarrollo
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': result['message'],
                'error': result.get('error', '')
            }, status=result['status_code'])

    def verify_code(self, request):
        """
        Verifica un código de verificación
        """
        # 1. Validar los datos de entrada usando el serializer
        serializer = VerifyCodeRequest(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'message': 'Datos de entrada inválidos',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # 2. Extraer datos validados
        validated_data = serializer.validated_data
        email = validated_data.get('email')
        code = validated_data.get('code')
        type_email = validated_data.get('type', 'password_recovery')

        # 3. Usar el servicio para verificar el código
        result = EmailService.verify_code(email, code, type_email)

        # 4. Retornar respuesta según el resultado del servicio
        if result['success']:
            return Response({
                'message': result['message'],
                'email': result['data']['email'],
                'username': result['data']['username'],
                'verification_type': result['data']['verification_type']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': result['message'],
                'error': result.get('error', '')
            }, status=result['status_code'])


# Crear instancias de las vistas para usar en urls.py
class SendVerifyCodeAPIView(APIView):
    """
    Vista para enviar código de verificación - Compatible con la estructura actual
    """
    def post(self, request):
        controller = EmailController()
        return controller.send_verify_code(request)


class VerifyCodeAPIView(APIView):
    """
    Vista para verificar código - Compatible con la estructura actual
    """
    def post(self, request):
        controller = EmailController()
        return controller.verify_code(request)

def dashboard_email(request):
    return render(request, 'dashboard_email.html')