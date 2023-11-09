from rest_framework import (viewsets, permissions)
from stopSystem import models
from stopSystem.api import serializers

class StopViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.StopSerializer
    queryset = models.Fleet.objects.all()
    permission_classes = [permissions.IsAuthenticated]