from apps.incidents.viewsets import IncidentViewSet
from apps.locations.viewsets import BuurtViewSet, WijkViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"incidents", IncidentViewSet, basename="incidents")
router.register(r"wijken", WijkViewSet, basename="wijken")
router.register(r"buurten", BuurtViewSet, basename="buurten")

# v1_urls = (
#     router.urls,
# )

urlpatterns = [
    # Used to determine API health when deploying
    path("status/", include("apps.health.urls")),
    # The Django admin
    path("admin/", admin.site.urls),
    path("v1/", include((router.urls, "app"), namespace="v1")),
]
