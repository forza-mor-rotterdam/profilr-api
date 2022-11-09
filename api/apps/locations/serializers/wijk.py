from apps.locations.models import Wijk
from rest_framework import serializers


class WijkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wijk
        fields = (
            "code",
            "name",
            "gemeente",
        )
