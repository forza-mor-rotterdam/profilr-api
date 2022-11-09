from django.contrib import admin
from apps.categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

admin.site.register(Category, CategoryAdmin)