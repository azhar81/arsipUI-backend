from PIL import Image
from io import BytesIO
from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APIClient
from .models import MediaItem, Tag, Event, Event_Category
from users.tests import create_contributor, create_verificator


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
        "file_paths": [
            create_dummy_image(),
            create_dummy_image()
            ],
        "event_date": "1000-12-01",
        "event_name": string,
        "event_category": string,
        "tag_names": string,
    }

    return data


class MediaItemTests(TestCase):
    def setUp(self):
        # Create a test user
        self.contributor_user = create_contributor(
            username="contributor", password="password123"
        )
        self.verificator_user = create_verificator(
            username="verificator", password="password123"
        )
        self.verificator_user_alternate = create_verificator(
            username="verificator2", password="password123"
        )
        # Create sample data for testing
        self.tag = Tag.objects.create(
            name = "Test"
        )
        self.event_category = Event_Category.objects.create(
            name="Test"
        )
        self.event = Event.objects.create(
            name="Test Event",
            date="1000-12-01",
            category=self.event_category
        )
        self.media_item = MediaItem.objects.create(
            title="Test Media Item",
            description="A test media item",
            event=self.event,
            tag_names="test"
        )
        # Create an API client
        self.client = APIClient()

    def test_media_item_detail(self):
        # Ensure that the media item detail endpoint returns the correct data
        response = self.client.get(f"/arsip/{self.media_item.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the reader count has increased after retrieving the media item
        self.assertEqual(
            self.media_item.reader_count + 1,
            MediaItem.objects.get(id=self.media_item.id).reader_count,
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

    def test_media_item_create(self):
        # Ensure that a new media item can be created
        data = dummy_image_data("test")
        self.client.force_authenticate(user=self.contributor_user)
        response = self.client.post("/arsip/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the contributor is correctly set
        created_media_item = MediaItem.objects.get(id=response.data["id"])
        self.assertEqual(created_media_item.contributor, self.contributor_user)

        # Check that the data in the response matches the expected data
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])

        # Check that the data in the database matches the expected data
        self.assertEqual(created_media_item.title, data["title"])
        self.assertEqual(created_media_item.description, data["description"])

    def test_media_item_create_with_event_id(self):
        # Ensure that a new media item can be created
        data = dummy_image_data("test")
        data.pop('event_name')
        data.pop('event_category')
        data.pop('event_date')
        data['event'] = self.event.id
        self.client.force_authenticate(user=self.contributor_user)
        response = self.client.post("/arsip/create", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tags_applied_correctly_using_API(self):
        data = dummy_image_data("test")
        data["tag_names"] = "tag1;tag2;tag3"

        self.client.force_authenticate(user=self.contributor_user)
        response = self.client.post("/arsip/create", data)

        media_item = MediaItem.objects.get(id=response.data["id"])
        tags = media_item.tags.all()

        self.assertEqual(tags.count(), 3)

        self.assertEqual(tags[0].name, "tag1")
        self.assertEqual(tags[1].name, "tag2")
        self.assertEqual(tags[2].name, "tag3")

    def test_media_item_approve(self):
        # Ensure that a verificator can approve a media item
        self.client.force_authenticate(user=self.verificator_user)
        response = self.client.get(f'/arsip/{self.media_item.id}/approve')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "approved")
        self.assertEqual(response.data['verificator'], self.verificator_user.id)

    def test_media_item_reject(self):
        # Ensure that a verificator can reject a media item
        self.client.force_authenticate(user=self.verificator_user)
        response = self.client.get(f'/arsip/{self.media_item.id}/reject')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "rejected")
        self.assertEqual(response.data['verificator'], self.verificator_user.id)
    
    def test_media_item_cancel_approval(self):
        self.client.force_authenticate(user=self.verificator_user)
        # Approve first
        self.client.get(f'/arsip/{self.media_item.id}/approve')
        # Ensure that a verificator can cancel a media item's approval        
        response = self.client.get(f'/arsip/{self.media_item.id}/cancel')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "waitlist")
        self.assertEqual(response.data['verificator'], None)

    def test_media_item_approve_by_contributor(self):
        # Ensure that a contributor cannot approve a media item
        self.client.force_authenticate(user=self.contributor_user)
        response = self.client.get(f'/arsip/{self.media_item.id}/approve')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_media_item_reject_by_contributor(self):
        # Ensure that a contributor cannot reject a media item
        self.client.force_authenticate(user=self.contributor_user)
        response = self.client.get(f'/arsip/{self.media_item.id}/reject')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_media_item_cancel_approval_by_contributor(self):
        self.client.force_authenticate(user=self.verificator_user)
        # Approve first
        self.client.get(f'/arsip/{self.media_item.id}/approve')
        # Ensure that a verificator can cancel a media item's approval    
        self.client.force_authenticate(user=self.contributor_user)
        response = self.client.get(f'/arsip/{self.media_item.id}/cancel')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_media_item_cancel_approval_by_other_verificator(self):
        self.client.force_authenticate(user=self.verificator_user)
        # Approve first
        self.client.get(f'/arsip/{self.media_item.id}/approve')
        # Ensure that a verificator can cancel a media item's approval
        self.client.force_authenticate(user=self.verificator_user_alternate)      
        response = self.client.get(f'/arsip/{self.media_item.id}/cancel')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
