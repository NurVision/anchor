# your_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from apps.reaction.models import Like, ItemBlock
# Serializer'ni ham import qilamiz, garchi u faqat javob uchun kerak bo'lsa ham
from apps.reaction.serializers.like import LikeSerializer 

class LikeToggleAPIView(APIView):
    """
    Block uchun 'like' qo'shish (POST) va olib tashlash (DELETE).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, block_pk, *args, **kwargs):
        """
        Block'ga 'like' qo'shadi. Agar 'like' mavjud bo'lsa, xatolik qaytaradi.
        """
        block = get_object_or_404(ItemBlock, pk=block_pk)
        
        # get_or_create yordamida 'like'ni yaratishga harakat qilamiz.
        # Bu metod (obyekt, yaratildi_mi) degan qiymat qaytaradi.
        like, created = Like.objects.get_or_create(user=request.user, block=block)
        
        # Agar 'created' True bo'lsa, demak yangi 'like' yaratildi.
        if created:
            # Yaratilgan like haqida ma'lumotni qaytaramiz
            serializer = LikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Agar 'created' False bo'lsa, demak bu 'like' avvaldan mavjud.
        return Response(
            {"detail": "Siz bu elementga allaqachon like bosgansiz."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, block_pk, *args, **kwargs):
        """
        Block'dan 'like'ni olib tashlaydi. Agar 'like' mavjud bo'lmasa, 404 xatolik qaytaradi.
        """
        block = get_object_or_404(ItemBlock, pk=block_pk)
        
        # O'chirilishi kerak bo'lgan 'like'ni topamiz.
        # Faqat shu user'ga va shu block'ga tegishli bo'lishi shart!
        like = get_object_or_404(Like, user=request.user, block=block)
        
        like.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
__all__ = [
    "LikeToggleAPIView",
]