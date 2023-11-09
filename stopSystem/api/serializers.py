from rest_framework import serializers
from stopSystem import models
from django.core.exceptions import ValidationError


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fleet
        fields = "__all__"
