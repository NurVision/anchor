from django.db import models

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.common.models import SlugMixin


class Category(SlugMixin):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    level = models.PositiveSmallIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['level', 'title']
        indexes = [
            models.Index(fields=['parent', 'level']),
        ]

    def __str__(self):
        return self.title

    def clean(self):
        if self.parent:
            if self.parent.level >= 2:
                raise ValidationError("Category tree cannot be deeper than 3 levels")
            if self.parent == self:
                raise ValidationError("Category cannot be its own parent")

    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0
        self.full_clean()
        super().save(*args, **kwargs)

    def get_ancestors(self):
        """Get all parent categories up to root"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return reversed(ancestors)

    def get_descendants(self):
        """Get all child categories recursively"""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    @property
    def is_root(self):
        return self.parent is None

    @property
    def is_leaf(self):
        return not self.children.exists()


class Item(SlugMixin):
    title = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="item/logo/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

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
    url = models.URLField(null=True, blank=True)
    appstore = models.CharField(max_length=255, null=True, blank=True)
    playstore = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Item block")
        verbose_name_plural = _("Item blocks")

    def __str__(self):
        return self.type
