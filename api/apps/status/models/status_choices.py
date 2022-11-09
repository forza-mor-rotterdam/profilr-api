from django.contrib.gis.db import models


class StatusChoices(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Status choices"
        ordering = ("name",)

    def __str__(self):
        return str(self.name)
