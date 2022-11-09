from apps.locations.models import Buurt
from django.contrib import admin


class BuurtAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "_type")


admin.site.register(Buurt, BuurtAdmin)
