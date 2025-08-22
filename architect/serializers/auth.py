from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError(_('Se requieres email y contraseña.'))

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if user is None:
            raise AuthenticationFailed(_('Credenciales inválidas.'))
        
        if user.is_active is None:
            raise AuthenticationFailed(_('Cuenta no activada.'))
        
        refresh = RefreshToken.for_user(user)

        return {
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate_password(self, value):
        # Validación personalizada de contraseña
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        
        # Verificar que no sea una contraseña común
        common_passwords = ['password', '123456', '12345678', 'qwerty', 'abc123', 'password123', 'admin', 'letmein']
        if value.lower() in common_passwords:
            raise serializers.ValidationError("Esta contraseña es demasiado común. Elige una contraseña más segura.")
        
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Las contraseñas no coinciden"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user 