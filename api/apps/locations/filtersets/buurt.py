from django_filters.rest_framework import FilterSet, filters


class BuurtFilterSet(FilterSet):
    code = filters.CharFilter(
        field_name="code",
    )
    wijk_code = filters.CharFilter(
        field_name="wijk__code",
    )
    gemeente_code = filters.CharFilter(
        field_name="wijk__gemeente__code",
    )
