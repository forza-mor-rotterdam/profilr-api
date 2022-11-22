from apps.categories.models import Category
from django_filters.rest_framework import FilterSet, filters


class SubCategoryFilterSet(FilterSet):
    category = filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.filter(is_active=True, parent__isnull=True),
        method="get_categories",
    )

    def get_categories(self, queryset, name, value):
        if value:
            return queryset.filter(
                parent__in=value,
            )
        return queryset
