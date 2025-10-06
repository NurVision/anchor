from rest_framework import serializers
from apps.reaction.models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'block']
