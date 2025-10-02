from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        allow_null=False
    )

    def validate(self, attrs):
        """
            Validate that the refresh token has a correct format and isn't already blacklisted.
        """
        try:
            token = RefreshToken(attrs['refresh_token'])

            if hasattr(token, "check_blacklist"):
                token.check_blacklist()

            return attrs

        except TokenError as e:
            raise serializers.ValidationError("Invalid or expired refresh token.")
        except Exception:
            raise serializers.ValidationError("Invalid refresh token format.")
