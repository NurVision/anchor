from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.item.models import Item
from apps.item.serialziers.itemserializer import ItemSerializer


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
    permission_classes = [permissions.IsAdminUser,]

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
    permission_classes = [permissions.IsAdminUser,]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemDeleteAPIView(DestroyAPIView):
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAdminUser,]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class ItemListAPIView(ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = Item.objects.all().prefetch_related("item_keywords__keyword")
        search = self.request.query_params.get('search')

        if search:
            base_filter = (
                Q(title_ru__icontains=search) |
                Q(title_en__icontains=search) |
                Q(title_uz__icontains=search) |
                Q(item_keywords__keyword__name__icontains=search)
            )
            queryset = queryset.filter(base_filter).distinct()

        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'Accept-Language',
                openapi.IN_HEADER,
                description="Язык ответа: uz, ru, en",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Поиск по title и keyword",
                type=openapi.TYPE_STRING
            )
        ]
    )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "Bu keyword bilan item topilmadi"})
        return super().list(request, *args, **kwargs)


class ItemAllListAPIView(ListAPIView):
    serializer_class = ItemSerializer
    permission_classes = []
    queryset = Item.objects.all()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)