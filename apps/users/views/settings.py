from django.utils.translation import activate
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.serializer.settings import SetLanguageSerializer, UserPreferencesSerializer


class SetLanguageView(generics.GenericAPIView):
    """
    Set user's preferred language.

    For authenticated users: Stores in user.settings and cookie
    For anonymous users: Stores only in cookie

    POST /api/v1/users/set-language/
    Body: {"language": "uz"}
    """
    serializer_class = SetLanguageSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        language = serializer.validated_data['language']

        activate(language)

        if request.user.is_authenticated:
            user = request.user

            if user.settings is None:
                user.settings = {}

            user.settings['language'] = language
            user.save(update_fields=['settings'])

            response_data = {
                "detail": f"Language successfully set to '{language}'",
                "language": language,
                "saved_to": "database and cookie"
            }
        else:
            response_data = {
                "detail": f"Language successfully set to '{language}'",
                "language": language,
                "saved_to": "cookie only (login to save permanently)"
            }

        response = Response(response_data, status=status.HTTP_200_OK)

        response.set_cookie(
            key='django_language',
            value=language,
            max_age=365 * 24 * 60 * 60,
            httponly=True,
            samesite='Lax',
            secure=False
        )

        return response


class UserPreferencesView(generics.RetrieveUpdateAPIView):
    """
    Get or update user preferences (settings).

    GET /api/v1/users/preferences/
    PUT/PATCH /api/v1/users/preferences/
    Body: {
        "settings": {
            "language": "uz",
            "theme": "dark",
            "notifications_enabled": true
        },
        "display_name": "John Doe"
    }
    """
    serializer_class = UserPreferencesSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return the current authenticated user."""
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Update preferences and sync language to cookie."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        settings_data = request.data.get('settings', {})
        new_language = settings_data.get('language')

        response = Response(serializer.data)

        if new_language:
            activate(new_language)
            response.set_cookie(
                key='django_language',
                value=new_language,
                max_age=365 * 24 * 60 * 60,
                httponly=True,
                samesite='Lax',
                secure=False
            )

        return response
