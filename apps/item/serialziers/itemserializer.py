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

    title_ru = serializers.CharField(required=False)
    title_en = serializers.CharField(required=False)
    title_uz = serializers.CharField()

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
            "title_uz",
            "title_ru",
            "title_en",
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