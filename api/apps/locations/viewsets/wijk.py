from apps.locations.models import Wijk
from apps.locations.serializers import WijkSerializer
from django_filters.rest_framework import DjangoFilterBackend
from apps.api.filters import RelatedOrderingFilter
from rest_framework import viewsets
from apps.locations.filtersets import WijkFilterSet


class WijkViewSet(viewsets.ModelViewSet):

    queryset = Wijk.objects.all()

    serializer_class = WijkSerializer

    http_method_names = ['get', ]

    filter_backends = (DjangoFilterBackend, RelatedOrderingFilter, )
    filterset_class = WijkFilterSet





