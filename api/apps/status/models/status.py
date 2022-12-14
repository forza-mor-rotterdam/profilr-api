from apps.incidents.models.mixins import CreatedUpdatedModel
from apps.status.managers import BulkCreateSignalsManager
from django.contrib.gis.db import models


class Status(CreatedUpdatedModel):
    incident = models.ForeignKey(
        "incidents.Incident", related_name="statuses", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=10000, null=True, blank=True)
    user_email = models.EmailField(null=True, blank=True)
    user_raw = models.CharField(max_length=100, null=True, blank=True)
    state = models.ForeignKey(
        to="status.StatusChoices", related_name="statuses", on_delete=models.CASCADE
    )

    extra_properties = models.JSONField(null=True, blank=True)

    send_email = models.BooleanField(default=False)

    objects = BulkCreateSignalsManager()

    class Meta:
        verbose_name_plural = "Statuses"
        get_latest_by = "datetime"
        ordering = ("created_at",)

    def __str__(self):
        return str(self.text)

    def save(self, *args, **kwargs):
        print(self.id)
        print(self.created_at)
        super().save(*args, **kwargs)
