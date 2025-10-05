from modeltranslation.utils import get_language
from rest_framework import serializers

from apps.item.models import Item, Category, Keyword
from apps.common.services.languagemixin import LocalizedSerializerMixin


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name']


class ItemSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    translatable_fields = ['title']

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    keywords = KeywordSerializer(
        many=True,
        read_only=True,
        source="get_keywords"
    )

    class Meta:
        model = Item
        fields = (
            "id",
            "title",
            "logo",
            "category",
            "keywords"
        )

    def to_representation(self, instance):
        lang = get_language()
        representation = super().to_representation(instance)

        representation['title'] = getattr(instance, f"title_{lang}", instance.title)
        representation['category'] = (
            instance.category.id if instance.category else None
        )
        representation['slug'] = instance.slug

        return representation