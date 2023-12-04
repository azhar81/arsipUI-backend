from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Event_Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    category = models.ForeignKey(Event_Category, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name


def media_file_path(instance, filename):
    # Define the file path for multimedia uploads
    return f"{instance.category}/{instance.event_date.year}/{instance.event_date.month}/{filename}"


class MediaItem(models.Model):
    VIDEO = "video"
    IMAGE = "image"
    AUDIO = "audio"

    CATEGORY_CHOICES = [
        (VIDEO, "Video"),
        (IMAGE, "Image"),
        (AUDIO, "Audio"),
    ]

    WAITLIST = "waitlist"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (WAITLIST, "Waitlist"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    title = models.CharField(max_length=255)
    contributor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        editable=False,
        related_name='contributions'
    )
    verificator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
        editable=False,
        related_name='verifications'
    )
    description = models.TextField()
    file_path = models.FileField(upload_to=media_file_path)
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    reader_count = models.IntegerField(default=0, editable=False)

    # Additional field to receive a user input for non-existing field objects
    event_name = models.CharField(max_length=255, blank=True)
    event_category = models.CharField(max_length=32, blank=True)
    event_date = models.DateField(null=True, blank=True)
    tag_names = models.CharField(max_length=255, blank=True)

    def handle_tags(self):
        # Clear existing tags and add new tags based on tag_names
        self.tags.clear()

        if self.tag_names:
            tag_names = [tag_name.strip() for tag_name in self.tag_names.split(";")]
            tags = [
                Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names
            ]
            self.tags.set(tags)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # On create:
        if self.id == None:
            self.status = self.WAITLIST

        # Check if event exists, create if not
        if not self.event_id and (self.event_name and self.event_date and self.event_category):
            event_category, created = Event_Category.objects.get_or_create(
                name=self.event_category
            )
            event, created = Event.objects.get_or_create(
                name=self.event_name, 
                date=self.event_date,
                category=event_category
            )
            self.event = event

        super().save(*args, **kwargs)

        # Handle tags
        if self.tag_names != "":
            self.handle_tags()

