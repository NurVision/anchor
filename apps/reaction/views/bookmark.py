from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from apps.reaction.models import Bookmark
from apps.reaction.serializers.bookmark import BookmarkSerializer

class BookmarkListCreateAPIView(APIView):
    """
    Foydalanuvchi uchun bookmark'lar ro'yxatini olish va yangi bookmark yaratish.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Autentifikatsiyadan o'tgan foydalanuvchining barcha bookmark'larini qaytaradi.
        """
        # Faqat so'rov yuborayotgan user'ga tegishli bookmark'larni filterlaymiz
        bookmarks = Bookmark.objects.filter(user=request.user)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Yangi bookmark yaratadi.
        """
        # Serializer'ga context orqali request'ni uzatamiz,
        # bu validate method'ida user'ni olish uchun kerak.
        serializer = BookmarkSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # User'ni avtomatik tarzda request'dan olib saqlaymiz
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookmarkDestroyAPIView(APIView):
    """
    Ma'lum bir bookmark'ni ID bo'yicha o'chirish.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        """
        ID (pk) bo'yicha bookmark'ni o'chiradi.
        """
        # Bookmark'ni topishga harakat qilamiz.
        # Muhim: faqat shu user'ga tegishli ekanligini ham tekshiramiz.
        # Agar boshqa user'ning bookmark'ini o'chirishga harakat qilinsa, 404 xatolik qaytadi.
        bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
        
        bookmark.delete()
        
        # O'chirish muvaffaqiyatli bo'lsa, bo'sh javob qaytaramiz.
        return Response(status=status.HTTP_204_NO_CONTENT)
    
__all__ = [
    "BookmarkListCreateAPIView",
    "BookmarkDestroyAPIView",
]