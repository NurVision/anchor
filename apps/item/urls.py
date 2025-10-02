from django.urls import path

from .views import *

app_name = "apps.item"


urlpatterns = [
    path("item/", ItemAPIView.as_view(), name="item-manage"),
]