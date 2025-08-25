from django.http import JsonResponse, HttpResponse
from company_reports.services.reports_services import ReportService
from company_reports.serialiazers.reports_serializers import (DateParameterSerializer, TherapistAppointmentSerializer, PatientByTherapistSerializer, DailyCashSerializer, AppointmentRangeSerializer, PDFContextSerializer)
from django.shortcuts import render
from django_xhtml2pdf.utils import pdf_decorator
import xlsxwriter
import io
from datetime import datetime
from django.utils.timezone import localtime

report_service = ReportService()

class ReportAPIView:
    """Responsable exclusivamente de endpoints JSON de reportes."""
    
    @staticmethod
    def get_number_appointments_per_therapist(request):
        """Devuelve JSON con el número de citas por terapeuta para una fecha dada."""
        # Validar parámetros
        serializer = DateParameterSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        # Obtener datos usando parámetros validados
        data = report_service.get_appointments_count_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)
        
        # Serializar respuesta
        response_serializer = TherapistAppointmentSerializer(
            data['therapists_appointments'], 
            many=True,
            context={'total_appointments': data['total_appointments_count']}
        )
        
        return JsonResponse({
            'therapists_appointments': response_serializer.data,
            'total_appointments_count': data['total_appointments_count']
        })
    
    @staticmethod
    def get_patients_by_therapist(request):
        """Devuelve JSON con los pacientes agrupados por terapeuta para una fecha dada."""
        # Validar parámetros
        serializer = DateParameterSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        # Obtener datos
        data = report_service.get_patients_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)
        
        # Serializar respuesta
        response_serializer = PatientByTherapistSerializer(data, many=True)
        return JsonResponse(response_serializer.data, safe=False)
    
    @staticmethod
    def get_daily_cash(request):
        """Devuelve JSON con el resumen diario de efectivo agrupado por tipo de pago."""
        # Validar parámetros
        serializer = DateParameterSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        # Obtener datos
        data = report_service.get_daily_cash(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)
        
        # Serializar respuesta
        response_serializer = DailyCashSerializer(data, many=True)
        return JsonResponse(response_serializer.data, safe=False)
    
    @staticmethod
    def get_appointments_between_dates(request):
        """Devuelve JSON con todas las citas entre dos fechas con info de paciente y terapeuta."""
        # Validar parámetros
        serializer = DateParameterSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        # Obtener datos
        data = report_service.get_appointments_between_dates(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)
        
        # Serializar respuesta
        response_serializer = AppointmentRangeSerializer(data, many=True)
        return JsonResponse(response_serializer.data, safe=False)


