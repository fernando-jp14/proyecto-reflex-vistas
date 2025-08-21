from django.contrib import admin
from .models import Appointment, AppointmentStatus, Ticket


@admin.register(AppointmentStatus)
class AppointmentStatusAdmin(admin.ModelAdmin):
    """
    Configuración del admin para AppointmentStatus.
    """
    list_display = ['name', 'description', 'appointments_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['appointments_count', 'created_at', 'updated_at']
    ordering = ['name']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'description')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Información del Sistema', {
            'fields': ('appointments_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Appointment.
    """
    list_display = [
        'id', 'appointment_date', 'appointment_hour', 'appointment_type', 
        'room', 'appointment_status', 'is_completed', 'is_active'
    ]
    list_filter = [
        'appointment_date', 'appointment_status', 'appointment_type', 
        'room', 'is_active', 'created_at'
    ]
    search_fields = [
        'ailments', 'diagnosis', 'observation', 'ticket_number'
    ]
    readonly_fields = ['is_completed', 'is_pending', 'created_at', 'updated_at']
    ordering = ['-appointment_date', '-appointment_hour']
    
    fieldsets = (
        ('Información de la Cita', {
            'fields': ('appointment_date', 'appointment_hour', 'appointment_type', 'room')
        }),
        ('Información Médica', {
            'fields': ('ailments', 'diagnosis', 'surgeries', 'reflexology_diagnostics', 'medications', 'observation')
        }),
        ('Fechas de Tratamiento', {
            'fields': ('initial_date', 'final_date')
        }),
        ('Información de Pago', {
            'fields': ('social_benefit', 'payment_detail', 'payment', 'ticket_number')
        }),
        ('Relaciones', {
            'fields': ('appointment_status',),
            'description': 'TODO: Agregar patient y therapist cuando estén disponibles'
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Información del Sistema', {
            'fields': ('is_completed', 'is_pending', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimiza las consultas con select_related"""
        return super().get_queryset(request).select_related('appointment_status')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Ticket.
    """
    list_display = [
        'ticket_number', 'amount', 'payment_method', 'status', 
        'is_paid', 'payment_date', 'is_active'
    ]
    list_filter = [
        'payment_method', 'status', 'payment_date', 'is_active', 'created_at'
    ]
    search_fields = ['ticket_number', 'description']
    readonly_fields = ['is_paid', 'is_pending', 'payment_date', 'created_at', 'updated_at']
    ordering = ['-payment_date']
    
    fieldsets = (
        ('Información del Ticket', {
            'fields': ('ticket_number', 'amount', 'payment_method', 'description')
        }),
        ('Estado del Pago', {
            'fields': ('status',)
        }),
        ('Relaciones', {
            'fields': (),
            'description': 'TODO: Agregar appointment cuando esté disponible'
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Información del Sistema', {
            'fields': ('is_paid', 'is_pending', 'payment_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_paid', 'mark_as_cancelled']
    
    def mark_as_paid(self, request, queryset):
        """Acción para marcar tickets como pagados"""
        updated = queryset.update(status='paid')
        self.message_user(request, f'{updated} tickets marcados como pagados.')
    mark_as_paid.short_description = "Marcar como pagado"
    
    def mark_as_cancelled(self, request, queryset):
        """Acción para marcar tickets como cancelados"""
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} tickets marcados como cancelados.')
    mark_as_cancelled.short_description = "Marcar como cancelado"
