from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from django.core.exceptions import ValidationError
import os
import logging
from datetime import timedelta
from .choices import GENRE_CHOICES, KEY_CHOICES, STATUS_CHOICES

logger = logging.getLogger(__name__)



def validate_audio_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ['.mp3', '.wav']:
        raise ValidationError('Only MP3 and WAV files are allowed.')

class Beat(models.Model):
    title = models.CharField(max_length=255, help_text="Name of the beat")
    key = models.CharField(max_length=10, choices=KEY_CHOICES, help_text="Choose the musical key")
    bpm = models.PositiveIntegerField(help_text="Tempo (beats per minute)")
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, help_text="Choose the genre")
    cover_image = models.ImageField(upload_to='covers/')
    audio_file = models.FileField(upload_to='protected/beats/', validators=[validate_audio_file])
    duration = models.DurationField(blank=True, null=True, help_text="Length of the beat")
    tags = models.CharField(max_length=255, help_text="Comma-separated tags like 'dark,trap,melodic'")
    youtube_link = models.URLField(blank=True, null=True, help_text="Optional YouTube promo link")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    play_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)
    allow_download = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="published",
        help_text="Select 'draft' to hide this beat from public until finished"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this beat without deleting it"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Highlight this beat on top of the homepage or featured section"
    )

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.count()

    def clean(self):
        if self.bpm < 50 or self.bpm > 300:
            raise ValidationError("BPM must be between 50 and 300.")

    def save(self, *args, **kwargs):
        is_new = self._state.adding and not self.pk
        super().save(*args, **kwargs)  # First save to ensure file is on disk

        # Now that the file exists on disk, extract duration
        if is_new and self.audio_file and not self.duration:
            try:
                path = self.audio_file.path
                ext = os.path.splitext(path)[1].lower()

                if ext == '.mp3':
                    audio = MP3(path)
                    self.duration = timedelta(seconds=round(audio.info.length))
                elif ext == '.wav':
                    audio = WAVE(path)
                    self.duration = timedelta(seconds=round(audio.info.length))

                # Save duration only
                super().save(update_fields=['duration'])

            except Exception as e:
                logger.warning(f"[Beat Save] Could not extract duration: {e}")

    def __str__(self):
        return self.title

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',')]

    def get_absolute_url(self):
        return reverse("beat-detail", kwargs={"slug": self.slug})

    def to_dict(self):
        return {
            "title": self.title,
            "key": self.key,
            "bpm": self.bpm,
            "genre": self.get_genre_display(),
            "cover_image_url": self.cover_image.url if self.cover_image else "",
            "audio_file_url": self.audio_file.url if self.audio_file else "",
            "duration": str(self.duration) if self.duration else "N/A",
            "tags": self.tag_list(),
            "youtube_link": self.youtube_link,
            "created_at": self.created_at.isoformat(),
            "slug": self.slug,
            "play_count": self.play_count,
            "allow_download": self.allow_download,
            "status": self.status,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "likes": self.like_count,
            "comments": self.comment_count,
        }

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Beat"
        verbose_name_plural = "Beats"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['genre']),
            models.Index(fields=['key']),
        ]

class BeatLike(models.Model):
    beat = models.ForeignKey('Beat', on_delete=models.CASCADE, related_name='likes')
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like on {self.beat.title} from {self.ip_address}"

    class Meta:
        ordering = ['-created_at']
        unique_together = ('beat', 'ip_address')

class BeatComment(models.Model):
    beat = models.ForeignKey('Beat', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.name} on {self.beat.title}"

    class Meta:
        ordering = ['-created_at']

