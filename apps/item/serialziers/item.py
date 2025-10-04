from modeltranslation.utils import get_language
from rest_framework import serializers

from apps.item.models import Item, Category
from apps.common.services.languagemixin import LocalizedSerializerMixin


class ItemSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    translatable_fields = ['title']

    title_ru = serializers.CharField(required=False)
    title_en = serializers.CharField(required=False)
    title_uz = serializers.CharField()

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Item
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "logo",
            "category"
        )

    def to_representation(self, instance):
        lang = get_language()
        instance = {
            'id': instance.id,
            'title': instance.title,
            'category': instance.category.id if instance.category else None,
            'logo': instance.logo,
            'slug': instance.slug,
        }

        return instance