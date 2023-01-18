from django.conf import settings

from .utils import get_service_class

incident_api_service = get_service_class(settings.INCIDENT_API_SERVICE)(
    settings.INCIDENT_API_URL
)
