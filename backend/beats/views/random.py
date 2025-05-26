from rest_framework.views import APIView
from beats.models import Beat
from beats.serializers import BeatSerializer
from beats.mixins import StandardResponseMixin
import random
import logging

logger = logging.getLogger(__name__)

class RandomBeatView(StandardResponseMixin, APIView):
    def get(self, request):
        try:
            beats = list(Beat.objects.filter(is_public=True, is_active=True))
            if not beats:
                return self.error_response(message="No beats found", status=404)
            random_beat = random.choice(beats)
            data = BeatSerializer(random_beat).data
            return self.success_response(data=data, message="Random beat retrieved successfully.")
        except Exception as e:
            logger.exception("Error retrieving random beat")
            return self.error_response(message="Failed to retrieve random beat.", errors=str(e), status=500)
