from rest_framework import status, exceptions
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializer.reset_password import ResetPasswordSerializer, RequestPasswordResetSerializer
from apps.users.services.user_services import UserService, UserTokenService
from apps.users.tasks.send_mail import send_password_reset_email


class RequestPasswordResetAPIView(CreateAPIView):
    """
    Request password reset by providing email address.
    No authentication required - anyone can request a reset.
    This is the standard approach for "forgot password" functionality.
    """
    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = RequestPasswordResetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']

        try:
            user = UserService.get_by_email(email)

            if user.is_active and not getattr(user, 'is_deleted', False):
                reset_link = UserTokenService.generate_email_link(
                    user,
                    purpose="password_reset",
                    expires_in=60 * 60
                )

                send_password_reset_email(user.email, reset_link)

        except User.DoesNotExist:

            pass
        except Exception as e:

            print(f"Password reset error: {str(e)}")

        return Response(
            {
                "detail": "If an account exists with this email, a password reset link has been sent. "
                          "Please check your inbox and spam folder."
            },
            status=status.HTTP_200_OK
        )


class ResetPasswordAPIView(GenericAPIView):
    """
    Reset password using the token from email link.
    No authentication required - token validation is sufficient.
    """
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        """Handle password reset with token."""
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:

            token_data = UserTokenService.decode_access_token(
                token,
                expected_purpose="password_reset"
            )
            email = token_data["email"]

            user = UserService.get_by_email(email)

            if not user.is_active or getattr(user, 'is_deleted', False):
                return Response(
                    {"detail": "This account is not active."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save(update_fields=['password'])

            return Response(
                {
                    "detail": "Password has been reset successfully. "
                              "You can now log in with your new password."
                },
                status=status.HTTP_200_OK
            )

        except exceptions.ValidationError as e:

            error_detail = str(e.detail.get("token", ["Invalid or expired token"])[0])
            return Response(
                {"detail": error_detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Password reset error: {str(e)}")
            return Response(
                {
                    "detail": "Failed to reset password. "
                              "Please try again or request a new reset link."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        """
        Validate token before showing reset form.
        Useful for frontend to check if token is valid.
        """
        token = request.query_params.get("token")

        if not token:
            return Response(
                {"detail": "Token is missing", "valid": False},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            token_data = UserTokenService.decode_access_token(
                token,
                expected_purpose="password_reset"
            )
            email = token_data["email"]

            user = UserService.get_by_email(email)

            if not user.is_active or getattr(user, 'is_deleted', False):
                return Response(
                    {"detail": "This account is not active", "valid": False},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "detail": "Token is valid",
                    "valid": True,
                    "email": email
                },
                status=status.HTTP_200_OK
            )

        except exceptions.ValidationError:
            return Response(
                {"detail": "Invalid or expired token", "valid": False},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found", "valid": False},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Token validation error: {str(e)}")
            return Response(
                {"detail": "Token validation failed", "valid": False},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


_all_ = ["ResetPasswordAPIView", "RequestPasswordResetAPIView"]
