from apps.health import views
from django.urls import path

urlpatterns = [
    path("health", views.health),
    path("data", views.check_data),
]
