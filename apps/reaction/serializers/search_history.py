from rest_framework import serializers
from apps.reaction.models import SearchHistory, Item, ItemBlock

class HistoryItemSerializer(serializers.ModelSerializer):
    """
    Tarixdagi ItemBlock'ning parent Item'i uchun qisqa serializer.
    """
    class Meta:
        model = Item
        fields = ['title', 'slug', 'logo']

class HistoryItemBlockSerializer(serializers.ModelSerializer):
    """
    Tarixdagi ItemBlock haqida ma'lumotni va uning Item'ini ko'rsatish uchun.
    """
    item = HistoryItemSerializer(read_only=True)

    class Meta:
        model = ItemBlock
        fields = ['id', 'title', 'type', 'item']

class SearchHistorySerializer(serializers.ModelSerializer):
    """
    SearchHistory'ni o'qish va yozish uchun asosiy serializer.
    """
    user = serializers.ReadOnlyField(source='user.username')
    # GET so'rovida block haqida yuqoridagi serializer orqali to'liq ma'lumot beramiz
    block = HistoryItemBlockSerializer(read_only=True)
    
    # POST so'rovida faqat block_id qabul qilamiz
    block_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'query', 'block', 'block_id', 'created_at']