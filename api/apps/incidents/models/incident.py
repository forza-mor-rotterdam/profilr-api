import uuid
from django.contrib.gis.db import models
from django.core import validators
from apps.incidents.models.mixins import CreatedUpdatedModel
from apps.locations.utils.rd_convert import rd_to_wgs
from apps.locations.validators.address.pdok import PDOKAddressValidation
from apps.locations.models import Location
from django.contrib.gis.geos import GEOSGeometry



class Incident(CreatedUpdatedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    incident_date_start = models.DateTimeField(null=False)
    external_id = models.CharField(max_length=200, null=True, blank=True)
    text = models.CharField(max_length=3000)
    priority = models.FloatField(default=0.5, validators=[
        validators.MinValueValidator(0),
        validators.MaxValueValidator(1),
    ],)

    parent = models.ForeignKey(to='self', related_name='children', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.ForeignKey(to='status.Status', related_name='incidents', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(to='categories.Category', related_name='incidents', null=True, blank=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(to='locations.Location', related_name='incidents', null=True, blank=True, on_delete=models.SET_NULL)

    extra_properties = models.JSONField(null=True)

    def set_location(self, data):
        address = {
            'openbare_ruimte': data["locatie"]["adres"]["straatNaam"], 
            'huisnummer': data["locatie"]["adres"]["huisnummer"],
            'woonplaats': "Rotterdam",
        }
        lat, lon = rd_to_wgs(data["locatie"]["x"], data["locatie"]["y"])
        location_data = {}
        location_validator = PDOKAddressValidation()
        validated_address = None
        alternative_address = dict(address)
        try:
            validated_address = location_validator.validate_address(address=address, lon=lon, lat=lat)
        except:
            alternative_address.update({
                "huisnummer": 1,
            })
            try:
                validated_address = location_validator.validate_address(address=alternative_address)
            except:
                pass
        if 'extra_properties' not in location_data or location_data["extra_properties"] is None:
            location_data["extra_properties"] = {}

        location_data["extra_properties"]["original_address"] = address
        location_data["extra_properties"]["alternative_address"] = alternative_address
        if validated_address:
            location_data["address"] = validated_address
            location_data["bag_validated"] = True
            geometrie = validated_address.pop("geometrie")
            location_data["geometrie"] = GEOSGeometry(geometrie)
            self.location = Location.objects.create(**location_data)
            self.save(update_fields=["location"])
        return False