from apps.locations.models import Gemeente
from django.contrib import admin


class GemeenteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "_type")


admin.site.register(Gemeente, GemeenteAdmin)
