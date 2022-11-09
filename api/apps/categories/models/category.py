from django.contrib.gis.db import models
from django_extensions.db.fields import AutoSlugField


class Category(models.Model):
    parent = models.ForeignKey('categories.Category',
                               related_name='children',
                               on_delete=models.PROTECT,
                               null=True, blank=True)
    slug = AutoSlugField(
        populate_from=['name', ], 
        blank=False, 
        overwrite=False, 
        editable=False
    )
    name = models.CharField(max_length=255)
    public_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)