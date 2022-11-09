from apps.locations.models import AreaType
from django.contrib import admin


class AreaTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


admin.site.register(AreaType, AreaTypeAdmin)
