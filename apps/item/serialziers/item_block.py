from modeltranslation.utils import get_language
from rest_framework import serializers

from apps.item.models import Item, ItemBlock
from apps.common.services.languagemixin import LocalizedSerializerMixin


class ItemBlockSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
    translatable_fields = ['title']

    title_ru = serializers.CharField(required=False)
    title_en = serializers.CharField(required=False)
    title_uz = serializers.CharField()

    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = ItemBlock
        fields = (
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "item",
            "type",
            "url",
            "appstore",
            "playstore",
            "latitude",
            "longitude"
        )

    def to_representation(self, instance):
        lang = get_language()
        instance = {
            'id': instance.id,
            'title': instance.title,
            'item': instance.item.id if instance.item else None,
            "type": instance.type,
            "url": instance.url,
            "appstore": instance.appstore,
            "playstore": instance.playstore,
            "latitude":instance.latitude,
            "longitude": instance.longitude
        }

        return instance