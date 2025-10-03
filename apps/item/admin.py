from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _, get_language

from apps.item.models import ItemBlock, Item, Category, ItemKeyword, Keyword
from apps.item.services.item_admin import MultilingualAdminMixin


class ItemBlockInline(admin.TabularInline):
    model = ItemBlock


@admin.register(ItemBlock)
class ItemBlockAdmin(MultilingualAdminMixin, admin.ModelAdmin):
    list_display = ("id", "get_title_display", "get_item_title", "type", "get_links_display")
    list_display_links = ("id", "get_title_display")
    search_fields = ("title", "item__title")
    list_filter = ("type",)
    autocomplete_fields = ['item']

    fieldsets = [
        (_('Basic Information'), {
            'fields': ('title_uz', 'title_ru', 'title_en', 'item', 'type'),
        }),
        (_('Website'), {
            'fields': ('url',),
            'classes': ('collapse',),
            'description': _('Fill this section only for Website type')
        }),
        (_('Mobile App'), {
            'fields': ('appstore', 'playstore'),
            'classes': ('collapse',),
            'description': _('Fill this section only for App type')
        }),
        (_('Location'), {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',),
            'description': _('Fill this section only for Location type')
        }),
    ]

    def get_title_display(self, obj):
        """Display title in current language or fallback"""
        if hasattr(obj, 'title'):
            return obj.title

        # Try to get title in current language
        current_lang = get_language()[:2]  # Get 'uz' from 'uz-uz'

        if hasattr(obj, f'title_{current_lang}'):
            return getattr(obj, f'title_{current_lang}') or obj.title_uz or '-'

        return obj.title_uz if hasattr(obj, 'title_uz') else '-'

    get_title_display.short_description = _('Title')
    get_title_display.admin_order_field = 'title_uz'  # Allow sorting

    def get_item_title(self, obj):
        """Display item title in current language or fallback"""
        if not obj.item:
            return '-'

        if hasattr(obj.item, 'title'):
            return obj.item.title

        # Try to get title in current language
        current_lang = get_language()[:2]  # Get 'uz' from 'uz-uz'

        if hasattr(obj.item, f'title_{current_lang}'):
            return getattr(obj.item, f'title_{current_lang}') or obj.item.title_uz or '-'

        return obj.item.title_uz if hasattr(obj.item, 'title_uz') else '-'

    get_item_title.short_description = _('Item')
    get_item_title.admin_order_field = 'item__title_uz'  # Allow sorting

    def get_links_display(self, obj):
        """Display relevant links based on type"""
        if obj.type == 'website':
            if obj.url:
                return f'🌐 {obj.url[:50]}{"..." if len(obj.url) > 50 else ""}'
            return '-'

        elif obj.type == 'app':
            links = []
            if obj.appstore:
                links.append(f'🍎 App Store')
            if obj.playstore:
                links.append(f'🤖 Play Store')
            return ' | '.join(links) if links else '-'

        elif obj.type == 'location':
            if obj.latitude and obj.longitude:
                return f'📍 {obj.latitude}, {obj.longitude}'
            return '-'

        return '-'

    get_links_display.short_description = _('Links/Details')

    def get_search_results(self, request, queryset, search_term):
        """
        Enhanced search including multilingual fields
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            from django.db.models import Q
            q_objects = Q()

            # Search in base title field if exists
            if hasattr(self.model, 'title'):
                q_objects |= Q(title__icontains=search_term)

            # Search in base item title field if exists
            if hasattr(self.model._meta.get_field('item').related_model, 'title'):
                q_objects |= Q(item__title__icontains=search_term)

            # Search in multilingual title fields
            for lang_code, _ in settings.LANGUAGES:
                title_field = f'title_{lang_code}'
                if hasattr(self.model, title_field):
                    q_objects |= Q(**{f'{title_field}__icontains': search_term})

                # Search in multilingual item title fields
                item_title_field = f'item__title_{lang_code}'
                try:
                    if hasattr(self.model._meta.get_field('item').related_model, f'title_{lang_code}'):
                        q_objects |= Q(**{f'{item_title_field}__icontains': search_term})
                except:
                    pass

            if q_objects:
                queryset |= self.model.objects.filter(q_objects)

        return queryset, use_distinct


@admin.register(Category)
class CategoryAdmin(MultilingualAdminMixin, admin.ModelAdmin):
    list_display = ("id", "get_title_display", "parent", "level")
    list_display_links = ("id", "get_title_display")
    search_fields = ("title", "slug")
    list_filter = ("level",)
    readonly_fields = ("level", "slug")
    autocomplete_fields = ['parent']
    list_per_page = 50

    fieldsets = [
        (_('Basic Information'), {
            'fields': ('parent', 'level', 'slug'),
        }),
    ]

    def get_title_display(self, obj):
        """Display title in current language or fallback"""
        if hasattr(obj, 'title'):
            return obj.title

        # Try to get title in current language
        current_lang = get_language()[:2]  # Get 'uz' from 'uz-uz'

        if hasattr(obj, f'title_{current_lang}'):
            return getattr(obj, f'title_{current_lang}') or obj.title_uz or '-'

        return obj.title_uz if hasattr(obj, 'title_uz') else '-'

    get_title_display.short_description = _('Title')
    get_title_display.admin_order_field = 'title_uz'  # Allow sorting

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit parent categories to level < 2"""
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.filter(level__lt=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_search_results(self, request, queryset, search_term):
        """
        Enhanced search for autocomplete including multilingual fields
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            from django.db.models import Q
            q_objects = Q()

            # Search in base title field if exists
            if hasattr(self.model, 'title'):
                q_objects |= Q(title__icontains=search_term)

            # Search in multilingual title fields
            for lang_code, _ in settings.LANGUAGES:
                title_field = f'title_{lang_code}'
                if hasattr(self.model, title_field):
                    q_objects |= Q(**{f'{title_field}__icontains': search_term})

            if q_objects:
                queryset |= self.model.objects.filter(q_objects)

        return queryset, use_distinct


class ItemKeywordInline(admin.TabularInline):
    model = ItemKeyword
    extra = 1
    autocomplete_fields = ['keyword']
    verbose_name = _("Keyword")
    verbose_name_plural = _("Keywords")


@admin.register(Keyword)
class KeywordAdmin(MultilingualAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_item_count']
    search_fields = ['name', 'slug']
    list_per_page = 50

    fieldsets = [
        (_('Basic Information'), {
            'fields': ('name', 'slug'),
        }),
    ]

    def get_item_count(self, obj):
        """Display count of items using this keyword"""
        return obj.item_keywords.count()

    get_item_count.short_description = _('Items Count')

    def get_search_results(self, request, queryset, search_term):
        """
        Enhanced search for autocomplete
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # Search in all language fields
            from django.db.models import Q
            q_objects = Q()

            for lang_code, _ in settings.LANGUAGES:
                name_field = f'name_{lang_code}'
                if hasattr(self.model, name_field):
                    q_objects |= Q(**{f'{name_field}__icontains': search_term})

            queryset |= self.model.objects.filter(q_objects)

        return queryset, use_distinct


@admin.register(Item)
class ItemAdmin(MultilingualAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'category', 'slug', 'get_keywords_display']
    list_filter = ['category']
    search_fields = ['title', 'slug', 'description']
    autocomplete_fields = ['category']
    list_per_page = 50

    fieldsets = [
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'category', 'logo'),
        }),
        (_('Content'), {
            'fields': ('description',),
        }),
    ]

    inlines = [ItemKeywordInline, ItemBlockInline]

    def get_keywords_display(self, obj):
        """Display keywords as comma-separated list"""
        keywords = obj.item_keywords.select_related('keyword').all()[:5]
        keyword_names = [ik.keyword.name for ik in keywords]
        result = ', '.join(keyword_names)

        if obj.item_keywords.count() > 5:
            result += f' (+{obj.item_keywords.count() - 5})'

        return result or '-'

    get_keywords_display.short_description = _('Keywords')

    def get_search_results(self, request, queryset, search_term):
        """
        Enhanced search including multilingual fields
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            from django.db.models import Q
            q_objects = Q()

            for lang_code, _ in settings.LANGUAGES:
                title_field = f'title_{lang_code}'
                desc_field = f'description_{lang_code}'

                if hasattr(self.model, title_field):
                    q_objects |= Q(**{f'{title_field}__icontains': search_term})

                if hasattr(self.model, desc_field):
                    q_objects |= Q(**{f'{desc_field}__icontains': search_term})

            queryset |= self.model.objects.filter(q_objects)

        return queryset, use_distinct


@admin.register(ItemKeyword)
class ItemKeywordAdmin(admin.ModelAdmin):
    list_display = ['item', 'keyword']
    search_fields = ['item__title', 'keyword__name']
    autocomplete_fields = ['item', 'keyword']
    list_per_page = 50

    def get_search_results(self, request, queryset, search_term):
        """
        Enhanced search for autocomplete
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            from django.db.models import Q
            q_objects = Q(item__title__icontains=search_term) | Q(keyword__name__icontains=search_term)

            # Search in multilingual fields
            for lang_code, _ in settings.LANGUAGES:
                if hasattr(Item, f'title_{lang_code}'):
                    q_objects |= Q(**{f'item__title_{lang_code}__icontains': search_term})

                if hasattr(Keyword, f'name_{lang_code}'):
                    q_objects |= Q(**{f'keyword__name_{lang_code}__icontains': search_term})

            queryset |= self.model.objects.filter(q_objects)

        return queryset, use_distinct
