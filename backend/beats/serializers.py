from rest_framework import serializers
from .models import Beat
from django.utils.text import slugify
import os
import re

class BeatSerializer(serializers.ModelSerializer):
    tag_list = serializers.SerializerMethodField()
    duration_display = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Beat
        fields = [
            'id', 'title', 'key', 'bpm', 'genre',
            'cover_image', 'audio_file', 'duration', 'duration_display',
            'tag_list', 'tags', 'youtube_link',
            'created_at', 'slug', 'play_count',
            'allow_download', 'status', 'is_featured',
            'like_count', 'comment_count'
        ]
        read_only_fields = [
            'duration', 'created_at', 'updated_at', 'slug', 'play_count',
            'like_count', 'comment_count'
        ]

    def create(self, validated_data):
        if not validated_data.get("slug"):
            validated_data["slug"] = slugify(validated_data["title"])
        return super().create(validated_data)

    def get_tag_list(self, obj):
        return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]

    def get_duration_display(self, obj):
        if obj.duration:
            total_seconds = int(obj.duration.total_seconds())
            minutes, seconds = divmod(total_seconds, 60)
            return f"{minutes}:{seconds:02d}"
        return None

    def validate_bpm(self, value):
        if value < 50 or value > 300:
            raise serializers.ValidationError("BPM must be between 50 and 300.")
        return value

    def validate_audio_file(self, file):
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ['.mp3', '.wav']:
            raise serializers.ValidationError("Only MP3 and WAV files are allowed.")

        max_size_mb = 60
        if file.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError(f"Audio file must be smaller than {max_size_mb}MB.")

        return file

    def validate_cover_image(self, file):
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png']:
            raise serializers.ValidationError("Cover image must be .jpg, .jpeg, or .png.")

        if file.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Cover image must be smaller than 5MB.")
        return file

    def validate_tags(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Tags must be a comma-separated string.")
        
        tag_pattern = r'^[\w\s,-]+$'
        if not re.match(tag_pattern, value):
            raise serializers.ValidationError("Tags can only contain letters, numbers, spaces, commas, and hyphens.")
        
        if len(value) > 255:
            raise serializers.ValidationError("Tags must be 255 characters or less.")

        return value
