from django.test import TestCase
from ..services import TherapistService
from ..models import Therapist
from datetime import date, time

class TherapistServiceTest(TestCase):
    def setUp(self):
        self.therapist = Therapist.objects.create(
            document_type='DNI',
            document_number='12345678',
            last_name_paternal='García',
            last_name_maternal='López',
            first_name='Juan',
            birth_date=date(1990, 1, 1),
            gender='Masculino',
            phone='123456789',
            email='juan@example.com'
        )

    def test_get_active_therapists(self):
        active_therapists = TherapistService.get_active_therapists()
        self.assertEqual(active_therapists.count(), 1)
        self.assertIn(self.therapist, active_therapists)

    def test_get_inactive_therapists(self):
        self.therapist.is_active = False
        self.therapist.save()
        inactive_therapists = TherapistService.get_inactive_therapists()
        self.assertEqual(inactive_therapists.count(), 1)
        self.assertIn(self.therapist, inactive_therapists)

    def test_soft_delete_therapist(self):
        result = TherapistService.soft_delete_therapist(self.therapist.id)
        self.assertTrue(result)
        self.therapist.refresh_from_db()
        self.assertFalse(self.therapist.is_active)

    def test_restore_therapist(self):
        self.therapist.is_active = False
        self.therapist.save()
        result = TherapistService.restore_therapist(self.therapist.id)
        self.assertTrue(result)
        self.therapist.refresh_from_db()
        self.assertTrue(self.therapist.is_active)