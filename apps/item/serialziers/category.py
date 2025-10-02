from django.utils.translation import get_language
from rest_framework import serializers

from apps.item.models import Category


class CategoryFlatSerializer(serializers.ModelSerializer):
    """Flat serializer - shows category with translated fields"""
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    parent_id = serializers.IntegerField(source='parent.id', read_only=True, allow_null=True)
    parent_title = serializers.SerializerMethodField()
    is_root = serializers.BooleanField(read_only=True)
    is_leaf = serializers.BooleanField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'level',
            'parent_id',
            'parent_title',
            'is_root',
            'is_leaf'
        ]

    def get_title(self, obj):
        lang = self.context.get('language', get_language())
        return getattr(obj, f'title_{lang}', obj.title)

    def get_slug(self, obj):
        lang = self.context.get('language', get_language())
        return getattr(obj, f'slug_{lang}', obj.slug)

    def get_parent_title(self, obj):
        if obj.parent:
            lang = self.context.get('language', get_language())
            return getattr(obj.parent, f'title_{lang}', obj.parent.title)
        return None


class CategoryTreeSerializer(serializers.ModelSerializer):
    """Recursive tree serializer - shows nested children"""
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    is_root = serializers.BooleanField(read_only=True)
    is_leaf = serializers.BooleanField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'level',
            'is_root',
            'is_leaf',
            'children'
        ]

    def get_title(self, obj):
        lang = self.context.get('language', get_language())
        return getattr(obj, f'title_{lang}', obj.title)

    def get_slug(self, obj):
        lang = self.context.get('language', get_language())
        return getattr(obj, f'slug_{lang}', obj.slug)

    def get_children(self, obj):
        """Recursively serialize children"""
        if obj.is_leaf:
            return []

        children = obj.children.all()
        serializer = CategoryTreeSerializer(
            children,
            many=True,
            context=self.context
        )
        return serializer.data


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with ancestors and descendants"""
    title = serializers.SerializerMethodField()
    slug = serializers.SerializerMethodField()
    parent = CategoryFlatSerializer(read_only=True)
    ancestors = serializers.SerializerMethodField()
    children = CategoryFlatSerializer(many=True, read_only=True)
    breadcrumb = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
            'level',
            'parent',
            'ancestors',
            'children',
            'breadcrumb',
            'is_root',
            'is_leaf'
        ]

    def get_title(self, obj):
        lang = self.context.get('language', get_language())
        return getattr(obj, f'title_{lang}', obj.title)

    def get_slug(self, obj):
        lang = self.context.get('language', get_language())
        return getattr(obj, f'slug_{lang}', obj.slug)

    def get_ancestors(self, obj):
        """Get all parent categories"""
        ancestors = list(obj.get_ancestors())
        return CategoryFlatSerializer(
            ancestors,
            many=True,
            context=self.context
        ).data

    def get_breadcrumb(self, obj):
        """Get breadcrumb path as string"""
        lang = self.context.get('language', get_language())
        ancestors = list(obj.get_ancestors())
        breadcrumb_items = [
            getattr(ancestor, f'title_{lang}', ancestor.title)
            for ancestor in ancestors
        ]
        breadcrumb_items.append(getattr(obj, f'title_{lang}', obj.title))
        return ' > '.join(breadcrumb_items)
