from django.contrib.gis.db import models


class CreatedUpdatedModel(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True
