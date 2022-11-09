from apps.status.models import StatusChoices
from django.contrib import admin


class StatusChoicesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


admin.site.register(StatusChoices, StatusChoicesAdmin)
