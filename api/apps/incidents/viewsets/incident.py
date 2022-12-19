import logging

from apps.api.filters import RelatedOrderingFilter
from apps.incidents.filtersets import IncidentFilterSet
from apps.incidents.models import Incident
from apps.incidents.serializers import IncidentListSerializer, IncidentSerializer
from apps.locations.models import Wijk
from deepdiff import DeepDiff
from django.utils.text import slugify
from django_filters.rest_framework import DjangoFilterBackend
from profilr_api_services import msb_api_service
from rest_framework import viewsets
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class IncidentViewSet(viewsets.ModelViewSet):

    queryset = (
        Incident.objects.select_related(
            "location",
            "status",
            "parent",
        )
        .prefetch_related()
        .all()
    )

    serializer_class = IncidentListSerializer
    serializer_detail_class = IncidentSerializer

    http_method_names = [
        "get",
    ]

    filter_backends = (
        DjangoFilterBackend,
        RelatedOrderingFilter,
    )
    filterset_class = IncidentFilterSet

    def list(self, request, *args, **kwargs):
        user_token = msb_api_service.get_user_token_from_request(request)

        trans_wijken = {
            "Rotterdam Centrum": "Stadscentrum",
        }

        wijken_codes = request.GET.getlist("wijk")
        wijken_names = [
            slugify(trans_wijken.get(w, w))
            for w in Wijk.objects.filter(code__in=wijken_codes).values_list(
                "name", flat=True
            )
        ]
        print(len(wijken_names))
        print(wijken_names)
        wijken_msb = msb_api_service.get_wijken(user_token)
        wijken_msb_codes = [
            w.get("omschrijving")
            for w in wijken_msb
            if slugify(w.get("omschrijving")) not in wijken_names
        ]
        print(len(wijken_msb_codes))
        print(wijken_msb_codes)

        data = msb_api_service.get_list(user_token, request.GET, no_cache=True)

        external_ids = []
        for d in data:
            external_id = d["id"]
            m = Incident.objects.filter(external_id=external_id).first()
            if not m:
                m = Incident()
                m.msb_data = d
                m.user_token = user_token
                m.save()
            else:
                ddiff = DeepDiff(m.msb_data, d)
                if ddiff:
                    m.msb_data = d
                    m.user_token = user_token
                    m.save()
            external_ids.append(external_id)

        # queryset = self.filter_queryset(self.get_queryset())
        queryset = self.get_queryset()
        queryset = queryset.filter(external_id__in=external_ids)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
