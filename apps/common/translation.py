from modeltranslation.translator import register, TranslationOptions

from apps.item.models import Category, Item, ItemBlock


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(ItemBlock)
class ItemBlockTranslationOptions(TranslationOptions):
    fields = ("title",)
