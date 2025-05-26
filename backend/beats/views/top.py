from rest_framework import generics
from beats.models import Beat
from beats.serializers import BeatSerializer
from beats.mixins import StandardResponseMixin
import logging

logger = logging.getLogger(__name__)

class TopBeatsView(StandardResponseMixin, generics.ListAPIView):
    serializer_class = BeatSerializer

    def get_queryset(self):
        return Beat.objects.filter(
            is_public=True,
            is_active=True
        ).order_by('-play_count').prefetch_related('likes', 'comments')[:20]  # top 20

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return self.success_response(data=response.data, message="Top beats retrieved successfully.")
        except Exception as e:
            logger.exception("Error retrieving top beats")
            return self.error_response(message="Failed to retrieve top beats.", errors=str(e), status=500)
