# your_app/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Obyekt egasi bo'lmagan foydalanuvchilarga faqat o'qish huquqini beradi.
    """
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS kabi xavfsiz so'rovlarga har doim ruxsat beriladi.
        if request.method in SAFE_METHODS:
            return True

        # Yozish (o'zgartirish, o'chirish) huquqi faqat obyekt egasiga beriladi.
        return obj.user == request.user