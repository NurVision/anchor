from django.contrib import admin

from .models import Comment, Searched, View, Like, Rate, Review, Bookmark

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "item__title",)
    list_display_links = ("id",)


@admin.register(Searched)
class SearchedAdmin(admin.ModelAdmin):
        list_display = ("id", "item__title",)
        list_display_links = ("id",)


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ("id", "item__title",)
    list_display_links = ("id",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "item__title",)
    list_display_links = ("id",)


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("id", "item__title", "rating")
    list_display_links = ("id",)
    search_fields = ("item__title", "rating")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "item__title",)
    list_display_links = ("id",)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("id", "item__title",)
    list_display_links = ("id",)