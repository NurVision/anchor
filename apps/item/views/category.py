from django.utils.translation import get_language
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.services.paginator import StandardResultsSetPagination
from apps.item.models import Category
from apps.item.serialziers.category import CategoryFlatSerializer, CategoryDetailSerializer, CategoryTreeSerializer
from apps.item.services.category import CategoryService


class CategoryListView(generics.ListAPIView):
    serializer_class = CategoryFlatSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = get_language()
        return context

    def get_queryset(self):
        queryset = Category.objects.select_related('parent').all()

        level = self.request.query_params.get('level')
        if level is not None:
            try:
                queryset = queryset.filter(level=int(level))
            except ValueError:
                pass

        parent_id = self.request.query_params.get('parent_id')
        if parent_id:
            try:
                queryset = queryset.filter(parent_id=int(parent_id))
            except ValueError:
                pass

        search = self.request.query_params.get('search')
        if search:
            lang = get_language()
            filter_field = f'title_{lang}__icontains'
            queryset = queryset.filter(**{filter_field: search})

        return queryset


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.select_related('parent').prefetch_related('children')
    serializer_class = CategoryDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = get_language()
        return context


class CategoryTreeView(APIView):

    def get(self, request):
        categories = CategoryService.get_category_tree()
        serializer = CategoryTreeSerializer(
            categories,
            many=True,
            context={'language': get_language(), 'request': request}
        )
        return Response(serializer.data)


class CategoryRootsView(generics.ListAPIView):
    serializer_class = CategoryFlatSerializer

    def get_queryset(self):
        return CategoryService.get_root_categories()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = get_language()
        return context


class CategoryLeavesView(generics.ListAPIView):
    serializer_class = CategoryFlatSerializer

    def get_queryset(self):
        return CategoryService.get_leaf_categories()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['language'] = get_language()
        return context


class CategoryBySlugView(APIView):

    def get(self, request, slug):
        try:
            category = CategoryService.get_category_by_slug(slug)
            serializer = CategoryDetailSerializer(
                category,
                context={'language': get_language(), 'request': request}
            )
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(
                {'detail': 'Category not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class CategoryChildrenView(generics.ListAPIView):
    serializer_class = CategoryFlatSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = CategoryService.get_category_by_slug(slug)
        return category.children.all()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["language"] = get_language()
        return ctx


class CategoryAncestorsView(generics.ListAPIView):
    serializer_class = CategoryFlatSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        category = CategoryService.get_category_by_slug(slug)
        return category.get_ancestors()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["language"] = get_language()
        return ctx
