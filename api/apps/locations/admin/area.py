from django.contrib import admin
from apps.locations.models import Area


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "_type")

admin.site.register(Area, AreaAdmin)