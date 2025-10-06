from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.item.models import Item, ItemBlock
from apps.users.models import User


class Comment(BaseModel):
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.text


class SearchHistory(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="search_history",
        verbose_name=_("User")
    )
    query = models.CharField(
        max_length=255,
        verbose_name=_("Search Query")
    )
    block = models.ForeignKey(
        ItemBlock,
        on_delete=models.CASCADE,
        verbose_name=_("Clicked Item Block")
    )

    class Meta:
        verbose_name = _("Search History")
        verbose_name_plural = _("Search Histories")
        ordering = ['-created_at']


class View(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("View")
        verbose_name_plural = _("Views")


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

        unique_together = ('user', 'block')


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0, null=False, blank=False,
                                 validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

        unique_together = ('user', 'block')

    def __str__(self):
        return self.text or f"Review by {self.user}"


class Bookmark(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block = models.ForeignKey(ItemBlock, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")
