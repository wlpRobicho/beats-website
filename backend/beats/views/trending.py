from rest_framework import generics
from beats.models import Beat
from beats.serializers import BeatSerializer
from beats.mixins import StandardResponseMixin
from django.db.models import Count
import logging

logger = logging.getLogger(__name__)

class TrendingBeatsView(StandardResponseMixin, generics.ListAPIView):
    serializer_class = BeatSerializer

    def get_queryset(self):
        return Beat.objects.filter(
            is_public=True,
            is_active=True
        ).annotate(like_count=Count('likes')).order_by('-like_count', '-play_count', '-created_at').prefetch_related('likes', 'comments')[:20]

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return self.success_response(data=response.data, message="Trending beats retrieved successfully.")
        except Exception as e:
            logger.exception("Error retrieving trending beats")
            return self.error_response(message="Failed to retrieve trending beats.", errors=str(e), status=500)
