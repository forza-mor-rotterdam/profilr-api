from apps.categories.viewsets import CategoryViewSet, SubCategoryViewSet
from apps.incidents.viewsets import IncidentViewSet
from apps.locations.viewsets import BuurtViewSet, WijkViewSet
from apps.users.views import show_profiles
from apps.users.viewsets import ProfileViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"incidents", IncidentViewSet, basename="incidents")
router.register(r"wijken", WijkViewSet, basename="wijken")
router.register(r"buurten", BuurtViewSet, basename="buurten")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"sub-categories", SubCategoryViewSet, basename="sub-categories")
router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = [
    # Used to determine API health when deploying
    path("status/", include("apps.health.urls")),
    # The Django admin
    path("admin/", admin.site.urls),
    path("v1/", include((router.urls, "app"), namespace="v1")),
    path("health/", include("health_check.urls")),
    path("profiles/", show_profiles, name="profiles"),
]
