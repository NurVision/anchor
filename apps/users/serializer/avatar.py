from rest_framework import serializers

from apps.users.models import User


class AvatarUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for uploading user avatar.
    """
    avatar = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = ['avatar']

    def validate_avatar(self, value):
        """
        Validate avatar file.
        """
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError("Avatar file size cannot exceed 5MB")

        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only JPEG, PNG, GIF, and WebP images are allowed")


        return value