from rest_framework import status, exceptions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializer.model_serializer import UserModelSerializer
from apps.users.services.user_services import UserService, UserTokenService
from apps.users.tasks.send_mail import send_welcome_email


class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """Handle email verification via token."""
        token = request.query_params.get("token")

        if not token:
            return Response(
                {"detail": "Token is missing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token_data = UserTokenService.decode_access_token(token, expected_purpose="email_validation")
            email = token_data["email"]

            user = UserService.get_by_email(email)

            if user.is_active:
                return Response(
                    {"detail": "Email already verified."},
                    status=status.HTTP_409_CONFLICT
                )

            user.is_active = True
            user.save()

            send_welcome_email(email)

            return Response(
                {
                    "detail": "Email successfully validated!",
                    "user": UserModelSerializer(
                        user,
                        context={
                            "exclude_fields": [
                                'username', 'display_name', "settings", "is_active",
                                "is_staff", "updated_at", "is_deleted", "deleted_at"
                            ]
                        }
                    ).data,
                    "token": user.generate_jwt(),
                },
                status=status.HTTP_200_OK
            )

        except exceptions.ValidationError as e:
            return Response(
                {"detail": str(e.detail.get("token", "Invalid token"))},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "An unexpected error occurred. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CancelAccountAPIView(APIView):
    """Handle account deletion requests via deletion token."""
    permission_classes = [AllowAny]

    def get(self, request):
        """Cancel account creation request."""
        token = request.query_params.get("token")

        if not token:
            return Response(
                {"detail": "Token is missing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token_data = UserTokenService.decode_access_token(token, expected_purpose="deletion")
            email = token_data["email"]

            user = UserService.get_by_email(email)

            if user.is_active:
                return Response(
                    {"detail": "Cannot cancel an already verified account. Please use account settings."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.delete()

            return Response(
                {"detail": "Account request cancelled successfully."},
                status=status.HTTP_200_OK
            )

        except exceptions.ValidationError as e:
            return Response(
                {"detail": str(e.detail.get("token", "Invalid token"))},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "Account request not found or already cancelled."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": "An unexpected error occurred. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


_all_ = ["ValidateEmailView", "CancelAccountAPIView"]
