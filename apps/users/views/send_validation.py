from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serialziers import SendValidationSerializer


class SendValidationView(GenericAPIView):
    serializer_class = SendValidationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
                Create a new user and send an email validation link.

                - Validates the provided email and password.
                - Creates the user if the email doesn't exist.
                - Generates and sends a validation link via email.
                - Returns a success message.

                Raises:
                    ValidationError: If validation fails (e.g., duplicate email, invalid password).
                """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = serializer.save()

        return Response(
            result,
            status=status.HTTP_201_CREATED
        )


__all__ = ["SendValidationView"]
