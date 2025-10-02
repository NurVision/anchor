from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.utils.translation import gettext_lazy as _

from apps.item.models import Item, ItemBlock
from apps.common.models import BaseModel
from apps.users.models import User


class Comment(BaseModel):
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.text


class Searched(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Searched")


class View(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("View")
        verbose_name_plural = _("Views")


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")



# foydalanib bolgandan keyingi sharh
class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0, null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return self.text


class Bookmark(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")