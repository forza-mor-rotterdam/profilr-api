from django.contrib import admin
from apps.locations.models import Gemeente


class GemeenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "_type")

admin.site.register(Gemeente, GemeenteAdmin)