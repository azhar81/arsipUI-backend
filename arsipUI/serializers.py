from rest_framework import serializers
from .models import MediaItem, Tag, Event, Event_Category, File


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event_Category
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer()
    class Meta:
        model = Event
        fields = "__all__"

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

class MediaItemReadSerializer(serializers.ModelSerializer):
    event = EventSerializer()
    tags = TagSerializer()
    file_paths = FileSerializer(many=True)
    class Meta:
        model = MediaItem
        fields = "__all__"

class MediaItemSerializer(serializers.ModelSerializer):
    file_paths = serializers.ListField(child=serializers.FileField(max_length=None), write_only=True, required=False)
    class Meta:
        model = MediaItem
        fields = "__all__"

    def create(self, validated_data):
        file_paths_data = validated_data.pop('file_paths')
            
        instance = super().create(validated_data)
        instance.handle_tags()
        
        for file_path in file_paths_data:
            file_instance = File.objects.create()
            instance.file_paths.add(file_instance)
            file_instance.file = file_path
            file_instance.save()

        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.handle_tags()
        return instance
