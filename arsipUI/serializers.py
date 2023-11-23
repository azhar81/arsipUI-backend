from rest_framework import serializers
from .models import MediaItem, Tag, Event


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class MediaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaItem
        fields = "__all__"

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.handle_tags()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.handle_tags()
        return instance
