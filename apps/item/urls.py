from django.urls import path

from apps.item import views

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

    path("item/list/", views.ItemListAPIView.as_view(), name="item-list"),
    path("item/detail/<int:id>/", views.ItemDetailAPIView.as_view(), name="item-detail"),
    path("item/post/", views.ItemCreateAPIView.as_view(), name="item-create"),
    path("item/update/<int:id>/", views.ItemUpdateAPIView.as_view(), name="item-update"),
    path("item/delete/<int:id>/", views.ItemDeleteAPIView.as_view(), name="item-delete"),
]
