from rest_framework import generics
from beats.models import Beat
from beats.serializers import BeatSerializer
from django.utils import timezone
from datetime import timedelta
from beats.mixins import StandardResponseMixin
import logging

logger = logging.getLogger(__name__)

class LatestBeatsView(StandardResponseMixin, generics.ListAPIView):
    serializer_class = BeatSerializer

    def get_queryset(self):
        week_ago = timezone.now() - timedelta(days=7)
        return Beat.objects.filter(
            is_public=True,
            is_active=True,
            created_at__gte=week_ago
        ).order_by('-created_at').prefetch_related('likes', 'comments')

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return self.success_response(data=response.data, message="Latest beats retrieved successfully.")
        except Exception as e:
            logger.exception("Error retrieving latest beats")
            return self.error_response(message="Failed to retrieve latest beats.", errors=str(e), status=500)
