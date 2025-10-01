from datetime import timedelta
from urllib.parse import urlparse

from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from apps.users.models import User


class UserService:
    @staticmethod
    def get_by_email(email):
        return User.objects.get(email=email)

    @staticmethod
    def get_by_username(username):
        return User.objects.get(username=username)




class UserTokenService(UserService):
    @staticmethod
    def generate_jwt_token(user: User):
        if not user.is_active or getattr(user, 'is_deleted', False):
            raise ValueError("Cannot generate token for inactive or soft-deleted user")

        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        access = refresh.access_token
        access["email"] = user.email
        expires_in = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME").total_seconds()
        access.set_exp(lifetime=timedelta(seconds=expires_in))
        return {"access": str(access), "refresh": str(refresh)}

    @staticmethod
    def generate_email_validation_link(user, expires_in=24 * 60 * 60):
        """
        Generates a link for email validation with a SimpleJWT access token.
        :param user: User instance
        :param expires_in: Expiry time in seconds (default 24 hours)
        :return: Full validation link with token as query param
        """
        if user.is_active or getattr(user, 'is_deleted', False):
            raise ValueError("Cannot generate token for active or soft-deleted user")

        base_url = settings.BASE_URL

        parsed = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid base URL: must include scheme and domain")

        access = AccessToken.for_user(user)
        access["email"] = user.email
        access["purpose"] = "email_validation"
        access.set_exp(lifetime=timedelta(seconds=expires_in))

        return f"{base_url.rstrip('/')}/?token={str(access)}"

    @staticmethod
    def refresh_access_token(refresh_token):
        """
        Use an existing refresh token to generate a NEW access token.

        - Accepts a refresh token string
        - Returns a new access token string derived from the refresh
        - Optionally overrides access token expiry with `expires_in`
        """
        try:
            refresh = RefreshToken(refresh_token)
        except TokenError as e:
            raise ValueError(f"Invalid or expired refresh token: {str(e)}")

        access = refresh.access_token
        if "email" in refresh.payload:
            access["email"] = refresh.payload["email"]

        expires_in = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME").total_seconds()
        access.set_exp(lifetime=timedelta(seconds=expires_in))

        response = {"access": str(access)}
        if settings.SIMPLE_JWT.get('ROTATE_REFRESH_TOKENS'):
            response["refresh"] = str(refresh)

        return response
