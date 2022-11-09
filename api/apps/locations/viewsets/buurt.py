from apps.locations.models import Buurt
from apps.locations.serializers import BuurtSerializer
from rest_framework import viewsets


class BuurtViewSet(viewsets.ModelViewSet):

    queryset = Buurt.objects.all()

    serializer_class = BuurtSerializer

    http_method_names = [
        "get",
    ]
