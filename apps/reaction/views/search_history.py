from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from apps.reaction.models import SearchHistory, ItemBlock
from apps.reaction.serializers.search_history import SearchHistorySerializer

class SearchHistoryListCreateAPIView(APIView):
    """
    Qidiruv tarixini ro'yxatini olish (GET) va yangi yozuv qo'shish (POST).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Foydalanuvchining qidiruv tarixini oxirgisidan boshlab qaytaradi.
        Optimallashtirish: block va uning item'ini bitta so'rovda olish uchun 'select_related' ishlatiladi.
        """
        history_items = SearchHistory.objects.filter(user=request.user) \
                                             .select_related('block__item')
        
        serializer = SearchHistorySerializer(history_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Qidiruv tarixiga yangi yozuv qo'shadi (qidiruv so'zi + bosilgan block).
        """
        serializer = SearchHistorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        block_id = validated_data['block_id']
        query = validated_data['query']
        
        block = get_object_or_404(ItemBlock, pk=block_id)
        
        # Eskisini o'chirib, yangisini yaratish mantiqi (agar kerak bo'lsa)
        # Hozircha har bir bosishni alohida tarix sifatida saqlaymiz.
        # Agar bir xil so'rov va bosish qaytarilsa, vaqtini yangilash kerak bo'lsa,
        # avval o'chirib, keyin yaratish mumkin.
        # SearchHistory.objects.filter(user=request.user, query=query, block=block).delete()
        
        new_history_item = SearchHistory.objects.create(
            user=request.user, 
            query=query, 
            block=block
        )
        
        response_serializer = SearchHistorySerializer(new_history_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class SearchHistoryClearAPIView(APIView):
    """
    Foydalanuvchining barcha qidiruv tarixini tozalash uchun.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        SearchHistory.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
__all__ = [
    "SearchHistoryListCreateAPIView",       
    "SearchHistoryClearAPIView",
]