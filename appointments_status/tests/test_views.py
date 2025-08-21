from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from decimal import Decimal
from ..models import Appointment, AppointmentStatus, Ticket


class AppointmentStatusViewTest(APITestCase):
    """
    Pruebas para las vistas de AppointmentStatus.
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.status_data = {
            'name': 'Pendiente',
            'description': 'Cita pendiente de confirmación'
        }
        self.status = AppointmentStatus.objects.create(**self.status_data)
    
    def test_list_appointment_statuses(self):
        """Prueba el listado de estados de citas"""
        url = reverse('appointments_status:appointment-status-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Pendiente')
    
    def test_create_appointment_status(self):
        """Prueba la creación de un estado de cita"""
        url = reverse('appointments_status:appointment-status-list')
        data = {
            'name': 'Confirmada',
            'description': 'Cita confirmada'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AppointmentStatus.objects.count(), 2)
        self.assertEqual(response.data['name'], 'Confirmada')
    
    def test_retrieve_appointment_status(self):
        """Prueba la obtención de un estado de cita específico"""
        url = reverse('appointments_status:appointment-status-detail', args=[self.status.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Pendiente')
    
    def test_update_appointment_status(self):
        """Prueba la actualización de un estado de cita"""
        url = reverse('appointments_status:appointment-status-detail', args=[self.status.id])
        data = {
            'name': 'Actualizada',
            'description': 'Descripción actualizada'
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Actualizada')
    
    def test_delete_appointment_status(self):
        """Prueba la eliminación de un estado de cita"""
        url = reverse('appointments_status:appointment-status-detail', args=[self.status.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AppointmentStatus.objects.count(), 0)


class AppointmentViewTest(APITestCase):
    """
    Pruebas para las vistas de Appointment.
    TODO: (Dependencia externa) - Completar cuando estén disponibles los modelos Patient y Therapist
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear un estado de cita para las pruebas
        self.status = AppointmentStatus.objects.create(
            name='Pendiente',
            description='Cita pendiente'
        )
        
        # Datos básicos para crear citas (sin dependencias externas)
        self.appointment_data = {
            'appointment_date': timezone.now().date(),
            'appointment_hour': timezone.now().time(),
            'ailments': 'Dolor de espalda',
            'diagnosis': 'Lumbalgia',
            'appointment_type': 'Consulta',
            'room': 1,
            'payment': Decimal('50.00'),
            'appointment_status': self.status.id
        }
    
    def test_list_appointments(self):
        """Prueba básica del listado de citas"""
        url = reverse('appointments_status:appointment-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_create_appointment_basic(self):
        """Prueba básica de creación de cita (sin dependencias externas)"""
        url = reverse('appointments_status:appointment-list')
        response = self.client.post(url, self.appointment_data, format='json')
        
        # Debería fallar por falta de dependencias externas
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR])


class TicketViewTest(APITestCase):
    """
    Pruebas para las vistas de Ticket.
    TODO: (Dependencia externa) - Completar cuando esté disponible el modelo Appointment
    """
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Datos básicos para crear tickets (sin dependencias externas)
        self.ticket_data = {
            'ticket_number': 'T001',
            'payment_date': timezone.now(),
            'amount': Decimal('50.00'),
            'payment_method': 'Efectivo',
            'description': 'Pago por consulta',
            'status': 'Pendiente'
        }
    
    def test_list_tickets(self):
        """Prueba básica del listado de tickets"""
        url = reverse('appointments_status:ticket-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
    
    def test_create_ticket_basic(self):
        """Prueba básica de creación de ticket (sin dependencias externas)"""
        url = reverse('appointments_status:ticket-list')
        response = self.client.post(url, self.ticket_data, format='json')
        
        # Debería fallar por falta de dependencias externas
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR])
