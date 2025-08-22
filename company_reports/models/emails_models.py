from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class User_Prueba(models.Model):
    username=models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=254, unique=True)
    password=models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Usuario: {self.username}"

class UserVerificationCode(models.Model):
    # Tipos de verificación
    VERIFICATION_TYPES = [
        ('account_verification', 'Verificación de cuenta'),
        ('password_recovery', 'Recuperación de contraseña'),
        ('email_change', 'Confirmación de cambio de correo'),
    ]
    
    user = models.ForeignKey(User_Prueba, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    verification_type = models.CharField(
        max_length=30, 
        choices=VERIFICATION_TYPES, 
        default='password_recovery'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Establece la expiración 10 minutos después de la creación
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.username} - {self.get_verification_type_display()} - {self.code}"