from rest_framework import serializers
from apps.reaction.models import Bookmark

class BookmarkSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'block']
        
    def validate(self, data):
        """
        Check that the user is not trying to create a duplicate bookmark.
        DRF automatically checks the `unique_together` constraint from the model,
        so this method provides a more user-friendly error message if needed,
        but is often not strictly necessary.
        """
        request_user = self.context['request'].user
        block = data.get('block')

        if Bookmark.objects.filter(user=request_user, block=block).exists():
            raise serializers.ValidationError("You have already bookmarked this item.")
            
        return data