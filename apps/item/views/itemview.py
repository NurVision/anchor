from rest_framework import permissions, status, parsers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.item.models import Item
from apps.item.serialziers.itemserializer import ItemSerializer


class ItemAPIView(GenericAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    # parser_classes = [parsers.MultiPartParser, parsers.FormParser]


    def get(self, request, *args, **kwargs):
        items = self.get_queryset()
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Item.objects.all()  # ✅ всегда заново вызываем .all()

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data, partial=True)  # ✅ лучше partial=True для PATCH
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
