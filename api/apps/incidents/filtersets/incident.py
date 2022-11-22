from apps.categories.models import Category
from apps.locations.models import Buurt, Wijk
from django.conf import settings
from django_filters.rest_framework import FilterSet, filters


class IncidentFilterSet(FilterSet):
    category = filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.filter(is_active=True), method="get_categories"
    )
    wijk = filters.ModelMultipleChoiceFilter(
        queryset=Wijk.objects.filter(gemeente__code=settings.GEMEENTE_CODE),
        to_field_name="code",
        method="get_wijken",
    )
    buurt = filters.ModelMultipleChoiceFilter(
        queryset=Buurt.objects.filter(wijk__gemeente__code=settings.GEMEENTE_CODE),
        to_field_name="code",
        method="get_buurten",
    )

    def get_categories(self, queryset, name, value):
        if value:
            return queryset.filter(
                category_id__in=value,
            )
        return queryset

    def get_wijken(self, queryset, name, value):
        if value:
            return queryset.filter(
                code__in=value,
            )
        return queryset

    def get_buurten(self, queryset, name, value):
        if value:
            return queryset.filter(
                code__in=value,
            )
        return queryset
