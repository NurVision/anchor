from rest_framework import serializers
from apps.reaction.models import SearchHistory, Item, ItemBlock


class HistoryItemSerializer(serializers.ModelSerializer):
    """ItemBlock'ning parent Item'i uchun qisqa serializer."""
    class Meta:
        model = Item
        fields = ['title', 'slug', 'logo']


class HistoryItemBlockSerializer(serializers.ModelSerializer):
    """ItemBlock haqida ma'lumot va uning Item'ini ko'rsatish."""
    item = HistoryItemSerializer(read_only=True)

    class Meta:
        model = ItemBlock
        fields = ['id', 'title', 'type', 'item']


class SearchHistorySerializer(serializers.ModelSerializer):
    """SearchHistory uchun asosiy serializer."""
    user = serializers.ReadOnlyField(source='user.username')
    block = HistoryItemBlockSerializer(read_only=True)
    block_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'query', 'block', 'block_id', 'created_at']

    def create(self, validated_data):
        """POST orqali yangi yozuv yaratish."""
        user = self.context['request'].user
        block_id = validated_data.pop('block_id')
        block = ItemBlock.objects.get(pk=block_id)
        history = SearchHistory.objects.create(user=user, block=block, **validated_data)
        return history
