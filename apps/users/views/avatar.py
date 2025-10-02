from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializer.avatar import AvatarUploadSerializer
from apps.users.serializer.model_serializer import UserModelSerializer
from apps.users.services.user_services import UserService


class UploadAvatarAPIView(APIView):
    """
    Upload or update user avatar.
    Supports: POST with multipart/form-data
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Handle file uploads

    def post(self, request):
        serializer = AvatarUploadSerializer(data=request.data)

        if serializer.is_valid():
            avatar_file = serializer.validated_data['avatar']

            try:
                updated_user = UserService.update_avatar(request.user, avatar_file)

                profile_serializer = UserModelSerializer(
                    updated_user,
                    context={
                        'request': request,
                        "exclude_fields": ["is_active", "is_staff", "created_at", "updated_at", "is_deleted",
                                           "deleted_at", ]
                    }
                )

                return Response(
                    {
                        "detail": "Avatar uploaded successfully",
                        "user": profile_serializer.data
                    },
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                return Response(
                    {"detail": f"Failed to upload avatar: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAvatarAPIView(APIView):
    """
    Delete user avatar.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user

        if not user.avatar:
            return Response(
                {"detail": "No avatar to delete"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            UserService.delete_avatar(user)

            return Response(
                {"detail": "Avatar deleted successfully"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": f"Failed to delete avatar: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )