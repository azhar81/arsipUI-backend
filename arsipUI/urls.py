from django.urls import path
from .views import MediaItemList, MediaItemDetail, MediaItemCreate, \
    MediaItemApproveView, MediaItemRejectView, MediaItemCancelView, \
    EventListView, CategoryListView, ContributorMediaItemList

urlpatterns = [
    path("", MediaItemList.as_view(), name="media-list"),
    path("user", ContributorMediaItemList.as_view(), name="user-media-list"),
    path("events", EventListView.as_view(), name="events-list"),
    path("categories", CategoryListView.as_view(), name="category-list"),
    path("create", MediaItemCreate.as_view(), name="media-create"),
    path("<int:pk>", MediaItemDetail.as_view(), name="media-detail"),
    path('<int:pk>/approve', MediaItemApproveView.as_view(), name='mediaitem-approve'),
    path('<int:pk>/reject', MediaItemRejectView.as_view(), name='mediaitem-reject'),
    path('<int:pk>/cancel', MediaItemCancelView.as_view(), name='mediaitem-cancel-approval'),
]
