from django.urls import path
from .views import MediaItemList, MediaItemDetail, MediaItemCreate, MediaItemApproveView, MediaItemRejectView

urlpatterns = [
    path("", MediaItemList.as_view(), name="media-list"),
    path("create", MediaItemCreate.as_view(), name="media-create"),
    path("<int:pk>", MediaItemDetail.as_view(), name="media-detail"),
    path('<int:pk>/approve', MediaItemApproveView.as_view(), name='mediaitem-approve'),
    path('<int:pk>/reject', MediaItemRejectView.as_view(), name='mediaitem-reject'),
]
