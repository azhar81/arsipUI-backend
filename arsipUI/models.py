import os
from django.db import models
from django.core.exceptions import ValidationError
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
    
def get_file_type(value):
    img_type = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg']
    vid_type = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.3gp', '.3gpp']
    doc_type = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pdf', '.txt', '.rtf', '.odt', '.ods', '.odp', '.csv']
    
    ext = os.path.splitext(value)[1].lower()
    
    if ext in img_type:
        return "img"
    elif ext in vid_type:
        return "vid"
    elif ext in doc_type:
        return "doc"
    else:
        return "others"

def validate_file_extension(value):
    if get_file_type(value.name) == None:
        raise ValidationError('Unsupported file extension.')

def media_file_path(instance, filename):
    category = get_file_type(filename)
    instance.file_type = category
    event_date = instance.media_items.first().event.date
    # Define the file path for multimedia uploads
    return f"{category}/{event_date.year}/{event_date.month}/{filename}"

class File(models.Model):
    FILE_TYPE = [
        ("img", "Images"),
        ("vid", "Videos"),
        ("doc", "Documents")
    ]
    file = models.FileField(upload_to=media_file_path, validators=[validate_file_extension], blank=True)
    file_type = models.CharField(choices=FILE_TYPE, max_length=3, editable=False)

    def __str__(self):
        return self.file.name

class MediaItem(models.Model):
    WAITLIST = "waitlist"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (WAITLIST, "Waitlist"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]
    
    FAKULTAS_CHOICES = [
        ('FK', 'Fakultas Kedokteran'),
        ('FF', 'Fakultas Farmasi'),
        ('FIPB', 'Fakultas Ilmu Pengetahuan Budaya'),
        ('FH', 'Fakultas Hukum'),
        ('FT', 'Fakultas Teknik'),
        ('FEB', 'Fakultas Ekonomi dan Bisnis'),
        ('FISIP', 'Fakultas Ilmu Sosial dan Ilmu Politik'),
        ('FPsi', 'Fakultas Psikologi'),
        ('Fasilkom', 'Fakultas Ilmu Komputer'),
        ('FMIPA', 'Fakultas Matematika Dan Ilmu Pengetahuan Alam'),
        ('FIB', 'Fakultas Ilmu Budaya'),
        ('FKM', 'Fakultas Kesehatan Masyarakat'),
        ('FKG', 'Fakultas Kedokteran Gigi'),
        ('FIK', 'Fakultas Ilmu Keperawatan'),
        ('FIA', 'Fakultas Ilmu Administrasi'),
        ('PPV', 'Program Pendidikan Vokasi'),
        ('SIL', 'Sekolah Ilmu Pengetahuan'),
        ('SKSG', 'Sekolah Kajian Stratejik dan Global')        
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
    file_paths = models.ManyToManyField(File, related_name='media_items')
    upload_date = models.DateTimeField(auto_now_add=True)
    fakultas = models.CharField(max_length=8, choices=FAKULTAS_CHOICES, blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    reader_count = models.IntegerField(default=0, editable=False)
    reject_reason = models.TextField(blank=True)

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
