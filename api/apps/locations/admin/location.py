from django.contrib import admin
from apps.locations.models import Location


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')

admin.site.register(Location, LocationAdmin)