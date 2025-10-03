from django.urls import path

from apps.item.views import *

app_name = "apps.item"

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    # Special views
    path('categories/tree/', CategoryTreeView.as_view(), name='category-tree'),
    path('categories/roots/', CategoryRootsView.as_view(), name='category-roots'),
    path('categories/leaves/', CategoryLeavesView.as_view(), name='category-leaves'),

    # Slug lookup
    path('categories/slug/<slug:slug>/', CategoryBySlugView.as_view(), name='category-by-slug'),

    # Related data
    path('categories/<slug:slug>/children/', CategoryChildrenView.as_view(), name='category-children'),
    path('categories/<slug:slug>/ancestors/', CategoryAncestorsView.as_view(), name='category-ancestors'),

    # Item views
    path("item/list/", ItemListAPIView.as_view(), name="item-list"),
    path("item/detail/<int:id>/", ItemDetailAPIView.as_view(), name="item-detail"),
    path("item/post/", ItemCreateAPIView.as_view(), name="item-create"),
    path("item/update/<int:id>/", ItemUpdateAPIView.as_view(), name="item-update"),
    path("item/delete/<int:id>/", ItemDeleteAPIView.as_view(), name="item-delete"),

    # Item Block views
    path("itemblock/list/", ItemBlockListAPIView.as_view(), name="itemblock-list"),
    path("itemblock/detail/<int:id>/", ItemBlockDetailAPIView.as_view(), name="itemblock-detail"),
    path("itemblock/post/", ItemBlockCreateAPIView.as_view(), name="itemblock-create"),
    path("itemblock/update/<int:id>/", ItemBlockUpdateAPIView.as_view(), name="itemblock-update"),
    path("itemblock/delete/<int:id>/", ItemBlockDeleteAPIView.as_view(), name="itemblock-delete"),
]
