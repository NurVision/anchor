from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=False, allow_null=False)
    username = serializers.CharField(
        required=False, allow_blank=False, allow_null=False
    )
    password = serializers.CharField(
        write_only=True, required=True, allow_blank=False, allow_null=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        password = attrs.get("password")

        if email and username:
            raise serializers.ValidationError(
                "Email and username cannot be both specified"
            )

        if not email and not username:
            raise serializers.ValidationError(
                "Either email or username must be provided"
            )

        login_field = email if email else username

        user = authenticate(
            request=self.context.get('request'),
            username=login_field,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid credentials. Please check your email/username and password."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Your account is inactive. Please verify your email first."
            )

        if user.is_deleted:
            raise serializers.ValidationError(
                "Your account has been deactivated. Please contact support."
            )

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        attrs['user'] = user
        return attrs
