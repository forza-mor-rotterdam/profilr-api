import logging

from apps.services import incident_api_service
from django.contrib.auth.models import User
from rest_framework import exceptions

logger = logging.getLogger(__name__)


class MSBAuthBackend:
    @staticmethod  # noqa: C901
    def authenticate(request):

        user_token = incident_api_service.get_user_token_from_request(request)
        if not user_token:
            raise exceptions.AuthenticationFailed("No token provided!")
        try:
            user_info = incident_api_service.get_user_info(user_token)
        except Exception:
            raise exceptions.AuthenticationFailed("Authentication failt!")

        if not user_info.get("success"):
            raise exceptions.AuthenticationFailed("Login failt")

        username = user_info.get("result").get("user")[-6:]
        name = user_info.get("result").get("naam")
        email = f"{username}@rotterdam.nl"

        auth_user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": name,
            },
        )
        logger.info(f"User: {auth_user.username}, created: {created}")

        return auth_user, created

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'Bearer realm="signals"'


AuthBackend = MSBAuthBackend
