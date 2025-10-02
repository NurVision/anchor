from modeltranslation.translator import register, TranslationOptions

from apps.item.models import Item, Category, SubcCategory, ChildCategory


@register(Item)
class ItemTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)

@register(SubcCategory)
class SubcategoryTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)

@register(ChildCategory)
class ChildCategoryTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)