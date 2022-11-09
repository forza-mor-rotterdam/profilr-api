from django_filters.rest_framework import FilterSet, filters


class WijkFilterSet(FilterSet):
    code = filters.CharFilter(
        field_name="code",
    )
    gemeente_code = filters.CharFilter(
        field_name="gemeente__code",
    )
