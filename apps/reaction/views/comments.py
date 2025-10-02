# your_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from apps.reaction.models import Comment, ItemBlock
from apps.reaction.serializers.comments import CommentSerializer
from apps.reaction.permissions import IsOwnerOrReadOnly


class CommentListCreateAPIView(APIView):
    """
    Block uchun izohlar ro'yxatini olish (GET) va yangi izoh yaratish (POST).
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, block_pk, *args, **kwargs):
        """
        URL'da berilgan 'block_pk' uchun barcha asosiy izohlarni qaytaradi.
        """
        block = get_object_or_404(ItemBlock, pk=block_pk)
        # Faqat shu block'ga tegishli va parent'i yo'q izohlarni olamiz.
        comments = Comment.objects.filter(block=block, parent__isnull=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, block_pk, *args, **kwargs):
        """
        URL'da berilgan 'block_pk' uchun yangi izoh yaratadi.
        """
        block = get_object_or_404(ItemBlock, pk=block_pk)
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            # User'ni va block'ni avtomatik bog'laymiz
            serializer.save(user=request.user, block=block)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    """
    Bitta izohni tahrirlash (PUT) va o'chirish (DELETE).
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        """Helper method to get the comment object."""
        return get_object_or_404(Comment, pk=pk)

    def put(self, request, pk, *args, **kwargs):
        """
        ID (pk) bo'yicha izohni tahrirlaydi.
        """
        comment = self.get_object(pk)
        # Faqat egasi o'zgartira olishini tekshirish
        self.check_object_permissions(request, comment)
        
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        ID (pk) bo'yicha izohni o'chiradi.
        """
        comment = self.get_object(pk)
        # Faqat egasi o'chira olishini tekshirish
        self.check_object_permissions(request, comment)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

__all__ = [
    "CommentListCreateAPIView",
    "CommentDetailAPIView",
]