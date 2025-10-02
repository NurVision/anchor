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
]
