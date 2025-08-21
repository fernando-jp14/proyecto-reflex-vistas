from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    """
    Modelo para gestionar las citas médicas.
    Basado en la estructura del módulo Laravel 05_appointments_status.
    """
    
    # TODO: (Dependencia externa) - patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    # TODO: (Dependencia externa) - therapist = models.ForeignKey('therapists.Therapist', on_delete=models.CASCADE)
    
    # Campos principales de la cita
    appointment_date = models.DateField(verbose_name="Fecha de la cita")
    appointment_hour = models.TimeField(verbose_name="Hora de la cita")
    
    # Información médica
    ailments = models.TextField(blank=True, null=True, verbose_name="Padecimientos")
    diagnosis = models.TextField(blank=True, null=True, verbose_name="Diagnóstico")
    surgeries = models.TextField(blank=True, null=True, verbose_name="Cirugías")
    reflexology_diagnostics = models.TextField(blank=True, null=True, verbose_name="Diagnósticos de reflexología")
    medications = models.TextField(blank=True, null=True, verbose_name="Medicamentos")
    observation = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    
    # Fechas de tratamiento
    initial_date = models.DateField(blank=True, null=True, verbose_name="Fecha inicial")
    final_date = models.DateField(blank=True, null=True, verbose_name="Fecha final")
    
    # Configuración de la cita
    appointment_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo de cita")
    room = models.CharField(max_length=50, blank=True, null=True, verbose_name="Habitación/Consultorio")
    
    # Información de pago
    social_benefit = models.CharField(max_length=100, blank=True, null=True, verbose_name="Beneficio social")
    payment_detail = models.TextField(blank=True, null=True, verbose_name="Detalle de pago")
    payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Pago")
    ticket_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de ticket")
    
    # Relaciones
    appointment_status = models.ForeignKey(
        'AppointmentStatus', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Estado de la cita"
    )
    
    # TODO: (Dependencia externa) - payment_type = models.ForeignKey('payment_types.PaymentType', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        db_table = 'appointments'
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-appointment_date', '-appointment_hour']
        indexes = [
            models.Index(fields=['appointment_date', 'appointment_hour']),
            models.Index(fields=['appointment_status']),
        ]
    
    def __str__(self):
        return f"Cita {self.id} - {self.appointment_date} {self.appointment_hour}"
    
    @property
    def is_completed(self):
        """Verifica si la cita está completada basándose en la fecha"""
        return self.appointment_date < timezone.now().date()
    
    @property
    def is_pending(self):
        """Verifica si la cita está pendiente"""
        return self.appointment_date >= timezone.now().date()
