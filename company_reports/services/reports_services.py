from datetime import datetime
from django.utils.timezone import localtime
from django.db.models import Count, Q, Sum
from appointments_status.models.appointment import Appointment
from therapists.models.therapist import Therapist
from django.db import models

class ReportService:
    """Responsable exclusivamente de consultas de base de datos para reportes."""
    
    def get_appointments_count_by_therapist(self, validated_data):
        """Obtiene el conteo de citas por terapeuta para una fecha dada."""
        query_date = validated_data.get("date")
        
        # Consultar terapeutas con la cantidad de citas
        therapists = (
            Therapist.objects
            .annotate(
                appointments_count=Count(
                    "appointment",
                    filter=Q(appointment__appointment_date=query_date)
                )
            )
            .filter(appointments_count__gt=0)
            .values("id", "first_name", "last_name_paternal", "last_name_maternal", "appointments_count")
        )
        
        # Sumar el total de citas
        total_appointments = sum(t["appointments_count"] for t in therapists)
        
        return {
            "therapists_appointments": list(therapists),
            "total_appointments_count": total_appointments
        }
    
    def get_patients_by_therapist(self, validated_data):
        """Obtiene pacientes agrupados por terapeuta para una fecha dada."""
        query_date = validated_data.get("date")
        
        # Consultar citas para la fecha
        appointments = (
            Appointment.objects
            .select_related("patient", "therapist")
            .filter(
                appointment_date=query_date
            )
        )
        
        # Procesar datos
        report = {}
        sin_terapeuta = {
            "therapist_id": "",
            "therapist": "Sin terapeuta asignado",
            "patients": {}
        }
        
        for appointment in appointments:
            patient = appointment.patient
            therapist = appointment.therapist
            
            if not patient:
                continue
            
            patient_data = {
                "patient_id": patient.id,
                "patient": f"{patient.paternal_lastname} {patient.maternal_lastname or ''} {patient.name}".strip(),
                "appointments": 1
            }
            
            if not therapist:
                # Paciente sin terapeuta
                key = patient.id
                if key not in sin_terapeuta["patients"]:
                    sin_terapeuta["patients"][key] = patient_data
                else:
                    sin_terapeuta["patients"][key]["appointments"] += 1
            else:
                # Paciente con terapeuta
                t_id = therapist.id
                if t_id not in report:
                    report[t_id] = {
                        "therapist_id": t_id,
                        "therapist": f"{therapist.last_name_paternal} {therapist.last_name_maternal or ''} {therapist.first_name}".strip(),
                        "patients": {}
                    }
                key = patient.id
                if key not in report[t_id]["patients"]:
                    report[t_id]["patients"][key] = patient_data
                else:
                    report[t_id]["patients"][key]["appointments"] += 1
        
        # Agregar pacientes sin terapeuta si existen
        if sin_terapeuta["patients"]:
            report["sinTherapist"] = sin_terapeuta
        
        # Convertir diccionarios a listas
        for therapist_id in report:
            report[therapist_id]["patients"] = list(report[therapist_id]["patients"].values())
        
        return list(report.values())
    
    def get_daily_cash(self, validated_data):
        """Obtiene el resumen diario de efectivo agrupado por tipo de pago."""
        query_date = validated_data.get("date")
        
        # Consultar pagos del día
        payments = (
            Appointment.objects
            .filter(
                appointment_date=query_date,
                payment__isnull=False,
                payment_type__isnull=False
            )
            .values('payment_type__name')
            .annotate(total_payment=models.Sum('payment'))
        )
        
        # Ordenar según orden requerido
        order = {"Cupón": 0, "EFECTIVO": 1, "Yape": 2}
        pagos_ordenados = []
        otros = []
        
        for p in payments:
            tipo = p['payment_type__name']
            if tipo in order:
                pagos_ordenados.append(p)
            else:
                otros.append(p)
        
        # Ordenar y combinar
        pagos_ordenados.sort(key=lambda x: order[x['payment_type__name']])
        pagos_ordenados.extend(otros)
        
        # Formatear resultado
        result = [
            {
                "payment_type": p['payment_type__name'],
                "total_payment": float(p['total_payment'])
            }
            for p in pagos_ordenados
        ]
        
        return result
    
    def get_appointments_between_dates(self, validated_data):
        """Obtiene citas entre dos fechas dadas."""
        start_date = validated_data.get("start_date")
        end_date = validated_data.get("end_date")
        
        # Consultar citas
        appointments = (
            Appointment.objects
            .select_related("patient", "therapist")
            .filter(
                appointment_date__gte=start_date,
                appointment_date__lte=end_date
            )
            .order_by("appointment_date", "appointment_hour")
        )
        
        # Formatear resultado
        result = []
        for app in appointments:
            therapist_name = "Sin terapeuta asignado"
            if app.therapist:
                therapist_name = " ".join(filter(None, [
                    app.therapist.last_name_paternal,
                    app.therapist.last_name_maternal,
                    app.therapist.first_name
                ]))
            
            patient_name = "Paciente desconocido"
            if app.patient:
                patient_name = " ".join(filter(None, [
                    app.patient.paternal_lastname,
                    app.patient.maternal_lastname,
                    app.patient.name
                ]))
            
            result.append({
                "appointment_id": app.id,
                "appointment_date": app.appointment_date.strftime("%Y-%m-%d"),
                "appointment_hour": app.appointment_hour if isinstance(app.appointment_hour, str) else app.appointment_hour.strftime("%H:%M"),
                "therapist": therapist_name,
                "patient": patient_name,
                "payment": float(app.payment) if app.payment else 0,
                "payment_type": app.payment_type.name if app.payment_type else "No definido"
            })
        
        return result