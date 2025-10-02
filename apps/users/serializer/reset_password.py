from rest_framework import serializers


class VerifyOTPAndResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, min_length=6, max_length=6)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """
        Validate that passwords match.
        """
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                "detail": "Passwords do not match"
            })
        return attrs


