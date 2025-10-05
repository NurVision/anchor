from datetime import timedelta
from typing import Dict
from urllib.parse import urlparse

from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


class UserService:
    @staticmethod
    def get_by_email(email):
        return User.objects.get(email=email)

    @staticmethod
    def get_by_username(username):
        return User.objects.get(username=username)

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
    def generate_email_link(user, purpose: str = "email_validation", expires_in=24 * 60 * 60):
        """
        Generate a verification link containing a JWT for email-related actions.

        This method creates a time-limited access token (using SimpleJWT)
        that encodes the user's email and the specified purpose. The token
        is then embedded into a full verification URL.

        Args:
            user (User): The user instance for whom the link is being generated.
                         The user must not be active or soft-deleted.
            purpose (str, optional): The purpose of the token
                                     (e.g., "email_validation", "deletion").
                                     Defaults to "email_validation".
            expires_in (int, optional): Expiration time in seconds.
                                        Defaults to 24 hours (24 * 60 * 60).

        Returns:
            str: A fully qualified verification link with the JWT token
                 included as a query parameter.

        Raises:
            ValueError: If the user is already active, soft-deleted,
                        if the base URL is invalid, or if the purpose is unsupported.
        """
        if purpose == "email_validation":
            if user.is_active or getattr(user, 'is_deleted', False):
                raise ValueError("Cannot generate token for active or soft-deleted user")

        if getattr(user, 'is_deleted', False):
            raise ValueError("Cannot generate token for soft-deleted user")

        base_url = settings.BASE_URL

        parsed = urlparse(base_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid base URL: must include scheme and domain")

        purpose_url_map = {
            "email_validation": "apps.user:verify-email",
            "deletion": "apps.user:cancel-account",
            "password_reset": "apps.user:reset-password",
        }

        url_name = purpose_url_map.get(purpose)
        if not url_name:
            raise ValueError(f"Unsupported purpose: {purpose}")

        access = AccessToken.for_user(user)
        access["email"] = user.email
        access["purpose"] = purpose
        access.set_exp(lifetime=timedelta(seconds=expires_in))

        try:
            relative_path = reverse(url_name)
        except Exception as e:
            raise ValueError(f"Could not resolve URL for purpose '{purpose}': {str(e)}")

        return f"{base_url.rstrip('/')}{relative_path}?token={str(access)}"

    @staticmethod
    def decode_access_token(token: str, expected_purpose: str = None) -> Dict[str, str]:
        """
        Decode and validate a SimpleJWT access token used for user actions.

        Args:
            token (str): The JWT access token string.
            expected_purpose (str, optional): If provided, the token's `purpose`
                                              claim must equal this value.

        Returns:
            dict: Token payload dict (at minimum contains 'email' and 'purpose').

        Raises:
            rest_framework.exceptions.ValidationError: On invalid/expired token,
                                                      missing claims, or wrong purpose.
        """
        try:
            access = AccessToken(token)
        except TokenError:
            raise exceptions.ValidationError({"token": "Invalid or expired token"})

        purpose = access.get("purpose")
        email = access.get("email")

        if expected_purpose and purpose != expected_purpose:
            raise exceptions.ValidationError({"token": "Invalid token purpose"})

        if not email:
            raise exceptions.ValidationError({"token": "Token missing email claim"})

        return {"email": email, "purpose": purpose}

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
