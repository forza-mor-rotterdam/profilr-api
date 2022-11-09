from django.contrib import admin
from apps.status.models import StatusChoices


class StatusChoicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

admin.site.register(StatusChoices, StatusChoicesAdmin)