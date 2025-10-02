from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin

from apps.item.models import ItemBlock, Item, Category


class ItemBlockInline(admin.TabularInline):
    model = ItemBlock


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)

    fieldsets = (
        (_("Uzbek"), {
            'fields': ('title_uz',)
        }),
        (_("English"), {
            'fields': ('title_en',)
        }),
        (_("Russian"), {
            'fields': ('title_ru',)
        }),
        (_("Main"), {
            'fields': ("category",)
        }),
    )

    inlines = [ItemBlockInline]


@admin.register(ItemBlock)
class ItemBlockAdmin(admin.ModelAdmin):
    list_display = ("id", "item__title",)
    list_display_links = ("id", "item__title")
    search_fields = ("item__title",)
    list_filter = ("type",)


@admin.register(Category)
class CategoryAdminTabbed(TabbedTranslationAdmin):
    list_display = ("id", "title", "parent", "level", "slug")
    list_display_links = ("id", "title")
    search_fields = ("title_uz", "title_en", "title_ru", "slug")
    list_filter = ("level",)
    readonly_fields = ("level",)

    fields = ('parent', 'title', 'slug', 'level')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.filter(level__lt=2)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
