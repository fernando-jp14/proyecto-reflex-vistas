from django.contrib import admin
from company_reports.models.company_models import CompanyData
from company_reports.models.emails_models import User_Prueba, UserVerificationCode
from company_reports.models.reports_statatistics_models import Therapist, Appointment, PaymentType, Patient

admin.site.register(Therapist)
admin.site.register(Appointment)
admin.site.register(PaymentType)
admin.site.register(Patient)

admin.site.register(CompanyData)

admin.site.register(User_Prueba)
admin.site.register(UserVerificationCode)