from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from django.db import transaction
from beats.models import Beat
from beats.serializers import BeatSerializer
from beats.mixins import StandardResponseMixin  # ✅ Add this
import logging

logger = logging.getLogger(__name__)

class BeatUploadView(StandardResponseMixin, generics.CreateAPIView):  # ✅ Add mixin
    queryset = Beat.objects.all()
    serializer_class = BeatSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return self.success_response(
                data=BeatSerializer(serializer.instance).data,
                message="Beat uploaded successfully.",
                status=status.HTTP_201_CREATED
            )

        except serializers.ValidationError as ve:
            return self.error_response(
                message="Validation failed.",
                errors=ve.detail,
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            logger.exception(f"[Beat Upload Error] User: {request.user} - {str(e)}")
            return self.error_response(
                message="Unexpected server error.",
                errors=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
