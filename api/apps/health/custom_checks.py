import logging

import requests
from django.conf import settings
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import HealthCheckException

logger = logging.getLogger(__name__)


class MSBAPIHealthCheck(BaseHealthCheckBackend):
    critical_service = True

    def check_status(self):
        health_check_response = requests.get(settings.INCIDENT_API_HEALTH_CHECK_URL)

        if health_check_response.status_code != 200:
            raise HealthCheckException(
                f"MSB not ready: status code: {health_check_response.status_code}"
            )
        if health_check_response.status_code == 404:
            raise HealthCheckException(
                f"MSB: health url not implemented: status code: {health_check_response.status_code}"
            )

    def identifier(self):
        return self.__class__.__name__
