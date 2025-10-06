# your_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from apps.reaction.models import Like, ItemBlock
from apps.reaction.serializers.like import LikeSerializer

class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, block_pk, *args, **kwargs):
        block = get_object_or_404(ItemBlock, pk=block_pk)

        like, created = Like.objects.get_or_create(user=request.user, block=block)
        
        if created:
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(
            {"detail": "Siz bu elementga allaqachon like bosgansiz."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, block_pk, *args, **kwargs):
        """
        Block'dan 'like'ni olib tashlaydi. Agar 'like' mavjud bo'lmasa, 404 xatolik qaytaradi.
        """
        block = get_object_or_404(ItemBlock, pk=block_pk)

        like = get_object_or_404(Like, user=request.user, block=block)
        
        like.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
__all__ = [
    "LikeToggleAPIView",
]