from apps.incidents.models.incident import Incident
from django.contrib import admin


class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_id",
        "location",
        "status",
    )


admin.site.register(Incident, IncidentAdmin)
