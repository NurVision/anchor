from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from apps.reaction.models import SearchHistory, ItemBlock
from apps.reaction.serializers.search_history import SearchHistorySerializer

class SearchHistoryListAPIView(APIView):
    """
    Foydalanuvchining qidiruv tarixini olish (GET).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Foydalanuvchining barcha qidiruv tarixini qaytaradi.
        """
        history_items = (
            SearchHistory.objects
            .filter(user=request.user)
            .select_related('block__item')
            .order_by('-created_at')
        )
        serializer = SearchHistorySerializer(history_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchHistoryCreateAPIView(APIView):
    """
    Yangi qidiruv tarix yozuvini yaratish (POST).
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['query', 'block_id'],
            properties={
                'query': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Qidiruv so'zi (matn)",
                    example="iPhone 15"
                ),
                'block_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ItemBlock ID raqami",
                    example=3
                ),
            },
        ),
        responses={201: SearchHistorySerializer},
        operation_summary="Qidiruv tarixiga yangi yozuv qo'shish",
        operation_description="Kerakli maydonlar: query (str), block_id (int).",
    )
    def post(self, request, *args, **kwargs):
        serializer = SearchHistorySerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        block_id = validated_data['block_id']
        query = validated_data['query']

        block = get_object_or_404(ItemBlock, pk=block_id)

        new_history_item = SearchHistory.objects.create(
            user=request.user,
            query=query,
            block=block
        )

        response_serializer = SearchHistorySerializer(new_history_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class SearchHistoryClearAPIView(APIView):
    """Foydalanuvchining barcha qidiruv tarixini o'chirish."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        deleted_count, _ = SearchHistory.objects.filter(user=request.user).delete()
        return Response(
            {"message": f"{deleted_count} ta yozuv o'chirildi."},
            status=status.HTTP_204_NO_CONTENT
        )


__all__ = [
    "SearchHistoryListAPIView",
    "SearchHistoryClearAPIView",
    "SearchHistoryCreateAPIView",
]
