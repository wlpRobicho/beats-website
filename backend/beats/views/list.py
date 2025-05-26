from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from beats.mixins import StandardResponseMixin
from beats.models import Beat
from beats.serializers import BeatSerializer
from beats.filters import BeatFilter

class BeatListView(StandardResponseMixin, generics.ListAPIView):
    serializer_class = BeatSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BeatFilter
    ordering_fields = ['created_at', 'play_count']
    ordering = ['-created_at']
    search_fields = ['title', 'tags']

    def get_queryset(self):
        return Beat.objects.filter(
            is_public=True,
            is_active=True
        ).prefetch_related('likes', 'comments')

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return self.success_response(data=response.data, message="Beats retrieved successfully.")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.exception("Error retrieving beats list")
            return self.error_response(message="Failed to retrieve beats.", errors=str(e), status=500)
