from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.item.models import Item
from apps.item.serialziers.item import ItemSerializer


class ItemListAPIView(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemDetailAPIView(RetrieveAPIView):
    serializer_class = ItemSerializer
    permission_classes = []
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        item_slug = self.kwargs.get('slug')
        return Item.objects.filter(slug=item_slug)


class ItemCreateAPIView(CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # permission_classes = [permissions.IsAdminUser,]

    def post(self, request, *args, **kwargs):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemUpdateAPIView(UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # permission_classes = [permissions.IsAdminUser,]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemDeleteAPIView(DestroyAPIView):
    queryset = Item.objects.all()
    # permission_classes = [permissions.IsAdminUser,]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)