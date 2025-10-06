from django.urls import path

from .views import (
    BookmarkListAPIView,
    BookmarkCreateAPIView,
    BookmarkDestroyAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
    CommentCreateAPIView,
    CommentDeleteAPIView,
    LikeToggleAPIView,
    ReviewDetailAPIView,
    ReviewListCreateAPIView,
    SearchHistoryClearAPIView,
    SearchHistoryListAPIView,
    SearchHistoryCreateAPIView,
)


app_name = 'apps.reaction'

urlpatterns = [
    path('bookmarks/', BookmarkListAPIView.as_view(), name='bookmark-list'),
    path('bookmarks/create/', BookmarkCreateAPIView.as_view(), name='bookmark-create'),
    path('bookmarks/<int:pk>/', BookmarkDestroyAPIView.as_view(), name='bookmark-destroy'),
    path('comments/<int:block_pk>/', CommentListAPIView.as_view(), name='comment-list'),
    path('comments/create/<int:block_pk>/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/<int:id>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('comments/delete/<int:pk>/', CommentDeleteAPIView.as_view(), name='comment-delete'),
    path('blocks/<int:block_pk>/like/', LikeToggleAPIView.as_view(), name='like-toggle'),
    path('blocks/<int:block_pk>/reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('search-history/', SearchHistoryListAPIView.as_view(), name='search-history-list-create'),
    path('search-history/create/', SearchHistoryCreateAPIView.as_view(), name='search-history-create'),
    path('search-history/clear/', SearchHistoryClearAPIView.as_view(), name='search-history-clear'),
]
