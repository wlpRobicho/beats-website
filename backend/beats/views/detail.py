from rest_framework import generics, permissions, status
from rest_framework.response import Response
from beats.models import Beat
from beats.serializers import BeatSerializer
from beats.mixins import StandardResponseMixin
import logging

logger = logging.getLogger(__name__)

class BeatDetailView(StandardResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Beat.objects.all()
    serializer_class = BeatSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]  

    def retrieve(self, request, *args, **kwargs):
        try:
            response = super().retrieve(request, *args, **kwargs)
            return self.success_response(data=response.data, message="Beat retrieved successfully.")
        except Exception as e:
            logger.exception("Error retrieving beat")
            return self.error_response(message="Failed to retrieve beat.", errors=str(e), status=500)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return self.success_response(data=response.data, message="Beat updated successfully.")
        except Exception as e:
            logger.exception("Error updating beat")
            return self.error_response(message="Failed to update beat.", errors=str(e), status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False
            instance.save(update_fields=['is_active'])
            return self.success_response(message="Beat has been deactivated.")
        except Exception as e:
            logger.exception("Error deactivating beat")
            return self.error_response(message="Failed to delete beat.", errors=str(e), status=500)
