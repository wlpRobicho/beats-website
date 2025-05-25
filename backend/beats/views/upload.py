from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from django.db import transaction
from beats.models import Beat
from beats.serializers import BeatSerializer
import logging

logger = logging.getLogger(__name__)

class BeatUploadView(generics.CreateAPIView):
    queryset = Beat.objects.all()
    serializer_class = BeatSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response({
                "success": True,
                "message": "Beat uploaded successfully.",
                "beat": BeatSerializer(serializer.instance).data
            }, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as ve:
            return Response({
                "success": False,
                "message": "Validation failed.",
                "errors": ve.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception(f"Beat upload failed for user {request.user}")
            return Response({
                "success": False,
                "message": "Unexpected server error.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
