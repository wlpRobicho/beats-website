from rest_framework import generics, permissions
from beats.models import Beat
from beats.serializers import BeatSerializer


class BeatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Beat.objects.all()
    serializer_class = BeatSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        # Soft delete instead of permanent removal
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        return Response({
            "success": True,
            "message": "Beat has been deactivated successfully."
        }, status=status.HTTP_204_NO_CONTENT)