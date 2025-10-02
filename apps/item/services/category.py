from django.db.models import Prefetch, Q
from django.utils.translation import get_language

from apps.item.models import Category


class CategoryService:

    @staticmethod
    def get_all_categories_flat(level=None, parent_id=None):
        """
        Get all categories as flat list

        Args:
            level: Filter by level (0, 1, or 2)
            parent_id: Filter by parent
        """
        queryset = Category.objects.select_related('parent').all()

        if level is not None:
            queryset = queryset.filter(level=level)

        if parent_id is not None:
            queryset = queryset.filter(parent_id=parent_id)

        return queryset

    @staticmethod
    def get_category_tree():
        """Get full category tree starting from root"""

        queryset = Category.objects.filter(parent=None).prefetch_related(
            Prefetch(
                'children',
                queryset=Category.objects.prefetch_related('children')
            )
        )
        return queryset

    @staticmethod
    def get_category_by_slug(slug, language=None):
        """
        Get category by slug in specific language

        Args:
            slug: Category slug
            language: Language code (uz, ru, en)
        """
        if not language:
            language = get_language()

        filter_kwargs = {f'slug_{language}': slug}

        try:
            category = Category.objects.select_related('parent').get(
                **filter_kwargs
            )
        except Category.DoesNotExist:
            category = Category.objects.select_related('parent').get(slug=slug)

        return category

    @staticmethod
    def get_category_with_children(category_id):
        """Get category with all nested children"""
        category = Category.objects.prefetch_related(
            Prefetch(
                'children',
                queryset=Category.objects.prefetch_related('children')
            )
        ).get(id=category_id)

        return category

    @staticmethod
    def get_leaf_categories():
        """Get only leaf categories (categories without children)"""

        return Category.objects.filter(children__isnull=True)

    @staticmethod
    def get_root_categories():
        """Get only root categories (top level)"""
        return Category.objects.filter(parent=None)

    @staticmethod
    def search_categories(query, language=None):
        """Search categories by title"""
        if not language:
            language = get_language()

        filter_field = f'title_{language}__icontains'

        return Category.objects.filter(
            Q(**{filter_field: query})
        ).select_related('parent')
