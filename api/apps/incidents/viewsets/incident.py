import logging
from datetime import datetime

from apps.incidents.models import Incident
from apps.incidents.serializers import IncidentSerializer
from apps.services.msb import MSBService
from deepdiff import DeepDiff
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

    serializer_class = IncidentSerializer

    http_method_names = [
        "get",
    ]

    def list(self, request, *args, **kwargs):

        user_token = MSBService.get_user_token_from_request(request)
        data = MSBService.get_list(user_token, request.GET, no_cache=True).get(
            "result", []
        )

        external_ids = []
        for d in data:
            external_id = d["id"]
            m = Incident.objects.filter(external_id=external_id).first()
            if not m:
                m = Incident.objects.create(
                    external_id=external_id,
                    extra_properties={"raw_list_item": d},
                    incident_date_start=datetime.strptime(
                        d["datumMelding"], "%Y-%m-%dT%H:%M:%S"
                    ),
                )
            elif DeepDiff(m.extra_properties.get("raw_list_item"), d):
                m.extra_properties["raw_list_item"] = d
                m.save(update_fields=["extra_properties"])
            external_ids.append(external_id)

        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(external_id__in=external_ids)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
