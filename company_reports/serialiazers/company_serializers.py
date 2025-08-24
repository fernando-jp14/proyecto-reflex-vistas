from rest_framework import serializers
from company_reports.models.company import CompanyData
import os


class ImageValidator:
    """Responsable de validar archivos de imagen (tamaño y formato)."""

    ALLOWED_FORMATS = ['jpeg', 'jpg', 'png']
    MAX_SIZE_MB = 2

    @staticmethod
    def get_file_size(file_obj):
        """Obtiene el tamaño del archivo de forma segura."""
        if hasattr(file_obj, 'size'):
            return file_obj.size
        if hasattr(file_obj, 'file'):
            return file_obj.file.size
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
        if not obj.company_logo:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.company_logo.url)
        return obj.company_logo.url

    def get_has_logo(self, obj):
        return bool(obj.company_logo)