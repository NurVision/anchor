import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

try:
    from transliterate import translit

    HAS_TRANSLITERATE = True
except ImportError:
    HAS_TRANSLITERATE = False


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def soft_delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.is_active = False
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.is_active = True
        self.save(update_fields=["is_deleted", "deleted_at"])


class VersionHistory(BaseModel):
    version = models.CharField(_("Version"), max_length=64)
    required = models.BooleanField(_("Required"), default=True)

    class Meta:
        verbose_name = _("Version history")
        verbose_name_plural = _("Version histories")

    def __str__(self):
        return self.version


class FrontendTranslation(BaseModel):
    key = models.CharField(_("Key"), max_length=255, unique=True)
    text = models.CharField(_("Text"), max_length=1024)

    class Meta:
        verbose_name = _("Frontend translation")
        verbose_name_plural = _("Frontend translations")

    def __str__(self):
        return str(self.key)


class SlugMixin(models.Model):
    slug = models.SlugField(max_length=255, blank=True, unique=False)

    class Meta:
        abstract = True

    def generate_slug(self, source_text, slug_field):
        if not source_text:
            return ""

        if HAS_TRANSLITERATE:
            try:
                transliterated = translit(source_text, "ru", reversed=True)
                slug = slugify(transliterated)
            except Exception:
                slug = slugify(source_text)
        else:
            slug = slugify(source_text)

        original_slug = slug
        counter = 1
        while self.__class__.objects.filter(**{slug_field: slug}).exclude(pk=self.pk).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        return slug

    def save(self, *args, **kwargs):
        """
        Автоматическая генерация единого slug на основе первого непустого title_xx.
        """
        # Проверяем, нужно ли регенерировать slug
        update_fields = kwargs.get('update_fields', None)
        should_generate_slug = update_fields is None or any(
            f'title_{lang}' in update_fields or 'slug' in update_fields
            for lang, _ in settings.LANGUAGES
        )

        if should_generate_slug:
            # Берём первый заполненный title_xx
            source_title = None
            for lang_code, _ in settings.LANGUAGES:
                title_field = f"title_{lang_code}"
                if hasattr(self, title_field):
                    val = getattr(self, title_field, None)
                    if val:
                        source_title = val
                        break

            # Генерируем slug только если нашли хотя бы один title
            if source_title:
                self.slug = self.generate_slug(source_title, "slug")

        super().save(*args, **kwargs)