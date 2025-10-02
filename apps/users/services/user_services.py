import random
import string
from datetime import timedelta
from urllib.parse import urlparse

from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import default_storage
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

    @staticmethod
    def generate_otp(user, expires_in=300):
        """
        Generates a random OTP for user and stores it in cache.
        :param user: User instance
        :param expires_in: Expiry time in seconds (default 5 minutes)
        :return: Generated OTP code
        """
        otp = ''.join(random.choices(string.digits, k=6))

        cache_key = f"otp_{user.username}"

        cache.set(cache_key, otp, timeout=expires_in)

        return otp

    @staticmethod
    def verify_otp(user, otp_code):
        """
        Verifies the OTP code for a user.
        :param user: User instance
        :param otp_code: OTP code to verify
        :return: Boolean indicating if OTP is valid
        """
        cache_key = f"otp_{user.username}"
        cached_otp = cache.get(cache_key)

        if cached_otp is None:
            return False

        if cached_otp == otp_code:
            cache.delete(cache_key)
            return True

        return False

    @staticmethod
    def resend_otp(user):
        """
        Resends OTP by generating a new one.
        Useful for "Resend OTP" functionality.
        """

        cache_key = f"otp_{user.username}"
        existing_otp = cache.get(cache_key)

        if existing_otp:
            cache.delete(cache_key)

        return UserService.generate_otp(user)

    @staticmethod
    def update_avatar(user, avatar_file):
        """
        Update user avatar and delete old one.
        :param user: User instance
        :param avatar_file: New avatar file (UploadedFile)
        :return: Updated user instance
        """
        if user.avatar:
            try:
                if default_storage.exists(user.avatar.name):
                    default_storage.delete(user.avatar.name)


            except Exception as e:
                print(f"Error deleting old avatar: {e}")

        user.avatar = avatar_file
        user.save(update_fields=['avatar', 'updated_at'])

        return user

    @staticmethod
    def delete_avatar(user):
        """
        Delete user avatar.
        :param user: User instance
        :return: Updated user instance
        """
        if user.avatar:
            try:
                if default_storage.exists(user.avatar.name):
                    default_storage.delete(user.avatar.name)
            except Exception as e:
                print(f"Error deleting avatar: {e}")

        user.avatar = None
        user.save(update_fields=['avatar', 'updated_at'])

        return user


class UserTokenService:
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
