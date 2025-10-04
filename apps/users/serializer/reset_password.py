from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


class RequestPasswordResetSerializer(serializers.Serializer):
    """Serializer for requesting password reset."""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """Normalize email to lowercase."""
        return value.lower().strip()


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for resetting password via email link."""
    token = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        max_length=128,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        max_length=128,
        style={'input_type': 'password'}
    )

    def validate_new_password(self, value):
        """Validate password using Django's password validators."""
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })
        return attrs
