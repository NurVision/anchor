from django.conf import settings


class MultilingualAdminMixin:
    """
    Mixin for handling multilingual fields in Django admin
    """

    def get_fieldsets(self, request, obj=None):
        """
        Dynamically create fieldsets for each language
        """
        fieldsets = list(super().get_fieldsets(request, obj))

        for lang_code, lang_name in settings.LANGUAGES:
            lang_fields = []

            if hasattr(self.model, f'title_{lang_code}'):
                lang_fields.append(f'title_{lang_code}')

            if hasattr(self.model, f'name_{lang_code}'):
                lang_fields.append(f'name_{lang_code}')

            if hasattr(self.model, f'description_{lang_code}'):
                lang_fields.append(f'description_{lang_code}')

            if lang_fields:
                fieldsets.append((
                    f'{lang_name}',
                    {
                        'fields': lang_fields,
                        'classes': ('collapse',) if lang_code != 'uz' else (),
                    }
                ))

        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        """
        Make slug fields readonly (they are auto-generated)
        """
        readonly = list(super().get_readonly_fields(request, obj))

        for lang_code, _ in settings.LANGUAGES:
            slug_field = f'slug_{lang_code}'
            if hasattr(self.model, slug_field) and slug_field not in readonly:
                readonly.append(slug_field)

        if hasattr(self.model, 'slug') and 'slug' not in readonly:
            readonly.append('slug')

        return readonly
