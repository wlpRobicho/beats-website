from rest_framework import serializers
from .models import Beat
import os

class BeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beat
        fields = '__all__'
        read_only_fields = ['slug', 'duration', 'created_at', 'updated_at', 'play_count']

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
