from apps.locations.models import Buurt
from rest_framework import serializers


class BuurtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buurt
        fields = (
            "code",
            "name",
        )
