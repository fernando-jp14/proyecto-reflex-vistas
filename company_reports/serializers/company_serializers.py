from rest_framework import serializers
from company_reports.models.company_models import CompanyData
import os


class ImageValidator:
    """Responsable de validar archivos de imagen (tamaño y formato)."""

    ALLOWED_FORMATS = ['jpeg', 'jpg', 'png']
    MAX_SIZE_MB = 2

    @staticmethod
    def get_file_size(file_obj):
        """Obtiene el tamaño del archivo sin consumirlo definitivamente."""
        size = getattr(file_obj, 'size', None)
        if size:
            return size

        file_like = getattr(file_obj, 'file', file_obj)
        try:
            cur = file_like.tell()
            file_like.seek(0, os.SEEK_END)
            size = file_like.tell()
            file_like.seek(cur)
            return size
        except Exception:
            try:
                content = file_like.read()
                size = len(content)
                if hasattr(file_like, 'seek'):
                    file_like.seek(0)
                return size
            except Exception:
                return 0

    @classmethod
    def validate_size(cls, file_obj):
        size = cls.get_file_size(file_obj)
        if size > cls.MAX_SIZE_MB * 1024 * 1024:
            raise serializers.ValidationError(
                f"El logo no puede superar los {cls.MAX_SIZE_MB} MB."
            )

    @classmethod
    def validate_format(cls, file_obj):
        try:
            fmt = file_obj.image.format.lower()
            if fmt not in cls.ALLOWED_FORMATS:
                raise serializers.ValidationError("Solo se permiten imágenes JPG o PNG.")
        except AttributeError:
            filename_ext = file_obj.name.split('.')[-1].lower()
            if filename_ext not in cls.ALLOWED_FORMATS:
                raise serializers.ValidationError("Solo se permiten imágenes JPG o PNG.")

    @classmethod
    def validate(cls, file_obj):
        cls.validate_size(file_obj)
        cls.validate_format(file_obj)
        return file_obj


class LogoUrlGenerator:
    """Responsable de generar URLs y verificar existencia de logos."""

    @staticmethod
    def has_logo(company: CompanyData) -> bool:
        return bool(company.company_logo)

    @staticmethod
    def get_logo_url(company: CompanyData, request=None):
        if not company.company_logo:
            return None
        if request:
            return request.build_absolute_uri(company.company_logo.url)
        return company.company_logo.url


class UploadImageRequest(serializers.Serializer):
    logo = serializers.ImageField()

    def validate_logo(self, value):
        return ImageValidator.validate(value)


class CompanyDataSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    has_logo = serializers.SerializerMethodField()

    class Meta:
        model = CompanyData
        fields = ['id', 'company_name', 'company_logo', 'logo_url', 'has_logo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'logo_url', 'has_logo']

    def get_logo_url(self, obj):
        request = self.context.get('request')
        return LogoUrlGenerator.get_logo_url(obj, request)

    def get_has_logo(self, obj):
        return LogoUrlGenerator.has_logo(obj)