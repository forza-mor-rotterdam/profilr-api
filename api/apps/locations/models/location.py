import copy

from apps.incidents.models.mixins import CreatedUpdatedModel
from apps.locations.utils.location import AddressFormatter
from django.contrib.gis.db import models
from django.contrib.gis.gdal import CoordTransform, SpatialReference


class Location(CreatedUpdatedModel):
    geometrie = models.PointField(name="geometrie")
    gemeente_code = models.CharField(null=True, max_length=6)
    wijk_code = models.CharField(null=True, max_length=8)
    buurt_code = models.CharField(null=True, max_length=10)
    address = models.JSONField(null=True)
    address_text = models.CharField(null=True, max_length=256, editable=False)
    created_by = models.EmailField(null=True, blank=True)

    extra_properties = models.JSONField(null=True)
    bag_validated = models.BooleanField(default=False)

    @property
    def short_address_text(self):
        # openbare_ruimte huisnummerhuiletter-huisnummer_toevoeging
        return (
            AddressFormatter(address=self.address).format("O hlT")
            if self.address
            else ""
        )

    def save(self, *args, **kwargs):
        if Location.objects.filter(
            address__postcode=self.address.get("postcode"),
            address__huisnummer=self.address.get("huisnummer"),
            address__huisletter=self.address.get("huisletter"),
            address__woonplaats=self.address.get("woonplaats"),
            address__openbare_ruimte=self.address.get("openbare_ruimte"),
            address__huisnummer_toevoeging=self.address.get("huisnummer_toevoeging"),
        ):
            raise Exception("Duplicate address")

        # Set address_text
        self.address_text = (
            AddressFormatter(address=self.address).format("O hlT p W")
            if self.address
            else ""
        )
        super().save(*args, **kwargs)

    def get_rd_coordinates(self):
        to_transform = copy.deepcopy(self.geometrie)
        to_transform.transform(
            CoordTransform(
                SpatialReference(4326), SpatialReference(28992)  # WGS84  # RD
            )
        )
        return to_transform
