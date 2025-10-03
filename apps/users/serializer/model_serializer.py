from rest_framework import serializers

from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'display_name', "settings", "avatar_url", "is_active", "is_staff",
                  "created_at","updated_at", "is_deleted", "deleted_at",)
        read_only_fields = ('created_at', 'id', "is_active", "is_staff", "is_deleted", "deleted_at", "email",
                            "avatar_url",)

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get("exclude_fields", [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}

    def get_avatar_url(self, obj):
        """
        Return full URL for avatar or None.
        """
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None