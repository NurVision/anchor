from django.contrib import admin

from .models import Comment, Searched, View, Like, Review, Bookmark

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "block__title",)
    list_display_links = ("id",)


@admin.register(Searched)
class SearchedAdmin(admin.ModelAdmin):
        list_display = ("id", "block__title",)
        list_display_links = ("id",)


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ("id", "block__title",)
    list_display_links = ("id",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "block__title",)
    list_display_links = ("id",)



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "block__title",)
    list_display_links = ("id",)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("id", "block__title",)
    list_display_links = ("id",)