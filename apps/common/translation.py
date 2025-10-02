from modeltranslation.translator import register, TranslationOptions

from apps.item.models import Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title", "slug",)
