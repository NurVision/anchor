from rest_framework import serializers

from apps.users.models import User


class UserSettingsSerializer(serializers.Serializer):
    """Serializer for user settings (theme, language, etc.)"""
    language = serializers.ChoiceField(
        choices=['uz', 'ru', 'en'],
        required=False
    )
    theme = serializers.ChoiceField(
        choices=['light', 'dark', 'auto'],
        required=False,
        default='light'
    )
    notifications_enabled = serializers.BooleanField(
        required=False,
        default=True
    )

    def validate_language(self, value):
        """Validate language code."""
        if value not in ['uz', 'ru', 'en']:
            raise serializers.ValidationError(
                "Invalid language. Supported: uz, ru, en"
            )
        return value


class SetLanguageSerializer(serializers.Serializer):
    """Serializer for setting user language preference."""
    language = serializers.ChoiceField(
        choices=['uz', 'ru', 'en'],
        required=True,
        help_text="Language code (uz, ru, or en)"
    )

    def validate_language(self, value):
        """Validate and normalize language code."""
        value = value.lower().strip()
        if value not in ['uz', 'ru', 'en']:
            raise serializers.ValidationError(
                "Invalid language code. Supported languages: uz, ru, en"
            )
        return value


class UserPreferencesSerializer(serializers.ModelSerializer):
    """Serializer for viewing/updating user preferences."""
    settings = UserSettingsSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'display_name', 'settings']
        read_only_fields = ['id', 'email', 'username']

    def update(self, instance, validated_data):
        """Update user settings, preserving existing settings."""
        settings_data = validated_data.pop('settings', None)

        if settings_data:
            current_settings = instance.settings or {}

            current_settings.update(settings_data)
            instance.settings = current_settings

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
