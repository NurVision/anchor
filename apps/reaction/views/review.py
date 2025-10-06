from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, serializers
from django.shortcuts import get_object_or_404

from apps.reaction.models import Review, ItemBlock
from apps.reaction.serializers.review import ReviewSerializer
from apps.reaction.permissions import IsOwnerOrReadOnly 

from rest_framework.generics import ListCreateAPIView

class ReviewListCreateAPIView(ListCreateAPIView):
    """
    Block uchun sharhlar ro'yxatini olish (GET) va yangi sharh yaratish (POST).
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        block_pk = self.kwargs.get('block_pk')
        block = get_object_or_404(ItemBlock, pk=block_pk)
        return Review.objects.filter(block=block)

    def perform_create(self, serializer):
        block_pk = self.kwargs.get('block_pk')
        block = get_object_or_404(ItemBlock, pk=block_pk)
        try:
            serializer.save(user=self.request.user, block=block)
        except IntegrityError:
            # unique_together (user, block) нарушено
            raise serializers.ValidationError({
                "detail": "Siz bu block uchun allaqachon sharh yozgansiz."
            })



class ReviewDetailAPIView(APIView):
    """
    Bitta sharhni tahrirlash (PUT) va o'chirish (DELETE).
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Review, pk=pk)

    def put(self, request, pk, *args, **kwargs):
        """
        ID (pk) bo'yicha sharhni tahrirlaydi.
        """
        review = self.get_object(pk)
        # Faqat egasi o'zgartira olishini tekshirish
        self.check_object_permissions(request, review)
        
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        ID (pk) bo'yicha sharhni o'chiradi.
        """
        review = self.get_object(pk)
        # Faqat egasi o'chira olishini tekshirish
        self.check_object_permissions(request, review)
        
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
__all__ = [
    "ReviewListCreateAPIView",
    "ReviewDetailAPIView",
]