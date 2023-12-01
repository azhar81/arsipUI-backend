from django.urls import path
from .views import MediaItemList, MediaItemDetail, MediaItemCreate

urlpatterns = [
    path("", MediaItemList.as_view(), name="media-list"),
    path("create", MediaItemCreate.as_view(), name="media-create"),
    path("<int:pk>", MediaItemDetail.as_view(), name="media-detail"),
]
