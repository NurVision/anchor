from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

from apps.users.models import User
from apps.users.serializer.model_serializer import UserModelSerializer
from apps.users.services.user_services import UserService
from apps.users.tasks.send_vadiation import send_welcome_email


class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"detail": "Token is missing"}, status=400)

        try:
            access_token = AccessToken(token)

            purpose = access_token.get("purpose")
            email = access_token.get("email")

            if purpose != "email_validation":
                return Response({"detail": "Invalid token purpose"}, status=status.HTTP_400_BAD_REQUEST)

            user = UserService.get_by_email(email)

            if user.is_active:
                return Response({"detail": "Email already verified"}, status=status.HTTP_409_CONFLICT)

            user.is_active = True
            user.save()
            send_welcome_email(email)

            return Response(
                {
                    "detail": "Email successfully validated!",
                    "user": UserModelSerializer(user, context={
                        "exclude_fields": ['username', 'display_name', "settings", "is_active", "is_staff",
                                           "updated_at", "is_deleted", "deleted_at"]}).data,
                    "token": user.generate_jwt(),
                },
                status=200,
            )

        except (InvalidToken, TokenError):
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": f"An unexpected error occurred {e}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


_all_ = ["ValidateEmailView"]
