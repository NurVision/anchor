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
