from modeltranslation.translator import register, TranslationOptions

from apps.item.models import Item, Category, Subcategory, Childcategory


@register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)

@register(Subcategory)
class SubcategoryTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)

@register(Childcategory)
class ChildcategoryTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)