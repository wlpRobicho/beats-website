from rest_framework.views import APIView
from beats.models import Beat
from beats.mixins import StandardResponseMixin
import logging

logger = logging.getLogger(__name__)

class TagListView(StandardResponseMixin, APIView):
    def get(self, request):
        try:
            all_tags = Beat.objects.filter(
                is_public=True,
                is_active=True
            ).values_list('tags', flat=True)

            tag_set = set()
            for tag_string in all_tags:
                if tag_string:
                    tags = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
                    tag_set.update(tags)

            return self.success_response(data=sorted(tag_set), message="Tags retrieved successfully.")
        except Exception as e:
            logger.exception("Error retrieving tags")
            return self.error_response(message="Failed to retrieve tags.", errors=str(e), status=500)
