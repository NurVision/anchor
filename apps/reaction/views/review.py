# your_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from apps.reaction.models import Review, ItemBlock
from apps.reaction.serializers.review import ReviewSerializer
from apps.reaction.permissions import IsOwnerOrReadOnly 

class ReviewListCreateAPIView(APIView):
    """
    Block uchun sharhlar ro'yxatini olish (GET) va yangi sharh yaratish (POST).
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, block_pk, *args, **kwargs):
        """
        URL'da berilgan 'block_pk' uchun barcha sharhlarni qaytaradi.
        """
        block = get_object_or_404(ItemBlock, pk=block_pk)
        reviews = Review.objects.filter(block=block)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, block_pk, *args, **kwargs):
        """
        URL'da berilgan 'block_pk' uchun yangi sharh yaratadi.
        Modeldagi 'unique_together' tufayli bir user qayta sharh yoza olmaydi.
        """
        block = get_object_or_404(ItemBlock, pk=block_pk)
        serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            # Agar user bu block'ga allaqachon sharh yozgan bo'lsa,
            # unique_together cheklovi avtomatik xatolik qaytaradi.
            serializer.save(user=request.user, block=block)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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