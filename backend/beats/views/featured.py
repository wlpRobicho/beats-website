from rest_framework import generics
from beats.models import Beat
from beats.serializers import BeatSerializer
from beats.mixins import StandardResponseMixin
import logging

logger = logging.getLogger(__name__)

class FeaturedBeatsView(StandardResponseMixin, generics.ListAPIView):
    serializer_class = BeatSerializer

    def get_queryset(self):
        return Beat.objects.filter(
            is_public=True,
            is_active=True,
            is_featured=True
        ).order_by('-created_at').prefetch_related('likes', 'comments')

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            response = super().list(request, *args, **kwargs)
            return self.success_response(data=response.data, message="Featured beats retrieved successfully.")
        except Exception as e:
            logger.exception("Error retrieving featured beats")
            return self.error_response(message="Failed to retrieve featured beats.", errors=str(e), status=500)
