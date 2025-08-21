from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from ..models import Appointment, AppointmentStatus, Ticket


class AppointmentStatusModelTest(TestCase):
    """
    Pruebas para el modelo AppointmentStatus.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.status_data = {
            'name': 'Pendiente',
            'description': 'Cita pendiente de confirmación'
        }
    
    def test_create_appointment_status(self):
        """Prueba la creación de un estado de cita"""
        status = AppointmentStatus.objects.create(**self.status_data)
        
        self.assertEqual(status.name, 'Pendiente')
        self.assertEqual(status.description, 'Cita pendiente de confirmación')
        self.assertTrue(status.is_active)
        self.assertIsNotNone(status.created_at)
        self.assertIsNotNone(status.updated_at)
    
    def test_appointment_status_str(self):
        """Prueba el método __str__ del modelo"""
        status = AppointmentStatus.objects.create(**self.status_data)
        self.assertEqual(str(status), 'Pendiente')
    
    def test_appointment_status_unique_name(self):
        """Prueba que el nombre sea único"""
        AppointmentStatus.objects.create(**self.status_data)
        
        with self.assertRaises(Exception):
            AppointmentStatus.objects.create(**self.status_data)
    
    def test_appointments_count_property(self):
        """Prueba la propiedad appointments_count"""
        status = AppointmentStatus.objects.create(**self.status_data)
        self.assertEqual(status.appointments_count, 0)


class AppointmentModelTest(TestCase):
    """
    Pruebas para el modelo Appointment.
    TODO: (Dependencia externa) - Completar cuando estén disponibles los modelos Patient y Therapist
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.status = AppointmentStatus.objects.create(
            name='Confirmada',
            description='Cita confirmada'
        )
        self.appointment_data = {
            'appointment_date': timezone.now().date() + timezone.timedelta(days=1),
            'appointment_hour': timezone.now().time(),
            'appointment_type': 'Consulta',
            'room': 'Sala 1',
            'appointment_status': self.status
        }
    
    def test_create_appointment_basic(self):
        """Prueba básica de creación de cita (sin dependencias externas)"""
        appointment = Appointment.objects.create(**self.appointment_data)
        
        self.assertEqual(appointment.appointment_type, 'Consulta')
        self.assertEqual(appointment.room, 'Sala 1')
        self.assertEqual(appointment.appointment_status, self.status)
        self.assertTrue(appointment.is_active)
    
    def test_appointment_str(self):
        """Prueba el método __str__ del modelo"""
        appointment = Appointment.objects.create(**self.appointment_data)
        expected_str = f"Cita {appointment.id} - {appointment.appointment_date} {appointment.appointment_hour}"
        self.assertEqual(str(appointment), expected_str)
    
    def test_appointment_properties(self):
        """Prueba las propiedades is_completed e is_pending"""
        # Cita futura
        future_appointment = Appointment.objects.create(**self.appointment_data)
        self.assertFalse(future_appointment.is_completed)
        self.assertTrue(future_appointment.is_pending)
        
        # Cita pasada
        past_data = self.appointment_data.copy()
        past_data['appointment_date'] = timezone.now().date() - timezone.timedelta(days=1)
        past_appointment = Appointment.objects.create(**past_data)
        self.assertTrue(past_appointment.is_completed)
        self.assertFalse(past_appointment.is_pending)


class TicketModelTest(TestCase):
    """
    Pruebas para el modelo Ticket.
    TODO: (Dependencia externa) - Completar cuando esté disponible el modelo Appointment
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.ticket_data = {
            'ticket_number': 'TICKET-001',
            'amount': Decimal('100.00'),
            'payment_method': 'efectivo',
            'description': 'Pago por consulta'
        }
    
    def test_create_ticket_basic(self):
        """Prueba básica de creación de ticket (sin dependencias externas)"""
        ticket = Ticket.objects.create(**self.ticket_data)
        
        self.assertEqual(ticket.ticket_number, 'TICKET-001')
        self.assertEqual(ticket.amount, Decimal('100.00'))
        self.assertEqual(ticket.payment_method, 'efectivo')
        self.assertEqual(ticket.status, 'pending')
        self.assertTrue(ticket.is_active)
    
    def test_ticket_str(self):
        """Prueba el método __str__ del modelo"""
        ticket = Ticket.objects.create(**self.ticket_data)
        expected_str = f"Ticket {ticket.ticket_number} - ${ticket.amount}"
        self.assertEqual(str(ticket), expected_str)
    
    def test_ticket_properties(self):
        """Prueba las propiedades is_paid e is_pending"""
        ticket = Ticket.objects.create(**self.ticket_data)
        
        # Por defecto es pendiente
        self.assertFalse(ticket.is_paid)
        self.assertTrue(ticket.is_pending)
        
        # Marcar como pagado
        ticket.mark_as_paid()
        self.assertTrue(ticket.is_paid)
        self.assertFalse(ticket.is_pending)
    
    def test_ticket_unique_number(self):
        """Prueba que el número de ticket sea único"""
        Ticket.objects.create(**self.ticket_data)
        
        duplicate_data = self.ticket_data.copy()
        duplicate_data['amount'] = Decimal('200.00')
        
        with self.assertRaises(Exception):
            Ticket.objects.create(**duplicate_data)
    
    def test_ticket_status_transitions(self):
        """Prueba las transiciones de estado del ticket"""
        ticket = Ticket.objects.create(**self.ticket_data)
        
        # Marcar como pagado
        ticket.mark_as_paid()
        self.assertEqual(ticket.status, 'paid')
        
        # Marcar como cancelado
        ticket.mark_as_cancelled()
        self.assertEqual(ticket.status, 'cancelled')
