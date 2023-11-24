from rest_framework import generics, viewsets, filters
from .models import MediaItem, Tag, Event
from .serializers import MediaItemSerializer, TagSerializer, EventSerializer
from rest_framework.response import Response


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class MediaItemList(generics.ListCreateAPIView):
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


class MediaItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Increment the reader count
        instance.reader_count += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
