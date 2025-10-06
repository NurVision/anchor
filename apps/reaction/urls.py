from django.urls import path

from .views import (
    BookmarkListAPIView,
    BookmarkCreateAPIView,
    BookmarkDestroyAPIView,
    CommentDetailAPIView,
    CommentListCreateAPIView,
    LikeToggleAPIView,
    ReviewDetailAPIView,
    ReviewListCreateAPIView,
    SearchHistoryClearAPIView,
    SearchHistoryListCreateAPIView,
)


app_name = 'apps.reaction'

urlpatterns = [
    path('bookmarks/', BookmarkListAPIView.as_view(), name='bookmark-list-create'),
    path('bookmarks/create/', BookmarkCreateAPIView.as_view(), name='bookmark-create'),
    path('bookmarks/<int:pk>/', BookmarkDestroyAPIView.as_view(), name='bookmark-destroy'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('blocks/<int:block_pk>/like/', LikeToggleAPIView.as_view(), name='like-toggle'),
    path('blocks/<int:block_pk>/reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('search-history/', SearchHistoryListCreateAPIView.as_view(), name='search-history-list-create'),
    path('search-history/clear/', SearchHistoryClearAPIView.as_view(), name='search-history-clear'),
]
