from apps.categories.models import Category
from django.contrib import admin


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


admin.site.register(Category, CategoryAdmin)
