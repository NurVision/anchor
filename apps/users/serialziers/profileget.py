from rest_framework import serializers

from apps.users.models import User


class ProfileGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'display_name',
            'email',
            'is_active',
            'is_staff'
        )