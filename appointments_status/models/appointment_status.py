from django.db import models


class AppointmentStatus(models.Model):
    """
    Modelo para gestionar los estados de las citas médicas.
    Basado en la estructura del módulo Laravel 05_appointments_status.
    """
    
    name = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Nombre del estado"
    )
    description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción"
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        db_table = 'appointment_statuses'
        verbose_name = "Estado de Cita"
        verbose_name_plural = "Estados de Citas"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def appointments_count(self):
        """Retorna el número de citas con este estado"""
        return self.appointment_set.count()
