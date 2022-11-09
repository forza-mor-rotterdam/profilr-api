from django.contrib import admin
from apps.locations.models import Buurt


class BuurtAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "_type")

admin.site.register(Buurt, BuurtAdmin)