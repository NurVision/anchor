from rest_framework import serializers
from apps.reaction.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    # Javobda user'ning username'ini ko'rsatish uchun
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'user', 'block', 'text', 'rating', 'created_at']
        
        # Bu maydonlar view tomonidan avtomatik to'ldiriladi
        read_only_fields = ['user', 'block']

    def validate_rating(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("Reyting 0 dan 5 gacha bo'lishi kerak.")
        return value