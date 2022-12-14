from apps.api.filters import RelatedOrderingFilter
from apps.categories.filtersets import SubCategoryFilterSet
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from profilr_api_services import msb_api_service
from rest_framework import viewsets


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.filter(is_active=True, parent__isnull=True)

    serializer_class = CategorySerializer

    http_method_names = [
        "get",
    ]

    def list(self, request, *args, **kwargs):
        user_token = msb_api_service.get_user_token_from_request(request)
        msb_api_service.get_onderwerpgroepen(user_token)
        return super().list(request, *args, **kwargs)


class SubCategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.filter(is_active=True, parent__isnull=False)

    serializer_class = CategorySerializer

    http_method_names = [
        "get",
    ]

    filter_backends = (
        DjangoFilterBackend,
        RelatedOrderingFilter,
    )
    filterset_class = SubCategoryFilterSet

    def list(self, request, *args, **kwargs):
        user_token = msb_api_service.get_user_token_from_request(request)
        msb_api_service.get_onderwerpgroepen(user_token)
        return super().list(request, *args, **kwargs)
