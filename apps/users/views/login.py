from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializer.login import LoginSerializer
from apps.users.services.user_services import UserTokenService


class LoginAPIView(GenericAPIView):
    """
    User login endpoint that supports both email and username authentication.
    Creates JWT tokens and manages user sessions with IP tracking.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data['user']

            response_data = UserTokenService.generate_jwt_token(user)

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


_all_ = ['LoginAPIView']
