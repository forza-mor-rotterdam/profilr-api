import logging

import requests
from django.conf import settings
from django.db import Error, connection
from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import HealthCheckException

logger = logging.getLogger(__name__)


class MSBAPIHealthCheck(BaseHealthCheckBackend):
    critical_service = True

    def check_status(self):
        health_check_response = requests.get(f"{settings.MSB_API_URL}/sbmob/api/logout")

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


class DatabaseHealthCheck(BaseHealthCheckBackend):
    critical_service = True

    def check_status(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("select 1")
                assert cursor.fetchone()
        except Error:
            error_msg = "Database connectivity failed"
            logger.exception(error_msg)
            raise HealthCheckException("Database connectivity failed")

    def identifier(self):
        return "Custom database health check"
