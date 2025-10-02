from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializer.logout import LogoutSerializer


class LogoutAPIView(GenericAPIView):  # Removed SoftDeleteCheckMixin
    """
    User logout endpoint that blacklists JWT refresh tokens.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            refresh_token = serializer.validated_data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )

        except serializers.ValidationError as e:
            return Response(
                {"detail": e.detail if hasattr(e, 'detail') else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except TokenError:
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": "An error occurred during logout"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


_all_ = ['LogoutAPIView']
