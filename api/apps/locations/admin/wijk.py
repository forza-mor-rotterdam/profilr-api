from apps.locations.models import Wijk
from django.contrib import admin


class WijkAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "_type")
    list_filter = (
        "gemeente__code",
        "gemeente__name",
    )
    search_fields = ("name",)


admin.site.register(Wijk, WijkAdmin)
