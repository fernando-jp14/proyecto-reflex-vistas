from django.core.mail import send_mail
from company_reports.models.emails_models import User_Prueba, UserVerificationCode
import random

class EmailService:
    """
    Servicio para manejar el envío de emails de verificación
    """
    
    @staticmethod
    def send_verification_email(email, type_email='password_recovery'):
        """
        Envía un email de verificación según el tipo especificado
        
        Args:
            email (str): Email del usuario
            type_email (str): Tipo de email ('account_verification', 'password_recovery', 'email_change')
            
        Returns:
            dict: Resultado de la operación
        """
        try:
            # 1. Verificar si el usuario existe
            try:
                user = User_Prueba.objects.get(email=email)
            except User_Prueba.DoesNotExist:
                return {
                    'success': False,
                    'message': 'El usuario no está registrado',
                    'status_code': 404
                }

            # 2. Generar código de 6 dígitos
            codigo_verificacion = str(random.randint(0, 999999)).zfill(6)

            # 3. Crear registro de verificación con expiración
            verification_code = UserVerificationCode.objects.create(
                user=user,
                code=codigo_verificacion,
                verification_type=type_email
            )

            # 4. Obtener contenido del email según el tipo
            subject, message = EmailService._get_email_content(
                type_email, user.username, codigo_verificacion
            )

            # 5. Enviar el correo
            send_mail(
                subject,
                message.strip(),
                None,  # Usa DEFAULT_FROM_EMAIL
                [user.email],
                fail_silently=False,
            )

            return {
                'success': True,
                'message': 'Correo enviado exitosamente',
                'data': {
                    'email': user.email,
                    'username': user.username,
                    'verification_type': type_email,
                    'code': codigo_verificacion,  # Solo para desarrollo
                },
                'status_code': 200
            }

        except Exception as e:
            return {
                'success': False,
                'message': 'Error al enviar el correo',
                'error': str(e),
                'status_code': 500
            }

    @staticmethod
    def verify_code(email, code, type_email='password_recovery'):
        """
        Verifica si el código ingresado es válido
        
        Args:
            email (str): Email del usuario
            code (str): Código de verificación
            type_email (str): Tipo de verificación
            
        Returns:
            dict: Resultado de la verificación
        """
        try:
            # 1. Buscar el usuario
            try:
                user = User_Prueba.objects.get(email=email)
            except User_Prueba.DoesNotExist:
                return {
                    'success': False,
                    'message': 'El usuario no está registrado',
                    'status_code': 404
                }

            # 2. Buscar el código de verificación más reciente
            try:
                verification_code = UserVerificationCode.objects.filter(
                    user=user,
                    code=code,
                    verification_type=type_email
                ).latest('created_at')
            except UserVerificationCode.DoesNotExist:
                return {
                    'success': False,
                    'message': 'Código incorrecto, no existe, o no coincide con el tipo de verificación',
                    'status_code': 400
                }

            # 3. Verificar si el código ha expirado
            if verification_code.is_expired():
                return {
                    'success': False,
                    'message': 'El código ha expirado. Solicita uno nuevo.',
                    'status_code': 400
                }

            # 4. Código válido
            return {
                'success': True,
                'message': 'Código válido',
                'data': {
                    'email': user.email,
                    'username': user.username,
                    'verification_type': verification_code.verification_type
                },
                'status_code': 200
            }

        except Exception as e:
            return {
                'success': False,
                'message': 'Error al verificar el código',
                'error': str(e),
                'status_code': 500
            }

    @staticmethod
    def _get_email_content(verification_type, username, code):
        """
        Retorna el asunto y mensaje del correo según el tipo de verificación
        """
        if verification_type == 'account_verification':
            subject = "Verificación de cuenta - ¡Bienvenido!"
            message = f"""
            ¡Hola {username}!
            
            ¡Bienvenido a nuestra plataforma! Para completar el registro de tu cuenta, necesitamos que verifiques tu correo electrónico.
            
            Tu código de verificación es: **{code}**
            
            Ingresa este código en nuestra plataforma para activar tu cuenta.
            
            ⚠️ Este código expirará en 10 minutos.
            ⚠️ No compartas este código con nadie.
            """
        
        elif verification_type == 'password_recovery':
            subject = "Código de recuperación de contraseña"
            message = f"""
            ¡Hola {username}!
            
            Hemos recibido una solicitud para restablecer la contraseña de tu cuenta.
            
            Tu código de recuperación es: **{code}**
            
            Ingresa este código en nuestra plataforma para restablecer tu contraseña.
            
            ⚠️ Este código expirará en 10 minutos.
            ⚠️ Si no solicitaste este cambio, puedes ignorar este mensaje.
            ⚠️ No compartas este código con nadie.
            """
        
        elif verification_type == 'email_change':
            subject = "Confirmación de cambio de correo electrónico"
            message = f"""
            ¡Hola {username}!
            
            Hemos recibido una solicitud para cambiar el correo electrónico de tu cuenta.
            
            Tu código de confirmación es: **{code}**
            
            Ingresa este código para confirmar el cambio de tu correo electrónico.
            
            ⚠️ Este código expirará en 10 minutos.
            ⚠️ Si no solicitaste este cambio, contacta con nuestro soporte inmediatamente.
            ⚠️ No compartas este código con nadie.
            """
        
        else:
            # Fallback por defecto
            subject = "Código de verificación"
            message = f"""
            ¡Hola {username}!
            
            Tu código de verificación es: **{code}**
            
            ⚠️ Este código expirará en 10 minutos.
            ⚠️ No compartas este código con nadie.
            """
        
        return subject, message