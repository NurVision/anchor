from rest_framework import permissions
from rest_framework.generics import UpdateAPIView

from apps.users.models import User
from apps.users.serialziers.profileupdate import ProfileUpdateSerializer


class ProfileUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user