from django.urls import path

# Ehtimol, sizning view'laringiz bitta faylda bo'lishi mumkin.
# Agar Item...APIView'lar boshqa faylda bo'lsa, importni to'g'rilarsiz.
from apps.item import views
from apps.item.views import (
    ItemListAPIView,
    ItemDetailAPIView,
    ItemCreateAPIView,
    ItemUpdateAPIView,
    ItemDeleteAPIView
)

app_name = "apps.item"

urlpatterns = [
    # Item uchun yo'llar
    path("item/list/", ItemListAPIView.as_view(), name="item-list"),
    path("item/detail/<int:id>/", ItemDetailAPIView.as_view(), name="item-detail"),
    path("item/post/", ItemCreateAPIView.as_view(), name="item-create"),
    path("item/update/<int:id>/", ItemUpdateAPIView.as_view(), name="item-update"),
    path("item/delete/<int:id>/", ItemDeleteAPIView.as_view(), name="item-delete"),

    # Category uchun yo'llar
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/tree/', views.CategoryTreeView.as_view(), name='category-tree'),
    path('categories/roots/', views.CategoryRootsView.as_view(), name='category-roots'),
    path('categories/leaves/', views.CategoryLeavesView.as_view(), name='category-leaves'),
    path('categories/slug/<slug:slug>/', views.CategoryBySlugView.as_view(), name='category-by-slug'),
    path('categories/<slug:slug>/children/', views.CategoryChildrenView.as_view(), name='category-children'),
    path('categories/<slug:slug>/ancestors/', views.CategoryAncestorsView.as_view(), name='category-ancestors'),
]