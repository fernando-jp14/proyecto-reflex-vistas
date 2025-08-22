from rest_framework import serializers
from company_reports.models.emails_models import UserVerificationCode

class EmailRequest(serializers.Serializer):
    """
    Serializer para validar el envío de código de verificación por email
    """
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'El campo "email" es requerido',
            'invalid': 'Ingrese un email válido'
        }
    )
    
    type = serializers.ChoiceField(
        choices=UserVerificationCode.VERIFICATION_TYPES,
        default='password_recovery',
        required=False,
        error_messages={
            'invalid_choice': 'Tipo de verificación inválido. Tipos válidos: {available_choices}'
        }
    )

    def validate_email(self, value):
        """
        Validación personalizada para el email (opcional)
        """
        # Aquí puedes agregar validaciones adicionales si las necesitas
        return value.lower().strip()


class VerifyCodeRequest(serializers.Serializer):
    """
    Serializer para validar la verificación de código
    """
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'El campo "email" es requerido',
            'invalid': 'Ingrese un email válido'
        }
    )
    
    code = serializers.CharField(
        max_length=6,
        min_length=6,
        required=True,
        error_messages={
            'required': 'El campo "code" es requerido',
            'max_length': 'El código debe tener exactamente 6 dígitos',
            'min_length': 'El código debe tener exactamente 6 dígitos'
        }
    )
    
    type = serializers.ChoiceField(
        choices=UserVerificationCode.VERIFICATION_TYPES,
        default='password_recovery',
        required=False,
        error_messages={
            'invalid_choice': 'Tipo de verificación inválido. Tipos válidos: {available_choices}'
        }
    )

    def validate_email(self, value):
        """
        Validación personalizada para el email
        """
        return value.lower().strip()
    
    def validate_code(self, value):
        """
        Validación personalizada para el código
        """
        # Solo números permitidos
        if not value.isdigit():
            raise serializers.ValidationError("El código solo debe contener números")
        return value