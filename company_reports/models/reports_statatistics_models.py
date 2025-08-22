from django.db import models

# Tabla Patient
class Patient(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    paternal_lastname = models.CharField(max_length=100, null=True, blank=True)  # Apellido paterno
    maternal_lastname = models.CharField(max_length=100, null=True, blank=True)  # Apellido materno

    def __str__(self):
        return f"{self.paternal_lastname} {self.maternal_lastname} {self.name}".strip()

# Tabla PaymentType
class PaymentType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.name

# Tabla Therapist
class Therapist(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    paternal_lastname = models.CharField(max_length=50, null=True, blank=True)
    maternal_lastname = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.paternal_lastname} {self.maternal_lastname} {self.name}".strip()

# Tabla Appointment

class Appointment(models.Model):
    appointment_date = models.DateField(null=True, blank=True)
    appointment_hour = models.TimeField(null=True, blank=True)
    appointment_type = models.CharField(max_length=255, null=True, blank=True)
    payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    #rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    therapist = models.ForeignKey(Therapist, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')

    def __str__(self):
        patient_name = self.patient.name if self.patient else "No patient"
        return f"Appointment #{self.id} - {patient_name} - {self.appointment_date}"