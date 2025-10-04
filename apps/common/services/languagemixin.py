from django.utils.translation import get_language


class LocalizedSerializerMixin:
    """
    Mixin for DRF serializers to automatically return localized fields
    based on Accept-Language header.

    Usage:
        class ArticleSerializer(LocalizedSerializerMixin, serializers.ModelSerializer):
            translatable_fields = ['title', 'description', 'slug']
    """
    translatable_fields = []

    def to_representation(self, instance):

        lang = get_language() or 'uz'
        data = super().to_representation(instance)

        for field in self.translatable_fields:
            translated_field = f"{field}_{lang}"
            if hasattr(instance, translated_field):
                data[field] = getattr(instance, translated_field)
            else:

                fallback_field = f"{field}_uz"
                if hasattr(instance, fallback_field):
                    data[field] = getattr(instance, fallback_field)

        return data
