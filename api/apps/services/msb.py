import json

import requests
from apps.categories.utils import sync_categories
from django.conf import settings
from django.core.cache import cache


class MSBService:
    url_base = f"{settings.MSB_API_URL}/sbmob/api"
    default_timeout = (5, 10)
    default_cache_timeout = 60 * 5
    GET = "get"
    POST = "post"

    @staticmethod
    def get_user_token_from_request(request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        auth_parts = auth_header.split(" ") if auth_header else []

        if len(auth_parts) == 2 and auth_parts[0] == "Bearer":
            return auth_parts[1]

    @staticmethod
    def do_request(
        url,
        user_token,
        method=GET,
        data={},
        no_cache=False,
        cache_timeout=default_cache_timeout,
    ):
        json_response = cache.get(url)
        action = getattr(requests, method, "get")
        if not json_response or no_cache:
            headers = {}
            if user_token:
                headers.update({"Authorization": f"Bearer {user_token}"})
            response = action(
                url=url,
                data=data,
                headers=headers,
                timeout=MSBService.default_timeout,
            )
            response.raise_for_status()
            if int(response.status_code) >= 200 and int(response.status_code) < 300:
                json_response = response.json()
                cache.set(url, json_response, cache_timeout)
        else:
            print(f"fetch from cache: {url}")
        return json_response

    @staticmethod
    def login(username: str, password: str):
        url = f"{MSBService.url_base}/login"
        data = {
            "uid": username,
            "pwd": password,
        }
        response_data = MSBService.do_request(
            url, user_token=None, method=MSBService.POST, data=data, no_cache=True
        )
        return bool(response_data.get("success")), response_data.get("result")

    @staticmethod
    def get_user_info(user_token):
        url = f"{MSBService.url_base}/gebruikerinfo"
        return MSBService.do_request(url, user_token, no_cache=True)

    @staticmethod
    def get_list(user_token, data={}, no_cache=False):
        url = f"{MSBService.url_base}/msb/openmeldingen"
        return MSBService.do_request(url, user_token, MSBService.POST, data, no_cache)

    @staticmethod
    def get_detail(melding_id, user_token):
        url = f"{MSBService.url_base}/msb/melding/{melding_id}"
        return MSBService.do_request(url, user_token, cache_timeout=30)

    @staticmethod
    def get_mutatieregels(melding_id, user_token):
        url = f"{MSBService.url_base}/msb/melding/{melding_id}/mutatieregels"
        return MSBService.do_request(url, user_token, cache_timeout=30)

    @staticmethod
    def get_wijken(user_token):
        url = f"{MSBService.url_base}/wijken"
        return MSBService.do_request(url, user_token, no_cache=True)

    @staticmethod
    def get_onderwerpgroepen(user_token):
        url = f"{MSBService.url_base}/msb/onderwerpgroepen"
        response = MSBService.do_request(url, user_token, no_cache=True)
        if response.get("success") and hash(json.dumps(response)) != cache.get(
            "onderwerpgroepen"
        ):
            sync_categories(response.get("result", []))
            cache.set("onderwerpgroepen", hash(json.dumps(response)), None)
        return response

    @staticmethod
    def get_afdelingen(user_token):
        url = f"{MSBService.url_base}/msb/afdelingen"
        return MSBService.do_request(url, user_token, cache_timeout=60 * 60 * 24)
