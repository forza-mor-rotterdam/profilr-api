from rest_framework import serializers
from apps.locations.models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = (
            "geometrie",
            "buurt_code",
            "address",
        )