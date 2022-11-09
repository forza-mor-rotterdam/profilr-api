from django.conf import settings
import requests
from django.core.cache import cache


class MSBService:
    url_base = f"{settings.MSB_API_URL}/sbmob/api"
    default_timeout = (5, 10)
    cache_timeout = 60 * 5
    GET = "get"
    POST = "post"

    @staticmethod
    def get_user_token_from_request(request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        auth_parts = auth_header.split(" ") if auth_header else []
        if settings.MSB_USER_TOKEN:
            return settings.MSB_USER_TOKEN
        if len(auth_parts) == 2 and auth_parts[0] == "Bearer":
            return auth_parts[1]

    @staticmethod
    def do_request(url, user_token, method=GET, data={}, no_cache=False):
        json_response = cache.get(url)
        action = getattr(requests, method, "get")
        if not json_response or no_cache:
            headers = {}
            if user_token:
                headers.update({
                    "Authorization": f"Bearer {user_token}"
                })
            response = action(
                url=url,
                data=data,
                headers=headers,
                timeout=MSBService.default_timeout,
            )
            json_response = response.json()
            cache.set(url, json_response, MSBService.cache_timeout)
        else:
            print(f"fetch from cache: {url}")
        return json_response

    @staticmethod
    def login(username: str, password: str):
        url=f"{MSBService.url_base}/login"
        data = {
            "uid": username,
            "pwd": password,
        }
        response_data = MSBService.do_request(
            url, 
            user_token=None, 
            method=MSBService.POST, 
            data=data, 
            no_cache=True
        )
        print(response_data)
        return bool(response_data.get("success")), response_data.get("result")

    @staticmethod
    def get_user_info(user_token):
        url=f"{MSBService.url_base}/gebruikerinfo"
        return MSBService.do_request(url, user_token, no_cache=True)

    @staticmethod
    def get_list(user_token, data={}, no_cache=False):
        default_data = {"x":92441,"y":437718,"radius":200}
        data = data.dict()
        data.update(default_data)
        url=f"{MSBService.url_base}/msb/openmeldingen"
        return MSBService.do_request(url, user_token, MSBService.POST, data, no_cache)

    @staticmethod
    def get_detail(melding_id, user_token):
        url=f"{MSBService.url_base}/msb/melding/{melding_id}"
        return MSBService.do_request(url, user_token)

    @staticmethod
    def get_mutatieregels(melding_id, user_token):
        url=f"{MSBService.url_base}/msb/melding/{melding_id}/mutatieregels"
        return MSBService.do_request(url, user_token)

