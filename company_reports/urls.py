from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company_reports.views.statistics_views import StatisticsViewSet, dashboard_view, GetMetricsView
from company_reports.views.company_views import CompanyDataViewSet
#from company_reports.views.emails_views import dashboard_email, SendVerifyCodeAPIView, VerifyCodeAPIView
from company_reports.views import reports_views as views

router = DefaultRouter()
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'company', CompanyDataViewSet, basename='company')

# Agrupar rutas por funcionalidad
api_urlpatterns = [
    path('', include(router.urls)),
    #path('api/send-email/', SendVerifyCodeAPIView.as_view(), name='send-email'),
    #path('api/verify-code/', VerifyCodeAPIView.as_view(), name='verify-code'),
]

reports_urlpatterns = [
    path('reports/statistics/', GetMetricsView.as_view(), name='statistics_metrics'),
    path('reports/appointments-per-therapist/', views.get_number_appointments_per_therapist, name='appointments_per_therapist'),
    path('reports/patients-by-therapist/', views.get_patients_by_therapist, name='patients_by_therapist'),
    path('reports/daily-cash/', views.get_daily_cash, name='daily_cash'),
    path('reports/appointments-between-dates/', views.get_appointments_between_dates, name='appointments_between_dates'),
]

export_urlpatterns = [
    path('exports/pdf/citas-terapeuta/', views.pdf_citas_terapeuta, name='pdf_citas_terapeuta'),
    path('exports/pdf/pacientes-terapeuta/', views.pdf_pacientes_terapeuta, name='pdf_pacientes_terapeuta'),
    path('exports/pdf/resumen-caja/', views.pdf_resumen_caja, name='pdf_resumen_caja'),
    path('exports/excel/citas-rango/', views.exportar_excel_citas, name='exportar_excel_citas'),
]
'''
views_urlpatterns = [
    path('form/', company_form_view, name='company_form'),
]
'''
urlpatterns = []
urlpatterns.extend(api_urlpatterns)
urlpatterns.extend(reports_urlpatterns)
urlpatterns.extend(export_urlpatterns)
#urlpatterns.extend(views_urlpatterns)