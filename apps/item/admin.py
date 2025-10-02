from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Item, ItemBlock, Category, SubcCategory, ChildCategory


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
class CategoryAdmin(admin.ModelAdmin):
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
    )


@admin.register(SubcCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent__title")
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
            'fields': ("parent",)
        }),
    )


@admin.register(ChildCategory)
class ChildCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent__title")
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
            'fields': ("parent",)
        }),
    )
