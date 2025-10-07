from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.common.models import SlugMixin, BaseModel


class Category(SlugMixin):
    slug = models.SlugField(unique=True, blank=True, editable=False)
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
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def _generate_unique_slug(self):
        """Generate unique slug from title"""
        base_slug = slugify(self.title)
        if not base_slug:
            base_slug = f"category-{self.pk or ''}"

        slug = base_slug
        counter = 1

        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def clean(self):
        if self.parent:
            if self.parent.level >= 2:
                raise ValidationError(_("Category tree cannot be deeper than 3 levels"))
            if self.parent_id == self.pk:
                raise ValidationError(_("Category cannot be its own parent"))

    def save(self, *args, **kwargs):
        self.level = self.parent.level + 1 if self.parent else 0

        if not self.slug or (self.pk and self._title_changed()):
            self.slug = self._generate_unique_slug()

        self.full_clean()
        super().save(*args, **kwargs)

    def _title_changed(self):
        """Check if title has changed"""
        if not self.pk:
            return True
        try:
            old_instance = Category.objects.only('title').get(pk=self.pk)
            return old_instance.title != self.title
        except Category.DoesNotExist:
            return True

    def get_ancestors(self):
        """Get all parent categories up to root"""
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return list(reversed(ancestors))

    def get_descendants(self):
        """Get all child categories recursively"""
        descendants = []
        for child in self.children.all():
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants

    @property
    def is_root(self):
        return self.parent_id is None

    @property
    def is_leaf(self):
        return not self.children.exists()


class Keyword(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Keyword")
        verbose_name_plural = _("Keywords")

    def __str__(self):
        return self.name


class Item(SlugMixin):
    slug = models.SlugField()
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    logo = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_("Logo URL")
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        verbose_name=_("Category"),
        related_name='items'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description")
    )

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_keywords(self):
        return [ik.keyword for ik in self.item_keywords.all()]


class ItemKeyword(BaseModel):
    keyword = models.ForeignKey(
        'Keyword',
        on_delete=models.CASCADE,
        verbose_name=_("Keyword"),
        related_name='item_keywords'
    )
    item = models.ForeignKey(
        'Item',
        on_delete=models.CASCADE,
        verbose_name=_("Item"),
        related_name='item_keywords'
    )

    class Meta:
        verbose_name = _("Item Keyword")
        verbose_name_plural = _("Item Keywords")
        ordering = ['item', 'keyword']

    def __str__(self):
        return f"{self.item.title} - {self.keyword.name}"


class ItemBlock(BaseModel):
    TYPE_CHOICES = (
        ("website", _("Website")),
        ("app", _("App")),
        ("location", _("Location")),
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        verbose_name=_("Item"),
        related_name='blocks'
    )
    type = models.CharField(
        max_length=255,
        choices=TYPE_CHOICES,
        verbose_name=_("Type")
    )
    url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("URL"),
        help_text=_("Website URL (for website type)")
    )
    appstore = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("App Store ID"),
        help_text=_("Apple App Store ID (for app type)")
    )
    playstore = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Play Store ID"),
        help_text=_("Google Play Store package name (for app type)")
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name=_("Latitude"),
        help_text=_("Location latitude (for location type)")
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name=_("Longitude"),
        help_text=_("Location longitude (for location type)")
    )

    class Meta:
        verbose_name = _("Item block")
        verbose_name_plural = _("Item blocks")

    def __str__(self):
        return f"{self.item.title} - {self.get_type_display()}"

    def clean(self):
        """Validate that required fields are filled based on type"""
        if self.type == 'website' and not self.url:
            raise ValidationError({'url': _('URL is required for website type')})

        if self.type == 'app':
            if not self.appstore and not self.playstore:
                raise ValidationError({
                    'appstore': _('At least one app store link is required for app type'),
                    'playstore': _('At least one app store link is required for app type')
                })

        if self.type == 'location':
            if not self.latitude or not self.longitude:
                raise ValidationError({
                    'latitude': _('Coordinates are required for location type'),
                    'longitude': _('Coordinates are required for location type')
                })
