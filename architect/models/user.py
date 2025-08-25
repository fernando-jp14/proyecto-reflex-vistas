from django.contrib.auth.models import AbstractUser
from django.db import models
from guardian.shortcuts import assign_perm, remove_perm, get_perms
from .base import BaseModel


class User(AbstractUser, BaseModel):
    """
    Modelo de usuario personalizado que extiende AbstractUser
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        verbose_name='Foto de Perfil'
    )
    ROL_CHOICES = (
        ('Admin', 'Admin'),
        ('User', 'User'),
    )
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='User')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def assign_permission(self, permission, obj):
        """
        Asigna un permiso a este usuario para un objeto específico
        """
        return assign_perm(permission, self, obj)

    def remove_permission(self, permission, obj):
        """
        Remueve un permiso de este usuario para un objeto específico
        """
        return remove_perm(permission, self, obj)

    def get_object_permissions(self, obj):
        """
        Obtiene todos los permisos de este usuario para un objeto específico
        """
        return get_perms(self, obj)

    def get_full_name(self):
        """Retorna el nombre completo del usuario"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def has_profile_photo(self):
        """Verifica si el usuario tiene una foto de perfil"""
        return bool(self.profile_photo)

    def get_profile_photo_url(self):
        """Retorna la URL de la foto de perfil o None"""
        if self.profile_photo:
            return self.profile_photo.url
        return None

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'