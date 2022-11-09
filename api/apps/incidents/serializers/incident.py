from datapunt_api.rest import DisplayField, HALSerializer
from django.conf import settings
from rest_framework import serializers
from apps.incidents.models import Incident
from apps.status.models import StatusChoices
import json
from apps.services.msb import MSBService
from apps.locations.serializers import LocationSerializer
from apps.locations.utils.rd_convert import rd_to_wgs


class IncidentListSerializer(serializers.ListSerializer):
    class Meta:
        model = Incident
        fields = (
            'id',
            'incident_date_start',
            'location',
            'status',
            'priority',
            'text',
            'extra_properties',
            'created_at',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'location',
            'status',
            'priority',
            'text',
            'extra_properties',
            'created_at',
            'updated_at',
        )


class AttachmentSerialzer(serializers.Serializer):
    pass


class InsidentMSBFieldsMixin:
    def get_attachments(self, obj):
        user_token = MSBService.get_user_token_from_request(self.context['request'])
        return MSBService.get_detail(obj.external_id, user_token).get("result", {}).get("fotos", [])
    
    def get_location(self, obj):
        if not obj.location:
            data = obj.extra_properties.get("raw_list_item")
            address = {
                "huisnummer": data.get("locatie", {}).get("adres", {}).get("huisnummer"),
                "openbare_ruimte": data.get("locatie", {}).get("adres", {}).get("straatNaam"),
                "woonplaats": "Rotterdam",
            }
            x, y = rd_to_wgs(data.get("locatie", {}).get("x"), data.get("locatie", {}).get("y"))
            if not obj.set_location(data):
                return {
                    "address": address,
                    "geometrie": {
                        "coordinates": [y, x],
                        "type": "Point",
                    }
                }
        serializer = LocationSerializer(obj.location)
        return serializer.data

    def get_status(self, obj):
        default_status_name = StatusChoices.objects.all().first().name if StatusChoices.objects.all() else "Nieuw"
        status = obj.extra_properties.get("raw_list_item", {}).get("status", default_status_name)
        print(status)
        return {
            "state": status,
        }

    # def get_category(self, obj):
    #     user_token = MSBService.get_user_token_from_request(self.context['request'])
    #     if hasattr(obj, "melding"):

    #         msb_data = json.loads(obj.melding.msb_list_item)

    #         obj.melding.set_signal_category(msb_data)
    #         serializer = _NestedCategoryModelSerializer(obj.category_assignment, context=self.context)
    #         return serializer.data
    #         print(status)

    #         return {
    #             "sub_category": MSB_TO_SIGNALS_STATE.get(status,  workflow.GEMELD),
    #         }
    #     return {}


class IncidentSerializer(InsidentMSBFieldsMixin, serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField(source='get_attachments', read_only=True)
    location = serializers.SerializerMethodField(source='get_location', read_only=True)
    status = serializers.SerializerMethodField(source='get_status', read_only=True)

    class Meta:
        model = Incident
        fields = "__all__"
        # fields = (
        #     'id',
        #     'incident_date_start',
        #     'location',
        #     'status',
        #     'priority',
        #     'text',
        #     'extra_properties',
        #     'created_at',
        #     'updated_at',
        # )
        # read_only_fields = (
        #     'id',
        #     'incident_date_start',
        #     'location',
        #     'status',
        #     'priority',
        #     'text',
        #     'extra_properties',
        #     'created_at',
        #     'updated_at',
        # )