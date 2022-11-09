from rest_framework import serializers
from apps.locations.models import Wijk


class WijkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wijk
        fields = (
            "code",
            "name",
            "gemeente",
        )