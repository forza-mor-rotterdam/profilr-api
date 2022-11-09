from django.contrib import admin
from apps.locations.models import AreaType


class AreaTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(AreaType, AreaTypeAdmin)