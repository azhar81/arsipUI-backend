from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
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
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_path = models.FileField(upload_to=media_file_path)
    upload_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    event_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    reader_count = models.IntegerField(default=0, editable=False)

    # Additional field to receive a comma-separated string of tag names and an event name
    event_name = models.CharField(max_length=255, blank=True)
    tag_names = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check if event exists, create if not
        if not self.event_id and self.event_name and self.event_date:
            event, created = Event.objects.get_or_create(
                name=self.event_name, date=self.event_date
            )
            self.event = event

        super().save(*args, **kwargs)

        # Handle tags
        if self.tag_names != "":
            self.handle_tags()

    def handle_tags(self):
        # Clear existing tags and add new tags based on tag_names
        self.tags.clear()

        if self.tag_names:
            tag_names = [tag_name.strip() for tag_name in self.tag_names.split(";")]
            tags = [
                Tag.objects.get_or_create(name=tag_name)[0] for tag_name in tag_names
            ]
            self.tags.set(tags)
