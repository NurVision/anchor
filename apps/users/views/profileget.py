
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serialziers.model_serializer import UserModelSerializer
from apps.users.serialziers.profileget import ProfileGetSerializer


class ProfileGetAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileGetSerializer(user)
        return Response(serializer.data)