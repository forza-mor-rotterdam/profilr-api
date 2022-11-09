from rest_framework import serializers
from apps.locations.models import Buurt


class BuurtSerializer(serializers.ModelSerializer):

    class Meta:
        model = Buurt
        fields = (
            "wijk",
            "code",
            "name",
        )