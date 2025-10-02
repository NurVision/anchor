from modeltranslation.translator import register, TranslationOptions

from apps.item.models import Category, Item


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)


@register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = ('title', 'slug',)
