from django.urls import path

from apps.item import views
from apps.item.tests.test_classifier import TestClassifierView

app_name = "apps.item"

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    # Special views
    path('categories/tree/', views.CategoryTreeView.as_view(), name='category-tree'),
    path('categories/roots/', views.CategoryRootsView.as_view(), name='category-roots'),
    path('categories/leaves/', views.CategoryLeavesView.as_view(), name='category-leaves'),

    # Slug lookup
    path('categories/slug/<slug:slug>/', views.CategoryBySlugView.as_view(), name='category-by-slug'),

    # Related data
    path('categories/<slug:slug>/children/', views.CategoryChildrenView.as_view(), name='category-children'),
    path('categories/<slug:slug>/ancestors/', views.CategoryAncestorsView.as_view(), name='category-ancestors'),

    # Item views
    # path("item/list/", views.ItemListAPIView.as_view(), name="item-list"),
    # path("item/detail/<int:id>/", views.ItemDetailAPIView.as_view(), name="item-detail"),
    # path("item/post/", views.ItemCreateAPIView.as_view(), name="item-create"),
    # path("item/update/<int:id>/", views.ItemUpdateAPIView.as_view(), name="item-update"),
    # path("item/delete/<int:id>/", views.ItemDeleteAPIView.as_view(), name="item-delete"),
    #
    # path('api/items/search/', views.ItemSearchView.as_view(), name='item-search'),
    #
    # # Item Block views
    # path("itemblock/list/", views.ItemBlockListAPIView.as_view(), name="itemblock-list"),
    # path("itemblock/detail/<int:id>/", views.ItemBlockDetailAPIView.as_view(), name="itemblock-detail"),
    # path("itemblock/post/", views.ItemBlockCreateAPIView.as_view(), name="itemblock-create"),
    # path("itemblock/update/<int:id>/", views.ItemBlockUpdateAPIView.as_view(), name="itemblock-update"),
    # path("itemblock/delete/<int:id>/", views.ItemBlockDeleteAPIView.as_view(), name="itemblock-delete"),

    # Test
    path("test/classifier/", TestClassifierView.as_view())
]
