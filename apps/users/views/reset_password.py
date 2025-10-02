from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializer.reset_password import VerifyOTPAndResetPasswordSerializer
from apps.users.services.user_services import UserService
from apps.users.tasks.send_vadiation import send_reset_password_email


class RequestPasswordResetAPIView(APIView):
    """
    Request password reset. Sends OTP to authenticated user's email.
    Requires valid JWT token in Authorization header.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            send_reset_password_email(user)

            return Response(
                {"detail": "Password reset OTP has been sent to your email"},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"detail": "Failed to send OTP. Please try again later"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResendOTPAPIView(APIView):
    """
    Resend OTP for password reset.
    Requires valid JWT token in Authorization header.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            UserService.resend_otp(user)
            send_reset_password_email(user)

            return Response(
                {"detail": "OTP has been resent to your email"},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"detail": "Failed to resend OTP. Please try again later"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyOTPAndResetPasswordAPIView(GenericAPIView):
    """
    Verify OTP and reset password for authenticated user.
    Requires valid JWT token in Authorization header.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyOTPAndResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            try:
                if UserService.verify_otp(user, otp):
                    user.set_password(new_password)
                    user.save()

                    return Response(
                        {"detail": "Password has been reset successfully"},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"detail": "Invalid or expired OTP"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            except Exception:
                return Response(
                    {"detail": "Failed to reset password. Please try again"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
