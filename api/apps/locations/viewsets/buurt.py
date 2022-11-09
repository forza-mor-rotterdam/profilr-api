from apps.api.filters import RelatedOrderingFilter
from apps.locations.filtersets import BuurtFilterSet
from apps.locations.models import Buurt
from apps.locations.serializers import BuurtSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets


class BuurtViewSet(viewsets.ModelViewSet):

    queryset = Buurt.objects.all()

    serializer_class = BuurtSerializer

    http_method_names = [
        "get",
    ]

    filter_backends = (
        DjangoFilterBackend,
        RelatedOrderingFilter,
    )
    filterset_class = BuurtFilterSet
