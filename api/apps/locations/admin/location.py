from apps.locations.models import Location
from django.contrib import admin


class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "address")


admin.site.register(Location, LocationAdmin)
