from django.contrib import admin

from .models import Comment, SearchHistory, View, Like, Review, Bookmark

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "block__title",)
    list_display_links = ("id",)


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user__username", "query", "block__title", "created_at")
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