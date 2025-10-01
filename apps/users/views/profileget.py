from rest_framework import permissions
from rest_framework.generics import GenericAPIView

from apps.users.models import User
from apps.users.serialziers.profileget import ProfileGetSerializer


class ProfileGetAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        return self.response(user)