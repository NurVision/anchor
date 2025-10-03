from rest_framework import serializers
from apps.reaction.models import Comment

class RecursiveField(serializers.Serializer):
    """
    O'z-o'ziga murojaat qiluvchi maydon uchun yordamchi serializer.
    Bu izohga yozilgan javoblarni (nested comments) ko'rsatish uchun kerak.
    """
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    # User'ning username'ini ko'rsatish uchun (faqat o'qish uchun)
    user = serializers.ReadOnlyField(source='user.username')
    
    # Izohga yozilgan javoblarni (replies) ko'rsatish uchun
    replies = RecursiveField(many=True, read_only=True, source='children') # 'children' related_name'dan keladi

    class Meta:
        model = Comment
        fields = [
            'id', 
            'user', 
            'text', 
            'parent', 
            'block', 
            'replies', 
            'created_at' # BaseModel'da bo'lsa
        ]
        
        # Bu maydonlar view tomonidan avtomatik to'ldiriladi,
        # shuning uchun client ularni yubormaydi.
        read_only_fields = ['user', 'block']

