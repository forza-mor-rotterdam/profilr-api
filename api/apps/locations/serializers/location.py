from apps.locations.models import Location
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "geometrie",
            "buurt_code",
            "address",
        )
