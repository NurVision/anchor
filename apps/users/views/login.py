from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serialziers.login import LoginSerializer
from apps.users.serialziers.model_serializer import UserModelSerializer


class LoginAPIView(APIView):
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

            response_data = {
                'success': True,
                'message': 'Login successful',
                'user': UserModelSerializer(user, context={
                    "exclude_fields": ["is_active", "is_staff", "updated_at", "is_deleted", "deleted_at"]}).data,
                'tokens': user.generate_jwt(),
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


_all_ = ['LoginAPIView']
