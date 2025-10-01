from rest_framework.generics import DestroyAPIView, GenericAPIView
from rest_framework import permissions

from apps.users.models import User


class ProfileDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()