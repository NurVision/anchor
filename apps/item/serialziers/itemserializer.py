from modeltranslation.utils import get_language
from rest_framework import serializers

from apps.item.models import Item
from apps.common.services.languagemixin import LocalizedSerializerMixin


class ItemSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    translatable_fields = ['title']

    title_ru = serializers.CharField(required=False)
    title_en = serializers.CharField(required=False)
    title_uz = serializers.CharField()

    class Meta:
        model = Item
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "logo",
        )

    def to_representation(self, instance):
        lang = get_language()
        instance = {
            'id': instance.id,
            'title': instance.title,
            'category': instance.category,
            'logo': str(instance.logo.url) if bool(instance.logo) is not False else '',
            'slug': instance.slug,
        }

        return instance