class PDFExportView:
    """Responsable exclusivamente de la generación de PDFs."""
    
    @staticmethod
    @pdf_decorator(pdfname='citas_terapeuta.pdf')
    def pdf_citas_terapeuta(request):
        # Validar parámetros
        serializer = DateParameterSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        # Obtener datos
        data = report_service.get_appointments_count_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)
        
        # Preparar contexto usando serializer
        context_data = {
            'date': serializer.validated_data.get('date'),
            'data': data,
            'title': 'Citas por Terapeuta'
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        
        return render(request, 'pdf_templates/citas_terapeuta.html', context)
    
    @staticmethod
    @pdf_decorator(pdfname='pacientes_por_terapeuta.pdf')
    def pdf_pacientes_terapeuta(request):
        # Validar parámetros
        serializer = DateParameterSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        # Obtener datos
        data = report_service.get_patients_by_therapist(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)
        
        # Preparar contexto usando serializer
        context_data = {
            'date': serializer.validated_data.get('date'),
            'data': data,
            'title': 'Pacientes por Terapeuta'
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        
        return render(request, 'pdf_templates/pacientes_terapeuta.html', context)
    
    @staticmethod
    @pdf_decorator(pdfname='resumen_caja.pdf')
    def pdf_resumen_caja(request):
        # Validar parámetros
        serializer = DateParameterSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        # Obtener datos
        data = report_service.get_daily_cash(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)
        
        # Calcular total usando serializer
        total = sum(item['total_payment'] for item in data) if data else 0
        
        # Preparar contexto usando serializer
        context_data = {
            'date': serializer.validated_data.get('date'),
            'data': data,
            'total': total,
            'title': 'Resumen de Caja Diaria'
        }
        context_serializer = PDFContextSerializer(context_data)
        context = context_serializer.data
        
        return render(request, 'pdf_templates/resumen_caja.html', context)


class ExcelExportView:
    """Responsable exclusivamente de la exportación a Excel."""
    
    @staticmethod
    def exportar_excel_citas(request):
        # Validar parámetros
        serializer = DateParameterSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        # Obtener datos
        data = report_service.get_appointments_between_dates(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)
        
        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Citas')
        
        # Formato para encabezados
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#2c3e50',
            'font_color': 'white',
            'border': 1
        })
        
        # Escribir encabezados
        headers = [
            'ID Paciente', 
            'DNI/Documento', 
            'Paciente', 
            'Teléfono', 
            'Fecha', 
            'Hora'
        ]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        # Escribir datos
        for row, appointment in enumerate(data, start=1):
            worksheet.write(row, 0, appointment['patient_id'])
            worksheet.write(row, 1, appointment['document_number_patient'])
            worksheet.write(row, 2, appointment['patient'])
            worksheet.write(row, 3, appointment['primary_phone_patient'])
            worksheet.write(row, 4, appointment['appointment_date'])
            worksheet.write(row, 5, appointment['appointment_hour'])
        
        # Ajustar anchos de columna
        worksheet.set_column('A:A', 12)  # ID Paciente
        worksheet.set_column('B:B', 15)  # DNI/Documento
        worksheet.set_column('C:C', 40)  # Paciente
        worksheet.set_column('D:D', 15)  # Teléfono
        worksheet.set_column('E:E', 12)  # Fecha
        worksheet.set_column('F:F', 10)  # Hora
        
        workbook.close()
        output.seek(0)
        
        # Generar respuesta
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=citas.xlsx'
        return response
        # Validar parámetros
        serializer = DateParameterSerializer(data=request.GET)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        
        # Obtener datos
        data = report_service.get_appointments_between_dates(serializer.validated_data)
        if isinstance(data, dict) and "error" in data:
            return JsonResponse(data, status=400)
        
        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Citas')
        
        # Formato para encabezados
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#2c3e50',
            'font_color': 'white',
            'border': 1
        })
        
        # Escribir encabezados
        headers = ['Fecha', 'Hora', 'Terapeuta', 'Paciente', 'Pago', 'Tipo de Pago']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        # Escribir datos
        for row, appointment in enumerate(data, start=1):
            worksheet.write(row, 0, appointment.get('appointment_date', ''))
            worksheet.write(row, 1, appointment.get('appointment_hour', ''))
            worksheet.write(row, 2, appointment.get('therapist', ''))
            worksheet.write(row, 3, appointment.get('patient', ''))
            worksheet.write(row, 4, float(appointment.get('payment', 0)))
            worksheet.write(row, 5, appointment.get('payment_type', ''))
        
        # Ajustar anchos de columna
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:D', 30)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 15)
        
        workbook.close()
        output.seek(0)
        
        # Generar nombre de archivo
        start_date = serializer.validated_data.get('start_date', '')
        end_date = serializer.validated_data.get('end_date', '')
        filename = f'citas_{start_date}_a_{end_date}.xlsx'
        
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


# Instancias de las clases para mantener compatibilidad
report_api = ReportAPIView()
pdf_export = PDFExportView()
excel_export = ExcelExportView()


# Funciones que mantienen la interfaz original (no rompen funcionalidad) "# Versión función wrapper (capa de protección)"
def get_number_appointments_per_therapist(request):
    try:
        return report_api.get_number_appointments_per_therapist(request)
    except Exception as e:
        import traceback
        print(f"Error en get_number_appointments_per_therapist: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'error': f'Error interno del servidor: {str(e)}',
            'traceback': traceback.format_exc()
        }, status=500)

def get_patients_by_therapist(request):
    try:
        return report_api.get_patients_by_therapist(request)
    except Exception as e:
        import traceback
        print(f"Error en get_patients_by_therapist: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'error': f'Error interno del servidor: {str(e)}',
            'traceback': traceback.format_exc()
        }, status=500)

def get_daily_cash(request):
    try:
        return report_api.get_daily_cash(request)
    except Exception as e:
        import traceback
        print(f"Error en get_daily_cash: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'error': f'Error interno del servidor: {str(e)}',
            'traceback': traceback.format_exc()
        }, status=500)

def get_appointments_between_dates(request):
    try:
        return report_api.get_appointments_between_dates(request)
    except Exception as e:
        import traceback
        print(f"Error en get_appointments_between_dates: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return JsonResponse({
            'error': f'Error interno del servidor: {str(e)}',
            'traceback': traceback.format_exc()
        }, status=500)


def reports_dashboard(request):
    return render(request, 'reports.html')

def pdf_citas_terapeuta(request):
    return pdf_export.pdf_citas_terapeuta(request)

def pdf_pacientes_terapeuta(request):
    return pdf_export.pdf_pacientes_terapeuta(request)

def pdf_resumen_caja(request):
    return pdf_export.pdf_resumen_caja(request)

def exportar_excel_citas(request):
    return excel_export.exportar_excel_citas(request)


