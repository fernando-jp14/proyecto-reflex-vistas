from django.urls import path, include
from rest_framework.routers import DefaultRouter
from company_reports.views.company_views import CompanyDataViewSet

router = DefaultRouter()
router.register(r'companydata', CompanyDataViewSet, basename='companydata')

urlpatterns = [
    # URLs del router para los ViewSets
    path('', include(router.urls)),
]