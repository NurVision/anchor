from rest_framework import serializers

from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'display_name', "settings", "is_active", "is_staff", "created_at",
                  "updated_at", "is_deleted", "deleted_at",)
        read_only_fields = ('created_at', 'id',)

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get("exclude_fields", [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}
