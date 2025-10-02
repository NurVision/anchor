from django.urls import path

from .views import *

app_name = "apps.item"


urlpatterns = [
    path("item/list/", ItemListAPIView.as_view(), name="item-list"),
    path("item/detail/<int:id>/", ItemDetailAPIView.as_view(), name="item-detail"),
    path("item/post/", ItemCreateAPIView.as_view(), name="item-create"),
    path("item/update/<int:id>/", ItemUpdateAPIView.as_view(), name="item-update"),
    path("item/delete/<int:id>/", ItemDeleteAPIView.as_view(), name="item-delete"),
]