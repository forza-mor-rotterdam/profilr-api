from apps.incidents.models import Incident
from apps.locations.serializers import LocationSerializer
from apps.locations.utils.rd_convert import rd_to_wgs
from profilr_api_services import msb_api_service
from rest_framework import serializers


class AttachmentSerialzer(serializers.Serializer):
    pass


class InsidentMSBFieldsMixin:
    def get_attachments(self, obj):
        user_token = msb_api_service.get_user_token_from_request(
            self.context["request"]
        )
        return msb_api_service.get_detail(obj.external_id, user_token).get("fotos", [])

    def get_location(self, obj):
        if not obj.location:
            data = obj.extra_properties.get("raw_list_item")
            address = {
                "huisnummer": data.get("locatie", {})
                .get("adres", {})
                .get("huisnummer"),
                "openbare_ruimte": data.get("locatie", {})
                .get("adres", {})
                .get("straatNaam"),
                "woonplaats": "Rotterdam",
            }
            x, y = rd_to_wgs(
                data.get("locatie", {}).get("x"), data.get("locatie", {}).get("y")
            )
            if not obj.set_location(data):
                return {
                    "address": address,
                    "geometrie": {
                        "coordinates": [y, x],
                        "type": "Point",
                    },
                }
        serializer = LocationSerializer(obj.location)
        return serializer.data

    def get_status(self, obj):
        status = obj.msb_data.get("status", "Nieuw")
        return {
            "state": status,
        }

    def get_omschrijving(self, obj):
        user_token = msb_api_service.get_user_token_from_request(
            self.context["request"]
        )
        return msb_api_service.get_detail(obj.external_id, user_token).get(
            "omschrijving", ""
        )

    # def get_category(self, obj):
    #     user_token = msb_api_service.get_user_token_from_request(self.context['request'])
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


class IncidentListSerializer(InsidentMSBFieldsMixin, serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField(read_only=True)
    location = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Incident
        fields = (
            "id",
            "incident_date_start",
            "location",
            "status",
            "priority",
            "attachments",
            "external_id",
        )
        read_only_fields = (
            "id",
            "incident_date_start",
            "location",
            "status",
            "priority",
            "attachments",
            "external_id",
        )


class IncidentSerializer(IncidentListSerializer):
    attachments = serializers.SerializerMethodField(
        method_name="get_attachments", read_only=True
    )
    location = serializers.SerializerMethodField(
        method_name="get_location", read_only=True
    )
    status = serializers.SerializerMethodField(method_name="get_status", read_only=True)
    spoed = serializers.SerializerMethodField(method_name="get_spoed", read_only=True)
    text = serializers.SerializerMethodField(
        method_name="get_omschrijving", read_only=True
    )

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
