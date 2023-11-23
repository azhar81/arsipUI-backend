from django.urls import path
from .views import MediaItemList, MediaItemDetail

urlpatterns = [
    path("", MediaItemList.as_view(), name="media-list"),
    path("<int:pk>/", MediaItemDetail.as_view(), name="media-detail"),
]
