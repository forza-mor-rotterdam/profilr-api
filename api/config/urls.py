from apps.users.views import config
from apps.users.viewsets import ProfileViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"profile", ProfileViewSet, basename="profile")

urlpatterns = [
    path("v1/", include((router.urls, "app"), namespace="v1")),
    path("health/", include("health_check.urls")),
    path("config/", config, name="config"),
    # The Django admin
    path("admin/", admin.site.urls),
]
