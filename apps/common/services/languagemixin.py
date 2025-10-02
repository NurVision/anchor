from django.utils.translation import get_language

class LocalizedSerializerMixin:
    translatable_fields = []  # задаются в наследниках

    def to_representation(self, instance):
        lang = get_language() or 'ru'
        data = super().to_representation(instance)

        for field in self.translatable_fields:
            translated_field = f"{field}_{lang}"
            if hasattr(instance, translated_field):
                data[field] = getattr(instance, translated_field)
        return data