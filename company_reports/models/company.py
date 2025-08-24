from django.db import models
from django.conf import settings

class CompanyData(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    company_logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def get_logo_url(self):
        """
        Retorna la URL del logo de la empresa o None si no tiene logo
        """
        if self.company_logo:
            return f"{settings.MEDIA_URL}{self.company_logo}"
        return None

    def has_logo(self):
        return bool(self.company_logo)

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = "Company Data"
        verbose_name_plural = "Companies Data"
        ordering = ['company_name'] 