from PIL import Image
from io import BytesIO
from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from .models import MediaItem, Tag
from .serializers import MediaItemSerializer


def create_dummy_image(width=100, height=100):
    # Create a blank white image
    image = Image.new("RGB", (width, height), "white")

    # Create a BytesIO stream to save the image
    image_stream = BytesIO()
    image.save(image_stream, "PNG")

    # Create a SimpleUploadedFile from the BytesIO stream
    return SimpleUploadedFile(
        "dummy_image.png", image_stream.getvalue(), content_type="image/png"
    )


def dummy_image_data(string):
    data = {
        "title": string,
        "description": string,
        "file_path": create_dummy_image(),
        "category": "image",
        "event_date": "1000-12-01",
        "event_name": string,
        "tag_names": string,
    }

    return data


class MediaItemTests(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.media_item = MediaItem.objects.create(
            title="Test Media Item",
            description="A test media item",
            # Add other necessary fields
        )

    def test_media_item_list_view(self):
        # Test the media item list view
        response = self.client.get(reverse("media-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Media Item")

    def test_media_item_detail_view(self):
        # Test the media item detail view
        response = self.client.get(reverse("media-detail", args=[self.media_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Media Item")

    def test_create_media_item(self):
        # Data to be sent in the POST request
        data = dummy_image_data("test")

        # URL for the view that handles media item creation
        url = reverse("media-list")

        # Perform the POST request
        response = self.client.post(url, data, format="json")

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that a new media item was created in the database
        self.assertEqual(
            MediaItem.objects.count(), 2
        )  # 2 because a media item was created in the set up

        # Retrieve the newly created media item from the database
        media_item = MediaItem.objects.get(id=response.data["id"])

        # Check that the data in the response matches the expected data
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])

        # Check that the data in the database matches the expected data
        self.assertEqual(media_item.title, data["title"])
        self.assertEqual(media_item.description, data["description"])

    def test_tags_applied_correctly(self):
        data = dummy_image_data("test")
        data["tag_names"] = "tag1;tag2;tag3"
        str_date = data["event_date"]
        date_type = date.fromisoformat(str_date)
        data["event_date"] = date_type

        media_item = MediaItem.objects.create(**data)

        tags = media_item.tags.all()

        self.assertEqual(tags[0].name, "tag1")
        self.assertEqual(tags[1].name, "tag2")
        self.assertEqual(tags[2].name, "tag3")

    def test_tags_applied_correctly_using_API(self):
        data = dummy_image_data("test")
        data["tag_names"] = "tag1;tag2;tag3"

        # URL for the view that handles media item creation
        url = reverse("media-list")

        # Perform the POST request
        response = self.client.post(url, data, format="json")

        media_item = MediaItem.objects.get(id=response.data["id"])
        tags = media_item.tags.all()

        self.assertEqual(tags.count(), 3)

        self.assertEqual(tags[0].name, "tag1")
        self.assertEqual(tags[1].name, "tag2")
        self.assertEqual(tags[2].name, "tag3")
