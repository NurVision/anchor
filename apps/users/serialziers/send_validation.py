from rest_framework import serializers

from apps.users.models import User
from apps.users.tasks.send_vadiation import send_validation_email


class SendValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=32, min_length=8)

    def validate(self, attrs):
        email = attrs.get("email")

        if not email:
            raise serializers.ValidationError("Email is required.")
        return attrs

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        if len(value) < 8:
            raise serializers.ValidationError("Password is too short.")
        if len(value) > 32:
            raise serializers.ValidationError("Password is too long.")
        return value

    def create(self, validated_data):
        """
        Create a new user with the given email and password, or raise an error if the email is already in use.

        Args:
            validated_data (dict): Contains 'email' and 'password' fields.

        Returns:
            User: The created user instance.

        Raises:
            serializers.ValidationError: If a user with the given email already exists or if required fields are missing.
        """
        email = validated_data.get("email")
        password = validated_data.get("password")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists"})

        user = User.objects.create(email=email, username=email)
        user.set_password(password)
        user.save()

        link = user.generate_validation_link()

        send_validation_email(email, link)

        return {
            "detail": f"Verification link has been sent to {email}. Please check your email to verify your account."
        }


_all_ = ["SendValidationSerializer"]
