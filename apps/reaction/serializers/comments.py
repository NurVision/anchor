from rest_framework import serializers
from apps.reaction.models import Comment


class RecursiveField(serializers.Serializer):
    """
    Rekursiv (nested) serializer — izoh ichidagi javoblarni ko‘rsatadi.
    """
    def to_representation(self, value):
        # value = child comment instance
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    replies = RecursiveField(many=True, read_only=True, source='children')

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'text',
            'parent',
            'block',
            'replies',
            'created_at',
        ]
        read_only_fields = ['user', 'block']
