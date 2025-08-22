from django.db import models
from django.conf import settings
from django.templatetags.static import static

class CompanyData(models.Model):
    company_name = models.CharField(max_length=255, unique=True)
    company_logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def get_logo_url(self):
        """
        Retorna la URL del logo de la empresa o una imagen por defecto
        """
        if self.company_logo:  # Imagen subida por el usuario
            return f"{settings.MEDIA_URL}{self.company_logo}"
        # Imagen por defecto desde static
        return static('img/default-logo.png')

    def has_logo(self):
        return bool(self.company_logo)

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name = "Company Data"
        verbose_name_plural = "Companies Data"
        ordering = ['company_name']  # Orden por defecto