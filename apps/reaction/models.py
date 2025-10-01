from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.utils.translation import gettext_lazy as _

from apps.item.models import Item
from apps.common.models import BaseModel


class Comment(models.Model, BaseModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.text


class Searched(models.Model, BaseModel):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Searched")


class View(models.Model, BaseModel):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("View")
        verbose_name_plural = _("Views")


class Like(models.Model, BaseModel):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")


class Rate(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = _("Rate")
        verbose_name_plural = _("Rates")

    def __str__(self):
        return str(self.rating)


class Review(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return self.text


class Bookmark(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")