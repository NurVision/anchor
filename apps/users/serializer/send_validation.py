from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.users.models import User
from apps.users.services.user_services import UserTokenService
from apps.users.tasks.send_mail import send_validation_email


class SendValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=32, min_length=8, write_only=True)

    def validate_email(self, value):
        """Validate email format and check for existing users."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate_password(self, value):
        """Validate password strength."""
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def create(self, validated_data):
        """
        Create a new user and send verification email.
        """
        email = validated_data["email"].lower()
        password = validated_data["password"]

        try:
            user = User.objects.create(
                email=email,
                username=email,
                is_active=False
            )
            user.set_password(password)
            user.save()

            validation_link = UserTokenService.generate_email_link(
                user,
                purpose="email_validation",
                expires_in=24 * 60 * 60
            )
            deletion_link = UserTokenService.generate_email_link(
                user,
                purpose="deletion",
                expires_in=48 * 60 * 60
            )

            email_sent = send_validation_email(email, validation_link, deletion_link)

            if not email_sent:
                if user.id:
                    user.delete()
                raise serializers.ValidationError(
                    "Failed to send verification email. Please try again later."
                )

            return {
                "detail": f"Verification link has been sent to {email}. Please check your email to verify your account.",
                "email": email
            }

        except Exception as e:
            if 'user' in locals() and getattr(user, "id", None):
                user.delete()
            raise serializers.ValidationError(f"Account creation failed: {str(e)}")


_all_ = ["SendValidationSerializer"]
