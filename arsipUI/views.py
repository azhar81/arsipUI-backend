from rest_framework import generics, viewsets, filters
from .models import MediaItem, Event, Event_Category
from .serializers import MediaItemSerializer, MediaItemReadSerializer, EventSerializer, EventCategorySerializer
from .permissions import IsContributorOrReadOnly, IsObjectVerificator
from users.permissions import IsContributor, IsVerificator
from rest_framework import permissions
from rest_framework.response import Response


class MediaItemList(generics.ListAPIView):
    serializer_class = MediaItemReadSerializer
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
        # Get the status parameter from the query parameters
        status = self.request.query_params.get("status", None)

        # Get all MediaItems and order them by upload_date in descending order
        queryset = MediaItem.objects.all().order_by("-upload_date")
        
        # classify the response by 'status'
        

        # Check if the user has requested to sort by reader_count
        if status:
            queryset = queryset.filter(status=status)
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
    serializer_class = MediaItemSerializer
    queryset = MediaItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Increment the reader count
        instance.reader_count += 1
        instance.save()

        serializer = MediaItemReadSerializer(instance, context={'request': request})
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

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Event_Category.objects.all()
    serializer_class = EventCategorySerializer

class ContributorMediaItemList(generics.ListAPIView):
    serializer_class = MediaItemReadSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
        "description",
        "tags__name",
        "tag_names",
        "event_date",
        "event__name",
    ]

    def get_queryset(self):
        queryset = MediaItem.objects.filter(contributor=self.request.user).order_by("-upload_date")
        
        return queryset
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        waitlist = queryset.filter(status="waitlist")
        approved = queryset.filter(status="approved")
        rejected = queryset.filter(status="rejected")
        
        waitlist_serializer = MediaItemReadSerializer(waitlist, many=True)
        approved_serializer = MediaItemReadSerializer(approved, many=True)
        rejected_serializer = MediaItemReadSerializer(rejected, many=True)

        data = {
            'waitlist': waitlist_serializer.data,
            'approved': approved_serializer.data,
            'rejected': rejected_serializer.data
        }
        
        return Response(data)
