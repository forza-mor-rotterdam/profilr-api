from apps.status.models import Status
from django.contrib import admin


class StatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "state",
        "created_at",
        "incident",
    )


admin.site.register(Status, StatusAdmin)
