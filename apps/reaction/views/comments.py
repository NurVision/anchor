from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from apps.reaction.models import Comment, ItemBlock
from apps.reaction.serializers.comments import CommentSerializer
from apps.reaction.permissions import IsOwnerOrReadOnly


class CommentListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, block_pk, *args, **kwargs):
        block = get_object_or_404(ItemBlock, pk=block_pk)
        # Faqat parent izohlarni olamiz, ichida replies chiqadi
        comments = Comment.objects.filter(block=block, parent__isnull=True).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer

    def post(self, request, block_pk, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Берём блок по pk
        try:
            block = ItemBlock.objects.get(pk=block_pk)
        except ItemBlock.DoesNotExist:
            return Response({"error": "Block not found"}, status=status.HTTP_404_NOT_FOUND)

        # Сохраняем с user и block
        serializer.save(user=request.user, block=block)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        comment_id = self.kwargs.get('id')
        return Comment.objects.filter(id=comment_id)


class CommentDeleteAPIView(APIView):
    """
    Izohni o‘chirish (DELETE) uchun.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        return comment

    def delete(self, request, pk, *args, **kwargs):
        """
        Faqat egasi o‘chira oladi.
        """
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

__all__ = [
    "CommentListAPIView",
    "CommentCreateAPIView",
    "CommentDetailAPIView",
    "CommentDeleteAPIView",
]