from rest_framework import permissions
from rest_framework.generics import UpdateAPIView

from apps.users.models import User
from apps.users.serialziers.profileupdate import ProfileUpdateSerializer


class ProfileUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)