from django.contrib.gis.db import models


class AreaType(models.Model):
    class Meta:
        verbose_name = "Gebiedstype"
        verbose_name_plural = "Gebiedstypen"
        ordering = ["code"]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=3000)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    _type = models.ForeignKey(AreaType, on_delete=models.CASCADE)
    geometry = models.MultiPolygonField()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        unique_together = ("code", "_type")
        ordering = ["_type", "code"]


class Gemeente(Area):
    class Meta:
        abstract = False
        verbose_name = "Gemeente"
        verbose_name_plural = "Gemeentes"
        unique_together = ("code", "_type")
        ordering = ["_type", "code"]


class Wijk(Area):
    gemeente = models.ForeignKey(Gemeente, on_delete=models.CASCADE)

    class Meta:
        abstract = False
        verbose_name = "Wijk"
        verbose_name_plural = "Wijken"
        unique_together = ("code", "_type")
        ordering = ["_type", "code"]


class Buurt(Area):
    wijk = models.ForeignKey(Wijk, on_delete=models.CASCADE)

    class Meta:
        abstract = False
        verbose_name = "Buurt"
        verbose_name_plural = "Buurten"
        unique_together = ("code", "_type")
        ordering = ["_type", "code"]
