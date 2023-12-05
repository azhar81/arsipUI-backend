from rest_framework import generics, viewsets, filters
from .models import MediaItem
from .serializers import MediaItemSerializer, MediaItemReadSerializer
from .permissions import IsContributorOrReadOnly, IsObjectVerificator
from users.permissions import IsContributor, IsVerificator
from rest_framework import permissions
from rest_framework.response import Response


class MediaItemList(generics.ListAPIView):
    serializer_class = MediaItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
        "description",
        "tags__name",
        "tag_names",
        "event_date",
        "event__name",
    ]

    # def create(self, request, *args, **kwargs):
    def get_queryset(self):
        # Get the limit parameter from the query parameters
        limit = self.request.query_params.get("limit", None)
        # Get the sort parameter from the query parameters
        sort_by_reader = self.request.query_params.get("sort_by_reader", False)

        # Get all MediaItems and order them by event_date in descending order
        queryset = MediaItem.objects.all().order_by("-event_date")

        # Check if the user has requested to sort by reader_count
        if sort_by_reader:
            queryset = queryset.order_by("-reader_count")

        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]
            except ValueError:
                # Handle the case where the provided limit is not a valid integer
                pass

        return queryset

    def perform_create(self, serializer):
        # Attach the current user as the contributor
        serializer.save(contributor=self.request.user, status="waitlist")


class MediaItemCreate(generics.CreateAPIView):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor]

    def perform_create(self, serializer):
        # Attach the current user as the contributor
        serializer.save(contributor=self.request.user)


class MediaItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsContributorOrReadOnly]
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Increment the reader count
        instance.reader_count += 1
        instance.save()

        serializer = MediaItemReadSerializer(instance)
        return Response(serializer.data)

class MediaItemApproveView(generics.RetrieveAPIView):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemReadSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerificator]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "approved"
        instance.verificator = request.user
        instance.save()
        
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)

class MediaItemRejectView(generics.RetrieveAPIView):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemReadSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerificator]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "rejected"
        instance.verificator = request.user
        instance.save()
        
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)

class MediaItemCancelView(generics.RetrieveAPIView):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemReadSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerificator, IsObjectVerificator]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = "waitlist"
        instance.verificator = None
        instance.save()
        
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)