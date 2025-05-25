from django.contrib import admin
from .models import Beat, BeatLike, BeatComment

@admin.register(Beat)
class BeatAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'genre', 'key', 'bpm',
        'status', 'is_public', 'is_featured',
        'play_count', 'like_count', 'comment_count',
        'created_at'
    )
    list_filter = (
        'genre', 'key', 'status',
        'is_public', 'is_active', 'is_featured',
        'created_at'
    )
    search_fields = ('title', 'tags', 'slug', 'key')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('duration', 'play_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    # Optional: group fields in sections
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'key', 'bpm', 'genre', 'tags')
        }),
        ("Media", {
            'fields': ('cover_image', 'audio_file', 'youtube_link', 'duration')
        }),
        ("Visibility", {
            'fields': ('status', 'is_public', 'is_active', 'is_featured', 'allow_download')
        }),
        ("Stats", {
            'fields': ('play_count', 'created_at', 'updated_at')
        }),
    )


@admin.register(BeatLike)
class BeatLikeAdmin(admin.ModelAdmin):
    list_display = ('beat', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('ip_address',)


@admin.register(BeatComment)
class BeatCommentAdmin(admin.ModelAdmin):
    list_display = ('beat', 'name', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'text')
    readonly_fields = ('created_at',)
