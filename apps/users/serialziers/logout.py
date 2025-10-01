from rest_framework import serializers


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True, required=True, allow_blank=False, allow_null=False)