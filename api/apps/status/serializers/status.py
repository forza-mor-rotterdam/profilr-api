from apps.status.models.status import Status
from rest_framework import serializers


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = (
            "state",
            "text",
            "created_at",
        )
