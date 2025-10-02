from django.db import models

from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title


class SubcCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Subcategory")
        verbose_name_plural = _("Subcategories")

    def __str__(self):
        return self.title


class ChildCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    parent = models.ForeignKey(SubcCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Childcategory")
        verbose_name_plural = _("Childcategories")

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    logo = models.ImageField(upload_to="item/logo/", blank=True, null=True)
    category = models.ForeignKey(ChildCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def __str__(self):
        return self.title


class ItemBlock(models.Model):
    TYPE_CHOICES = (
        ("website", "Website"),
        ("app", "App"),
        ("location", "Location"),
    )

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    url = models.URLField()
    appstore = models.CharField(max_length=255)
    playstore = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Item block")
        verbose_name_plural = _("Item blocks")

    def __str__(self):
        return self.type