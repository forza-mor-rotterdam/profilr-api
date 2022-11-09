from django.contrib import admin
from apps.locations.models import Wijk


class WijkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "_type")
    list_filter = (
        "gemeente__code",
        "gemeente__name",
    )
    search_fields = (
        "name", 
    )

admin.site.register(Wijk, WijkAdmin)