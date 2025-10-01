from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that checks for soft deleted users.
    If a user is soft deleted, authentication will fail with appropriate error.
    """

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        Raises InvalidToken if the user is soft deleted.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise InvalidToken('User not found')

        if getattr(user, 'is_deleted', False):
            raise InvalidToken('User account has been deleted')

        return user


class SoftDeleteCheckMixin:
    """
    Mixin class to check for soft deleted users in views.
    Can be used in APIView classes to add soft delete checking.
    """

    def check_user_not_deleted(self, user):
        """
        Check if user is not soft deleted. Raises ValidationError if deleted.
        """
        if getattr(user, 'is_deleted', False):
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'detail': 'User account has been deleted'})

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to check for soft deleted users on authenticated requests.
        """
        response = super().dispatch(request, *args, **kwargs)

        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                self.check_user_not_deleted(request.user)
            except exceptions.ValidationError as e:
                from rest_framework.response import Response
                from rest_framework import status
                return Response(e.detail, status=status.HTTP_403_FORBIDDEN)

        return response
